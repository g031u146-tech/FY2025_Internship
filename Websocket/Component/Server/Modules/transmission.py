# -*- coding: utf-8 -*-
from .image_processing import ImageProcessing
from ..Constant import SEGMENTATION
from ..data_source import DataSource
from Common.Constant import *
from Common.import_libraries import *

class Transmission:
    ''' Websocketサーバ伝送処理クラス '''
    
    def __init__(self):
        ''' コンストラクタ '''
        pass

    @staticmethod
    def handover(client, json_data):
        ''' 伝送引渡し '''
        transmission_type = json_data['transmissionType']
        
        # 伝送種別が「0x00：接続」の場合
        if transmission_type == CONECT:
            Transmission.__connection_process(client, json_data)
        # 伝送種別が「0x01：ストリーミング」の場合
        elif transmission_type == STREAMING:
            Transmission.__streaming_process(client, json_data)
        # 伝送種別が「0x10：カメラ接続情報要求」の場合
        elif transmission_type == CAMERA_CONNECTION_INFO:
            Transmission.__get_camera_connection_info(client, json_data)
        # 伝送種別が「0x11：カメラ登録情報要求」の場合 
        elif transmission_type == CAMERA_REGISTRATION_INFO:
            Transmission.__get_camera_registration_info(client, json_data)
        # 伝送種別が「0x20：カメラ登録要求」の場合
        elif transmission_type == CAMERA_REGISTERATION:
            Transmission.__regist_camera(client, json_data)
        # 伝送種別が「0x21：カメラ設定変更要求」の場合
        elif transmission_type == CHANGE_CAMERA_SETTINGS:
            Transmission.__change_setting_camera(client, json_data)
        # 伝送種別が「0x25：カメラ削除要求」の場合
        elif transmission_type == CAMERA_DELETE:
            Transmission.__delete_camera(client, json_data)
        # 不明な伝送種別の場合
        else:
            print(json_data['transmissionType'])

        # メッセージ送信関数

    @staticmethod 
    def send_data_to_client(client, data):
        '''メッセージ送信関数'''
        # メッセージ送信
        DataSource.websocket.send_message(client, json.dumps(data))
        DataSource.logger.info(f'クライアントへデータを送信しました。【接続ID： {client["id"]}】')

    @staticmethod
    def __connection_process(client, json_data):
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

    @staticmethod
    def __streaming_process(client, json_data):
        ''' ストリーミング処理関数 '''
        # 画像情報格納
        ImageProcessing.image_data_store(json_data)

        # データ終点
        if (json_data['endPoint']):
            # カメラのクライアント情報を取得
            cameraClient = next((x for x in DataSource.camera_clients if x['id'] == client['id']), None)
            
            file_path = ImageProcessing.image_save(json_data)
            cameraClient['image_path'].append(file_path)
        
            # 保存数が3件の場合
            if len(cameraClient['image_path']) > 3:
                delete_file_path = cameraClient['image_path'].pop(0)
                os.remove(delete_file_path)

            cameraClient['isProcess'] = False

    @staticmethod
    def __get_camera_connection_info(client, json_data):
        ''' カメラ接続情報関数 '''
        json_data['data'] = DataSource.camera_clients
        Transmission.send_data_to_client(client, json_data)

    @staticmethod
    def __get_camera_registration_info(client, json_data):
        ''' カメラ登録情報関数 '''
        json_data['data'] = DataSource.camera_clients
        Transmission.send_data_to_client(client, json_data)

    @staticmethod
    def __regist_camera(client, json_data):
        ''' カメラ登録関数 '''
        #viewerClient = next((x for x in self.clients[VIEWER] if x['id'] == client['id']), None)
        Transmission.send_data_to_client(client, json_data)

    @staticmethod
    def __change_setting_camera(client, json_data):
        ''' カメラ設定変更関数 '''
        Transmission.send_data_to_client(client, json_data)

    @staticmethod
    def __delete_camera(client, json_data):
        ''' カメラ削除関数 '''
        Transmission.send_data_to_client(client, json_data)
