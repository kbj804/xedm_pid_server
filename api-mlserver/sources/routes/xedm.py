from typing import List

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
# from future.utils import PY2
from sqlalchemy.orm import Session
from starlette.requests import Request

from common.consts import UPLOAD_DIRECTORY, ML_MODEL_PATH, IMG_OUTPUT_PATH, IMG_OUTPUT

from database.conn import db
from database.schema import Train, Files
import models as m
from errors import exceptions as ex
from inspect import currentframe as frame
from utils.file_module.load_file_manager import loadFileManager
from utils.preprocess_reg import preprocess_reg
from utils.logger_handler import get_logger
from utils.ml.preprocess_train import preprocess, xedm_post, connect_session, pycaret_pred


import json
from collections import OrderedDict

from ast import literal_eval

import os
router = APIRouter(prefix='/xedm')
logger = get_logger()


@router.get('/imageread')
async def get_image_read(request: Request):
    """
	AI OCR의 결과값(rslt.json)을 읽어오는 함수. 
    Docker Volume을 활용한 임시 연동 결과를 보기 위해서 구현함.

	Parameters
	---
        noparams

    Returns
    ---
        AI OCR 결과
        
	"""
    request.state.inspect = frame()
    try:
        if os.listdir(IMG_OUTPUT):
            # files =  os.listdir(IMG_OUTPUT)
            RESULT_PATH = os.path.join(IMG_OUTPUT, 'rslt.json')
            with open(RESULT_PATH) as json_file:
                json_data = json.load(json_file)
                
            return json_data
    
    except:
        return ex.FileSearchEx()

@router.post("/uploadTest")
async def upload_files_read_test(request: Request, files: List[UploadFile] = File(...)):
    """
	File 업로드 테스트 함수
    업로드한 파일을 분석 가능한 포맷으로 변경 후 Return
	
	Parameters
	---
        noparams

    Returns
    ---
        File Object
        
	"""
    if not files:
        raise ex.XedmUploadFailEx()

    for file in files:
        contents = await file.read()
        FILE_PATH = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(FILE_PATH, "wb") as fp:
            fp.write(contents)
        
        f = loadFileManager(FILE_PATH)
    
    return f.data

