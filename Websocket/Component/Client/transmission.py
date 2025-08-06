# -*- coding: utf-8 -*-
from .data_source import DataSource
from Common.Constant import MAX_DIVISION_NUMBER, CAMERA, STREAMING
from Common.import_libraries import *

class Tramsmission:
    ''' 伝送クラス '''

    def __init__(self):
        ''' コンストラクタ '''
        pass

    @staticmethod
    async def send_connect_information(json_data: dict):
        ''' 接続情報送信 '''
        DataSource.logger.info(json_data['message'])
        DataSource.id = json_data['id']
        
        json_data['clientType'] = CAMERA
        json_data['hostname'] = socket.gethostname()
        json_data['capacity'] = DataSource.capacity
                  
        await DataSource.websocket.send(json.dumps(json_data))

    @staticmethod
    async def send_image_information():
        ''' 画像情報送信 '''
        while True:
            result, frame = DataSource.capture.read()
            if not result:
                continue

            json_data = {
                'id': DataSource.id,
                'transmissionType': STREAMING,
                'clientType': CAMERA,
                'timestamp': int(time.time()),
                'totalSendNumber': 0,
                'sendNumber': -1,
                'endPoint': False,
                'data': ''
            }
                        
            frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5)
            frame = cv2.putText(frame, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), (0, 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1, cv2.LINE_AA)
            _, encoded = cv2.imencode('.png', frame)
            base64_data = base64.b64encode(encoded).decode()
                            
            total_sned_number = math.ceil(len(base64_data) / MAX_DIVISION_NUMBER)
            json_data['totalSendNumber'] = total_sned_number

            for i in range(total_sned_number):
                start_index = i * MAX_DIVISION_NUMBER

                json_data['sendNumber'] = i
                json_data['endPoint'] = total_sned_number - 1 == i
                json_data['data'] = base64_data[start_index : start_index + MAX_DIVISION_NUMBER] if i < total_sned_number else base64_data[start_index : ]

                await DataSource.websocket.send(json.dumps(json_data))

            break