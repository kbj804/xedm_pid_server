import base64
import hmac
import time
import typing
import jwt
import re

from fastapi.params import Header
from jwt import PyJWTError
from jwt.exceptions import ExpiredSignatureError, DecodeError

from pydantic import BaseModel
from starlette.requests import Request
from starlette.datastructures import URL, Headers
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from Scripts.fastapp.errors import exceptions as ex

from starlette.types import ASGIApp, Receive, Scope, Send

from Scripts.fastapp.database.conn import db
from Scripts.fastapp.database.schema import Users, ApiKeys, Train
from Scripts.fastapp.models import UserToken, Test

from Scripts.fastapp.common import config, consts
from Scripts.fastapp.common.config import conf
from Scripts.fastapp.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from Scripts.fastapp.errors.exceptions import APIException, SqlFailureEx, APIQueryStringEx


from Scripts.fastapp.utils.date_utils import D
from Scripts.fastapp.utils.logger import api_logger
from Scripts.fastapp.utils.query_utils import to_dict


# FastAPI 공식 문서에 따라 미들웨어 생성
async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    # 핸들링안되는 에러를 로딩하기 위한 inspect Ex) 500 Error
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    request.state.train = None

    # 로드밸런서를 거치지 않으면 x-forwarded-for를 거치지 않기 때문에 else request.client.host를 써줌
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip # 전처리
    headers = request.headers
    cookies = request.cookies
    url = request.url.path
    # Except path regex에 url이 있다면 토큰검사 안하고 바로 다음 함수,미들웨어호출
    # url이 루트 패스가 아니면 api_logger 로 로그찍어라
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    try:
        if url.startswith("/api"):
            # api 인경우 헤더로 토큰 검사
            if url.startswith("/api/services"):
                # query_params 는 url뒤에 ? 뒤에 있는것들
                # ex) "xyz.com?key=1236timestamp=12234234"
                # qs = "key=1236timestamp=12234234"
                qs = str(request.query_params)
                qs_list = qs.split("&")

                try:
                    # &로 나눈 각 명령들을 dictionary로 
                    qs_dict = {qs_split.split("=")[0]: qs_split.split("=")[1] for qs_split in qs_list}
                except Exception:
                    raise ex.APIQueryStringEx()

                qs_keys = qs_dict.keys()
                if "key" not in qs_keys or "timestamp" not in qs_keys:
                    raise ex.APIQueryStringEx()

                # if "secret" not in headers.keys():
                #     raise ex.APIHeaderInvalidEx()
                session = next(db.session())
                # 여기서 session을 넣어주지 않으면 get 이후에 세션이 끊어짐
                api_key = ApiKeys.get(session=session, access_key=qs_dict["key"])
                if not api_key:
                    raise ex.NotFoundAccessKeyEx(api_key=qs_dict["key"])
                
                # hmac: 해싱 -> base64 바꾼 값을 header에 넣고 요청 -> 서버에서 base64값 저장해둠 -> 다시 header요청 오면 가지고있는 값이랑 비교
                # secret_key를 가지고 qs를 Hash화
                mac = hmac.new(bytes(api_key.secret_key, encoding='utf8'), bytes(qs, encoding='utf-8'), digestmod='sha256')
                d = mac.digest()
                validating_secret = str(base64.b64encode(d).decode('utf-8'))

                # header가 가지고있는 거랑 같지않으면 오류
                if headers["secret"] != validating_secret:
                    raise ex.APIHeaderInvalidEx()

                # 현재 시간을 가져옴.
                now_timestamp = int(D.datetime(diff=9).timestamp()) # diff=0 : KST / timestamp를 가져와서 인트화
                # 10초전에 만든 요청까지만 유효하게 인증함 / Replay attack 방지. 
                if now_timestamp - 10 > int(qs_dict["timestamp"]) or now_timestamp < int(qs_dict["timestamp"]):
                    raise ex.APITimestampEx()

                # api_key = DB에서 가져오는 것. API_KEY에 relation을 걸어놓았기 때문에 검색 가능
                user_info = to_dict(api_key.users)
                print("#### user_ info ####",user_info)
                request.state.user = UserToken(**user_info)
                session.close()
                response = await call_next(request)
                return response

            elif url.startswith("/api/pid"):
                print("########## /api/pid start ############")
                # session = next(db.session())
                # # train = Train.get(session=session)
                # # print("##################################",train)
                # # request.state.train = Test(id=1, reg_count=3, y=1)
                # session.close()
                # response = await call_next(request)
                # print("######  RESPONSE  ######", response)
                # return response
                
            elif url.startswith("/api/ml"):
                print("########## /api/ml start ############")

            elif url.startswith("/api/xedm"):
                print("########## /api/xedm start ############")
                
            else:
                if "authorization" in headers.keys():
                    token_info = await token_decode(access_token=headers.get("Authorization"))
                    print("#### token info ####", token_info)
                    request.state.user = UserToken(**token_info)
                    # 토큰 없음
                else:
                    if "Authorization" not in headers.keys():
                        raise ex.NotAuthorized()
        else:
            # 템플릿 렌더링인 경우 쿠키에서 토큰 검사 - 토큰을 임의로 넣어줌
            cookies["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoia29hbGFAZGluZ3JyLmNvbSIsIm5hbWUiOm51bGwsInBob25lX251bWJlciI6bnVsbCwicHJvZmlsZV9pbWciOm51bGwsInNuc190eXBlIjpudWxsfQ.4vgrFvxgH8odoXMvV70BBqyqXOFa2NDQtzYkGywhV48"

            if "Authorization" not in cookies.keys():
                raise ex.NotAuthorized()

            token_info = await token_decode(access_token=cookies.get("Authorization"))
            request.state.user = UserToken(**token_info)
        
        # 여기까지오면 토큰검사 끝난거
        print("### TOKEN VALIDATION OK ###")
        response = await call_next(request) # 함수 실행 (API) -> 리턴 값이 나올 때 까지 await 함
        print("#### Response #### \n",response)
        await api_logger(request=request, response=response)
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)
    print("#### Respnse 직전 ####")
    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error