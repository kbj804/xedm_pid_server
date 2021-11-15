import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import matplotlib.cm as cm
import pandas as pd
from scipy.ndimage import interpolation as inter
import os
import pytesseract
import re
from scipy import stats
import argparse
import file_utils
import imgproc
import time
import json
import tqdm
from tensorflow.keras.models import load_model

import h2o
h2o.init()

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)

    return best_angle, rotated

def psm(num, crop_img, text_sub, post_wrd_m):
    if (len(''.join(text_sub.split())) == 0) or (num == 11):
        print('psm :', num)
        config='--psm '+str(num)+' -c preserve_interword_spaces=1'
        text_sub = pytesseract.image_to_string(crop_img, lang="Hangul", config=config)
        for n in range(len(post_wrd_m)):
            text_sub = text_sub.replace(post_wrd_m[n],' ')
        text_sub = text_sub.replace('\n',' ')
        if text_sub == '0':text_sub=' '
        elif ''.join(text_sub.split()) == '':text_sub=' ' 
    else: text_sub = text_sub
    return text_sub

def run_psm(text, crop_img, post_wrd_m, test):
    text_sub = ""      
    config='--psm 6 -c preserve_interword_spaces=1'
    text_sub = pytesseract.image_to_string(crop_img, lang="Hangul", config=config)
    if text_sub.count('\n') > 2:
        text_sub = psm(11, crop_img, text_sub, post_wrd_m)        
    text_sub = text_sub.replace('\n',' ')
    if text_sub == '0':text_sub=' '
    elif ''.join(text_sub.split()) == '':text_sub=' '
      
    text_sub = psm(7, crop_img, text_sub, post_wrd_m)
    text_sub = psm(10, crop_img, text_sub, post_wrd_m)
    text_sub = psm(1, crop_img, text_sub, post_wrd_m)
    text_sub = psm(8, crop_img, text_sub, post_wrd_m)
    text_sub = psm(4, crop_img, text_sub, post_wrd_m) 
    text_sub = ' '.join(text_sub.split())
    text_sub = text_sub.replace('\n',' ')
    text_sub = text_sub.strip()

#     if test == 'y':
#         print('#### Final :', text_sub, len(text_sub))
    if text == "":
        text = text + "" + text_sub.strip() 
    else:
        text = text + " " + text_sub.strip()
    return text_sub, text

def t2t(path_, record, test, p_num, plan, save_subimg):    
    # Model : Padding
    model_prepad_path = 'model/prepad/prepad'
    aml = h2o.load_model(model_prepad_path)    
    
    # Model : Empty Cell
    model_emptycell_path = 'model/emptycell/emptycell.ckpt'
    nullcell = load_model(model_emptycell_path)
       
    if test == 'y':
        plt.rcParams["figure.figsize"] = (17,30)   
        
    stop_wrd = pd.read_csv('stop_wrd.txt',sep='\t',keep_default_na=False)
    replace_wrd = pd.read_csv('replace_wrd.txt',sep='\t',keep_default_na=False)
    post_wrd_e = list(stop_wrd['end'])
    stop_wrd_m = list(stop_wrd.loc[stop_wrd['midle']!='', 'midle'])
    
    post_wrd_m = []
    for i in stop_wrd_m:
        tmp = i.replace("\\n", "\n")
        post_wrd_m.append(tmp)

    orig = cv2.imread(path_)   

    if orig.shape[1] > 1024:   
        orig = cv2.resize(orig, dsize=(int(orig.shape[1]/(orig.shape[1]/1024)), int(orig.shape[0]/(orig.shape[1]/1024)))
                         , interpolation=cv2.INTER_AREA)
    if orig.shape[1] < 1024:
        orig = cv2.resize(orig, dsize=(int(orig.shape[1]/(orig.shape[1]/1024)), int(orig.shape[0]/(orig.shape[1]/1024)))
                 , interpolation=cv2.INTER_LANCZOS4)

    ngle, orig = correct_skew(orig)

    img = orig.copy()

    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = cv2.adaptiveThreshold(gray_scale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1) 

    img_bin = cv2.Laplacian(img_bin, cv2.CV_8U, ksize=5)

    if test == 'y':
        plt.subplot(1,2,1)
        plt.title('Image orig')
        plt.imshow(orig, cmap='gray')
        plt.subplot(1,2,2)
        plt.title('img_bin')
        plt.imshow(img_bin, cmap='gray');plt.show()

    line_min_width_v = 50
    line_min_width_h = 35    
    kernal_h = np.ones((1,line_min_width_v), np.uint8)
    kernal_v = np.ones((line_min_width_h,1), np.uint8)

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

        if test == 'y':
            plt.subplot(1,2,1)
            plt.title('Image Bin H')
            plt.imshow(img_bin_h, cmap='gray')
            plt.subplot(1,2,2)
            plt.title('Image Bin V')
            plt.imshow(img_bin_v, cmap='gray');plt.show()

