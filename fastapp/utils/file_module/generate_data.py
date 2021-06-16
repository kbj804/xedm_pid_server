import pandas as pd

from Scripts.fastapp.common.consts import KEYWORD_DICTIONARY_PATH, DEFAULT_CSV_PATH
from Scripts.fastapp.utils.file_module.regex_dic_manager import regexDictionaryManager
from Scripts.fastapp.utils.file_module.keyword_extract import KeywordExtract
from Scripts.fastapp.utils.file_module.load_file_manager import loadFileManager

class GenerateData:
    def __init__(self) -> None:
        # super().__init__()
        # self.default_csv_model_path = './regex_result/model.csv'
        self.origin_regex_dic = regexDictionaryManager()
        self.kwd = KeywordExtract(KEYWORD_DICTIONARY_PATH)
        # self.kwd = KeywordExtract(r'D:\\Project\\tesseract\\tesseract_Project\Scripts\\tp\\nlp\\dic.txt')

    def set_default_datafram(self):
        self.default_model_df = pd.read_csv(DEFAULT_CSV_PATH, encoding='UTF-8')

    def update_model_df(self, df_data):
        # print(self.default_model_df)
        # print(df_data)
        c_df = pd.concat([self.default_model_df, df_data]).reset_index(drop=True)
        c_df.to_csv(DEFAULT_CSV_PATH, sep=',', na_rep='NaN', encoding='UTF-8', index=False)
        return c_df


    # need generate file path
    def file_to_dataframe(self, file_path):
        # file type: Dictionary
        file = loadFileManager(file_path)
        pages = list(file.data.keys())

        data =[]

        for page in range(0, len(pages)):
            # regex name, count, regex_ruslt_list
            _, c, _= self.origin_regex_dic.get_all_regex(file.data[page])

            row_list = [c]

            # Keyword List에 Regex Count가 추가되어있기 때문에 인덱스 1부터시작 해줘야 함
            for i in range(1, len(self.kwd.keywords)):
                # fileData / search() or findall()
                if self.kwd.keyword_dictionary[i].search(file.data[page]): 
                    # print(ke.keyword_dictionary[i].search(file.data[page]))
                    row_list.append(1)
                else:
                    row_list.append(0)
            
            data.append(row_list)
        
        df = pd.DataFrame(data, columns=self.kwd.keywords)
        return df