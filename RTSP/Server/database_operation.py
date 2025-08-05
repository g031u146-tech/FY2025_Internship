# -*- coding: utf-8 -*-

import pymongo

from configparser import ConfigParser

DEVICE_INFO = 'deviceInfo'
'''デバイス情報コレクション'''

class DatabaseOperation:
    '''データベース操作クラス'''
     
    def __init__(self, config: ConfigParser):
        ''' コンストラクタ 

        :param ConfigParser config: 設定情報
        '''

        self.mongo_client = pymongo.MongoClient(
            config['mongoDB']['host'], int(config['mongoDB']['port']), username=config['mongoDB']['username'], password=config['mongoDB']['password'])
        self.db = self.mongo_client[config['mongoDB']['database']]
        self.collections = {
            DEVICE_INFO: self.db[DEVICE_INFO]
        }

    # データ件数取得
    def count_data(self, target_collection: str, conditions: dict = {}):
        ''' データ件数取得

        :param str target_collection: 検索対象コレクション
        :param dict confitions: 検索条件
        :return: 件数 
        :rtype: int
        '''
        
        return self.collections[target_collection].count_documents(conditions)

    # 複数データ検索
    def find_data(self, target_collection: str, conditions: dict = {}):
        ''' 複数データ検索

        :param str target_collection: 検索対象コレクション
        :param dict confitions: 検索条件
        :return: 検索データ 
        :rtype: dict
        '''
        
        return self.collections[target_collection].find(conditions)
    
    # データ一件検索
    def find_one_data(self, target_collection: str, conditions: dict):
        ''' データ検索

        :param str target_collection: 検索対象コレクション
        :param dict confitions: 検索条件
        :return: 検索データ 
        :rtype: dict
        '''
        
        return self.collections[target_collection].find_one(conditions)

    # データ挿入
    def insert_one_data(self, target_collection: str, data: dict):
        ''' データ挿入 
        
        :param str target_collection: 対象コレクション
        :param dict data: 挿入データ
        :return: 挿入件数
        :rtype: int
        '''
        
        return self.collections[target_collection].insert_one(data)
    
    def insert_many_data(self, target_collection: str, data: list, ordered: bool = False):
        ''' データ挿入 
        
        :param str target_collection: 対象コレクション
        :param list data: 挿入データ
        :return: 挿入件数
        :rtype: int
        '''
        return self.collections[target_collection].insert_many(data, ordered=ordered)

    # データ更新
    def update_one_data(self, target_collection: str, conditions: dict, data: dict):
        ''' データ更新 
        
        :param str target_collection: 対象コレクション
        :param dict conditons: 条件
        :param dict data: 更新データ
        :return: 更新件数
        :rtype: int
        '''

        return self.collections[target_collection].update_one(conditions,  {'$set': data} )
    
        # データ更新
    def update_many_data(self, target_collection: str, conditions: dict, data: dict):
        ''' データ更新 
        
        :param str target_collection: 対象コレクション
        :param dict conditons: 条件
        :param dict data: 更新データ
        :return: 更新件数
        :rtype: int
        '''

        return self.collections[target_collection].update_many(conditions,  {'$set': data} )

    # データ削除
    def delete_one_data(self, target_collection: str, conditions: dict):
        ''' データ削除

        :param str target_collection: 対象コレクション
        :param dict conditions: 条件
        :return: 削除件数
        :rtype: int
        '''

        return self.collections[target_collection].delete_one(conditions)
    
    def delete_many_data(self, target_collectoin: str, conditions: dict = {}):
        ''' データ削除

        :param str target_collection: 対象コレクション
        :param dict conditions: 条件
        :return: 削除件数
        :rtype: int
        '''

        return self.collections[target_collectoin].delete_many(conditions)