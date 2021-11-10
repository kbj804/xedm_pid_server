import re

class KeywordExtract:
    """
    개인정보검출시 필요한 KEY WORD

    ---
    Parameters

        keyword_path: 단어가 들어가있는 txt파일

    ---
    Returns

        단어를 keyword_dictionary에 Dictionary Type으로 저장

    """
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


# ------------------ ------------------ #
#  사용 예제
# ------------------ ------------------ #
# a = KeywordExtract(PATH)
# print(a.keywords)
# print(a.keyword_dictionary)
# text = "jdgajdsngj sdfsadkljn kfgoodf sd f njlksdfn agter  sdalfafter sdnfj good"

# for i in range(0, len(list(a.keyword_dictionary.keys()))):
#     print(a.keyword_dictionary[i].search(text))


