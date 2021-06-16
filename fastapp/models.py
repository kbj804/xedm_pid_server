from datetime import datetime
from enum import Enum
from typing import List

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr, IPvAnyAddress


class UserRegister(BaseModel):
    # pip install 'pydantic[email]'
    email: str = None
    pw: str = None

# Enum : 이 중에 한가지만 들어올 수 있음
class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"

# Response Model. 
class Token(BaseModel):
    Authorization: str = None

class Test(BaseModel):
    id: int = None
    reg_count: int= None

    class Config:
        orm_mode = True
    
# class Label(Test):
#     y: int=None

class AddLabel(BaseModel):
    y: int = None
    
    class Config:
        orm_mode = True


class UpdateLabel(AddLabel):
    pre_y: int = None
    


class EmailRecipients(BaseModel):
    name: str
    email: str


class SendEmail(BaseModel):
    email_to: List[EmailRecipients] = None


class KakaoMsgBody(BaseModel):
    msg: str = None


class MessageOk(BaseModel):
    message: str = Field(default="OK")

# 토큰을 객체화 해서 사용하기 위해 만듬
class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True

class AddIsTrain(BaseModel):
    is_train: bool = False

    class Config:
        orm_mode = True

class AddApiKey(BaseModel):
    user_memo: str = None

    class Config:
        orm_mode = True


class GetApiKeyList(AddApiKey):
    id: int = None
    access_key: str = None
    created_at: datetime = None


class GetApiKeys(GetApiKeyList):
    secret_key: str = None


class CreateAPIWhiteLists(BaseModel):
    ip_addr: str = None


class GetAPIWhiteLists(CreateAPIWhiteLists):
    id: int

    class Config:
        orm_mode = True

class GetIsPID(BaseModel):
    id: int = None
    name: str = None
    ext: str = None
    is_pid: bool = False
    
    class Config:
        orm_mode = True

class Label(BaseModel):
    id: int = None
    y: int = None
    is_train: bool = False

    class Config:
        orm_mode = True

class FeatureToken(Label):
    reg_count: int = None
    column1: int = None
    column2: int = None
    column3: int = None
    column4: int = None
    column5: int = None
    column6: int = None
    column7: int = None
    column8: int = None
    column9: int = None
    column10: int = None


class XedmPinfoToken(BaseModel):
   name: str = None
   value: str = None

class AttrData(BaseModel):
    docId: str = None
    attrList: List[XedmPinfoToken] = None

class XedmToken(BaseModel):
    attrData: AttrData = Field(...)

    class Config:
        orm_mode = True