# -*- coding: utf-8 -*-
from .client_operation import ClientOperation
from .image_processing import ImageProcessing
from ..Constant import SEGMENTATION
from ..data_source import DataSource
from Common.Constant import MAX_DIVISION_NUMBER, CAMERA, STREAMING, VIEWER
from Common.import_libraries import *

class Threading:
    ''' スレッドクラス '''
    def __init__(self):
        ''' コンストラクタ '''
        pass

    @classmethod
    def initialize(cls):
        cls.straming_thread = Thread(target=Threading.threading, daemon=True, args=(True,))
        cls.analysis_thread = Thread(target=Threading.threading, daemon=True, args=(False,))

    @staticmethod
    def threading(is_streaming: bool):
        while True:
            for camera_client in DataSource.camera_clients:
                try:
                    if is_streaming:
                        Threading.streaming(camera_client)
                    else:
                        Threading.analysis(camera_client)
                except Exception:
                    continue

            time.sleep(1)

    @staticmethod
    def streaming(camera_client):
        ''' ストリーミングスレッド関数 '''
        # Websocketサーバ情報からクライアントの接続情報を取得
        client = next((x for x in DataSource.websocket.clients if x['id'] == camera_client['id']), None)
       
        # 処理中の場合はスキップ
        if camera_client['isProcess']:
            raise Exception
        # 該当しない場合はスキップ
        elif client == None:
            # 未接続のクライアント情報を削除
            DataSource.camera_clients = [i for i in DataSource.camera_clients if i['id'] != client['id']]
            raise Exception

        # 伝送データを作成
        json_data = {
            'id': client['id'],
            'transmissionType': STREAMING
        }

        # クライアントへメッセージ送信
        ClientOperation.send_data_to_client(client, json_data)
        # 処理中フラグを「処理中」に変更
        camera_client['isProcess'] = True

        # 次のクライアントへの送信処理まで500msスリープ
        time.sleep(0.75)

    # 解析スレッド関数
    @staticmethod
    def analysis(camera_client):
        ''' 解析スレッド関数 '''
        # 画像ファイルが0枚の場合はスキップ
        if len(camera_client['image_path']) == 0:
            raise Exception

        # 最新の画像パスの要素番号を取得
        index = len(camera_client['image_path']) - 1
        file_path, count = ImageProcessing.exec_image_process(camera_client['image_path'][index], SEGMENTATION)
        
        # キャパシティを格納
        camera_client['count'] = count

        with open(file_path, 'rb') as f:
            base64_data = base64.b64encode(f.read()).decode()

        json_data = {
            'id': camera_client['id'],
            'capacity': camera_client['capacity'],
            'transmissionType': STREAMING
        }

        totalSnedNumber = math.ceil(len(base64_data) / MAX_DIVISION_NUMBER)
        json_data['totalSnedNumber'] = totalSnedNumber

        for i in range(totalSnedNumber):
            startIndex = i * MAX_DIVISION_NUMBER

            json_data['sendNumber'] = i
            json_data['endPoint'] = totalSnedNumber - 1 == i
            json_data['data'] = base64_data[startIndex : startIndex + MAX_DIVISION_NUMBER] if i < totalSnedNumber else base64_data[startIndex : ]

            for viewerClient in DataSource.viewer_clients:
                client = next((x for x in DataSource.websocket.clients if x['id'] == viewerClient['id']), None)
            
                if client == None:
                    DataSource.viewer_clients = [i for i in DataSource.viewer_clients if i['id'] != client['id']]
                    continue

                ClientOperation.send_data_to_client(client, json_data)
            
            time.sleep(1)