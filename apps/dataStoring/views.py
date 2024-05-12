from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models as M
from . import serializers as S
from . import utils as U
from . import forms as F
import json


# In[temp data]
def insertTempData(request):
    if request.method == 'POST':
        form = F.tempDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('importTempData')  # Redirect to the same page after successful submission
    else:
        form = F.tempDataForm()
    return render(request, 'dataStoring/importTempData.html', {'form': form})


@api_view(['GET', 'POST'])
def tempData(request):
    if request.method == 'GET':
        data = M.TempData.objects.all()
        serializer = S.tempDataSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = S.tempDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# In[json]
@api_view(['POST'])
def jsonShort(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToJsonShortTableColumn(request.data)
        serializer = S.jsonShortSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def jsonLong(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToJsonLongTableColumn(request.data)
        serializer = S.jsonLongSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# In[Organized views]

@api_view(['POST'])
def net(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToNetTableColumn(request.data)
        serializer = S.netSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def snmp(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToSnmpTableColumn(request.data)
        serializer = S.snmpSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def tx(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToTxTableColumn(request.data)
        serializer = S.txSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ctc(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToCtcTableColumn(request.data)
        serializer = S.ctcSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sigPrc(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToSigPrcTableColumn(request.data)
        serializer = S.sigPrcSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def pcs(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToPcsTableColumn(request.data)
        serializer = S.pcsSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def adsb(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToAdsbTableColumn(request.data)
        serializer = S.adsbSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def operation(request):
    if request.method == 'POST':
        cleanData = U.convertRequestDataToOperationTableColumn(request.data)
        serializer = S.operationSerializer(data=cleanData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
