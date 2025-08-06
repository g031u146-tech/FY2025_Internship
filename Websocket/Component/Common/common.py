# -*- coding: utf-8 -*-
from .Constant import NETWORK_ALIVE_CHECK_SHELL
from .import_libraries import *

class Common:
    ''' 共通クラス '''

    def __init__(self):
        '''  コンストラクタ '''
        pass
        
    @staticmethod
    def delete_directory(target_dir: str, is_create_dir: bool = False):
        ''' ディレクトリ削除

        :param str target_dir: 対象ディレクトリ
        :param bool is_create_dir: ディレクトリ作成フラグ（デフォルト： False）
        '''
        # 対象のディレクトリが存在するかチェック
        if os.path.exists(target_dir):  
            # 存在する場合は削除
            shutil.rmtree(target_dir)

        # 作成フラグがTrueの場合
        if is_create_dir:
            os.mkdir(target_dir)

    @staticmethod
    def read_file(target_file: str):
        ''' ファイル読み込み
        
        :param str target_file: 対象ファイル

        :return: ファイルデータ
        :rtype: Any | bytes
        '''
        with open(target_file, 'rb') as f:
            # JSONファイルの場合
            if 'json' in target_file:
                return json.load(f)
            elif 'yaml' in target_file:
                return yaml.safe_load(f)
            else:
                return f.read()

    @staticmethod
    def network_alive_check(mac_address: str = '', interface: str = '') -> tuple[str, str]:
        ''' ネットワーク死活チェック
        
        :param str mac_address: macアドレス
        :param str interface: ネットワークインターフェース
        '''
        # ネットワーク内に接続している機器の死活チェック
        subprocess.run(NETWORK_ALIVE_CHECK_SHELL, stdout=subprocess.DEVNULL)
        
        args = ['arp', '-a'] if mac_address else ['ip', '-4', 'addr', 'show', 'dev', interface]
        grep = ['grep', mac_address] if mac_address else ['grep', 'inet']

        sp = subprocess.Popen(args, encoding='utf-8', stdout=subprocess.PIPE)
        sp_grep = subprocess.Popen(grep, stdin=sp.stdout, encoding='utf-8', stdout=subprocess.PIPE)
        
        sp.stdout.close()
        return sp_grep.communicate()
