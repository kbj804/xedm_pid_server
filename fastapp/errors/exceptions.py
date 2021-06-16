from Scripts.fastapp.common.consts import MAX_API_KEY
class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class APIException(Exception):
    '''
    code: Custom Error Code
    msg: Error msg for User
    detail: Info of Error
    '''
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex

        super().__init__(ex)

# 지금은 파일에 넣었지만 나중엔 DB에 넣고 관리해야 함
class NotFoundUserEx(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"해당 유저를 찾을 수 없습니다.",
            detail=f"Not Found User ID : {user_id}",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"로그인이 필요한 서비스 입니다.",
            detail="Authorization Required",
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )

class NoKeyMatchEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"해당 키에 대한 권한이 없거나 해당 키가 없습니다.",
            detail="No Keys Matched",
            code=f"{StatusCode.HTTP_404}{'3'.zfill(4)}",
            ex=ex,
        )


class MaxKeyCountEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"API 키 생성은 {MAX_API_KEY}개 까지 가능합니다.",
            detail="Max Key Count Reached",
            code=f"{StatusCode.HTTP_400}{'4'.zfill(4)}",
            ex=ex,
        )


class SqlFailureEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"이 에러는 서버측 에러 입니다. 자동으로 리포팅 되며, 빠르게 수정하겠습니다..",
            detail="Internal Server Error",
            code=f"{StatusCode.HTTP_500}{'2'.zfill(4)}",
            ex=ex,
        )

class APIQueryStringEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"쿼리스트링은 key, timestamp 2개만 허용되며, 2개 모두 요청시 제출되어야 합니다.",
            detail="Query String Only Accept key and timestamp.",
            code=f"{StatusCode.HTTP_400}{'7'.zfill(4)}",
            ex=ex,
        )


class APIHeaderInvalidEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"헤더에 키 해싱된 Secret 이 없거나, 유효하지 않습니다.",
            detail="Invalid HMAC secret in Header",
            code=f"{StatusCode.HTTP_400}{'8'.zfill(4)}",
            ex=ex,
        )


class APITimestampEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"쿼리스트링에 포함된 타임스탬프는 KST 이며, 현재 시간보다 작아야 하고, 현재시간 - 10초 보다는 커야 합니다.",
            detail="timestamp in Query String must be KST, Timestamp must be less than now, and greater than now - 10.",
            code=f"{StatusCode.HTTP_400}{'9'.zfill(4)}",
            ex=ex,
        )


class NotFoundAccessKeyEx(APIException):
    def __init__(self, api_key:str,  ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"API 키를 찾을 수 없습니다.",
            detail=f"Not found such API Access Key : {api_key}",
            code=f"{StatusCode.HTTP_404}{'10'.zfill(4)}",
            ex=ex,
        )

class FileExtEx(APIException):
    def __init__(self, file_name:str,  ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"지원하지 않는 확장자 입니다. (현재 지원가능 확장자:pdf, txt, csv, xlsx, pptx) ",
            detail=f"Not support EXT : {file_name}",
            code=f"{StatusCode.HTTP_400}{'10'.zfill(4)}",
            ex=ex,
        )

class XedmLoadFailEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"Machin Learning Model 로드에 실패하였습니다..",
            detail=f"Fail the ML Model Load",
            code=f"{StatusCode.HTTP_500}{'10'.zfill(4)}",
            ex=ex,
        )

class XedmUploadFailEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"File Upload에 실패했습니다.",
            detail=f"Fail the File Upload",
            code=f"{StatusCode.HTTP_400}{'10'.zfill(4)}",
            ex=ex,
        )