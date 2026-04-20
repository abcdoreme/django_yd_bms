from rest_framework import serializers
from .models import Record, Device

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
    
    def create(self, validated_data):
        # 创建新的 Device 实例
        Device.objects.create(mac=validated_data.get('mac'), 
                        gponsn=validated_data.get('gponsn'),
                        status = 0)
        
        # 创建 Record
        record = Record.objects.create(**validated_data)
        return record

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

