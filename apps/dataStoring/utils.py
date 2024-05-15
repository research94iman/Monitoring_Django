import time
from typing import Union, List
import re
import json
from apps.dataStoring import serializers as S
from apps.dataStoring import models as M

# In[utils]
def valuesListToDict(valueList: List):
    output = {}
    for item in valueList[1:]:
        # find valid key
        counter = 1
        suggested_key = item[0]
        valid_key = False
        while valid_key == False:
            if counter == 1:
                suggested_key = item[0]
            else:
                suggested_key = item[0] + "_" + str(counter)

            if suggested_key not in output.keys():
                valid_key = True
            else:
                counter += 1
        output[suggested_key] = item[1]
    return output


def statusToInt(status):
    if status in ["Disconnected"]:
        output = 0

    elif status in ["Connected", "OK", "ok", "Ok"]:
        output = 1

    elif status in ["Warning"]:
        output = 2
    else:
        print(f'[warning] status not in valid list status = {status}')
        output = -1
    return output


# In[json]
def convertRequestDataToJsonShortTableColumn(requestData):
    output = {}
    q = requestData['DeviceList']
    output['name'] = requestData['name']
    output['TX'] = q[0]['Sensors']
    output['RX'] = q[1]['Sensors']
    output['Operation'] = q[2]['Sensors']
    output['AllPCs'] = q[3]['Sensors']
    output['SNMPAgents'] = q[4]['Sensors']
    output['SherkatNet'] = q[5]['Sensors']
    output['RXNet'] = q[6]['Sensors']
    output['TxNet'] = q[7]['Sensors']
    return output


def convertRequestDataToJsonLongTableColumn(requestData):
    output = {}
    output['Name'] = requestData['Name']
    output['AllData'] = requestData['AllData']
    return output



# In[Organized]
def convertRequestDataToNetTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Values"] = valuesListToDict(requestData['Values'])
    return output


def convertRequestDataToSnmpTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Values"] = valuesListToDict(requestData['Values'])
    return output


def convertRequestDataToTxTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Values"] = valuesListToDict(requestData['Values'])
    output["Message"] = requestData.__getitem__('message')
    return output


def convertRequestDataToCtcTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Values"] = valuesListToDict(requestData['Values'])
    output["Message"] = requestData.__getitem__('message')
    output["TimeLabel"] = requestData['TimeLabel']
    output["TimeLabelIntegrated"] = requestData['TimeLabelIntegrated']
    output["NRXIntegrated"] = requestData['NRXIntegrated']
    output["RXValues"] = valuesListToDict(requestData['RXValues'])
    return output


def convertRequestDataToSigPrcTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["TimeLabel"] = requestData['TimeLabel']
    output["Values"] = valuesListToDict(requestData['Values'])
    output["ChProps"] = valuesListToDict(requestData['ChProps'])
    # output["ChProps"]= {}
    # for i, item in enumerate(requestData['ChProps'][1:]):
    #     output["ChProps"]["AvMx" + str(i)] = item[1]
    return output


def convertRequestDataToPcsTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Values"] = valuesListToDict(requestData['Values'])
    output["MemPer"] = requestData['MemPer']
    output["CPULoad"] = requestData['CPULoad']
    output["HDDValues"] = valuesListToDict(requestData['HDDValues'])
    output["Cores"] = valuesListToDict(requestData['Cores'])
    return output


def convertRequestDataToAdsbTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["Message"] = requestData['message']
    output["UpTime"] = requestData['UpTime']
    output["FrameRate"] = requestData['FrameRate']
    output["Connected"] = requestData['Connected']
    return output


def convertRequestDataToOperationTableColumn(requestData):
    output = {}
    output["ID"] = requestData['ID']
    output["Name"] = requestData['Name']
    output["Status"] = statusToInt(requestData['status'])
    output["IP"] = requestData['IP']
    output["NLayer"] = requestData['NLayer']
    output["AX"] = requestData['AX']
    output["AY"] = requestData['AY']
    output["UpTime"] = requestData.get('UPTime',"0")
    output["Layers"] = valuesListToDict(requestData['Layers'])
    return output

# In[]
class JsonToDB:
    def __init__(self):
        pass

    def _readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def _sigPrc(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("ID[0-9][0-9]SigPrc", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToSigPrcTableColumn(r) for r in rows]
        serializer_instances = [S.sigPrcSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.SigPrc.objects.bulk_create([M.SigPrc(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _net(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("NT[0-9][0-9][0-9]", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToNetTableColumn(r) for r in rows]
        serializer_instances = [S.netSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Net.objects.bulk_create([M.Net(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _snmp(self, jsonData):
        rows = []
        for item in jsonData:
            q1 = re.search("UPS", item["ID"])
            q2 = re.search("Generator", item["ID"])
            q3 = re.search("NetPing", item["ID"])
            if q1 or q2 or q3:
                rows.append(item)
        cleanData = [convertRequestDataToSnmpTableColumn(r) for r in rows]
        serializer_instances = [S.snmpSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Snmp.objects.bulk_create([M.Snmp(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _ctc(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("CTCSoft", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToCtcTableColumn(r) for r in rows]
        serializer_instances = [S.ctcSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Ctc.objects.bulk_create([M.Ctc(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _adsb(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("ADSB", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToAdsbTableColumn(r) for r in rows]
        serializer_instances = [S.adsbSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Adsb.objects.bulk_create([M.Adsb(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _pcs(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("PCInfo", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToPcsTableColumn(r) for r in rows]
        serializer_instances = [S.pcsSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Pcs.objects.bulk_create([M.Pcs(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _tx(self, jsonData):
        rows = []
        for item in jsonData:
            q1 = re.search("TXTXSoft", item["ID"])
            q2 = re.search("PA", item["ID"])
            if q1 or q2:
                rows.append(item)
        cleanData = [convertRequestDataToTxTableColumn(r) for r in rows]
        serializer_instances = [S.txSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Tx.objects.bulk_create([M.Tx(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def _operation(self, jsonData):
        rows = []
        for item in jsonData:
            q = re.search("PPI", item["ID"])
            if q:
                rows.append(item)
        cleanData = [convertRequestDataToOperationTableColumn(r) for r in rows]
        serializer_instances = [S.operationSerializer(data=c) for c in cleanData]
        valid_instances = [serializer.is_valid() for serializer in serializer_instances]
        if all(valid_instances):
            validated_data_list = [serializer.validated_data for serializer in serializer_instances]
            M.Operation.objects.bulk_create([M.Operation(**data) for data in validated_data_list])
            return "Success"
        else:
            errors = [serializer.errors for serializer in serializer_instances]
            return "Validation Error: {}".format(errors)

    def run(self, jsonpath):
        jsonData = self._readJson(jsonFile=jsonpath)

        _a1 = self._sigPrc(jsonData)
        _a2 = self._net(jsonData)
        _a3 = self._snmp(jsonData)
        _a4 = self._ctc(jsonData)
        _a5 = self._adsb(jsonData)
        _a6 = self._pcs(jsonData)
        _a7 = self._tx(jsonData)
        _a8 = self._operation(jsonData)
        return