@router.get('/session')
async def connect_xedm_session(request: Request):
    """
	XEDM에 Session ID를 요청하는 함수
	
	Parameters
	---
        noparams

    Returns
    ---
        XEDM Session ID
        
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
	XEDM에 요청한 데이터 포맷.
    단순 참고용이므로 삭제해도 무방함
	
	Parameters
	---
        noparams

    Returns
    ---
        XedmToken

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
async def upload_files_predict_y(request: Request, background_tasks: BackgroundTasks, docid: str, sid: str, files: List[UploadFile] = File(...) ,session: Session = Depends(db.session)):
    """
	XEDM으로부터 파일을 받아와서 BackgroundTasks로 Predict 진행
    BackgroundTasks로 진행하지 않으면 XEDM측에서 응답을 기다리고 있어야 하기 때문에 바로 OK 메세지를 Return한다.
	predict_using_pycaret()를 실행

	Parameters
    ---
        requests: predict_using_pycaret() 인자값으로 사용
        background_tasks: predict_using_pycaret() 실행 - FastAPI 제공
        docid: predict_using_pycaret() 인자값으로 사용
        sid: predict_using_pycaret() 인자값으로 사용
        files: predict_using_pycaret() 인자값으로 사용
        session: predict_using_pycaret() 인자값으로 사용
	
    Returns
    ---
        MessageOk() == "ok"

	"""
    if not files:
        raise ex.XedmUploadFailEx()
    for file in files:
        contents = await file.read()
        FILE_PATH = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(FILE_PATH, "wb") as fp:
            fp.write(contents)

        background_tasks.add_task(predict_using_pycaret, request = request, docid=docid, sid = sid, session = session, files=file)
    return m.MessageOk()
 

def predict_using_pycaret(request, docid, sid, session, files):
    """
    AutoML tools: Pycaret
    Pycaret이 생성한 모델 파일(ckpt)을 사용하여 새로 들어온 문서(files)에 예측을 적용함

    Parameters
    ---
    request: 사용자의 요청 정보가 담긴 객체. 이 함수에서는 사용자의 ip를 사용함
    docid: XEDM에서 받아온 Document ID
    sid: XEDM에서 받아온 Session ID
    session: Database 연결 유지를 위한 Session. XEDM session과 관련 없음
    files: 문서 File 객체

    """
    print("## START PREDICT ON pyCaret ###")
    file_data = OrderedDict()
    # pageList : list = []
    ispid: str = 'F'

    file_path = os.path.join(UPLOAD_DIRECTORY, files.filename)
    file = loadFileManager(file_path, docid)
    
    # 확장자 검사
    if not file.data:
        raise ex.FileExtEx(file.name)
    
    obj = Files.create(session, auto_commit=False, name=file.name, ext=file.ext, ip_add= request.state.ip, doc_id=docid )


    # 초기화
    # page = 0
    # total_reg_count = 0
    # tempList = []

    # logger.info(file.data)
    # for p in file.data:
    #     df = preprocess_reg(p["td"])

    #     page += 1
    #     total_reg_count += df["reg_count"][0]
        
    #     if df["reg_count"][0] > 0:
    #         pageList.append(str(page))
    #         tempList.append(1)
    #     else:
    #         tempList.append(0)

    #     Train.create(session, auto_commit=True, file_id=obj.id ,y=-1, page=p["page"]+1, text_data=p["td"],
    #                                             reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
    #                                             column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
    #                                             column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
    #                 )
    total_reg_count, df = create_trains(session, file.data, docid)

    # page_list = Train.filter(file_id=obj.id).order_by("page").all()
    # df = preprocess(page_list)

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



def create_trains(session, file_data, doc_id):
    pageList, tempList = []
    page, total_reg_count = 0
    file = Files.get(doc_id=doc_id)
    for p in file_data:
        df = preprocess_reg(p["td"])

        page += 1
        total_reg_count += df["reg_count"][0]
        
        if df["reg_count"][0] > 0:
            pageList.append(str(page))
            tempList.append(1)
        else:
            tempList.append(0)

        Train.create(session, auto_commit=True, file_id=file.id ,y=-1, page=p["page"]+1, text_data=p["td"],
                                                reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
                                                column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
                                                column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
                    )

        page_list = Train.filter(file_id=file.id).order_by("page").all()
        df = preprocess(page_list)
        
        return total_reg_count, df

@router.get("/ocrTest")
async def ai_ocr_test(request: Request, session: Session = Depends(db.session)):
    """
    AI OCR 테스트를 위한 함수
    현재는 사용하지 않는다.
    """
    request.state.inspect = frame()

    test = aiocr(IMG_OUTPUT_PATH)
    result = test.run()

    # start PID
    file_data = OrderedDict()
    pageList : list = []
    ispid: str = 'F'
    total_reg_count : int = 0
    page : int = 0
    tempList : list = []

    # config for testing
    fileid = 12345
    docid = 12345

    obj = Files.create(session, auto_commit=False, name='test', ext='pdf', ip_add= request.state.ip, doc_id=docid )
    for p in result:
        df = preprocess_reg(p["td"])

        # page += 1
        total_reg_count += df["reg_count"][0]
        
        if df["reg_count"][0] > 0:
            pageList.append(str(page))
            tempList.append(1)
        else:
            tempList.append(0)

        Train.create(session, auto_commit=True, file_id = obj.id ,y=-1, page=p["page"], text_data=p["td"],
                                                reg_count=int(df["reg_count"][0]), column1=int(df["col1"][0]), column2=int(df["col2"][0]),
                                                column3=int(df["col3"][0]),column4=int(df["col4"][0]),column5=int(df["col5"][0]),column6=int(df["col6"][0]),
                                                column7=int(df["col7"][0]),column8=int(df["col8"][0]),column9=int(df["col9"][0]),column10=int(df["col10"][0])
                    )
    

    page_list = Train.filter(file_id= obj.id).order_by("page").all()
    df = preprocess(page_list)

    # 모델 안켜져 있을 경우 로드
    # PyCaret Model Load
    if df.empty:
        raise ex.DataframeEmpty(df)
        
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
    
    # res = xedm_post(file_data, sid)
    # print(res.text)

    return file_data

