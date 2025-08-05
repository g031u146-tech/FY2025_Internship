# -*- coding: utf-8 -*-
from .Constant import *
from .data_source import DataSource
from .transmission import Tramsmission
from Common import Common, Logger
from Common.Constant import CONECT, STREAMING
from Common.import_libraries import *

class Client:
    ''' Websocketクライアントクラス '''

    def __init__(self):
        ''' コンストラクタ '''
        pass
    
    @staticmethod
    def initialize():
        ''' 初期化処理 '''
        # 設定ファイルを読み込み
        conf = Common.read_file(CONFIG_FILE)
        log_level = logging._nameToLevel[conf['log']['level']]
        DataSource.logger = Logger.initialize(log_level, LOG_FILE)

        ip_addr = '127.0.0.1'
        if conf['server']['macAddress']:
            out, _ = Common.network_alive_check(mac_address = conf['server']['macAddress'])
            if not out:
                raise Exception('接続先のサーバが見つかりません。')
        
            ip_addr = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', out)[0]
        
        DataSource.url = f'ws://{ip_addr}:{conf["server"]["port"]}'
        DataSource.capacity = conf['camera']['capacity']
        DataSource.capture = VideoCapture(conf['camera']['id'])

    @staticmethod
    async def run():
        ''' Websocketクライアント実行 '''
        DataSource.id = -1

        async with websockets.connect(DataSource.url, ping_timeout=86400) as websocket:
            DataSource.logger.name = __name__

            try:
                DataSource.websocket = websocket
                
                while True:
                    msg = await websocket.recv()
                    json_data = json.loads(msg)
                    
                    if json_data['transmissionType'] == CONECT:
                        await Tramsmission.send_connect_information(json_data)
                    elif json_data['transmissionType'] == STREAMING:
                        await Tramsmission.send_image_information()
                    
            except websockets.ConnectionClosed as err:
                DataSource.logger.error('サーバとの接続が解除されました。')
                DataSource.logger.error(err)
            except Exception as err:
                DataSource.logger.error('エラーが発生しました。')
                DataSource.logger.error(err)
