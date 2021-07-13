import pandas as pd
from common.consts import XEDM_URL, ML_MODEL_PATH
from common.config import get_logger

import requests
import json

import pycaret
from pycaret.classification import load_model, predict_model

logger = get_logger()

def preprocess(results:list):
    """
    학습용 Data Frame 생성
    """
    data: list = []
    columns = ['id','reg_count','column1','column2','column3','column4','column5','column6','column7','column8','column9','column10']
    for _, r in enumerate(results):
        a=[]
        a.append(r.id)
        a.append(r.reg_count)

        for i in range(1, 11):
            a.append(eval(f"r.column{i}"))

        data.append(a)
    
    print(pd.DataFrame(data, columns=columns))
    return pd.DataFrame(data, columns=columns)


def xedm_post(data, sid):
    print("####### PUSH PUSH POST ######")
    # url = f"http://183.111.96.15:7086/xedrm/json/updateDocEx?sid={sid}"
    url = f"http://{XEDM_URL}/xedrm/json/updateDocEx?sid={sid}"
    jsondata = json.dumps(data, indent=4)
    # logger.info(jsondata)
    headers = {'Content-Type': 'application/json;'}
    res = requests.post(url, headers= headers, data = jsondata, timeout=10 )
    logger.info(res)
    print(res)
    print(jsondata)
    print("####### PUSH DONE ######")
    return res

def connect_session():
    print("####### Connection Xedm Session ######")
    url = 'http://{XEDM_URL}/xedrm/json/login?isAgent=True&lang=ko&userId=Qmhp/4rwH78=&mode=jwt'

    res = requests.get(url)
    res = json.loads(res.text)
    session = res['list'][0]['xedmSession']

    return session

def pycaret_pred(data):
    saved_model = load_model(ML_MODEL_PATH)
    pred = predict_model(saved_model, data=data)

    return pred['Label'].tolist()

# pycaret_pred()
# sid = connect_session()
# res = xedm_post({'asd':1}, 'sid')
# print(res)