#         for i in range(img_bin_final.shape[0]):
#             w = 0
#             b = 0
#             s = 0
#             e = 0
#             for j in range(img_bin_final.shape[1]):     
#                 if img_bin_final[i][j] > 1:
#                     w += 1
#                     b += 1
#                     if w < 2:            
#                         s = j
#                     if w == 2:
#                         e = j
#                         w = 0
#                         dif = (e - s)
#                         if (dif > 0) and (dif < 50) and (b > 30):
#                             for k in range((e - s + 1)):
#                                 img_bin_final[i][j-k] = 255
#                         s = j
#                         w = 1

        itr = 3
        itr2 = 1

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        img_bin_final = cv2.dilate(img_bin_final, kernel, iterations=itr)
        img_bin_final = cv2.erode(img_bin_final, kernel, iterations=itr-itr2)
        
        if test == 'y':
            plt.subplot(1,2,1)    
            plt.imshow(img, cmap='gray')

        _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)   
        
        points = stats[2:]
        points = np.append(np.array([[0, 0, orig.shape[0], points[0][1],1]]), points, axis=0)
        points = np.append(points, np.array([[0, points[len(points)-1][1]+points[len(points)-1][3],orig.shape[0],orig.shape[1],1]]), axis=0)
        
        pad = 10
        text = ''
        
        if test == 'y':
            plt.imshow(gray_scale, cmap='gray');plt.show()
        
        num = 0
        
        for x,y,w,h,area in points:
            num += 1
                
            if x == min_col+min_col_itr+itr-itr2:     
                x = x-min_col_itr-itr-pad
                w = w+min_col_itr+itr+pad
                
            if x+w > max_col-10:
                w = w+min_col_itr+itr+pad   
                
            if y == 0:
                w = gray_scale.shape[1]                
                    
            if gray_scale[y:y+h, x:x+w].shape[0] == 0:
                pass
            else:  
                sub_img = cv2.Laplacian(gray_scale[y:y+h, x:x+w], cv2.CV_8U, ksize=5)

                if gray_scale[y:y+h, x:x+w].shape[0] == 0:
                    pass
                else:
                    eroded = cv2.morphologyEx(sub_img, cv2.MORPH_OPEN, kernal_h)
                    indices = np.nonzero(eroded)
                    rows = np.unique(indices[0])

                    if (len(rows) > 10) and (x > 0):
                        pass
                    else:
                        cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),1)
                        plt.rcParams["figure.figsize"] = (7,7)   
                        
                        if y > 3:
                            y = y-4
                            h = h+(4*2)

                        crop_img = gray_scale[y:y+h, x:x+w]
                        crop_bin_v = img_bin_v[y:y+h, x:x+w]
                        crop_bin_h = img_bin_h_o[y:y+h, x:x+w]
                                                       
                        mask_v = cv2.findNonZero(crop_bin_v)
                        mask_h = cv2.findNonZero(crop_bin_h)   
                        
                        if type(mask_v) is np.ndarray:
                            if test == 'y':
                                print('Remove vertical line')
