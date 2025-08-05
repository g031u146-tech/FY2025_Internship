# -*- coding: utf-8 -*-
from .Constant import *
from .transmission import Tramsmission
from Common import Common, Logger
from Common.Constant import CONECT, STREAMING
from Common.import_libraries import *

class Client(Logger):
    ''' Websocketクライアントクラス '''

    def __init__(self):
        ''' コンストラクタ '''
    
    @classmethod
    def initialize(cls):
        ''' 初期化処理 '''
        # 設定ファイルを読み込み
        conf = Common.read_file(CONFIG_FILE)
        log_level = logging._nameToLevel[conf['log']['level']]
        super().initialize(log_level, LOG_FILE)

        ip_addr = 'localhost'
        if conf['server']['macAddress']:
            out, _ = Common.network_alive_check(mac_address = conf['server']['macAddress'])
            if not out:
                raise Exception('接続先のサーバが見つかりません。')
        
            ip_addr = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', out)[0]
        
        cls.url = f'ws://{ip_addr}:{conf["server"]["port"]}'
        
        Tramsmission.capacity = conf['camera']['capacity']
        Tramsmission.capture = VideoCapture(conf['camera']['id'])
        Tramsmission.logger = cls.logger

    @classmethod
    async def run(cls):
        ''' Websocketクライアント実行 '''
        Tramsmission.id = -1

        async with websockets.connect(cls.url, ping_timeout=86400) as websocket:
            cls.logger.name = __name__

            try:
                Tramsmission.websocket = websocket
                
                while True:
                    msg = await websocket.recv()
                    json_data = json.loads(msg)
                    
                    if json_data['transmissionType'] == CONECT:
                        await Tramsmission.send_connect_information(json_data)
                    elif json_data['transmissionType'] == STREAMING:
                        await Tramsmission.send_image_information()
                    
            except websockets.ConnectionClosed as err:
                cls.logger.error('サーバとの接続が解除されました。')
                cls.logger.error(err)
            except Exception as err:
                cls.logger.error('エラーが発生しました。')
                cls.logger.error(err)
