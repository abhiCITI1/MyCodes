import itertools
import collections
from itertools import groupby
import csv
import sys
import psutil

class NetStat:

    #This function will find out all TCP connections to my system and print the grouped and sorted record in CSV format
    def findAndPrintNetStat(self):
        rowDict = {}
        connectionExractedList = []
        net_connections = psutil.net_connections(kind='tcp')
        splitAddr = []
        exceptPIDRecordsList = []
        connectionExractedDict = {}
        finalDictList = []
        pidList = []
        completeRecordList = []
        counterDictionary = {}
        countPidList = []
        csvTupleList = ()

        #looping to iterate and extract the 4 value(PID,LADDR,RADDR,STATUS) record from all the TCP connections record
        for connectionRow in range(len(net_connections)):
            connectionTupleRow = net_connections[connectionRow]
            #checking only for the records having LADDR and RADDR
            if connectionTupleRow.laddr and connectionTupleRow.raddr:
                laddr = str(connectionTupleRow.laddr[0])+'@'+str(connectionTupleRow.laddr[1])
                raddr = str(connectionTupleRow.raddr[0])+'@'+str(connectionTupleRow.raddr[1])

                rowDict2 = {'PID': connectionTupleRow.pid,
                             'LADDR': laddr,
                             'RADDR': raddr,
                             'STATUS': connectionTupleRow.status}
                rowDict.update(rowDict2)
                connectionExractedList.append(rowDict.items())

        """/**looping to extract the PID and adding it to a separate list, also etracting 4 values
        which are stored in a key:value format from the list and storing them again to a seperate list **/"""
        for connectionRecord in range(len(connectionExractedList)):
            connectionExractedDict = dict(connectionExractedList[connectionRecord])
            pidList.append(connectionExractedDict['PID'])
            exceptPIDRecordsString = str(connectionExractedDict['PID'])+'/'+connectionExractedDict['LADDR']+'/'+connectionExractedDict['RADDR']+'/'+connectionExractedDict['STATUS']
            exceptPIDRecordsList.append(exceptPIDRecordsString)

        #this api will group the common PIDs and store them in a list
        groupByPidList = [list(v) for k,v in itertools.groupby(pidList)]
        for i in range(len(groupByPidList)):
            for j in range(len(groupByPidList[i])):
                countPidList.append(groupByPidList[i][j])

        #this api will count the grouped common PIDs based on their no of occurences
        counterOfPIDs=collections.Counter(countPidList)

        #these two nested for loops will compare the PID from one complete record list with the PID:Counter values in other list
        for record in range(len(exceptPIDRecordsList)):

            splitRecordOfEachRow = exceptPIDRecordsList[record].split('/')
            for pid,pidCount in counterOfPIDs.items():
                if int(splitRecordOfEachRow[0]) == int(pid):
                    completeRecordDict = {str(splitRecordOfEachRow[0]) + '/' + str(splitRecordOfEachRow[1]) + '/' + str(splitRecordOfEachRow[2]) + '/' + str(splitRecordOfEachRow[3]): int(pidCount)}
                    completeRecordList.append(completeRecordDict)
        #this for loop will prepare the complete record in tuple format with key as complete record, value as their count
        for recordValue in range(len(completeRecordList)):
            csvTupleList = csvTupleList + tuple(completeRecordList[recordValue].items())
        #this api will sort the final tuple list of records based on their counter values
        sortedCSVList = sorted(list(csvTupleList), key=lambda value:value[1],reverse = True)

        #printing the output in csv format
        csvFile = open("csvOutput.txt", 'wt')
        try:
            writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
            writer.writerow( ("pid","laddr","raddr","status") )
            for i in range(len(sortedCSVList)):
                splitRow = str(sortedCSVList[i]).split('/')
                writer.writerow( (splitRow[0].strip("('"),
                splitRow[1],
                splitRow[2],
                str(splitRow[3].split(',')[0]).strip("\'")) )
        finally:
            csvFile.close()

        print open("csvOutput.txt", 'rt').read()

netStat = NetStat()
netStat.findAndPrintNetStat()
