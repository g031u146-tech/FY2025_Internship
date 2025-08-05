# -*- coding: utf-8 -*-
from Common.Constant import MAX_DIVISION_NUMBER, CAMERA, STREAMING, VIEWER
from Common.import_libraries import *

class Threading:
    ''' スレッドクラス '''

    def __init__(self):
        ''' コンストラクタ '''
        pass

    # ストリーミングスレッド関数
    @classmethod
    def straming(cls):
        ''' ストリーミングスレッド関数 '''

        while True:
            for cameraClient in self.clients[CAMERA]:
                # Websocketサーバ情報からクライアントの接続情報を取得
                client = next((x for x in self.server.clients if x['id'] == cameraClient['id']), None)

                # 処理中の場合はスキップ
                if cameraClient['isProcess']:
                    continue
                # 該当しない場合はスキップ
                elif client == None:
                    # 未接続のクライアント情報を削除
                    self.clients[CAMERA] = [i for i in self.clients[CAMERA] if i['id'] != client['id']]
                    continue

                # 伝送データを作成
                json_data = {
                    'id': client['id'],
                    'transmissionType': STREAMING
                }

                # クライアントへメッセージ送信
                self.send_data_to_client(client, json_data)
                # 処理中フラグを「処理中」に変更
                cameraClient['isProcess'] = True

                # 次のクライアントへの送信処理まで500msスリープ
                time.sleep(0.75)

            # 1sスリープ
            time.sleep(1)

    # 解析スレッド関数
    def analysis(self):
        ''' 解析スレッド関数 '''

        while True:
            for cameraClient in self.clients[CAMERA]:
                # 画像ファイルが0枚の場合はスキップ
                if len(cameraClient['image_path']) == 0:
                    continue

                # 最新の画像パスの要素番号を取得
                index = len(cameraClient['image_path']) - 1
                file_path, count = self.image_processing.exec_image_process(cameraClient['image_path'][index], SEGMENTATION)
        
                # キャパシティを格納
                cameraClient['count'] = count

                with open(file_path, 'rb') as f:
                    base64_data = base64.b64encode(f.read()).decode()

                json_data = {
                    'id': cameraClient['id'],
                    'capacity': cameraClient['capacity'],
                    'transmissionType': STREAMING
                }

                totalSnedNumber = math.ceil(len(base64_data) / MAX_DIVISION_NUMBER)
                json_data['totalSnedNumber'] = totalSnedNumber

                for i in range(totalSnedNumber):
                    startIndex = i * MAX_DIVISION_NUMBER

                    json_data['sendNumber'] = i
                    json_data['endPoint'] = totalSnedNumber - 1 == i
                    json_data['data'] = base64_data[startIndex : startIndex + MAX_DIVISION_NUMBER] if i < totalSnedNumber else base64_data[startIndex : ]

                    for viewerClient in self.clients[VIEWER]:
                        client = next((x for x in self.server.clients if x['id'] == viewerClient['id']), None)
                    
                        if client == None:
                            self.clients[VIEWER] = [i for i in self.clients[VIEWER] if i['id'] != client['id']]
                            continue

                        self.send_data_to_client(client, json_data)
            
            time.sleep(1)