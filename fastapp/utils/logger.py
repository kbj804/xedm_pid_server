import json
import logging
from datetime import timedelta, datetime
from time import time
from fastapi.requests import Request

from fastapi import Body
from fastapi.logger import logger

logger.setLevel(logging.INFO)

# respense: Json, error: 아까 만든 객체
async def api_logger(request: Request, response=None, error=None):
    time_format = "%Y/%m/%d %H:%M:%S"
    # time()은 token_validator.py 의 call_next()의 시간이고, request.state.start를 시작 시간이므로, t는 함수가 실행되는데 얼마나 걸렸는지 알려줌
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user
    # body: 나중에 DEBUG용으로 사용하기 위해 넣어 둠. 어디서 에러가 났는지 알기 위해서 넣어주는게 좋음
    # body = await request.body()
    if error:
        if request.state.inspect:
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"

        error_log = dict(
            errorFunc=error_func,
            location="{} line in {}".format(str(error_line), error_file),
            raised=str(error.__class__.__name__),
            msg=str(error.ex),
        )

    # email은 개인정보니까 마스킹 하기 위해서 전처리
    email = user.email.split("@") if user and user.email else None
    user_log = dict(
        client=request.state.ip,
        user=user.id if user and user.id else None,
        email="**" + email[0][2:-1] + "*@" + email[1] if user and user.email else None,
    )
    # 이게 중요..!! 에러에 대한 전체적인 정보를 나타냄
    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )
    # if body:
    #     log_dict["body"] = body
    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))