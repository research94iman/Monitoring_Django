from rest_framework import serializers
# from .models import TempData, JsonShort, JsonLong, SigPrc
from . import models as M


# In[temp serializer]
class tempDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.TempData
        fields = ['id', 'name', 'value', 'date']


# In[raw json serializer]
class jsonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.JsonShort
        # fields = '__all__'
        exclude = ['date']


class jsonLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.JsonLong
        # fields = '__all__'
        exclude = ['Date']


# In[Organized]
class netSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Net
        # fields = '__all__'
        exclude = ['Date']


class snmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Snmp
        # fields = '__all__'
        exclude = ['Date']


class txSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Tx
        # fields = '__all__'
        exclude = ['Date']


class ctcSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Ctc
        # fields = '__all__'
        exclude = ['Date']


class sigPrcSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.SigPrc
        # fields = '__all__'
        exclude = ['Date']


class pcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Pcs
        # fields = '__all__'
        exclude = ['Date']


class adsbSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Adsb
        # fields = '__all__'
        exclude = ['Date']


class operationSerializer(serializers.ModelSerializer):
    class Meta:
        model = M.Operation
        # fields = '__all__'
        exclude = ['Date']
