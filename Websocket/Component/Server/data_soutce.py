# -*- coding: utf-8 -*-
from ..Common.Constant import CAMERA, VIEWER
from ..Common.import_libraries import *

class DataSource:
    ''' データセットクラス '''

    websocket: WebsocketServer = None
    ''' Websocketサーバ '''
    camera_clients: list[dict] = []
    ''' カメラクライアント '''
    viewer_clients: list[dict] = []

    def __init__(self):
        ''' コンストラクタ '''
        pass
        
    @classmethod
    def initialize(cls):
        ''' 初期化 '''
        cls.camera_clients = []
        cls.viewer_clients = []
        