from typing import List

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, BackgroundTasks
# from future.utils import PY2
from sqlalchemy.orm import Session
from starlette.requests import Request

from Scripts.fastapp.common.consts import UPLOAD_DIRECTORY, ML_MODEL_PATH
from Scripts.fastapp.database.conn import db
from Scripts.fastapp.database.schema import Train, Files
from Scripts.fastapp import models as m
from Scripts.fastapp.errors import exceptions as ex
from inspect import currentframe as frame

from utils.file_module.load_file_manager import loadFileManager
from utils.preprocess_reg import preprocess_reg

from Scripts.fastapp.utils.ml.preprocess_train import preprocess, xedm_post, connect_session, pycaret_pred

from Scripts.fastapp.common.config import get_logger

import json
from collections import OrderedDict

from ast import literal_eval

import os
router = APIRouter(prefix='/xedm')
logger = get_logger()


# @router.get('/loadml')
# async def load_ml_for_xedm(request: Request):
#     """
#     no params\n
#     :return\n
#     Load ML Model
#     """
#     request.state.inspect = frame()
#     hoo.load_md(USING_MODEL_PATH)
#     if not hoo.model:
#         raise ex.XedmLoadFailEx()

#     return m.MessageOk()

@router.post("/uploadTest")
async def upload_files_read_test(request: Request, background_tasks: BackgroundTasks, files: List[UploadFile] = File(...) , session: Session = Depends(db.session)):
    """
    params: file \n
    return: Last File's \n
    return Sample: \n
    "file contents"
    """
    if not files:
        raise ex.XedmUploadFailEx()
    for file in files:
        contents = await file.read()
        with open(UPLOAD_DIRECTORY + file.filename, "wb") as fp:
            fp.write(contents)
        
        f = loadFileManager(UPLOAD_DIRECTORY + file.filename)
    
    return f.data
# @router.get('/loadml')
# async def load_ml_for_xedm(request: Request):
#     """
#     no params\n
#     :return\n
#     Load ML Model
#     """
#     request.state.inspect = frame()
#     hoo.load_md(USING_MODEL_PATH)
#     if not hoo.model:
#         raise ex.XedmLoadFailEx()

#     return m.MessageOk()

@router.get('/session')
async def connect_xedm_session(request: Request):
    """
    no params\n
    :return\n
    Connect session
    """
    request.state.inspect = frame()
    res = connect_session()
    logger.info(res)
    if not res:
        raise ex.XedmLoadFailEx()

    return res


@router.get('/xedmresponse', response_model = m.XedmToken)
async def xedm_response_test(request: Request):
    """
    no params \n
    descriptions: Xedm Token Test \n
    return XedmToken: \n
    """
    request.state.inspect = frame()
    docid = "2021050310132101"
    page = ['1','25','33','124']

    file_data = OrderedDict()
    ispid: str = 'T'

    pinfo_data = {"name":"ext:pinfo", "value": ispid }
    pPage_data = {"name":"ext:pPage", "value": ', '.join(page) }

    file_data["attrData"] = {"docId": docid, "attrList":[pinfo_data, pPage_data]}

    return file_data




@router.post("/uploadFiles")
async def upload_files_predict_y(request: Request, background_tasks: BackgroundTasks,docid: str, sid: str, files: List[UploadFile] = File(...) ,session: Session = Depends(db.session)):
    """
    params: docid, sid(session id) file \n
    return: Last File's \n
    return Sample: \n
    "OK"
    """
    if not files:
        raise ex.XedmUploadFailEx()
    for file in files:
        contents = await file.read()
        print(os.path.join('./', file.filename))
        # with open(os.path.join('./', file.filename), "wb") as fp:
        with open(UPLOAD_DIRECTORY + file.filename, "wb") as fp:
            # print(f'### UPLOAD DIRECTORY ### {UPLOAD_DIRECTORY + file.filename}')
            fp.write(contents)

        background_tasks.add_task(predict_using_pycaret, request = request, docid=docid, sid = sid, session = session, files=file)
    return m.MessageOk()
 

