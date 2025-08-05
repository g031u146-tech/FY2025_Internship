# -*- coding: utf-8 -*-
from .Constant import *
from .data_soutce import DataSource
from .threading import Threading
from .transmission import Transmission
from .image_processing import ImageProcessing
from .database_operation import DatabaseOperation
from Common import Common, Logger
from Common.Constant import *
from Common.import_libraries import *

class Server(Logger):
    '''Websocketサーバ処理クラス'''

    # コンストラクタ
    def __init__(self):
        ''' コンストラクタ'''
        pass

    # 初期化処理
    @classmethod
    def initialize(cls):
        ''' 初期化処理 '''
        # 設定ファイル読み込み
        conf = Common.read_file(CONFIG_FILE)
        log_level = logging._nameToLevel(conf['log']['level'])
        super().__init__(log_level, LOG_FILE)

        Common.delete_directory(RUNS_DIRECTORY)
        Common.delete_directory(TMP_DIRECTORY, is_create_dir=True)

        DataSource.initialize()

        cls.receive_data = {}
        
        out, _ = Common.network_alive_check(interface = conf['websocket']['interface'])        
        ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', out)[0]
        
        DataSource.websocket = WebsocketServer(ip_address, conf['websocket']['port'], log_level)
    
        cls.straming_thread = Thread(target=Threading.straming, daemon=True)
        cls.analysis_thread = Thread(target=Threading.analysis, daemon=True)

        ImageProcessing.initialize()
        DatabaseOperation.initialize(conf['database'])

    # Websocketサーバ起動関数
    @classmethod
    def run(cls):
        ''' Websocketサーバ起動関数 '''
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        DataSource.websocket.set_fn_new_client(cls.__new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        DataSource.websocket.set_fn_client_left(cls.__client_left)
        # メッセージ受信時のコールバック関数にself.message_received関数をセット
        DataSource.websocket.set_fn_message_received(cls.__message_received)
        # サーバ起動
        DataSource.websocket.run_forever()

    # クライアント接続関数
    @classmethod
    def __new_client(cls, client, server):
        ''' クライアント接続関数 '''
        cls.logger.info(f'クライアントの接続が開始されました。【接続ID： {client["id"]}】')

        json_data = {
            'id': client['id'],
            'transmissionType': CONECT,
            'message': '接続が開始されました。',
        }

        # クライアントへメッセージ送信
        cls.__send_data_to_client(client, json_data)

    # クライアント切断関数
    @classmethod
    def __client_left(cls, client, server):
        ''' クライアント切断関数 '''

        DataSource.camera_clients = [i for i in DataSource.camera_clients if i['id'] != client['id']]
        DataSource.viewer_clients = [i for i in DataSource.viewer_clients if i['id'] != client['id']]

        # 切断したクライアントの画像格納フォルダを削除
        if os.path.exists(f'{TMP_DIRECTORY}/{client['id']}'):
            shutil.rmtree(f'{TMP_DIRECTORY}/{client['id']}')

        cls.logger.info(f'クライアントとの接続が終了しました。【接続ID： {client["id"]}】')

    # メッセージ受信関数
    @classmethod
    def __message_received(self, client, server, message):
        '''  メッセージ受信関数 '''
        self.logger.info(f'クライアントからメッセージを受信しました。【接続ID： {client['id']}】')

        # JSONに変換
        json_data = json.loads(message)
        if type(json_data) is str:
            json_data = (json.loads(json_data))

        transmission_type = json_data['transmissionType']

        # 伝送種別が「0x00：接続」の場合
        if transmission_type == CONECT:
            Transmission.connection_process(client, json_data)
        # 伝送種別が「0x01：ストリーミング」の場合
        elif transmission_type == STREAMING:
            Transmission.streaming_process(client, json_data)
        # 伝送種別が「0x10：カメラ接続情報要求」の場合
        elif transmission_type == CAMERA_CONNECTION_INFO:
            Transmission.get_camera_connection_info(client, json_data)
        # 伝送種別が「0x11：カメラ登録情報要求」の場合 
        elif transmission_type == CAMERA_REGISTRATION_INFO:
            Transmission.get_camera_registration_info(client, json_data)
        # 伝送種別が「0x20：カメラ登録要求」の場合
        elif transmission_type == CAMERA_REGISTERATION:
            Transmission.regist_camera(client, json_data)
        # 伝送種別が「0x21：カメラ設定変更要求」の場合
        elif transmission_type == CHANGE_CAMERA_SETTINGS:
            Transmission.change_setting_camera(client, json_data)
        # 伝送種別が「0x25：カメラ削除要求」の場合
        elif transmission_type == CAMERA_DELETE:
            Transmission.delete_camera(client, json_data)
        # 不明な伝送種別の場合
        else:
            print(json_data['transmissionType'])

    # メッセージ送信関数
    @classmethod
    def __send_data_to_client(cls, client, data):
        '''メッセージ送信関数'''
        # メッセージ送信
        DataSource.websocket.send_message(client, json.dumps(data))
        cls.logger.info(f'クライアントへデータを送信しました。【接続ID： {client["id"]}】')


