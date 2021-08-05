import numpy as np
import cv2
import math
import pandas as pd
from scipy.ndimage import interpolation as inter
import os
import pytesseract
import re
from scipy import stats
import argparse
from utils.aiocr.file_utils import get_files
import utils.aiocr.imgproc
import time
import json
from tqdm import tqdm

class aiocr():
    def __init__(self, path_in='./input'):
        self.path_in = path_in
        self.image_list, _, _ = get_files(self.path_in)        
        self.start = time.time()
        self.record = pd.DataFrame(columns=['src','id','pg','cdnt','y','x','h','w','shp_h','shp_w','cntNotBlack','cntBlack','percnt','mtd','txt'])
        self.rslt = []

    def determine_score(self, arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    def correct_skew(self, image, delta=1, limit=5):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for a in angles:
            histogram, score = self.determine_score(arr=thresh, angle=a)
            scores.append(score)

        best_angle = angles[scores.index(max(scores))]

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
                borderMode=cv2.BORDER_REPLICATE)

        return best_angle, rotated

    def psm(self, num, crop_img, text_sub, post_wrd):
        if len(''.join(text_sub.split())) == 0:
            config='--psm '+str(num)+' -c preserve_interword_spaces=1'
            text_sub = pytesseract.image_to_string(crop_img, lang="Hangul", config=config)
            for n in range(len(post_wrd)):
                text_sub = text_sub.replace(post_wrd[n],' ')
            text_sub = text_sub.replace('\n',' ')
            if text_sub == '0':text_sub=' '
            elif ''.join(text_sub.split()) == '':text_sub=' ' 
        else: text_sub = text_sub
        return text_sub

    def run_psm(self, text, crop_img, post_wrd, test):
        text_sub = ""      
        config='--psm 6 -c preserve_interword_spaces=1'
        text_sub = pytesseract.image_to_string(crop_img, lang="Hangul", config=config)
        for n in range(len(post_wrd)):
            text_sub = text_sub.replace(post_wrd[n],' ')
        text_sub = text_sub.replace('\n',' ')
        if text_sub == '0':text_sub=' '
        elif ''.join(text_sub.split()) == '':text_sub=' '

        text_sub = self.psm(7, crop_img, text_sub, post_wrd)
        text_sub = self.psm(10, crop_img, text_sub, post_wrd)
        text_sub = self.psm(1, crop_img, text_sub, post_wrd)
        text_sub = self.psm(8, crop_img, text_sub, post_wrd)
        text_sub = ' '.join(text_sub.split())

        if text == "":
            text = text + "" + text_sub.strip() 
        else:
            text = text + " " + text_sub.strip()
        return text_sub, text

    def t2t(self, path_, record, test, p_num, plan):   
        
        post_wrd = ['[of','|]','~\n','Po','JJ','|','(00 ','1 E',"'",'. ',"~,",'I',',','ㅣ','게게에','“','qo\n','ees\n','”'
                    ,'mo\n','meme\n','EE\n','CN\n','os\n','CO\n','Cs\n','Co\n','ff %','ff-','ff -','~ CE]','oo\n','ommmnl','—'
                    ,'pe =','sitet oes','%:']

        orig = cv2.imread(path_)   

        if orig.shape[1] > 1024 :   
            orig = cv2.resize(orig, dsize=(int(orig.shape[1]/(orig.shape[1]/1024)), int(orig.shape[0]/(orig.shape[1]/1024)))
                            , interpolation=cv2.INTER_AREA)       

        ngle, orig = self.correct_skew(orig)

        img = orig.copy()

        gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_bin = cv2.adaptiveThreshold(gray_scale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1) 

        img_bin = cv2.Laplacian(img_bin, cv2.CV_8U, ksize=5)

        line_min_width = 50
        kernal_h = np.ones((1,line_min_width), np.uint8)
        kernal_v = np.ones((line_min_width,1), np.uint8)

        img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
        img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
        img_bin_h_o = img_bin_h.copy()

        indices = np.nonzero(img_bin_h[300:img_bin_h.shape[0]-300,:])
        col = np.unique(indices[1])
        if len(col) == 0:
            text = ''
            table_yn = 'n'
        else:
            table_yn = 'y'
            indices = np.nonzero(img_bin_h)
            row = np.unique(indices[0])
            row = row[row>50]
            min_col = np.min(col)
            max_col = np.max(col)
            min_col_itr = 9    
            img_bin_h[np.min(row):np.max(row),np.min(col):min_col+min_col_itr] = 255
            img_bin_h[np.min(row):np.max(row),np.max(col)] = 255

            img_bin_final = img_bin_h|img_bin_v

            for i in range(img_bin_final.shape[0]):
                w = 0
                b = 0
                s = 0
                e = 0
                for j in range(img_bin_final.shape[1]):     
                    if img_bin_final[i][j] > 1:
                        w += 1
                        b += 1
                        if w < 2:            
                            s = j
                        if w == 2:
                            e = j
                            w = 0
                            dif = (e - s)
                            if (dif > 0) and (dif < 50) and (b > 30):
                                for k in range((e - s + 1)):
                                    img_bin_final[i][j-k] = 255
                            s = j
                            w = 1

            itr = 3
            itr2 = 1

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            img_bin_final = cv2.dilate(img_bin_final, kernel, iterations=itr)
            img_bin_final = cv2.erode(img_bin_final, kernel, iterations=itr-itr2)

            _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)   
            
            points = stats[2:]
            points = np.append(np.array([[0, 0, orig.shape[0], points[0][1],1]]), points, axis=0)
            points = np.append(points, np.array([[0, points[len(points)-1][1]+points[len(points)-1][3],orig.shape[0],orig.shape[1],1]]), axis=0)
            
            pad = 10
            text = ''
            
            num = 0
            
            for x,y,w,h,area in points:
                num += 1
                    
                if x == min_col+min_col_itr+itr-itr2:     
                    x = x-min_col_itr-itr-pad
                    w = w+min_col_itr+itr+pad
                    
                if x+w > max_col-10:
                    w = w+min_col_itr+itr+pad            

                # 수정한 부분
                # sub_img = cv2.Laplacian(gray_scale[y:y+h, x:x+w], cv2.CV_8U, ksize=5)

                if gray_scale[y:y+h, x:x+w].shape[0] == 0:
                    pass

                else:
                    # FastAPI 서버에서 Laplacian 할때, x의 shpae가 0인 경우에 문제가 생김.
                    # 일반적으로 kernel에서 실행하면 정상적이지만.. 내부적으로 에러 처리가 되어있는 듯 함 
                    sub_img = cv2.Laplacian(gray_scale[y:y+h, x:x+w], cv2.CV_8U, ksize=5)
                    
                    if test == 'y':
                        print(sub_img.shape)
                    eroded = cv2.morphologyEx(sub_img, cv2.MORPH_OPEN, kernal_h)
                    indices = np.nonzero(eroded)
                    rows = np.unique(indices[0])

                    if (len(rows) > 10) and (x > 0):
                        pass
                    else:
                        cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),2)

                        crop_img = gray_scale[y:y+h, x:x+w]

                        crop_bin_v = img_bin_v[y:y+h, x:x+w]
                        crop_bin_h = img_bin_h_o[y:y+h, x:x+w]

                        mask_v = cv2.findNonZero(crop_bin_v)
                        mask_h = cv2.findNonZero(crop_bin_h)
                        
                        sub = crop_img.copy()
                                        
                        if type(mask_v) is np.ndarray:
                            for i in range(len(mask_v)):
                                crop_img[mask_v[i][0][1],mask_v[i][0][0]] = 255
                        
                        if type(mask_h) is np.ndarray:
                            if (crop_img.shape[1] < 500):
                                for i in range(len(mask_h)):
                                    crop_img[mask_h[i][0][1],mask_h[i][0][0]] = 255
                            
                        sub_bin = cv2.adaptiveThreshold(sub, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1)             

                        cntNotBlack = cv2.countNonZero(sub_bin)
                        cntBlack = sub_bin.shape[0]*sub_bin.shape[1]- cntNotBlack
                        percnt = cntBlack/(cntBlack+cntNotBlack)
                        if test == 'y':
                            print('cntNotBlack :',cntNotBlack,'cntBlack :',cntBlack, 'percnt :', percnt)
            
                        mtd = ''

                        if type(mask_v) is np.ndarray:                    
                            if (crop_img.shape[1] < 500):
                                if (x > 10) and (x < 300) and (percnt > 0.18):
                                    if test == 'y':
                                        print('# crop_img[crop_img<230]')
                                for i in range(len(mask_v)):
                                    crop_img[mask_v[i][0][1],mask_v[i][0][0]] = 255
                                    
                        if (percnt < 0.009) or (cntBlack < 140):
                            if test == 'y':
                                print('Pass ...')
                            text_sub = ''

                        else:
                            if plan == 1:
                                crop_img[crop_img<230] = 0
                            elif plan == 2:
                                crop_img[crop_img<200] = 0
                                crop_img = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91,91)
                            elif plan == 3:
                                crop_img = cv2.resize(crop_img, dsize=(crop_img.shape[1]*10, crop_img.shape[0]*11), interpolation=cv2.INTER_LANCZOS4)
                            elif plan == 4:
                                crop_img[crop_img<200] = 0
                                crop_img = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91,91)
                                crop_img = cv2.resize(crop_img, dsize=(crop_img.shape[1]*10, crop_img.shape[0]*11), interpolation=cv2.INTER_LANCZOS4)
                            elif plan == 5:
                                crop_img[crop_img<230] = 0
                                crop_img = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91,91)     
                            elif plan == 6:
                                crop_img[crop_img<230] = 0
                                crop_img = cv2.resize(crop_img, dsize=(crop_img.shape[1]*10, crop_img.shape[0]*11), interpolation=cv2.INTER_LANCZOS4)                                                                                    
                            elif plan == 7:
                                crop_img[crop_img<230] = 0
                                crop_img = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91,91)                    
                                crop_img = cv2.resize(crop_img, dsize=(crop_img.shape[1]*10, crop_img.shape[0]*11), interpolation=cv2.INTER_LANCZOS4)
                                                                                
                            if cntNotBlack > cntBlack:
                                text_sub, text = self.run_psm(text, crop_img, post_wrd, test) 
                            else:
                                text_sub, text = self.run_psm(text, ~crop_img, post_wrd, test)
                                               
                        record = record.append(pd.DataFrame({'src':[path_]
                                                            ,'id':[path_+str(num)]
                                                            ,'pg':[p_num]
                                                            ,'cdnt': [str(y)+', '+str(h)+', '+str(x)+', '+str(w)]
                                                            ,'y':[y]
                                                            ,'x':[x]         
                                                            ,'h':[h]
                                                            ,'w':[w]
                                                            ,'shp_h': [sub_img.shape[0]]                                                     
                                                            ,'shp_w': [sub_img.shape[1]]
                                                            ,'cntNotBlack':[cntNotBlack]
                                                            ,'cntBlack':[cntBlack]
                                                            ,'percnt':[percnt]
                                                            ,'mtd':[mtd]
                                                            ,'txt':[text_sub]}))

            record = record.reset_index(drop=True)
                                            
            text = text.replace('',' ')
            text = text.replace('\n',' ')
            text = ' '.join(text.split())    
        
        return record, text, table_yn

    def run(self): # 이미지 리스트 받아오는거 자체를 변경
        for i in range(len(self.image_list)):
            print(self.image_list)
            record_dict = {}
            p_num = ''
            p_num = re.sub(r".+\|p([0-9]{1,10000})\.jpg", r"\1", self.image_list[i])
            
            if len(p_num) == len(self.image_list[i]):
                p_num = '1'

            print('> Start :', self.image_list[i])
            self.record, text, table_yn = self.t2t(path_=self.image_list[i], record=self.record, test='n', p_num=p_num, plan=3)
            print('< Complete :', self.image_list[i])
            if table_yn == 'y':
                record_dict['page'] = p_num
                data = []
                for j in range(len(self.record)):
                    data_sub = {}
                    data_sub['xy'] = self.record['cdnt'][j]
                    data_sub['text'] = self.record['txt'][j]
                    data.append(data_sub)
                record_dict['data'] = data
                record_dict['td'] = ' '.join([ x['text'] for x in data ])
                self.rslt.append(record_dict)
            else:
                pass
        
        print('>> Run time (Sec):', time.time() - self.start)
        return self.rslt
