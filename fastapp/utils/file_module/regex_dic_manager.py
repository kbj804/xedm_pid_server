import re
import time

# import os
# print(os.path.abspath(os.path.dirname(__file__)))
from Scripts.fastapp.common.regex_config import RegexConfigs
from Scripts.fastapp.common.consts import REGEX_FOLDER_PATH, ADDRESS_UmMyunDong, ADDRESS_SiGunGu, ADDRESS_RoGil

class regexDictionaryManager(RegexConfigs):
    def __init__(self):
        super().__init__()

        # new regex Dictionary
        self.dictionary={}
    
        # origin_regex = RegexConfigs()
        # self.origin_Dictionary = origin_regex.preComfile_dic
        self.origin_Dictionary = self.preComfile_dic
    
    # 키값 있는지 없는지 검사
    def check_key(self, key):
        try:
            if self.origin_Dictionary[key]:    # else시 에러
            # if key in self.origin_Dictionary:    # return값 boolean 
                value = self.origin_Dictionary.get(key)    # return값 value
                return value
            else:
                print("@ # @ # {} For Debugging... @ # @ #".format(key))
        
        except Exception as e:
            print("####ERROR#### {0} dose not exist in Regualr-Dictionary".format(e))
    
    # Dictionary에 정규표현식 추가
    def add_regex(self, key):
        v = self.check_key(key)
        if v == None:
            pass
        else:
            self.dictionary.setdefault(key, v)
            print("Success Add Regular Expression Dictionary")

    def show_dictionary(self):
        keys = list(self.dictionary.keys())
        print("key list = {}".format(keys))
        print(self.dictionary)

    # string file을 csv로 추출
    def extract_csv(self, data, filename):
        with open(REGEX_FOLDER_PATH + filename + '.csv', "w") as file:
            file.write(filename + '\n' + data)
            file.write(data)
            file.close()

    # 문자
    def get_regex_result(self, data):
        keys = list(self.dictionary.keys())

        for i in range(0, len(keys)):
            result = ''
            for regex in self.dictionary[keys[i]].findall(data):
                result += str(regex[0]) + '\n'
            
            self.extract_csv(result, keys[i])
            print("{} is Success Extract".format(keys[i]))
    
    # 모든 정규식 다 돌림
    def get_all_regex(self, data):
        keys = list(self.origin_Dictionary.keys())
        total_count = 0
        regex_name_list = []
        regex_result_list = []
        for i in range(0, len(keys)):
            sub_count=0
            # ADDRESS Regex
            for regex in self.origin_Dictionary[keys[i]].findall(data):
                print(regex)
                if i >= 15 and i <= 16:
                    """ADDRESS Regex
                    ADDRESS_RoGil, ADDRESS_SiGunGu, ADDRESS_UmMyunDong,
                    """
                    if regex[0] in self.rogilDict:
                        regex_result_list.append(regex[0])
                        sub_count+=1
                    elif regex[0] in self.sigunguDict:
                        regex_result_list.append(regex[0])
                        sub_count+=1
                    elif regex[0] in self.umdDict:
                        regex_result_list.append(regex[0])
                        sub_count+=1
                
                else:
                    # result = ''
                    # result += str(regex[0]) + '\n'
                    regex_result_list.append(regex[0])
                    sub_count+=1

            if sub_count > 0:
                total_count += sub_count
                regex_name_list.append(keys[i])
                
                # print(f"{keys[i]}[{sub_count}]: {result}")

        
        return regex_name_list, total_count, regex_result_list


a = regexDictionaryManager()
r  = a.get_all_regex("asdfafdasf 010-6328-0391 서울시 영등포구 여의도 국회로 서울특별시 구로구 여의도동 44-11 종로2가 모택동 짱구 걸어서 세계속으로 코로나 아니길 국회의사당로 세종대로")
print(r)