def predict_using_pycaret(request, docid, sid, session, files):
    print("## START PREDICT ON pyCaret ###")
    file_data = OrderedDict()
    pageList : list = []
    ispid: str = 'F'

    file_path = UPLOAD_DIRECTORY + files.filename
    file = loadFileManager(file_path)
    
    if not file.data:
        raise ex.FileExtEx(file.name)
    
    obj = Files.create(session, auto_commit=False, name=file.name, ext=file.ext, ip_add= request.state.ip, doc_id=docid )

    # Init 
    page = 0
    total_reg_count = 0
    tempList = []

    logger.info(file.data)
    for p in file.data:
        df = preprocess_reg(p["td"])

        page += 1
        total_reg_count += df["reg_count"][0]
        
        if df["reg_count"][0] > 0:
            pageList.append(str(page))
            tempList.append(1)
        else:
            tempList.append(0)

        Train.create(session, auto_commit=True, file_id=obj.id ,y=-1, page=p["page"]+1, text_data=p["td"],
                                                reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
                                                column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
                                                column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
                    )
    

    page_list = Train.filter(file_id=obj.id).order_by("page").all()
    df = preprocess(page_list)

    # 모델 안켜져 있을 경우 로드

    # PyCaret Model Load
    preds = pycaret_pred(df)

    result_list = [str(p+1) for  p, value in enumerate(preds) if value == 1]
    # model = load_ml_model(USING_MODEL_PATH)
    # if result_list or total_reg_count > 0:
    if result_list or total_reg_count > 0:
        ispid = "T"

        info = literal_eval("{'is_pid': True}") # literal_eval: str -> dict
        ret = Files.filter(id=obj.id)
        ret.update(auto_commit=True, **info)


    pinfo_data = {"name":"ext:pinfo", "value": ispid }
    pPage_data = {"name":"ext:pPage", "value": ', '.join(result_list) }

    file_data["attrData"] = {"docId": docid, "attrList":[pinfo_data, pPage_data]}
    print(file_data)
    res = xedm_post(file_data, sid)
    print(res.text)

    # remove upload file
    os.remove(file_path)

    # return file_data
"""def predict_using_h2o(request, docid, sid, session, file):
    print("## START PREDICT ON H2O")
    file_data = OrderedDict()
    pageList : list = []
    ispid: str = 'F'

    f = loadFileManager(UPLOAD_DIRECTORY + file.filename)
    
    if not f.data:
        raise ex.FileExtEx(f.name)

    obj = Files.create(session, auto_commit=False, name=f.name, ext=f.ext, ip_add= request.state.ip, doc_id=docid )
    # print(obj.id, f.name, f.ext, f.data)
    
    # Init 
    page = 0
    total_reg_count = 0
    tempList = []

    logger.info(f.data)
    for p in f.data:
        df = preprocess_reg(p["td"])

        page += 1
        total_reg_count += df["reg_count"][0]
        
        if df["reg_count"][0] > 0:
            pageList.append(str(page))
            tempList.append(1)
        else:
            tempList.append(0)

        Train.create(session, auto_commit=True, file_id=obj.id ,y=-1, page=p["page"]+1, text_data=p["td"],
                                                reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
                                                column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
                                                column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
                    )
    

    page_list = Train.filter(file_id=obj.id).order_by("page").all()
    df = preprocess(page_list)
    # hf = hoo.df_to_hf(df)

    # # 모델 안켜져 있을 경우 로드
    # if not hoo.model:
    #     hoo.load_md(USING_MODEL_PATH)
    # hoo.predict(hf)

    result_list = [str(p+1) for  p, value in enumerate(tempList) if value == 1]
    # model = load_ml_model(USING_MODEL_PATH)
    # if result_list or total_reg_count > 0:
    if result_list:
        ispid = "T"

        info = literal_eval("{'is_pid': True}") # literal_eval: str -> dict
        ret = Files.filter(id=obj.id)
        ret.update(auto_commit=True, **info)


    pinfo_data = {"name":"ext:pinfo", "value": ispid }
    pPage_data = {"name":"ext:pPage", "value": ', '.join(result_list) }

    file_data["attrData"] = {"docId": docid, "attrList":[pinfo_data, pPage_data]}
    print(file_data)
    res = xedm_post(file_data, sid)
    print(res.text)
    os.remove(UPLOAD_DIRECTORY + file.filename)"""