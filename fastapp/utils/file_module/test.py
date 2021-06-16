'''from Scripts.fastapp.utils.file_module.regex_dic_manager import regexDictionaryManager
from Scripts.fastapp.utils.file_module.keyword_extract import KeywordExtract
from Scripts.fastapp.utils.file_module.load_file_manager import loadFileManager

import pandas as pd

from Scripts.fastapp.common.consts import SAMPLE_FOLDER_PATH, KEYWORD_DICTIONARY_PATH

def t_load_data(file_name):
    origin_regex = regexDictionaryManager()
    file = loadFileManager(SAMPLE_FOLDER_PATH + file_name)

    # 사전에서 키워드 추출
    ke = KeywordExtract(KEYWORD_DICTIONARY_PATH)
    pages = list(file.data.keys())

    # 정규식 검출 수 Column을 Keyword List에 추가
    ke.keywords.insert(0, "reg_count")
    ke.keywords.insert(0, "page")

    data = []

    # df = pd.DataFrame(data, columns= ke.keywords)


    # CSV파일은 ,으로 구분
    row = ','.join(ke.keywords)

    # ke.keywords.insert(0, "page")

    # Page별 데이터 로드
    for page in range(0, len(pages)):
        print(f"############# PAGE: {page+1} #################")
        
        # regex name, count, regex_ruslt_list
        rn, c, rrl= origin_regex.get_all_regex(file.data[page])

        # 정규식 검출 수 Column 값 추가    
        row += '\n' + str(c)

        row_list=[page+1]
        row_list.append(c)

        # Keyword List에 Regex Count가 추가되어있기 때문에 -1 해줘야 함
        for i in range(0, len(ke.keywords)-2):
            row += ','
            # fileData / search() or findall()
            if ke.keyword_dictionary[i].search(file.data[page]): 
                # print(ke.keyword_dictionary[i].search(file.data[page]))
                row += '1'
                row_list.append(1)
            else:
                row += '0'
                row_list.append(0)
        
        data.append(row_list)
        print(row)

    print(data)
    c = ['page','reg_count','col1','col2','col3','col4','col5','col6','col7','col8','col9','col10']
    df = pd.DataFrame(data, columns= c)
    print(df)
    print("#")
    # print(df.to_json(orient='records'))
    return df
    '''