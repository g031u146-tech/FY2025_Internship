# -*- coding: utf-8 -*-
from Common.import_libraries import *

class DataSource:
    ''' データソースクラス '''

    url: str = ''
    ''' 接続先URL ''' 
    id: int = -1
    ''' WebsocketID '''
    capacity: int = -1
    ''' キャパシティ '''
    capture: VideoCapture = None
    ''' ビデオキャプチャ '''
    websocket: ClientConnection = None
    ''' Websocketクライアント '''
    logger: logging = None
    ''' ロガー '''

    def __init__(self):
        ''' コンストラクタ '''
        pass