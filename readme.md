## XEDM PID Server

## BUILD

#### normal
``` docker-compose up --build ```

#### env
``` docker-compose up --build --env_file=.env ```


## Config

### 필요한 파일 목록

#### api-mlserver
- ```common/const.py```: API Server Config file

#### api-aiocr
- /model/emptycell/emptycell.ckpt/saved_model.pb
- /model/emptycell/emptycell.ckpt/variables.data-00000-of-00001
- /model/emptycell/emptycell.ckpt/variables.index
- /model/prepad/prepad
- h2o-3.34.0.3-py2.py3-none-any.whl

#### Container간 Volume 공유 폴더
``` /ocr_work/input ``` : ```api-mlserver```에서 pdf to img 결과 저장  
``` /ocr_work/input ``` : ```api-aiocr```에서 img to data 결과 저장


