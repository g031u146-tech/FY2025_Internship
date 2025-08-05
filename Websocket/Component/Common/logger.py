# -*- coding: utf-8 -*-
from .Constant import SAVE_DIR
from .import_libraries import *

class Logger:
    ''' ロガークラス '''

    def __init__(self):
        ''' コンストラクタ '''
    
    @classmethod
    def initialize(cls, log_level: int, log_file: str, max_bytes: int = 100000000, backup_count = 10):
        ''' 初期化

        :param int log_level: ログレベル
        :param str log_file: ログファイル名
        :param int max_bytes: ログ最大保存容量（デフォルト：100MB）
        :param int backup_count: ログファイルバックアップ世代数（デフォルト：10）
        '''

        cls.logger = logging.getLogger()
        cls.logger.setLevel(log_level)

        # ログ出力ディレクトリがあるかチェック
        if not os.path.exists(SAVE_DIR):
            # 無ければ作成
            os.mkdir(SAVE_DIR)

        # 出力フォーマット
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(message)s')

        # ログファイル出力設定
        file_handler = logging.handlers.RotatingFileHandler(os.path.join(SAVE_DIR, log_file), maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
    
        # ストリーミング出力設定
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)

        # ログハンドラ設定
        cls.logger.addHandler(file_handler)
        cls.logger.addHandler(stream_handler)
        