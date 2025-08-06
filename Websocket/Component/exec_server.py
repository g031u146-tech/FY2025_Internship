# -*- coding: utf-8 -*-
from Server import Server, DataSource
from Common.import_libraries import *

def main():
    ''' メイン関数 '''
    try:
        # 初期化
        Server.initialize()
    except Exception as e:
        DataSource.logger.error(e)
        return
    
    try:
        asyncio.run(Server.run())
    except Exception as e:
        DataSource.logger.error(e)
        DataSource.logger.info('プログラムを終了しました。')
    
if __name__ == '__main__':
    main()
