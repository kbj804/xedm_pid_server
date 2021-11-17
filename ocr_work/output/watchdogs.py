import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import call
import requests
import json
class Target:
    watchDir = os.getcwd()
    print(watchDir)
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        pre = 1
        try:
            while True:
                time.sleep(5)

                # 새로운 파일이 들어왔을 경우 갱신
                if pre != len(os.listdir(self.watchDir)):
                    pre = len(os.listdir(self.watchDir))
                    print(f"[EVENT] New file length : {len(os.listdir(self.watchDir))}")
                
                # 파일 입출력 대기(listening) 상태
                elif pre == 1:
                    print("[WARNING] File System Monitoring ... ")

                # 모든 이미지가 다 추출되면 OCR 실행
                else:
                    RESULT_PATH = os.path.join(self.watchDir, 'rslt.json')
                    pre = 1
                    session = get_sessionid()
                    print(session)
                    p = read_json(RESULT_PATH)
                    print(p)

                    # watchdogs 파일 제외하고 삭제
                    for file in os.listdir(self.watchDir):
                        if file == "watchdogs.py":
                            pass
                        else:
                            FILEPATH = os.path.join(self.watchDir, file)
                            os.remove(FILEPATH)
                            print(f"[REMOVE] {FILEPATH}")
                    print("[RUNNING] Run AI-OCR ...")
                    

        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

def read_json(json_path):
    """ 
    json file read
    """
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file) # type: dict
    return json_data

def get_sessionid():
    print("####### Connection Xedm Session ######")
    XEDM_URL = "192.168.21.211:2021"
    url = f'http://{XEDM_URL}/xedrm/json/login?isAgent=True&lang=ko&userId=Qmhp/4rwH78=&mode=jwt'

    res = requests.get(url)
    res = json.loads(res.text)
    session = res['list'][0]['xedmSession']

    return session

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        print(event)

    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(event)

if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
    w = Target()
    w.run()