#                                 plt.imshow(crop_bin_v, cmap='gray');plt.show()
                            for i in range(len(mask_v)):
                                crop_img[mask_v[i][0][1],mask_v[i][0][0]] = 255
                                if mask_v[i][0][0]+1 < crop_img.shape[1]:
                                    crop_img[mask_v[i][0][1],mask_v[i][0][0]+1] = 255
                                if mask_v[i][0][0]-1 > 0:
                                    crop_img[mask_v[i][0][1],mask_v[i][0][0]-1] = 255
                                    
                        if (crop_img.shape[0] * crop_img.shape[1]) > 0:
                            sub = crop_img.copy()
                            sub_bin = cv2.adaptiveThreshold(sub, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1)             

                            cntNotBlack = cv2.countNonZero(sub_bin)
                            cntBlack = sub_bin.shape[0]*sub_bin.shape[1]- cntNotBlack
                            percnt = cntBlack/(cntBlack+cntNotBlack)
                            if test == 'y':
                                print('cntNotBlack :',cntNotBlack,'cntBlack :',cntBlack, 'percnt :', percnt)

                        if type(mask_h) is np.ndarray:
#                             if percnt <= 0.5:
                            if test == 'y':
                                print('Remove horizontal line')
#                                 plt.imshow(crop_bin_h, cmap='gray');plt.show()
#                             if (crop_img.shape[1] < 500):
                            for i in range(len(mask_h)):
                                crop_img[mask_h[i][0][1],mask_h[i][0][0]] = 255
                                if mask_h[i][0][1]+1 < crop_img.shape[0]:
                                    crop_img[mask_h[i][0][1]+1,mask_h[i][0][0]] = 255
                                if mask_h[i][0][1]-1 > 0:
                                    crop_img[mask_h[i][0][1]-1,mask_h[i][0][0]] = 255
                                    
                        chk_img = cv2.GaussianBlur(crop_img,(1,1),0)
                        _, chk_img = cv2.threshold(chk_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                        coords = np.column_stack(np.where(chk_img < 255))
                        xx = []
                        yy = []
                        for i in range(len(coords)):
                            xx.append(coords[i][1])
                            yy.append(coords[i][0])

                        if len(xx) > 0:
                            xx_min = min(xx)
                            xx_max = max(xx)
                            if xx_min > 1:
                                crop_img = crop_img[:, xx_min-2:xx_max+2]   
                                x = x+(xx_min-2)
                                w = xx_max+2-(xx_min-2)
                            else:
                                crop_img = crop_img[:, xx_min:xx_max]
                                x = x+(xx_min)
                                w = xx_max-(xx_min)

                        if len(yy) > 0:
                            yy_min = min(yy)
                            yy_max = max(yy)
                            if yy_min > 1:
                                crop_img = crop_img[yy_min-2:yy_max+2, :]
                                y = y+(yy_min-2)
                                h = yy_max+2-(yy_min-2)
                                                                
                        if test == 'y':
                            print('#################################################################################################################')
                            print(path_)
                            print(path_+str(num))
                            print('y, h, x, w')
                            print(y, ', ', h, ', ', x, ', ', w)
                            print('Shape :', crop_img.shape)
                                    
                        if ((crop_img.shape[0] * crop_img.shape[1]) > 0) and (crop_img.shape[0] > 4):
                            mtd = ''
                            
                            sub = crop_img.copy()
                            sub_bin = cv2.adaptiveThreshold(sub, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1)             

                            cntNotBlack = cv2.countNonZero(sub_bin)
                            cntBlack = sub_bin.shape[0]*sub_bin.shape[1]- cntNotBlack
                            percnt = cntBlack/(cntBlack+cntNotBlack)
                                
                            if test == 'y':
                                print('cntNotBlack :',cntNotBlack,'cntBlack :',cntBlack, 'percnt :', percnt)
                                
                            if save_subimg == 'y':
                                cv2.imwrite('cropimg/'+path_.split('/')[-1].split('.')[0]+str(num)+'.jpg', crop_img)
                                                  
                            new_img = crop_img.copy()
                            lm = 200
                            if new_img.shape[1] > lm:  
                                new_img = cv2.resize(new_img, dsize=(int(new_img.shape[1]/(new_img.shape[1]/lm)), int(new_img.shape[0]/(new_img.shape[1]/lm)))
                                                     , interpolation=cv2.INTER_AREA)

                            if new_img.shape[1] < lm:
                                new_img = cv2.resize(new_img, dsize=(int(new_img.shape[1]/(new_img.shape[1]/lm)), int(new_img.shape[0]/(new_img.shape[1]/lm)))
                                                     , interpolation=cv2.INTER_LANCZOS4)

                            if new_img.shape[0] > lm:
                                new_img = new_img[0:lm-1, :]

                            if new_img.shape[0] < lm:    
                                p1 = lm - new_img.shape[0]
                                p2 = lm - new_img.shape[1]

                                new_img = cv2.copyMakeBorder(new_img, 0, p1, 0, 0,  cv2.BORDER_CONSTANT, value=255)
                                new_img = cv2.copyMakeBorder(new_img, 0, 0, 0, p2,  cv2.BORDER_CONSTANT, value=255)
                                
                            xTest = new_img.reshape((1,)+new_img.shape)
                            xTest = xTest.astype('float32')/255
                            
                            prediction = nullcell.predict(xTest)
                            prediction = np.argmax(prediction[0])
                                                        
#                             if (percnt < 0.009) or (cntBlack < 140):
                            if (percnt < 0.009) or (cntBlack < 140) or (prediction == 1):
                                if test == 'y':
                                    print('Pass ...')
                                text_sub = ''                         

                            else:           
                                sp = crop_img.shape[0]/crop_img.shape[1]
                                
                                p = int(aml.predict(h2o.H2OFrame(pd.DataFrame({'shp':[sp], 'percnt':[percnt]})))[0])
                                        
                                if test == 'y':
                                    print('P : '+str(p)+', Shape : '+str(sp))

                                crop_img = cv2.copyMakeBorder(crop_img, p, p, 0, 0,  cv2.BORDER_CONSTANT, value=255)
                                

                                if cntNotBlack > cntBlack:
                                    if test == 'y':                                    
                                        plt.imshow(crop_img, cmap='gray'); plt.show()
                                    text_sub, text = run_psm(text, crop_img, post_wrd_m, test) 
                                else:
                                    chk_img = crop_img.copy()
                                    chk_img[chk_img>170] = 255
                                    sub_bin = cv2.adaptiveThreshold(chk_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 1)
                                    cntNotBlack = cv2.countNonZero(sub_bin)
                                    cntBlack = sub_bin.shape[0]*sub_bin.shape[1]- cntNotBlack
                                    percnt = cntBlack/(cntBlack+cntNotBlack)
                                    
                                    if percnt > 0.5:
                                        crop_img = ~crop_img
                                        crop_img[crop_img>120] = 255
                                        if test == 'y':                     
                                            print('BG = black, Font = white')
                                            plt.imshow(crop_img, cmap='gray'); plt.show()
                                        text_sub, text = run_psm(text, ~crop_img, post_wrd_m, test)                                             
                                    else:
                                        crop_img[crop_img>170] = 255
                                        if test == 'y':  
                                            print('BG = black, Font = black')
                                            plt.imshow(crop_img, cmap='gray'); plt.show()                                            
                                        text_sub, text = run_psm(text, crop_img, post_wrd_m, test)
                                        
#                                 if test == 'y':
#                                     cv2.imwrite('cropimg/'+path_.split('/')[-1].split('.')[0]+str(num)+'.jpg', crop_img)                           
                                
                                same = 0
                                for n in range(len(post_wrd_m)):
                                    text_sub = text_sub.replace(post_wrd_m[n],' ')

                                for i in post_wrd_e:
                                    if text_sub == i:
    #                                     if test == 'y':
    #                                         print('Yes same : ', text_sub)
                                        text_sub = ''
                                        same += 1

                                for j in range(len(replace_wrd)):
                                    text_sub = text_sub.replace(replace_wrd['end'][j], replace_wrd['endto'][j])
#                                     if text_sub == replace_wrd['end'][j]:
#     #                                     if test == 'y':
#     #                                         print('Replace : ', replace_wrd['end'][j], 'to', replace_wrd['endto'][j])
#                                         text_sub = replace_wrd['endto'][j]                                    

    #                             if same == 0:
    #                                 if test == 'y':
    #                                     print('No same : ', text_sub)

                                if test == 'y':
                                    print('#### Final(Modi) :', text_sub)
                                    print('#################################################################################################################')


                                record = record.append(pd.DataFrame({'src':[path_]
                                                                    ,'id':[path_+str(num)]
                                                                    ,'pg':[p_num]
                                                                    ,'cdnt': [str(y)+', '+str(h)+', '+str(x)+', '+str(w)]
                                                                    ,'y':[y]
                                                                    ,'x':[x]         
                                                                    ,'h':[h]
                                                                    ,'w':[w]
                                                                    ,'percnt':[percnt]
                                                                    ,'txt':[text_sub]}))

        record = record.reset_index(drop=True)
                                        
        if test == 'y':
            plt.rcParams["figure.figsize"] = (17,30)
            plt.subplot(1,2,2)
            plt.title('Result')
            plt.imshow(orig);plt.show()

            plt.subplot(1,2,1)
            plt.title('Image Bin')
            plt.imshow(img_bin_final, cmap='gray')
            plt.subplot(1,2,2)
            plt.title('Result')
            plt.imshow(orig);plt.show()
        
        text = text.replace('',' ')
        text = text.replace('\n',' ')
        text = ' '.join(text.split())
        if test == 'y':
            print('Result :',text)    
    
    return record, text, table_yn

def run(path_in, path_out, file_out):
    start = time.time()

    record = pd.DataFrame(columns=['src','id','pg','cdnt','y','x','h','w','percnt','txt'])

    rslt = []

    if os.path.isdir(path_in):
        print('Exist')

        image_list, _, _ = file_utils.get_files(path_in)

        if len(image_list) > 0:
            for i in range(len(image_list)):
                record_dict = {}
                p_num = ''
                p_num = re.sub(r".+\|p([0-9]{1,10000})\.jpg", r"\1", image_list[i])
                
                if len(p_num) == len(image_list[i]):
                    p_num = '1'

                print('> Start :', image_list[i])
                record, text, table_yn = t2t(path_=image_list[i], record=record, test='n', p_num=p_num, plan='1', save_subimg='n')
                print('< Complete :', image_list[i])
                if table_yn == 'y':
                    if file_out == 'y':
                        record.to_csv(path_out+'/record.csv', encoding='utf-8-sig')
                    record_dict['page'] = p_num
                    data = []
                    for j in range(len(record)):
                        data_sub = {}
                        data_sub['xy'] = record['cdnt'][j]
                        data_sub['text'] = record['txt'][j]
                        data.append(data_sub)
                    record_dict['data'] = data
                    record_dict['td'] = ' '.join([ x['text'] for x in data ])
                    rslt.append(record_dict)
                else:
                    pass

            if file_out == 'y':
                with open(path_out+'/rslt.json', 'w') as outfile:
                    json.dump(rslt, outfile)
        else:
            print('Empty ....')
    else:
        print('Not exist')

    print('In :', args.in_)
    print('Out :', args.out_)
    runtime = time.time() - start
    print('>> Run time (Sec):', runtime)

    return rslt, runtime

if __name__ == '__main__':
    print('Parsing Args ....')
    parser = argparse.ArgumentParser(description='Image To Text')
    parser.add_argument('--in_', default='/ocr_work/input', type=str)
    parser.add_argument('--out_', default='/ocr_work/output', type=str)
    parser.add_argument('--outfile_', default='y', type=str)

    args = parser.parse_args()   
    
    print('Processing ....')
    run(path_in=args.in_, path_out=args.out_, file_out=args.outfile_)

    print('Complete ....')
