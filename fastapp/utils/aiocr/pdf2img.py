from pdf2image import convert_from_path 
import os

pdf_list = os.popen('find ./pdf -name *.pdf').read().split('\n')
pdf_list = list(filter(None, pdf_list))

for p in pdf_list:        
    file_name = p.split('/')[2]
    file_name = file_name.split('.')[0]    
    print(p)
    print(file_name)
    pages = convert_from_path(p) 
    for i, page in enumerate(pages): 
        page.save("./input/"+file_name+'|p'+str(i)+".jpg", "JPEG")
