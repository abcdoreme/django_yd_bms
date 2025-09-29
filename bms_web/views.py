from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests
from requests.exceptions import RequestException, HTTPError, Timeout, TooManyRedirects, ConnectionError
 

from django.db import IntegrityError

from .models import Record, Device
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import RecordSerializer, DeviceSerializer

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
            # return JsonResponse({'status': 'success', 'message': '操作成功！'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
        except IntegrityError as mysqlErr:
            if 'Duplicate entry' in str(mysqlErr):
                print('设备信息已存在')
                return JsonResponse({'status': 'fail', 'message': '设备信息已存在'}, status=400)
        except Exception as err:
            print("exception:", str(err))
            return JsonResponse({'status': 'error', 'message': '添加失败，请重试！'}, status=400)
        
        # 同时添加Device实例
        data_from_json = json.loads(request.body)
        # ... 处理数据 ...
        obj = Device(mac=data_from_json.get('mac'), 
                        gponsn=data_from_json.get('sn'),
                        status = 0)
        obj.save()
        
        return JsonResponse({'status': 'success', 'message': '操作成功！'})
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

class CustomPagination(PageNumberPagination):
    """自定义分页类"""
    page_size = 10
    page_size_query_param = 'page_size'  # 允许前端指定每页大小
    max_page_size = 100  # 限制最大每页数量


class RecordViewSet(viewsets.ModelViewSet):
    # queryset = Record.objects.all()
    # print(queryset)
    serializer_class = RecordSerializer
    pagination_class = CustomPagination
    
    search_fields = ['mac', 'gponsn']
    
    ordering_fields = ['id', 'mac', 'gponsn']
    
    def get_queryset(self):
        """动态获取查询集，支持搜索"""
        queryset = Record.objects.all()
        
        # 获取搜索关键词
        keyword = self.request.query_params.get('keyword', None)
        print("keyword:", keyword)
        if keyword:
            queryset = queryset.filter(
                Q(mac__icontains=keyword) | 
                Q(gponsn__icontains=keyword)
            )
        
        return queryset
    
    # 重写list方法
    # def list(self, request, *args, **kwargs):
    #     """重写 list 方法，返回自定义格式的分页数据"""
    #     queryset = self.filter_queryset(self.get_queryset())
        
    #     # 获取分页参数
    #     page = request.query_params.get('page', 1)
    #     page_size = request.query_params.get('page_size', 10)
        
    #     try:
    #         page = int(page)
    #         page_size = int(page_size)
    #         page_size = min(page_size, 100)  # 限制最大每页100条
    #     except ValueError:
    #         page = 1
    #         page_size = 10
        
    #     # 手动分页
    #     paginator = Paginator(queryset, page_size)
    #     page_obj = paginator.get_page(page)
        
    #     serializer = self.get_serializer(page_obj, many=True)
        
    #     return Response({
    #         'code': 200,
    #         'data': {
    #             'list': serializer.data,
    #             'total': paginator.count,
    #             'page': page,
    #             'page_size': page_size,
    #             'total_pages': paginator.num_pages
    #         },
    #         'message': 'success'
    #     })
    
    # 手动添加 PATCH 支持
    # def partial_update(self, request, pk=None):
    #     """
    #     手动实现 partial_update 方法
    #     """
    #     print("partial_update!")
    #     try:
    #         instance = Record.objects.get(pk=pk)
    #     except Record.DoesNotExist:
    #         print("partial_update:not existed!")
    #         return Response(
    #             {'error': '对象不存在'}, 
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        
    #     serializer = self.serializer_class(
    #         instance, 
    #         data=request.data, 
    #         partial=True  # 关键：允许部分更新
    #     )
    #     print("partial_update,serializer:", serializer)
    #     if serializer.is_valid():
    #         print("valid!!!")
    #         serializer.save()
    #         return Response(serializer.data)
        
    #     print("invalid!!!")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # lookup_field = 'mac'  # 使用mac字段作为查找条件
    print("clss,queryset:", queryset)
    
    # def get_object(self, request, *args, **kwargs):
    #     # 获取URL中的参数
    #     print("get object")
    #     # MAC = self.kwargs.get('mac')
    #     MAC = request.GET.get('mac')
    #     if MAC:
    #         print("get_object,MAC:", MAC)
    #     # 根据条件获取对象
    #     # device = Device.objects.get(mac=MAC)
    #     # if device:
    #     #     device_serial = DeviceSerializer(device)
    #     #     return Response(device_serial.data)
    #     # else:
    #     #     return Response()
    #     queryset = self.filter_queryset(self.get_queryset())
    #     obj = get_object_or_404(queryset, mac=MAC)
    #     return obj

    # 自定义动作（会自动生成路由）
    @action(detail=True, methods=['get'])
    def plugin_query(self, request, pk=None):
        device = self.get_object()
        print("plugin query:", device.mac)
        device_serial = DeviceSerializer(device)
        
        return Response(device_serial.data)
    
    @action(detail=True, methods=['post'])
    def plugin_action(self, request, pk=None):
        device = self.get_object()
        action = request.data.get('action')
        print("plugin action:", device.mac, action, request.data.get('Plugin_Name'))
        
        if action == 'run':
            result = json.loads(runPlugin(device.mac, generate_timestamp_based_id(), request.data.get('Plugin_Name')))
        elif action == 'stop':
            result = json.loads(stopPlugin(device.mac, generate_timestamp_based_id(), request.data.get('Plugin_Name')))
        elif action == 'reset':
            result = json.loads(factoryPlugin(device.mac, generate_timestamp_based_id(), request.data.get('Plugin_Name')))
        elif action == 'install':
            result = json.loads(installPlugin(device.mac, generate_timestamp_based_id(), request.data.get('Plugin_Name'), 
                           request.data.get('Version'), request.data.get('Plugin_Size'), request.data.get('url')))
        elif action == 'uninstall':
            result = json.loads(uninstallPlugin(device.mac, generate_timestamp_based_id(), request.data.get('Plugin_Name')))
        
        print("plugin action", action, "result:", result)
        if result.get('result') == 0:
            return JsonResponse({'status': 'success', 'result': 0}, safe=False)
        elif result.get('result') == -998:
            print("run plugin timeout")
            return JsonResponse({'status': 'error', 'result': -998}, safe=False)
        elif result.get('result') == -997:
            print("connect refused")
            return JsonResponse({'status': 'error', 'result': -997}, safe=False)
        else:
            return JsonResponse({'status': 'error', 'result': result.get('result')}, safe=False)

    @action(detail=False, methods=['get'])
    def by_mac(self, request, pk=None):
        MAC = request.GET.get('mac')
        print("MAC:", MAC)        
        device = get_object_or_404(Device, mac=MAC)
        serializer = self.get_serializer(device)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def online(self, request, pk=None):
        # 通过curl唤醒设备
        status = None
        result = 0
        MAC = request.data.get('mac')
        tr069 = Device.objects.get(mac=MAC).tr069
        print("tr069:{}".format(tr069))
        try:
            response = requests.get(tr069 + "?platform=pms", timeout=5)  # 设置超时时间为5秒
            response.raise_for_status()  # 如果请求返回的不是2xx状态码，将抛出HTTPError异常
            status = 'success'
        except requests.Timeout:
            status = 'error'
            result = -998
        except ConnectionRefusedError:
            status = 'error'
            result = -997
        except Exception as err:
            print(f'Other error occurred: {err}')  # 打印其他类型的错误信息
            status = 'error'
            result = -999
        return JsonResponse({'status': status, 'result': result}, safe=False)