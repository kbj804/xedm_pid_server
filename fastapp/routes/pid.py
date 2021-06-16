from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from starlette.requests import Request

from Scripts.fastapp.common.consts import UPLOAD_DIRECTORY
from Scripts.fastapp.database.conn import db
# from Scripts.fastapp.database.schema import Users, ApiKeys, ApiWhiteLists
from Scripts.fastapp.database.schema import Train, Files
from Scripts.fastapp import models as m
from Scripts.fastapp.errors import exceptions as ex
import string
import secrets
from inspect import currentframe as frame

from Scripts.fastapp.models import MessageOk, Test, Label
# from Scripts.fastapp.utils.file_module.test import t_load_data

from Scripts.fastapp.utils.file_module.load_file_manager import loadFileManager
from Scripts.fastapp.utils.preprocess_reg import preprocess_reg

import os


router = APIRouter(prefix='/pid')


@router.get('/getIsPID', response_model=List[m.GetIsPID])
# @router.get('')
async def show_data(request: Request, ispid):
    """
    no params\n
    :return\n
    [\n
        {\n
            id: int = None\n
            name: str = None\n
            ext: str = None\n
            is_pid: bool = False\n
        },{\n
            ...\n
        }\n
    ]\n
    """
    request.state.inspect = frame()
    print("### state.user : ", request.state.user)
    print("### state.inspect : ", request.state.inspect)
    print("###", request.url.hostname + request.url.path )
    print("###", request.state.ip)
    result = Files.filter(is_pid=ispid).all()
    
    print("##RESULT##", result)
    # return dict(id=result[0].id, reg_count=result[0].reg_count)
    return result

@router.get('/getTrain')
async def get_train_data(request: Request, id: int):
    """
    no params\n
    :return\n
    Train Model
    """
    request.state.inspect = frame()
    result = Train.filter(file_id=id).order_by("id").all()
    
    print("##RESULT##", result)
    # return dict(id=result[0].id, reg_count=result[0].reg_count)
    return result


# @router.post("/register", status_code=201, response_model=Label)
'''@router.post("/register/{file_path}", status_code=201)
async def input_data(file_path ,request: Request, session: Session = Depends(db.session)):
    """
    file path를 입력해서 해당 파일을 DB에 등록하는 함수
    지금은 사용 안함
    """
    print("start#########################################")
    request.state.inspect = frame()
    print(file_path)
    df = t_load_data(file_path)
    for row in df.itertuples():
        print(row)
        print(row.page)
        Train.create(session, auto_commit=True,page=row.page ,reg_count=row.reg_count, column1=row.col1, column2=row.col2,column3=row.col3,column4=row.col4,column5=row.col5,column6=row.col6,column7=row.col7,column8=row.col8,column9=row.col9,column10=row.col10, y=-1)

    # d = Train.create(session, auto_commit=True, reg_count=3, column3=1, column7=1, y=1)
    # print(d.reg_count, d.id)
    print("#########################################")
    return MessageOk()
'''

@router.put('/update_y')
async def update_label(request: Request, label_info: m.AddLabel):
    """
    File Label Update\n
    :param request:
    :param y:
    :param label:
    :return:
    """
    # user = request.state.user
    n_data = Train.filter(y= -1)
    request.state.inspect = frame()

    reet = n_data.update(auto_commit=True, **label_info.dict())
    print("2##########################################")
    return reet
    
@router.post('/show_file')
async def show_file_data(request:Request, file_path):
    """
    Ex_> D:/Project/pid/Scripts/fastapp/data/samples/pdf_sample2.pdf
    """
    request.state.inspect = frame()

    # file type: Dictionary
    file = loadFileManager(file_path)
    return file.data

@router.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}
    

@router.post("/uploadfiles")
async def create_upload_files(request: Request, files: List[UploadFile] = File(...), session: Session = Depends(db.session)):
    """
    params: Files \n
    return: Last File's \n
    [
            {
                page:1
                td: dfsdf
            },{
                page:2
                td: asdasdasda
            }
        ]
    """
    for file in files:
        contents = await file.read()
        print(os.path.join('./', file.filename))
        # with open(os.path.join('./', file.filename), "wb") as fp:
        with open(UPLOAD_DIRECTORY + file.filename, "wb") as fp:
            fp.write(contents)
        f = loadFileManager(UPLOAD_DIRECTORY + file.filename)
        try:
            obj = Files.create(session, auto_commit=False, name=f.name, ext=f.ext, ip_add= request.state.ip )
            # print(obj.id, f.name, f.ext, f.data)

            for p in f.data:
                df = preprocess_reg(p["td"])
                Train.create(session, auto_commit=True, file_id=obj.id ,y=-1, page=p["page"]+1, text_data=p["td"],
                                                        reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
                                                        column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
                                                        column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
                            )

        except Exception as e:
            raise ex.FileExtEx(file.filename)

    # 마지막 파일 f.data
    return f.data

