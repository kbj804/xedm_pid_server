import re

class RegexConfigs:

    def __init__(self):
        
        # 지역별 전화번호
        # 02서울 / 031경기 / 032인천 / 033강원 / 041충남 / 042대전 / 043충북 / 051부산 / 052울산 / 053대구 / 054경북 / 055경남 / 061전남 / 062광주 / 063전북 / 064제주
        localphoneRegex = re.compile(r'''(
            (\()?           # 괄호 있거나 없거나
            [0]{1}          # 맨 앞 1
            [2-6]{1}        # 지역번호 두번째 자리 2~6
            ([1-5]{1})?     # 지역번호 세번째 자리 1~5 (있거나 없거나)
            (\))?           
            (\W)?           # 숫자나 문자가 아닌 특수기호가 있거나 없거나(공백포함)
            (\d{3}|\d{4})   
            (\W)            # 이거까지 '?'를 붙이면 왠만한 숫자는 전부 전화번호로 찾아버림..
            ([0-9]{4})
            )''', re.VERBOSE)  

        # 휴대폰 번호
        phoneRegex = re.compile(r'''(
            \s
            ([01]{2})
            ([0|1|6|7|9]{1})
            (\W)?
            ([0-9]{3,4})
            (\W)?
            ([0-9]{4})
            )''', re.VERBOSE)

        # 이메일
        emailRegex = re.compile(r'''(  
            ([a-zA-Z0-9._%+-]+)      # 사용자명   
            @                        # @  
            ([a-zA-Z0-9.-]+)         # 도메인 이름  
            (\.[a-zA-Z]{2,4})        # 최상위 도메인  
            )''', re.VERBOSE)  

        # 주민등록번호
        registNumberRegex = re.compile(r'''(
            (\d{2})         # YY
            ([0-1]{1})      # MM 앞자리 0 ~ 1
            ([0-9]{1})      # MM 뒷자리
            ([0-3]{1})      # DD 앞자리 0 ~ 3
            ([0-9]{1})      # DD 뒷자리
            (\s)?
            [-]           # 하이푼
            (\s)?
            ([1-4]{1})      # 뒷자리 시작 1~4
            (\d{6})
            )''', re.VERBOSE)

        # 신용카드
        # 시작번호에 따른 카드 종류 (3:아메리칸익스프레스,JBC카드 등 / 4: 비자카드 / 5: 마스터카드 / 6: 중국은련카드 / 9: 각 국가 내에서 사용하는 카드번호)
        creditcardRegex = re.compile(r'''(
            ([3-6]{1}|[9]{1})
            (\d{3})
            ([-]\d{4}[-]\d{4}[-]\d{4})
        )''', re.VERBOSE)

        # 계좌번호
        accountRegex = re.compile(r'''(
            (\d{3})
            -
            (\d{6})
            -
            (\d{2})
            -
            (\d{3})
        )''', re.VERBOSE)

        accountConfig = '''
        # 기업은행 / 우리은행
        \d{3}[-]\d{6}[-]\d{2}[-]\d{3}

        # 경남은행
        \d{3}[-]\d{2}[-]\d{7}

        # 국민은행
        \d{6}[-]\d{2}[-]\d{6}

        # 농협은행 / 신한은행 / 제일은행
        \d{3}[-]\d{2}[-]\d{6}

        # 대구은행
        \d{3}[-]\d{2}[-]\d{6}[-]\d{1}

        # 부산은행
        \d{3}[-]\d{2}[-]\d{2}[-]\d{4}[-]\d{1}

        # 산업은행
        \d{3}[-]\d{4}[-]\d{4}[-]\d{3}

        # 외환은행
        \d{3}[-]\d{2}[-]\d{5}[-]\d{1}

        # 하나은행
        \d{3}[-]\d{6}[-]\d{5}

        # 한미은행
        \d{3}[-]\d{5}[-]\d{3}

        '''
        
        # IP 주소
        ipAddressRegex = re.compile(r'''(
            (\d{1,3})
            [.]
            (\d{1,3})
            [.]
            (\d{1,3})
            [.]
            (\d{1,3})
        )''', re.VERBOSE)

        # MAC 주소
        macAddressRegex = re.compile(r'''(
            ([0-9A-F]{2}[:-]){5}
            ([0-9A-F]{2})
        )''', re.VERBOSE)


        # 여권 번호
        # T 여행자증명서, M 복수여권, S 단수여권, R 거주여권, G 공무원 관용여권, D 외교관 여권
        passportRegex = re.compile(r'''(
            ([T|M|S|R|G|D|t|m|s|r|g|d])
            (\d{8})
        )''', re.VERBOSE)

        # 운전면허 번호 (2014년 이전 이후)
        # 서울 11, 경기 13, 가원 14, 충북 15, 충남 16, 전북 17, 광주전남 18, 경북 19, 경남 20, 제주 21, 대구 22, 인천 23, 대전 25, 울산 26
        driverLicenseRegex = re.compile(r'''(
            ([1-2]{1}\d{1}|서울|경기|강원|충북|충남|전북|광주전남|경북|경남|제주|대구|인천|대전|울산)
            ([-])
            (\d{2}[-])
            (\d{6}[-])
            (\d{2})
        )''', re.VERBOSE)

        # 건강보험번호
        healthInsRegex = re.compile(r'''(
            ([1,2,5,7]{1})      # 1-1900년도에 발금된 지역건강보험 가입자 / 2-2000년도에 발급된 지역건강보험 발급자 / 5-공무원 및 사립학교 가입자 / 7-기타직장건강보험 가입자
            [-]
            (\d{10})
        )''', re.VERBOSE)

        # 이미지 파일
        imageRegex = re.compile(r'''(
            (([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]|\w)+.(jpg|png|gif|bmp|tif))
        )''', re.VERBOSE)

        # 압축파일
        compressionRegex = re.compile(r'''(
            (([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]|\w)+.(tar|zip|gzip|alz|egg|iso|7zip))
        )''', re.VERBOSE)

        # 오디오파일
        audioRegex = re.compile(r'''(
            (([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]|\w)+.(mp3|wav))
        )''', re.VERBOSE)

        # 문서파일
        docRegex = re.compile(r'''(
            (([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]|\w)+.(pdf|rtf|html|xml|csv|txt|ppt|hwp|xlxs|docx|log))
        )''', re.VERBOSE)


        # 위 정규식 통합 Dictionary
        self.preComfile_dic = {
            'E-mail': emailRegex,
            'Local_PhoneNumber': localphoneRegex,
            'PhoneNumber': phoneRegex,
            'ResidentRegistrationNumber': registNumberRegex,
            'CreditCardNumber':creditcardRegex,
            'ipAddress':ipAddressRegex,
            'macAddress':macAddressRegex,
            'PassportNumber': passportRegex,
            'DriverLicenseNumber': driverLicenseRegex,
            'HealthInsuranceCertification' : healthInsRegex,
            'ImageFile': imageRegex,
            'CompressionFile': compressionRegex,
            'AudioFile': audioRegex,
            'DocumentFile':docRegex
        }


        # Dictionary로 KEY List 생성
        self.preComfile_list = list(self.preComfile_dic.keys())