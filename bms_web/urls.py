from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    
    path('', views.home, name='home'),    
    path('device', views.home, name='home'),
    path('plugin', views.plugin, name='plugin'),
    path('device_add_popup', views.add_device_node, name='device_add_popup'),
    path('device_mod_popup', views.mod_device_node, name='device_mod_popup'),
    path('device_info', views.device_info, name='device_info'),
    path('add_dev', views.device_add, name='add_dev'),
    path('online_dev', views.online_dev, name='online_dev'),
    path('query_plugin_list', views.device_plugin_list, name='query_plugin_list'),
    path('plugin_install', views.device_plugin_install, name='plugin_install'),
    path('plugin_uninstall', views.device_plugin_uninstall, name='plugin_uninstall'),
    path('plugin_run', views.device_plugin_run, name='plugin_run'),
    path('plugin_stop', views.device_plugin_stop, name='plugin_stop'),
    path('plugin_upgrade', views.device_plugin_upgrade, name='plugin_upgrade'),
    path('plugin_factory', views.device_plugin_factory, name='plugin_factory'),
]
