from typing import Union, List


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
        print(f"[warning] status not in valid list status = {status}")
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
