
import random
import socket
import json
import time

from bms_django import settings


SOCKET_PATH = '/tmp/.bms.sock'

def query_test(user_id):
    # curl http://192.168.46.109:46000?platform=pms
    #request = json.dumps({'RPCMethod': 'ListPlugin', 'MAC':'C824964791A9', 'ID': user_id})
    #request = json.dumps({'RPCMethod': 'Stop', 'MAC':'C824964791A9', 'ID': user_id, 'Plugin_Name':'com.chinamobile.smartgateway.cmccdpi'})
    #request = json.dumps({'RPCMethod': 'Install', 'MAC':'C824964791A9', 'ID': user_id, 'Plugin_Name':'com.cmcc.hy.osgitest', 'Version':'1.0.6', 'Download_url':'http://192.168.20.29/download/com.cmcc.hy.osgitest_1.0.6.jar', 'Plugin_size':281966})
    request = json.dumps({'RPCMethod': 'Rusn', 'MAC':'981E8927A1B0', 'ID': user_id, 'Plugin_Name':'com.chinamobile.smartgateway.cmccdpi'})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.send(request.encode())
    response = client.recv(1024)
    print(response)
    if response:
        return json.loads(response.decode())
    else:
        return ""

def listPlugin(mac, user_id):
    request = json.dumps({'RPCMethod': 'ListPlugin', 'MAC':mac, 'ID': user_id})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()
    

def runPlugin(mac, user_id, pluginName):
    request = json.dumps({'RPCMethod': 'Run', 'MAC':mac, 'ID': user_id, 'Plugin_Name': pluginName})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

def stopPlugin(mac, user_id, pluginName):
    request = json.dumps({'RPCMethod': 'Stop', 'MAC':mac, 'ID': user_id, 'Plugin_Name': pluginName})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

def installPlugin(mac, user_id, pluginName, pluginVersion, pluginSize, url):
    request = json.dumps({
        'RPCMethod': 'Install',
        'MAC':mac,
        'ID': user_id,
        'Plugin_Name': pluginName,
        'Version': pluginVersion,
        'Plugin_size': pluginSize,
        'Download_url': url        
    })
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

def uninstallPlugin(mac, user_id, pluginName):
    request = json.dumps({'RPCMethod': 'UnInstall', 'MAC':mac, 'ID': user_id, 'Plugin_Name': pluginName})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

def upgradePlugin(mac, user_id, pluginName, pluginVersion, pluginSize, url):
    request = json.dumps({
        'RPCMethod': 'Install',
        'MAC':mac,
        'ID': user_id,
        'Plugin_Name': pluginName,
        'Version': pluginVersion,
        'Plugin_size': pluginSize,
        'Download_url': url        
    })
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

def factoryPlugin(mac, user_id, pluginName):
    request = json.dumps({'RPCMethod': 'FactoryPlugin', 'MAC':mac, 'ID': user_id, 'Plugin_Name': pluginName})
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(settings.SOCKET_TIMEOUT)
    try:
        client.connect(SOCKET_PATH)
        client.send(request.encode())
        response = client.recv(1024)
        print(response)
        if response:
            print(response.decode())
            return response
        else:
            return json.dumps({'result': -999})
    except socket.timeout:
        print("timeout")
        return json.dumps({'result': -998})
    finally:
        client.close()

@staticmethod
def generate_timestamp_based_id():
    """基于时间戳生成ID"""
    # 获取当前时间戳（微秒级）
    timestamp = int(time.time())
    
    # 添加随机数
    random_component = random.randint(0, 9999)
    
    # 组合成唯一ID
    unique_id = timestamp + random_component
    
    return unique_id



    
