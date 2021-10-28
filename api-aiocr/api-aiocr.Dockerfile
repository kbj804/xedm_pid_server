FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /aiocr
COPY *.txt ./
COPY imgproc.py /usr/local/lib/python3.8/dist-packages/ 
COPY file_utils.py /usr/local/lib/python3.8/dist-packages/ 
COPY aiocr.py ./
COPY model ./model
COPY h2o-3.34.0.3-py2.py3-none-any.whl ./
ADD input /aiocr/input/
ADD output /aiocr/output/

RUN apt-get update -y
RUN apt-get -y install tesseract-ocr tesseract-ocr-kor libtesseract-dev tesseract-ocr-script-hang tesseract-ocr-script-hang-vert 
RUN apt-get -y install libgl1-mesa-dev libgl1-mesa-dev libgl1-mesa-glx ffmpeg libsm6 libxext6 poppler-utils

RUN apt-get -y install python3.8 python3-pip python3-dev build-essential libpq-dev
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get install -y openjdk-8-jdk

# RUN pip install requests
# RUN pip install tabulate
# RUN pip install "colorama>=0.3.8"
# RUN pip install future
# RUN pip uninstall h2o
# RUN pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o

RUN pip install h2o-3.34.0.3-py2.py3-none-any.whl
 
# CMD ["python", "aiocr.py"]
CMD tail -f /dev/null


