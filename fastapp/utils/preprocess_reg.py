# -*- coding: utf-8 -*-

from Scripts.fastapp.utils.file_module.regex_dic_manager import regexDictionaryManager
from Scripts.fastapp.utils.file_module.keyword_extract import KeywordExtract
from Scripts.fastapp.utils.file_module.load_file_manager import loadFileManager
import pandas as pd

from Scripts.fastapp.common.consts import SAMPLE_FOLDER_PATH, KEYWORD_DICTIONARY_PATH

def preprocess_reg(textdata:str):
    """
    정규표현식
    return: Dataframe
    """
    origin_regex = regexDictionaryManager()

    # 사전에서 키워드 추출
    ke = KeywordExtract(KEYWORD_DICTIONARY_PATH)

    # 정규식 검출 수 Column을 Keyword List에 추가
    ke.keywords.insert(0, "reg_count")
    print(ke.keyword_dictionary)
    data = []

    # df = pd.DataFrame(data, columns= ke.keywords)

    # regex name, count, regex_ruslt_list
    _, c, _= origin_regex.get_all_regex(textdata)

    # 정규식 검출 수 Column 값 추가
    row_list=[]
    row_list.append(c)

    # Keyword List에 Regex Count가 추가되어있기 때문에 -1 해줘야 함
    for i in range(0, len(ke.keywords)-1):
        # fileData / search() or findall()
        if ke.keyword_dictionary[i].search(textdata): 
            # print(ke.keyword_dictionary[i].search(file.data[page]))
            row_list.append(1)
        else:
            row_list.append(0)
    
    data.append(row_list)

    # print(data)
    c = ['reg_count','col1','col2','col3','col4','col5','col6','col7','col8','col9','col10']
    df = pd.DataFrame(data, columns= c)
    print(df)
    print("#")
    
    # print(df.to_json(orient='records'))
    return df

# text = "asfsdfajksfdkal;sdafkl;jsdfkl"
# df = preprocess_reg(text)
# print(type(df["col1"][0]))
# print(df["col1"][0])
# print(df["reg_count"].iloc[0])