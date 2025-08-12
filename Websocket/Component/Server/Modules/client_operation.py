# -*- coding: utf-8 -*-
from .transmission import Transmission
from .database_operation import DatabaseOperation as db
from ..Constant import TMP_DIRECTORY, REGIST_CAMERA_INFO
from ..data_source import DataSource
from Common.Constant import CONECT
from Common.import_libraries import *

class ClientOperation(Transmission):
    ''' クライアント操作クラス '''

    def __init__(self):
        ''' コンストラクタ '''
        pass

    # クライアント接続関数
    @staticmethod
    def new_client(client, server):
        ''' クライアント接続関数 '''
        DataSource.logger.info(f'クライアントの接続が開始されました。【接続ID： {client["id"]}】')

        json_data = {
            'id': client['id'],
            'transmissionType': CONECT,
            'message': '接続が開始されました。',
        }

        # クライアントへメッセージ送信
        ClientOperation.send_data_to_client(client, json_data)

    @staticmethod
    def client_left(client, server):
        ''' クライアント切断関数 '''
        camera_length = len(DataSource.camera_clients)

        DataSource.camera_clients = [i for i in DataSource.camera_clients if i['id'] != client['id']]
        DataSource.viewer_clients = [i for i in DataSource.viewer_clients if i['id'] != client['id']]

        # カメラの接続が切れた場合はIPアドレスを空文字にする
        if len(DataSource.camera_clients) != camera_length:
            db.update_data(REGIST_CAMERA_INFO, 
                           {'ipAddress': client['address'][0]},
                           {'ipAddress': ''})

        # 切断したクライアントの画像格納フォルダを削除
        if os.path.exists(f'{TMP_DIRECTORY}/{client['id']}'):
            shutil.rmtree(f'{TMP_DIRECTORY}/{client['id']}')

        DataSource.logger.info(f'クライアントとの接続が終了しました。【接続ID： {client["id"]}】')

    # メッセージ受信関数
    @staticmethod
    def message_received(client, server, message):
        '''  メッセージ受信関数 '''
        DataSource.logger.info(f'クライアントからメッセージを受信しました。【接続ID： {client['id']}】')

        # JSONに変換
        json_data = json.loads(message)
        
        if type(json_data) is str:
            json_data = (json.loads(json_data))

        ClientOperation.handover(client, json_data)
