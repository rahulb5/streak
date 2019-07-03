import json
import requests
from django.http import HttpResponseBadRequest
counter = 500

def compare (first_parameter, condition, second_parameter):
    if condition == 'greater than':
        if first_parameter[-1] > second_parameter[-1]:
            return True
        else :
            return False
    elif condition == 'less than':
        if first_parameter[-1] < second_parameter[-1]:
            return True
        else :
            return False
    elif condition == 'crossed above':
        if first_parameter[-1] > second_parameter[-1] and first_parameter[-2] < second_parameter[-2]:
            return True
        else :
            return False
    elif condition == 'crossed below':
        if first_parameter[-1] < second_parameter[-1] and first_parameter[-2] > second_parameter[-2]:
            return True
        else :
            return False
    elif condition == 'equal to': 
        if first_parameter[-1] == second_parameter[-1]:
            return True
        else :
            return False


def check_conditions(entry_condition, exit_condition, datapoints, temp, live_results):
    
    
    if temp.buy_flag == 0:
        entry_flag = 1
        for i in range(0, len(entry_condition.first_parameter)):
            first_parameter = datapoints[entry_condition.first_parameter[i]]
            condition = entry_condition.condition[i]
            second_parameter = datapoints[entry_condition.second_parameter[i]]
            if compare(first_parameter, condition, second_parameter) == False:
                entry_flag = 0
                break
        if entry_flag == 1:
            temp.buy_flag = 1
            temp.save()
            live_results.buy_price.append(datapoints['close'][-1])
            live_results.buy_time.append(datapoints['ltt'][-1])
            live_results.save()
            print("Buy")
    else:
        exit_flag = 1
        for i in range(0,len(exit_condition.first_parameter)):
            first_parameter = datapoints[exit_condition.first_parameter[i]]
            condition = exit_condition.condition[i]
            second_parameter = datapoints[exit_condition.second_parameter[i]]
            if compare(first_parameter, condition , second_parameter) == False:
                exit_flag = 0
                break
        if exit_flag == 1:
            temp.buy_flag = 0
            temp.save()
            live_results.exit_price.append(datapoints['close'][-1])
            profit = float(live_results.buy_price[-1]) - live_results.exit_price[-1]
            live_results.exit_time.append(datapoints['ltt'][-1])
            live_results.profit.append(profit)
            live_results.save()
            print("Exit")
      
def deployed(entry_condition, exit_condition, temp, live_results):
    global counter
    api_url = 'https://emt.edelweiss.in/edelmw-content/content/charts/v2/main/M1/NSE/EQUITY/11536_NSE'
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImV4cCI6MTU2NDE2NjU2MCwiZmYiOiJNIiwiaXNzIjoiZW10IiwibmJmIjoxNTYxNTc0MjYwLCJhcHBpZCI6IjhiMDk2N2FlMDVkMDgzMmEyNTdlMzEyNzcxYWRmMjc2Iiwic3JjIjoiZW10bXciLCJpYXQiOjE1NjE1NzQ1NjAsImF2IjoiNC4xLjEiLCJiZCI6ImFuZHJvaWQtcGhvbmUifQ.PuKISoLOvi1cf0tY_zbivH2mc4yQE_EuosVBYEPpyN4'
    headers = {
        'accept': 'application/json',
        'appidkey': api_key,
        'content-type': 'application/json',
    }
    
    data = '{"frcConti":false,"crpAct":true,"conti":false, "chTyp":"Interval", "tiInLst": [{"tiTyp": "SMA", "tiIn": {"period" : 14}}, {"tiTyp": "SMA", "tiIn": {"period" : 100}}], "isPvl":true}'
    
    try:
        response = requests.post(api_url, headers=headers, data=data)
    except:
        return HttpResponseBadRequest("check your internet connection")
    
    data = json.loads(response.content.decode('utf-8'))
    datapoints = {}
    pltpnts = data['data']['pltPnts']
    
    
    key_list = ['open','close', 'high', 'low' , 'vol' , 'ltt']
    tiOut = data['data']['tiOut']
    for i in key_list:
        temp_list = [pltpnts[i][counter-1] ,pltpnts[i][counter]]
        datapoints[i] = temp_list
        
    for i in range(0 , len(tiOut)):
        datapoints[str(i)] = [tiOut[i]['rsltSet'][0]['vals'][counter-1], tiOut[i]['rsltSet'][0]['vals'][counter]]
    counter += 1
    check_conditions(entry_condition , exit_condition, datapoints, temp, live_results)
    print(datapoints['ltt'])