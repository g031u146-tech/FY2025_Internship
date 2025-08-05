# -*- coding: utf-8 -*-
from Client.client import Client
from Client.transmission import Tramsmission
from Common.import_libraries import *

RECONECT_SEC = 5

def main():
    ''' メイン関数 '''
    try:
        # 初期化
        Client.initialize()        
    except Exception as e:
        Client.logger.error(e)
        return

    try:
        while True:
            try:
                ''' Websocketクライアント実行 '''
                asyncio.run(Client.run())
            except ConnectionRefusedError as e:
                Client.logger.error('サーバとの接続に失敗しました。')
            except Exception as e:
                Client.logger.error('エラーが発生しました。')
                Client.logger.error(e)
                
            Client.logger.info(f'{RECONECT_SEC}秒後に再接続を行います。')
            time.sleep(RECONECT_SEC)
    except KeyboardInterrupt:
        Tramsmission.capture.release()
        Client.logger.info('プログラムを終了しました。')

if __name__ == '__main__':   
    main()
    