import re

class KeywordExtract:
    def __init__(self, keyword_path) -> None:
        self.keywords : list = []
        # self.keywords=['reg_count']
        self.keyword_dictionary = {}

        with open(keyword_path, mode="r", encoding='UTF8') as kwd_file:
            for kwd in kwd_file:
                # preprocessing for reducing tail string
                index = kwd.find('\t')
                word = kwd[:index]

                self.keywords.append(word)
        
        for i, kwd in enumerate(self.keywords):
            self.keyword_dictionary[i] = re.compile(kwd)


# a = KeywordExtract(r"./tesseract_Project/Scripts/tp/nlp/dic.txt")
# print(a.keywords)
# print(a.keyword_dictionary)
# text = "jdgajdsngj sdfsadkljn kfgoodf sd f njlksdfn agter  sdalfafter sdnfj good"

# 사용 예제
# for i in range(0, len(list(a.keyword_dictionary.keys()))):
#     print(a.keyword_dictionary[i].search(text))


