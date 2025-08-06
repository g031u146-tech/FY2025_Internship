# -*- coding: utf-8 -*-
from .Constant import *
from .Modules import *
from .data_source import DataSource
from Common import Common, Logger
from Common.Constant import *
from Common.import_libraries import *

class Server:
    '''Websocketサーバ処理クラス'''

    # コンストラクタ
    def __init__(self):
        ''' コンストラクタ'''
        pass

    # 初期化処理
    @staticmethod
    def initialize():
        ''' 初期化処理 '''
        # 設定ファイル読み込み
        conf = Common.read_file(CONFIG_FILE)
        
        DataSource.initialize()
        Threading.initialize()
        ImageProcessing.initialize()
        DatabaseOperation.initialize(conf['database'])

        log_level = logging._nameToLevel[conf['log']['level']]
        DataSource.logger = Logger.initialize(log_level, LOG_FILE)

        out, _ = Common.network_alive_check(interface = conf['websocket']['interface'])        
        ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', out)[0]
        DataSource.websocket = WebsocketServer(ip_address, conf['websocket']['port'], log_level)

        Common.delete_directory(RUNS_DIRECTORY)
        Common.delete_directory(TMP_DIRECTORY, is_create_dir=True)    
        
    # Websocketサーバ起動関数
    @staticmethod
    def run():
        ''' Websocketサーバ起動関数 '''
        # ストリーミングスレッド開始
        Threading.straming_thread.start()
        # 解析スレット開始
        Threading.analysis_thread.start()

        # クライアント接続時のコールバック関数にself.new_client関数をセット
        DataSource.websocket.set_fn_new_client(ClientOperation.new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        DataSource.websocket.set_fn_client_left(ClientOperation.client_left)
        # メッセージ受信時のコールバック関数にself.message_received関数をセット
        DataSource.websocket.set_fn_message_received(ClientOperation.message_received)
        # サーバ起動
        DataSource.websocket.run_forever()

    