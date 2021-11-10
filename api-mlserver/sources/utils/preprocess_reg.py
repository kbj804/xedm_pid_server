# -*- coding: utf-8 -*-

from utils.file_module.regex_dic_manager import regexDictionaryManager
from utils.file_module.keyword_extract import KeywordExtract
from utils.file_module.load_file_manager import loadFileManager
import pandas as pd

from common.consts import SAMPLE_FOLDER_PATH, KEYWORD_DICTIONARY_PATH

def preprocess_reg(textdata:str):
    """
	키워드 사전(dictionary_PATH)에서 읽어온 키워드들을 column으로 사용하여 
    정규식으로 text에 키워드의 유무를 검사한다. 
    검사 결과로 dataframe 생성 후 리턴
	
	Parameters
	---
        textdata: 검사하려고하는 text 데이터

    Returns
    ---
        Dataframe: 키워드 검사 결과
        
	"""
    origin_regex = regexDictionaryManager()

    # 사전에서 키워드 추출
    ke = KeywordExtract(KEYWORD_DICTIONARY_PATH)

    # 정규식 검출 수 Column을 Keyword List에 추가
    ke.keywords.insert(0, "reg_count")
    print(ke.keyword_dictionary)
    data = []

    # regex name, count, regex_ruslt_list
    _, c, _= origin_regex.get_all_regex(textdata)

    # 정규식 검출 수 Column 값 추가
    row_list=[]
    row_list.append(c)

    # Keyword List에 Regex Count가 추가되어있기 때문에 -1 해줘야 함
    for i in range(0, len(ke.keywords)-1):
        # fileData / search() or findall()
        if ke.keyword_dictionary[i].search(textdata): 
            row_list.append(1)
        else:
            row_list.append(0)
    
    data.append(row_list)

    c = ['reg_count','col1','col2','col3','col4','col5','col6','col7','col8','col9','col10']
    df = pd.DataFrame(data, columns= c)
    print(df)
    print("#")
    
    return df

# ------------------ ------------------ #
#  사용 예제
# ------------------ ------------------ #
# text = "asfsdfajksfdkal;sdafkl;jsdfkl"
# df = preprocess_reg(text)
# print(type(df["col1"][0]))
# print(df["col1"][0])
# print(df["reg_count"].iloc[0])