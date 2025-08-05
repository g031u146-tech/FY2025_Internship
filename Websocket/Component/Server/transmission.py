# -*- coding: utf-8 -*-
from .Constant import SEGMENTATION
from .data_soutce import DataSource
from Common.Constant import *
from Common.import_libraries import *

class Transmission:
    ''' Websocketサーバ伝送処理クラス '''
    
    def __init__(self):
        ''' コンストラクタ '''
        pass

    # 接続処理関数
    def connection_process(self, client, json_data):
        ''' 接続処理関数 '''
        clientType = json_data['clientType']

        # クライアントが「カメラ」の場合
        if clientType == CAMERA:
            DataSource.camera_clients.append({
                'id': client['id'],
                'address': client['address'][0],
                'hostname': json_data['hostname'],
                'count':0,
                'capacity': json_data['capacity'],
                'isProcess': False,
                'image_path': [],
            })
        # クライアントが「ビューアー」の場合
        elif clientType == VIEWER:
            DataSource.viewer_clients.append({
                'id': client['id'],
                'selectCameraId': -1,
                'modelType': SEGMENTATION
            })

    # ストリーミング処理関数
    def streaming_process(self, client, json_data):
        ''' ストリーミング処理関数 '''          
                    
        # 画像情報格納
        self.image_processing.image_data_store(json_data)

        # データ終点
        if (json_data['endPoint']):
            # カメラのクライアント情報を取得
            cameraClient = next((x for x in self.clients[CAMERA] if x['id'] == client['id']), None)
                
            file_path = self.image_processing.image_save(json_data)
            cameraClient['image_path'].append(file_path)
        
            # 保存数が3件の場合
            if len(cameraClient['image_path']) > 3:
                delete_file_path = cameraClient['image_path'].pop(0)
                os.remove(delete_file_path)

            cameraClient['isProcess'] = False

    # カメラ接続情報関数
    def get_camera_connection_info(self, client, json_data):
        ''' カメラ接続情報関数 '''

        json_data['data'] = self.clients[CAMERA]
        self.send_data_to_client(client, json_data)

    # カメラ登録情報関数
    def get_camera_registration_info(self, client, json_data):
        ''' カメラ登録情報関数 '''

        json_data['data'] = self.clients[CAMERA]
        self.send_data_to_client(client, json_data)

    # カメラ登録関数
    def regist_camera(self, client, json_data):
        ''' カメラ登録関数 '''
        #viewerClient = next((x for x in self.clients[VIEWER] if x['id'] == client['id']), None)
        self.send_data_to_client(client, json_data)

    # カメラ設定変更関数
    def change_setting_camera(self, client, json_data):
        ''' カメラ設定変更関数 '''

        self.send_data_to_client(client, json_data)

    # カメラ削除関数
    def delete_camera(self, client, json_data):
        ''' カメラ削除関数 '''

        self.send_data_to_client(client, json_data)
