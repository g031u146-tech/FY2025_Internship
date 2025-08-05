# -*- coding: utf-8 -*-

from configparser import ConfigParser
import datetime
import json
import re
import subprocess
import sys
import threading
import time
import requests

# from Analysis.analysis_type import NA, MOTION, OBJECT
# from server import Server

from database_operation import DEVICE_INFO, DatabaseOperation

config = ConfigParser()
config.read('db_config.ini')
db = DatabaseOperation(config)

def registDevice(hostname, ip):
     db.insert_one_data(DEVICE_INFO, 
                        {'hostname':hostname, 
                         'ipAddress':ip,
                         'capacity':-1, 
                         'isValid':False, 
                         'registDate':datetime.datetime.now(), 
                         'isActive':True, 
                         'lastConnectionCheckDate':datetime.datetime.now(), 
                         'errorCount':0})
     
# デバイス情報の存在判定
def isExistDeviceForHostname(hostname):
    if(db.count_data(DEVICE_INFO, {'hostname':hostname}) == 1):
        return True
    
    else:
        return False
    
def isExistDeviceForIpaddress(ip):
    if(db.count_data(DEVICE_INFO, {'ipAddress':ip}) == 1):
        return True
    
    else:
        return False

# デバイス情報の取得
def getDeviceInfo(hostname):
    data = db.find_one_data(DEVICE_INFO, {'hostname':hostname})

    return data

# isActiveの取得
def getIsActiveForHostname(hostname):
    data = db.find_one_data(DEVICE_INFO, {'hostname':hostname})
    isActive = data['isActive']

    return isActive

def getIsActiveForIpaddress(ip):
    data = db.find_one_data(DEVICE_INFO, {'ipAddress':ip})
    isActive = data['isActive']

    return isActive

# errorCountの取得
def getErrorCount(ip):
    data = db.find_one_data(DEVICE_INFO, {'ipAddress':ip})
    errorCount = data['errorCount']

    return errorCount

# isActiveの更新
def updateIsActiveForHostname(hostname, isActive: bool):
    db.update_one_data(DEVICE_INFO, 
                       {'hostname':hostname}, 
                       {'isActive':isActive})
    
def updateIsActiveForIpaddress(ip, isActive: bool):
    db.update_one_data(DEVICE_INFO, 
                       {'ipAddress':ip}, 
                       {'isActive':isActive})

# lastConnectionCheckDateの更新
def updateLastConnectionCheckDate(hostname):
    db.update_one_data(DEVICE_INFO, 
                       {'hostname':hostname}, 
                       {'lastConnectionCheckDate':datetime.datetime.now()})

# errorCountのインクリメント
def incrementErrorCount(ip):
    data = db.find_one_data(DEVICE_INFO, {'hostname':ip})

    db.update_one_data(DEVICE_INFO, 
                       {'ipAddress':ip}, 
                       {'errorCount':data['errorCount']+1})



def main():
    threads = []

    # 同一ネットワーク接続機器の確認
    check_alive_list_cp = subprocess.run('./NetWorkAliveCheck.sh', encoding='utf-8', stdout=subprocess.PIPE)
    check_alive_list = check_alive_list_cp.stdout.splitlines()

    # 同一ネットワーク接続機器のipアドレスのリスト作成
    ip_list = []
    for check_alive_line in check_alive_list:
        ip_list.append(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', check_alive_line)[0])
    
    try:
        while(True):
            for ip_address in ip_list:
                # URLにリクエストを送信
                http_url = f'http://{ ip_address }:8000/DeviceInfo'

                try:
                    response = requests.get(http_url, timeout=1.5)
                    status_code = response.status_code

                    if(status_code == requests.codes['ok']):
                        json_load = response.json()
                        
                        # DB登録済みならisActiveとcheckConnectionCheckDateを更新
                        if(isExistDeviceForHostname(json_load['hostname'])):
                            # 直前までFalseだった場合isActiveをTrueにしてサーバー起動
                            if(getIsActiveForHostname(json_load['hostname']) == False):
                                updateIsActiveForHostname(json_load['hostname'], True)

                                # # サーバー起動
                                # rtsp_url = f'rtsp://{ ip_address }:8554/unicast'
                                # server = Server(rtsp_url)
                                # thread = threading.Thread(target=server.run, args=(NA, ))
                                # thread.start()
                                # # threads.append({
                                # #     'ip_address': ip_address,
                                # #     'thread': threading.Thread(target=server.run, args=(NA, ))
                                # # })
                                # #threads[-1]['thread'].start()
                            
                            # 最終接続確認日時を更新
                            updateLastConnectionCheckDate(json_load['hostname'])

                            continue
                        
                        else:
                            # DBに登録
                            registDevice(json_load['hostname'], ip_address)

                            # # サーバー起動
                            # rtsp_url = f'rtsp://{ ip_address }:8554/unicast' 
                            # server = Server(rtsp_url)
                            # thread = threading.Thread(target=server.run, args=(NA, ))
                            # threads.append({
                            #     'ip_address': ip_address,
                            #     'thread': thread
                            # })
                            # thread.start()
                        
                    else :
                        # DB登録済みなら
                        if(isExistDeviceForIpaddress(ip_address)):
                            # errorCountを増加
                            incrementErrorCount(ip_address)
                            
                            # errorCountが一定以上の場合、isActiveをFalseにしてサーバー停止
                            if(getErrorCount(ip_address) > 4):
                                # target_thread = next((x for x in threads if x['ip_address'] == ip_address), None)
                                # threads.remove(target_thread)
                                
                                updateIsActiveForIpaddress(ip_address, False)


                except Exception as e:
                    # DB登録済みなら
                    if(isExistDeviceForIpaddress(ip_address)):
                        # 直前までTrueだった場合isActiveをFalseにしてサーバー停止
                        if(getIsActiveForIpaddress(ip_address) == True):
                            updateIsActiveForIpaddress(ip_address, False)
                            # target_thread = next((x for x in threads if x['ip_address'] == ip_address), None)
                            # threads.remove(target_thread)
                    # print(e, "\n")
                    
                    time.sleep(1.5)


    except KeyboardInterrupt:
        print('\nプログラム終了')
    


if __name__ == '__main__':   
    main()