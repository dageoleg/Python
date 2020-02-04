

#https://github.com/aws-samples/aws-cost-explorer-report/blob/master/src/lambda.py

import boto3
import datetime
import pprint
import csv
from openpyxl import Workbook

### const

ACCESS_KEY = ""
SECRET_KEY = ""

awsregion = "us-east-1"

### Main

ce_client = boto3.client(
    'ce',
    region_name=awsregion,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)


today = datetime.date.today()

first_period_start = today + datetime.timedelta(days=-today.weekday(), weeks=-2)
first_period_start_str = str(first_period_start)
first_period_end_str = str(first_period_start + datetime.timedelta(days=7))
second_period_start = today + datetime.timedelta(days=-today.weekday(), weeks=-1)
second_period_start_str = str(second_period_start)
second_period_end_str = str(second_period_start + datetime.timedelta(days=7))


# get list of accounts

def get_accounts():
    accounts = {}
    client = boto3.client(    'organizations',
        region_name=awsregion,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    paginator = client.get_paginator('list_accounts')
    response_iterator = paginator.paginate()
    for response in response_iterator:
        for acc in response['Accounts']:
            accounts[acc['Id']] = acc
    return accounts

### Main

accounts_json = get_accounts()


# get 1st period costs by account
response = ce_client.get_cost_and_usage( 
    TimePeriod={ 
        'Start': first_period_start_str, 
        'End': first_period_end_str }, 
    Granularity='MONTHLY', 
    Metrics=[ 'AmortizedCost',],
    GroupBy=[
        {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
    ],
)
#first_period_costs_by_account.extend(response['ResultsByTime'][0]['Groups'])
first_period_costs_by_account = []
for r in response['ResultsByTime']:  # if week is spread across two months 
    first_period_costs_by_account.append(r['Groups'])


# TODO nexttoken
# while 'nextToken' in response:
#     nextToken = response['nextToken']
#     response = self.client.get_cost_and_usage(
#         NextPageToken=nextToken
#     )
#     first_period_costs_by_account.extend(response['ResultsByTime'][0]['Groups'])


#pprint.pprint(first_period_costs_by_account['Groups'])

# get 2nd period costs by account
response = ce_client.get_cost_and_usage( 
    TimePeriod={ 
        'Start': second_period_start_str, 
        'End': second_period_end_str }, 
    Granularity='MONTHLY', 
    Metrics=[ 'AmortizedCost',],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'LINKED_ACCOUNT'
        },
    ],
)
#second_period_costs_by_account.extend(response['ResultsByTime'][0]['Groups'])
second_period_costs_by_account = []
for r in response['ResultsByTime']:  # if week is spread across two months 
    second_period_costs_by_account.append(r['Groups'])

#pprint.pprint(second_period_costs_by_account)

workbook1 = Workbook()
sheet = workbook1.active
sheet["A1"] = "Account number"
sheet["B1"] = "Account name"
sheet["C1"] = "Cost of week " + first_period_start_str
sheet["D1"] = "Absolute delta"
sheet["E1"] = "Percent"
sheet["F1"] = "Cost of week" + second_period_start_str

r = 2
first_groups = first_period_costs_by_account #[0]['Groups']
second_groups = second_period_costs_by_account #[0]['Groups']
for second_group in second_groups:
    second_period_account = second_group['Keys'][0]
    second_period_amount = float(second_group['Metrics']['AmortizedCost']['Amount'])
    for first_group in first_groups:
        if first_group['Keys'][0] == second_period_account:
            first_period_amount = float(first_group['Metrics']['AmortizedCost']['Amount'])
    increase = (1-(float(first_period_amount)/float(second_period_amount)))
    #if increase > 0.005:
    print(second_period_account, accounts_json[second_period_account]['Name'].replace(' ',''), round(first_period_amount,2), round(increase,2), round(second_period_amount,2))
    sheet["A"+str(r)] = second_period_account
    sheet["B"+str(r)] = accounts_json[second_period_account]['Name']
    sheet["C"+str(r)] = round(first_period_amount,2)
    sheet["D"+str(r)] = round(second_period_amount-first_period_amount,2)
    sheet["E"+str(r)] = round(increase,2)
    sheet["F"+str(r)] = round(second_period_amount,2)
    round(second_period_amount,2)
    r += 1

workbook1.save(filename="Comparsion_"+first_period_start_str+"_"+second_period_start_str+".xlsx")



# TODO for accounts with cost increased - make drill-down by: usageType



