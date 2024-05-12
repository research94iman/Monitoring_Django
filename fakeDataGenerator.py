import os.path
import threading
import multiprocessing
import requests
from faker import Faker
import json
from datetime import datetime
import random
import time
import copy
import re
import signal

fake = Faker()


class fakeTempDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/insert-temp-data/'
        self.sensors = [
            "SMain",
            "S1",
            "S2",
            "S3",
            "S4",
            "QMain",
            "Q1",
            "Q2",
            "Q3",
            "Q4"
        ]
        self.valueRange = {
            "SMain_values": [0, 1],
            "S1_min": -1,
            "S1_max": 1,
            "S2_min": -1,
            "S2_max": 1,
            "S3_min": -1,
            "S3_max": 1,
            "S4_min": -1,
            "S4_max": 1,
            "QMain_values": [0, 1],
            "Q1_values": [0, 1, 3, 4, 5],
            "Q2_values": [0, 1, 3, 4, 5],
            "Q3_values": [0, 1, 3, 4, 5],
            "Q4_values": [0, 1, 3, 4, 5],
        }

    def valueGenerator(self, sensorName):
        if sensorName + "_values" in self.valueRange.keys():
            key = sensorName + "_values"
            v = random.choice(self.valueRange[key])
        else:
            min_key = sensorName + "_min"
            max_key = sensorName + "_max"
            v = random.uniform(self.valueRange[min_key], self.valueRange[max_key])
        return v

    def fakeGen(self):
        sensorName = random.choice(self.sensors)
        value = self.valueGenerator(sensorName)
        # date = datetime.strftime(fake.date_time_this_year(), "%Y-%m-%dT%H:%M:%SZ")
        date = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")

        fakeData = {
            'name': sensorName,
            'value': value,  # Adjust as needed
            'date': date,
        }
        return fakeData

    def run(self, number=1000, sleep=1, log_interval=100):
        print('start inserting fake temp data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Temp Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number and number != -1:
                break

class fakeJsonDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/jsonShort/'
        self.sampleJson = './privateFiles/Json/logShotrJson6.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        fakedata = copy.copy(self.jsonData)
        fakedata['name'] = os.path.basename(self.sampleJson)

        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake jsonShort data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, JsonShort Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeJsonLongDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/jsonLong/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'
        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):
        fakedata = {}
        fakedata['Name'] = os.path.basename(self.sampleJson)
        fakedata['AllData'] = copy.copy(self.jsonData)

        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Json Long data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, JsonLong Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeSigPrcDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/sigPrc/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def _changeDelay(self, fakeDate):
        delay = random.randint(1, 4)
        labelOut = int(fakeDate["Values"][1][1])
        labelIn = labelOut + delay
        fakeDate["Values"][1][1] = labelIn
        fakeDate["Values"][2][1] = labelOut
        return fakeDate

    def _changeNShot(self, fakeDate):
        Nshot = random.randint(100, 200)
        fakeDate["Values"][4][1] = int(Nshot)
        return fakeDate

    def fakeGen(self):
        fakedata = {}
        fakedata['Name'] = os.path.basename(self.sampleJson)
        fakedata['AllData'] = copy.copy(self.jsonData)

        available_fake_data = []
        for item in self.jsonData:
            q = re.search("ID[0-9][0-9]SigPrc", item["ID"])
            if q:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        fakedata = self._changeDelay(fakedata)
        fakedata = self._changeNShot(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake SigPro data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, sigPrc Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeNetDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/net/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q = re.search("NT[0-9][0-9][0-9]", item["ID"])
            if q:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Net data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Net Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeSnmpDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/snmp/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("UPS", item["ID"])
            q2 = re.search("Generator", item["ID"])
            q3 = re.search("NetPing", item["ID"])
            if q1 or q2 or q3:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Snmp data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Snmp Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeCtcDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/ctc/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("MainCTCCTCSoft", item["ID"])
            if q1:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Ctc data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Ctc Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeAdsbDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/adsb/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("ADSBMainAdsbSoft", item["ID"])
            if q1:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Adsb data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Adsb Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakePcsDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/pcs/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("PCInfo", item["ID"])
            if q1:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Pc data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Pcs Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeTxDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/tx/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data

    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("TXTXSoft", item["ID"])
            q2 = re.search("PA1", item["ID"])
            if q1 or q2:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Tx data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Tx Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break

class fakeOperationDataGenerator:
    def __init__(self):
        # API endpoint
        self.url = 'http://localhost:8000/data/operation/'
        self.sampleJson = './privateFiles/Json/LatestState27.json'

        self.jsonData = self.readJson(self.sampleJson)

    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as file:
            data = json.load(file)
        return data


    def fakeGen(self):

        available_fake_data = []
        for item in self.jsonData:
            q1 = re.search("PPI", item["ID"])
            if q1:
                available_fake_data.append(item)
        fakedata = random.choice(available_fake_data)
        # fakedata = self._changeDelay(fakedata)
        return fakedata

    def run(self, number=1000, sleep=1, log_interval=1):
        print('start inserting fake Operation data!!!')
        counter = 0
        while True:
            data = self.fakeGen()
            response = requests.post(self.url, json=data)
            counter += 1
            time.sleep(sleep)
            if counter % log_interval == 0:
                print(counter)
                if response.status_code == 201:
                    print(f'counter={counter}, Operation Data successfully imported:', "data")
                else:
                    print(f'counter={counter}, Failed to import data:', response.text)

            if counter > number != -1:
                break
# In[]
if __name__ == '__main__':
    # Generator = fakeTempDataGenerator()
    # Generator.run(number=1000, sleep=1, log_interval=100)


    listFakeDataGenerator = [
        fakeJsonLongDataGenerator(),
        fakeSigPrcDataGenerator(),
        fakeNetDataGenerator(),
        fakeSnmpDataGenerator(),
        fakeCtcDataGenerator(),
        fakeAdsbDataGenerator(),
        fakePcsDataGenerator(),
        fakeTxDataGenerator(),
        fakeOperationDataGenerator()
        ]

    number = 100000
    sleep = 1
    log_interval = 100

    process = []
    for generator in listFakeDataGenerator:
        process.append(multiprocessing.Process(target=generator.run, args=(number, sleep, log_interval)))


    for p in process:
        p.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Terminate the processes when Ctrl+C is pressed
        for p in process:
            p.terminate()



    # G0 = fakeJsonLongDataGenerator()
    # G1 = fakeSigPrcDataGenerator()
    # G2 = fakeNetDataGenerator()
    # G3 = fakeSnmpDataGenerator()
    # G4 = fakeCtcDataGenerator()
    # G5 = fakeCtcDataGenerator()


    # # Create processes for each class with arguments
    # process0 = multiprocessing.Process(target=G0.run, args=(number, sleep, log_interval))
    # process1 = multiprocessing.Process(target=G1.run, args=(number, sleep, log_interval))
    # process2 = multiprocessing.Process(target=G2.run, args=(number, sleep, log_interval))
    # process3 = multiprocessing.Process(target=G3.run, args=(number, sleep, log_interval))
    # process4 = multiprocessing.Process(target=G3.run, args=(number, sleep, log_interval))

    # # Start the processes
    # process0.start()
    # process1.start()
    # process2.start()
    # process3.start()

    # Wait for Ctrl+C
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     # Terminate the processes when Ctrl+C is pressed
    #     process0.terminate()
    #     process1.terminate()
    #     process2.terminate()
    #     process3.terminate()

    ## Create threads for each class with arguments
    # thread0 = threading.Thread(target=G0.run, args=(number, sleep, log_interval), name="G0")
    # thread1 = threading.Thread(target=G1.run, args=(number, sleep, log_interval), name="G1")
    # thread2 = threading.Thread(target=G2.run, args=(number, sleep, log_interval), name="G2")

    # def signal_handler(sig, frame):
    #     print('Stopping threads...')
    #     # Stop the threads here
    #     thread0.join()
    #     thread1.join()
    #     thread2.join()
    #     print('Threads stopped.')
    #     # Exit the program
    #     exit(0)
    #
    #
    # # Set threads as daemons
    # thread0.daemon = True
    # thread1.daemon = True
    # thread2.daemon = True
    #
    # # Start the threads
    # thread0.start()
    # thread1.start()
    # thread2.start()
    #
    # # Register the signal handler for SIGINT (Ctrl+C)
    # signal.signal(signal.SIGINT, signal_handler)
    #
    # # Wait indefinitely, the threads will stop when the program exits
    # while True:
    #     time.sleep(1)
