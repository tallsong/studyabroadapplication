from rest_framework import serializers
from universitylist.models import *

class UserInfoSerializer(serializers.ModelSerializer):
    '''创建序列化器'''
    class Meta:
        model = Country  # 数据库表名
        fields = '__all__' # 所有的字段都要
        # 注册Book下面那些字段

