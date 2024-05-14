#imports
import requests
import pandas as pd
import json
from datetime import datetime

###CLASSES
class ReportStringParam:
###Class Definition###
    def __init__(self):
        self._requested_report = '' 
        self._report_StartDate = ''
        self._report_EndDate = ''

    ###Setters###   
    def setter_RequestReport(self, x):
        self._requested_report = x

    #start and end dates should be in year-month format (YYYY-MM)
    def setter_ReportStartDate(self, x):    
        self._report_StartDate = x

    def setter_ReportEndDate(self, x):    
        self._report_EndDate = x 

    ###Getters###
    def getter_RequestReport(self):
        return self._requested_report

    def getter_ReportStartDate(self):    
        return self._report_StartDate

    def getter_ReportEndDate(self):    
        return self._report_EndDate
    
    requested_report = property(getter_RequestReport,setter_RequestReport)
    report_StartDate = property(getter_ReportStartDate,setter_ReportStartDate)
    report_EndDate = property(getter_ReportEndDate,setter_ReportEndDate)

class vendorSUSHIinfo:
###Class Definition###    
    def __init__(self):
        self._baseURL = ''
        self._customer_id = '' 
        self._requestor_id = ''
    ###Setters###  
    def setter_BaseURL(self, x):
        self._baseURL = x
    def setter_Customer_ID(self, x):
        self._customer_id = x    
    def setter_Requestor_ID(self, x):
        self._requestor_id = x
    
    ###Getters###
    def getter_BaseURL(self):    
        return self._baseURL
    def getter_Customer_ID(self):
        return self._customer_id
    def getter_Requestor_ID(self):
        return self._requestor_id
    
    baseURL = property(setter_BaseURL,getter_BaseURL)
    customer_id = property(setter_Customer_ID,getter_Customer_ID)
    requestor_id = property(setter_Requestor_ID,getter_Requestor_ID)


#Definitions
def parser(jsonData):
    buildArray = []
    vendor_ID = jsonData['Report_Header']['Created_By']
    for titleIndex in jsonData['Report_Items']:
        title = titleIndex['Title']
        isbn = ''
        print_issn = '' 
        online_issn = ''
        proprietary = '' 
        #print(title)
        if 'Item_ID' in titleIndex.keys():
            
            for itemID in titleIndex['Item_ID']:
                        
                if 'ISBN' in itemID['Type']:
                    isbn = itemID['Value']
                elif 'Print_ISSN' in itemID['Type']:
                    print_issn = itemID['Value']
                elif 'Online_ISSN' in itemID['Type']:
                    online_issn = itemID['Value']
                elif 'Proprietary' in itemID['Type']:
                    proprietary = itemID['Value']
                else:
                    print('null')

        for itemIndexing in titleIndex['Performance']:
            BeginDate = datetime.strptime(itemIndexing['Period']['Begin_Date'], "%Y-%m-%d")
            EndDate = datetime.strptime(itemIndexing['Period']['End_Date'], "%Y-%m-%d")
    

            for c in itemIndexing['Instance']:
                metrictype = c['Metric_Type']
                metricCount = c['Count']
                eventDict = {"Vendor":vendor_ID, "Title":title, "ISBN":isbn, "PrintISSN":print_issn, "OnlineISSN":online_issn, "Proprietary":proprietary, "Begin_Date":BeginDate, "End_Date":EndDate, "Metric":metrictype, "Metric_count":metricCount}  
                buildArray.append(eventDict)
            #print(eventDict)
    return buildArray

def buildCallString(vendorSUSHIinfo,ReportStringParam):
    requestURL = f"{vendorSUSHIinfo.getter_BaseURL()}/reports/{ReportStringParam.getter_RequestReport()}?customer_id={vendorSUSHIinfo.getter_Customer_ID()}&requestor_id={vendorSUSHIinfo.getter_Requestor_ID()}&begin_date={ReportStringParam.getter_ReportStartDate()}&end_date={ReportStringParam.getter_ReportEndDate()}"
    return requestURL

###MAIN FUNCTIONS###
def main():
    #creating the report params object
    reportParams = ReportStringParam()
    reportParams.setter_RequestReport('tr')
    reportParams.setter_ReportStartDate('2023-01')
    reportParams.setter_ReportEndDate('2023-12')

    #load vendor.json file
    data = json.load(open('vendor.json'))

    #building vendor dataframes from vendor.json file
    builtVendor = []
    dataframeOUTS = []
    for i in data['vendor']:
        print(i)
        var = vendorSUSHIinfo()
        print(var)
        #globals()[f'{i}_SUSHIinfo'] = vendorSUSHIinfo()
        var.setter_BaseURL(data['vendor'][i]['baseURL'])
        var.setter_Customer_ID(data['vendor'][i]['customer_id'])
        var.setter_Requestor_ID(data['vendor'][i]['requestor_id'])
        #print(globals()[f'{i}_SUSHIinfo'].getter_BaseURL())
        print(var.getter_BaseURL())
        #print(data['vendor'][i]['baseURL'])
        print(var.getter_Customer_ID())
        print(var.getter_Requestor_ID())
        loopbuildString = buildCallString(var,reportParams)
        print(loopbuildString)
        builtVendor.append({i:loopbuildString})
        APICall = requests.get(loopbuildString)
        dataframe = pd.DataFrame(parser(APICall.json()))
        dataframeOUTS.append({i:dataframe})

    #binding all created dataframes into a flatfile

    megamergeDataframe = pd.DataFrame()

    for i in range(len(dataframeOUTS)):
        print(dataframeOUTS[i].keys())
        for x in dataframeOUTS[i].keys():
            #print(x)
            #print(dataframeOUTS[i][x])
            megamergeDataframe = pd.concat([megamergeDataframe,dataframeOUTS[i][x]])
    print('wrapping megamerge for output...')
    megamergeDataframe.to_excel('megamergeSushiBuffetOutput.xlsx')
    megamergeDataframe.to_csv('megamergeSushiBuffetOutput.csv')
    print('dataframe Outputted!')
    print('Process finished!')

if __name__ == "__main__":
    main()
