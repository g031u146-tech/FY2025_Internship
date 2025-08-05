import datetime
import os
import cv2
import queue
import sys
import threading
import time

from Analysis.motion_detection import MotionDetect
from Analysis.object_detection import ObjectDetect
from Analysis.analysis_type import NA, MOTION, OBJECT


# 読込と出力でフレームのやり取りを行うためのキュー
queue = queue.Queue()

# 読込処理 #
def load_frame():
    while True: 
        # 動画読み込み
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    continue  

                # タイムスタンプ
                now = datetime.datetime.now()
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

                queue.put(frame)

        except Exception as e:
            print(e)
            time.sleep(1)
            
        finally:
            cap.release() 


# 出力処理 #
def out_stream(type):

    if type == MOTION:
        motionDetect = MotionDetect()
    elif type == OBJECT:
        objectDetect = ObjectDetect()

    while True:
        if queue.empty():
            time.sleep(1.5)
            continue
    
        try:
            frame = queue.get()

            # 動体検知
            if type == MOTION:
                frame = motionDetect.detection(frame)
                if frame is None:
                    continue
            # 物体検出
            elif type == OBJECT:
                frame = objectDetect.detection(frame)

            # 標準出力に出力
            ret, jpg = cv2.imencode('.jpg', frame)
            sys.stdout.buffer.write(jpg.tobytes())

        except:
            time.sleep(1)


# main #
if __name__ == "__main__":
    # rtspのパス
    url = 'rtsp://puma.local:8554/unicast'
    # url = 'rtsp://192.168.130.18:8554/unicast'

    # 出力先パス
    out_path = '/var/www/html/stream'
    
    # 出力先(streamフォルダ)がなければ作成
    if(os.path.isdir(out_path) == False):
        os.mkdir(out_path)
    
    # 検知の種類選択
    detectType = NA # 初期値
    # detectType = MOTION # 動体検知
    # detectType = OBJECT # 物体検出

    load_frame_thread = threading.Thread(target=load_frame)
    out_stream_thread = threading.Thread(target=out_stream, args=(detectType,))

    load_frame_thread.start()
    out_stream_thread.start()