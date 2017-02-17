import subprocess

from decimal import *

dictionary = {'us-east-1': '23.23.255.255',
        'us-east-2': '52.14.64.0',
        "us-west-1": '50.18.56.1',
        "eu-west-1": '34.248.60.213',
        "us-west-2": '35.160.63.253',
        "eu-central-1": '35.156.63.252',
        "eu-west-2" : '52.56.34.0',
        "us-gov-west-1": '52.222.9.163',
        "ap-northeast-1": '13.112.63.251',
        "ca-central-1": '52.60.50.0',
        "ap-northeast-2" : '52.79.52.64',
        "ap-southeast-1": '52.74.0.2',
        "ap-southeast-2": '54.66.0.2',
        "ap-south-1": '52.66.66.2',
        "sa-east-1":'54.233.127.252'
        }

latencyDict1 = {}

for i in dictionary:

    host =  dictionary[i]
    ping = subprocess.Popen(
    ["ping", "-c", "3", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    list = out.decode().splitlines(out.decode().count('\n'))

    indexLen = len(list)

    val2= list[indexLen-1]

    list2 = val2.split('=',1)

    avgLatency = list2[1].strip().split('/')

    decimalAvgLatency = float(avgLatency[1])
    latencyDict2 = {i + " ["+host+"]": decimalAvgLatency}
    latencyDict1.update(latencyDict2)

sortList = sorted(latencyDict1.items(), key=lambda value: value[1])

counter=1
for key,value in sortList:
    if(counter==1):
        print (str(counter)+"."+key+" - "+"Smallest Average Latency")
    elif(counter==int(len(sortList))):
        print (str(counter)+"."+key+" - "+"Largest Average Latency")
    else:
        print (str(counter)+"."+key+" - "+ str(value))
    counter=counter+1
