# -*- coding: utf-8 -*-
from ..Constant import *
from Common import *
from Common.import_libraries import *

class DatabaseOperation():
    ''' DB操作クラス '''

    # コンストラクタ
    def __init__(self):
        ''' コンストラクタ '''
        pass

    @classmethod
    def initialize(cls, conf: dict):
        ''' 初期化 '''

        cls.mongo_client = pymongo.MongoClient(conf['host'], conf['port'], username=conf['username'], password=conf['password'])
        cls.db = cls.mongo_client['clientDB']
        cls.collections = {
            REGIST_CAMERA_INFO: cls.db[REGIST_CAMERA_INFO]
        }

    # データ全件検索
    @classmethod
    def find_data(cls, target_collection: str):
        ''' データ検索
        
        :param str target_collection: 対象コレクション
        '''
        return cls.collections[target_collection].find()
    
    # データ一件検索（条件）
    @classmethod
    def find_one_data(cls, target_collection: str, conditions: dict):
        ''' データ検索（条件）
        
        :param str target_collection: 対象コレクション
        :param dir target_collection: 検索条件
        '''
        return cls.collections[target_collection].find_one(conditions)
    
    # データ挿入
    @classmethod
    def insert_data(cls, target_collection: str, data: dict):
        ''' データ挿入 
        
        :param str target_collection: 対象コレクション
        :param dict data: 挿入データ
        :return: 挿入件数
        :rtype: int
        '''
        return cls.collections[target_collection].insert_one(data)

    # データ更新
    @classmethod
    def update_data(cls, target_collection: str, conditions: dict, data: dict):
        ''' データ更新 
        
        :param str target_collection: 対象コレクション
        :param dict conditons: 条件
        :param dict data: 更新データ
        :return: 更新件数
        :rtype: int
        '''

        return cls.collections[target_collection].update_one(conditions,  {'$set': data} )

    # データ削除
    @classmethod
    def delete_data(cls, target_collection: str, conditions: dict):
        ''' データ削除

        :param str target_collection: 対象コレクション
        :param dict conditions: 条件
        :return: 削除件数
        :rtype: int
        '''
        return cls.collections[target_collection].delete_one(conditions)
    