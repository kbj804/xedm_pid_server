# ML Test용 RestAPI, 실제 동작에는 영향 없음

from typing import List

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
# from future.utils import PY2
# from h2o.h2o import resume
from sqlalchemy.orm import Session
from starlette.requests import Request

# from Scripts.fastapp.common.consts import UPLOAD_DIRECTORY, USING_MODEL_PATH
from database.conn import db
from database.schema import Train, Files
import models as m
from errors import exceptions as ex
from inspect import currentframe as frame

# from utils.ml.h2o_helper import H2oClass
from utils.ml.preprocess_train import preprocess
from ast import literal_eval

import os
router = APIRouter(prefix='/ml')
# hoo = H2oClass()

@router.get('/getTrainData', response_model=List[m.FeatureToken])
async def show_data(request: Request):
    """
    no params\n
    :return\n
    Train Model
    """
    request.state.inspect = frame()
    result = Train.filter(is_train=False).all()
    train_save_model(result)

    return result


@router.get('/getPidTest')
async def get_pidpidpid(request: Request, id:int):
    """    
    Train에서 is_train True 인것들 중에
    중복제거하고 file_id로 sum(reg_count)가 0이상이면 File의 is_pid = True
    """
    request.state.inspect = frame()
    result = Train.filter(is_train=True, file_id=id, reg_count__gt= 0).count()  # reg_count가 0이상인게 한개라도 있으면..
    # if result > 0:
    #     info = literal_eval("{'is_pid': True}")
    #     ret = Files.filter(file_id=id)
    #     ret.update(auto_commit=True, **info)

    return result

@router.put('/updateTD')
# async def update_train_data(request:Request, info : m.AddIsTrain):
async def update_train_data(request:Request):
    """
    train데이터 중 학습에 활용된 데이터는 True로 변경
    """
    request.state.inspect = frame()
    result = Train.filter(is_train=False)

    # 여기에서 True로 바꿔주면 됨..
    info = literal_eval("{'is_train': True}") # literal_eval: str -> dict
    print("#################",info)

    ret = result.update(auto_commit=True, **info)
    
    return ret


@router.get('/getLoadML')
async def get_load_ml_md(request: Request):
    """
    no params\n
    :return\n
    Load ML Model
    """
    request.state.inspect = frame()
    # result = Train.filter(y=1).all()
    hoo.load_md(USING_MODEL_PATH)

    result = Files.filter(is_pid=False).all()
    # print("##RESULT##", result)
    # return dict(id=result[0].id, reg_count=result[0].reg_count)
    return result

@router.get('/getPredictFile')
async def get_predict_file_id(request: Request, file_id: int):
    """
    params: file_id\n
    :return\n
    Predict Result
    hoo.predict: List
    ex) [0, 0, 1, 0, 0] / index + 1 = page
    """
    request.state.inspect = frame()
    result = Train.filter(file_id=file_id).order_by("page").all()
    df = preprocess(result)
    hf = hoo.df_to_hf(df)
    hoo.predict(hf)
    
    result_list = [i+1 for  i, value in enumerate(hoo.preds) if value == 1]
    # model = load_ml_model(USING_MODEL_PATH)
    if not result_list:
        return "NO PID"

    return result_list

@router.get('/getPredictPage')
async def get_predict_train_id(request: Request, train_id: int):
    """
    params: train_id(page_id)\n
    :return\n
    Predict Result
    ex) [0] or [1]
    """
    request.state.inspect = frame()
    result = Train.filter(id= train_id).all()
    print("######",result)
    df = preprocess(result)
    hf = hoo.df_to_hf(df)
    hoo.predict(hf)
    
    # model = load_ml_model(USING_MODEL_PATH)

    return hoo.preds
