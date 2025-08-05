# -*- coding: utf-8 -*-
from Server.server import Server
from Common.import_libraries import *

def main():
    ''' メイン関数 '''
    try:
        # 初期化
        Server.initialize()
    except Exception as e:
        Server.logger.error(e)
        return
    
    try:
        asyncio.run(Server.run())
    except Exception as e:
        Server.logger.error(e)
        Server.logger.info('プログラムを終了しました。')
    
if __name__ == '__main__':
    main()
