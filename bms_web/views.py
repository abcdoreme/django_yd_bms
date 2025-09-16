from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests
from requests.exceptions import RequestException, HTTPError, Timeout, TooManyRedirects, ConnectionError
 

from django.db import IntegrityError

from .models import Record, Device

from .pluginApi import *


def index(request):
    """首页视图"""
    return render(request, 'index.html')

def about(request):
    """关于页面视图"""
    return render(request, 'about.html')

def home(request):
    """首页视图"""
    # 获取所有device
    records = Record.objects.all()
    context = {
        'records': records,
    }
    print(context)
    return render(request, 'home.html', context)

# 处理AJAX POST请求（返回JSON）
# @csrf_exempt  # 仅用于示例，实际项目慎用或配合其他认证方式
def add_device_node(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data_from_json = json.loads(request.body)
            print(data_from_json)
            # ... 处理数据 ...
            obj = Record(mac=data_from_json.get('mac'), 
                         gponsn=data_from_json.get('sn'),
                         ssid=data_from_json.get('ssid'),
                         psk=data_from_json.get('psk'),
                         userpass=data_from_json.get('userpass'),
                         password=data_from_json.get('password'),
                         haswifi=data_from_json.get('haswifi'),
                         province=data_from_json.get('province'),
                         shortconn=data_from_json.get('shortconn'),
                         heartbeat=data_from_json.get('heartbeat'))
            obj.save()
            # 返回JSON响应
            return JsonResponse({'status': 'success', 'message': '操作成功！'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
        except IntegrityError as mysqlErr:
            if 'Duplicate entry' in str(mysqlErr):
                print('设备信息已存在')
                return JsonResponse({'status': 'fail', 'message': '设备信息已存在'}, status=400)
        except Exception as err:
            print("exception:", str(err))
        
        # 同时添加Device实例
        data_from_json = json.loads(request.body)
        # ... 处理数据 ...
        obj = Device(mac=data_from_json.get('mac'), 
                        gponsn=data_from_json.get('sn'),
                        status = 0)
        obj.save()
    else:
        return JsonResponse({'status': 'error', 'message': '只支持POST请求'}, status=405)


def mod_device_node(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data_from_json = json.loads(request.body)
            print(data_from_json)
            # ... 处理数据 ...
            # obj = Record().objects.get(mac=data_from_json.get('mac'))
            obj = Record.objects.get(mac=data_from_json.get('mac'))
            if obj:
                obj.userpass = data_from_json.get('userpass')
                obj.ssid = data_from_json.get('ssid')
                obj.psk = data_from_json.get('psk')
                obj.haswifi = data_from_json.get('haswifi')
                obj.password = data_from_json.get('password')
                obj.province = data_from_json.get('province')
                obj.shortconn = data_from_json.get('shortconn')
                obj.heartbeat = data_from_json.get('heartbeat')
                obj.save()
                # 返回JSON响应
                return JsonResponse({'status': 'success', 'message': '操作成功！'})
            else:
                print('设备信息不存在')
                return JsonResponse({'status': 'fail', 'message': '设备信息不存在'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
        except IntegrityError as mysqlErr:
            if 'Duplicate entry' in str(mysqlErr):
                print('设备信息已存在')
                return JsonResponse({'status': 'fail', 'message': '设备信息已存在'}, status=400)
        except Exception as err:
            print("exception:", str(err))
    else:
        return JsonResponse({'status': 'error', 'message': '只支持POST请求'}, status=405)

def plugin(request):
    # 获取所有device
    devices = Record.objects.all()
    context = {
        'devices': devices,
    }
    return render(request, 'device_plugin.html', context)

def device_add(request):
    # 获取所有device
    devices = Record.objects.all()
    context = {
        'devices': devices,
    }
    return render(request, 'device_add.html', context)

def online_dev(request):
    # 通过curl唤醒设备
    status = None
    result = 0
    data_from_json = json.loads(request.body)
    print(data_from_json)
    tr069 = Device.objects.get(mac=data_from_json.get('mac')).tr069
    print("tr069:{}".format(tr069))
    try:
        response = requests.get(tr069 + "?platform=pms", timeout=5)  # 设置超时时间为5秒
        response.raise_for_status()  # 如果请求返回的不是2xx状态码，将抛出HTTPError异常
        status = 'success'
    except requests.Timeout:
        status = 'error'
        result = -998
    except Exception as err:
        print(f'Other error occurred: {err}')  # 打印其他类型的错误信息
        status = 'error'
        result = -999
    return JsonResponse({'status': status, 'result': result}, safe=False)

def device_info(request):
    """插件信息"""
    # 获取所有device
    MAC = request.GET.get('mac')
    devices = Device.objects.filter(mac=MAC)
    context = {
        'devices': devices,
    }
    print(context)
    return render(request, 'device_info.html', context)

def device_plugin_list(request):
    """刷新插件列表"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    # print(data_from_json)
    result = json.loads(listPlugin(data_from_json.get('mac'), generate_timestamp_based_id()))
    print("result={}".format(result.get('result')))
    if result.get('result') == 0:
        plugins = Device.objects.filter(mac=data_from_json.get('mac')).values('pluginList')
        pluginList = list(plugins)
        print("pluginList={}".format(pluginList))
        return JsonResponse({'status': 'success', 'result': 0, 'pluginList': pluginList}, safe=False)
    elif result.get('result') == -998:
        print("install plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)



def device_plugin_install(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(installPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName'),
        data_from_json.get('pluginVersion'),
        data_from_json.get('pluginSize'),
        data_from_json.get('url')
    ))
    print("result={}".format(result.get('result')))
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("install plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)


def device_plugin_uninstall(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(uninstallPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName')
    ))
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("uninstall plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

def device_plugin_run(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(runPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName')
    ))
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("run plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

def device_plugin_stop(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(stopPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName')
    ))
    print(result)
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("stop plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

def device_plugin_upgrade(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(installPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName'),
        data_from_json.get('pluginVersion'),
        data_from_json.get('pluginSize'),
        data_from_json.get('url')
    ))
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("upgrade plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

def device_plugin_factory(request):
    """安装插件"""
    # 解析JSON数据
    data_from_json = json.loads(request.body)
    print(data_from_json)
    result = json.loads(factoryPlugin(
        data_from_json.get('mac'),
        generate_timestamp_based_id(),
        data_from_json.get('pluginName')
    ))
    if result.get('result') == 0:
        return JsonResponse({'status': 'success', 'result': 0}, safe=False)
    elif result.get('result') == -998:
        print("factory plugin timeout")
        return JsonResponse({'status': 'error', 'result': -998}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

