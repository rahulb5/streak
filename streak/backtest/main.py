import json

class trade:
    
    def __init__(self):
        self.pos = 0
        self.neg = 0
        self.profit = 0
        self.transaction = []
        self.investment = []
        self.sell = []
        self.entry_date = []
        self.exit_date = []
    
    
    def summary(self):
        print("Total Profit: " + str(self.profit))
        print("Successful trades " + str(self.pos))
        print("Unsuccessful trade " + str(self.neg))
        
class query:
    def __init__ (self):
        self.first_parameter = ""
        self.condition = ""
        self.second_parameter = "" 
    
#double GetDouble(JsonObject jObject) {
#	return atof(jObject.toString().c_str());
#}
#
def compare (condition , first_parameter, prev_first_paramter , second_parameter , prev_second_parameter):
    if condition == 'greater than':
        if first_parameter > second_parameter:
            return True
        else :
            return False
    elif condition == 'less than':
        if first_parameter < second_parameter:
            return True
        else :
            return False
    elif condition == 'crossed above':
        if first_parameter > second_parameter and prev_first_paramter < prev_second_parameter:
            return True
        else :
            return False
    elif condition == 'crossed below':
        if first_parameter < second_parameter and prev_first_paramter > prev_second_parameter:
            return True
        else :
            return False
    elif condition == 'equal to': 
        if first_parameter == second_parameter:
            return True
        else :
            return False

def backtest(user_entry_condition , user_exit_condition , datapoints , qty):
    
    buy_flag = 0
    back = trade()
    count = 0
    f = open('data.txt', "w")
    
    for i in range(1,len(datapoints['open'])):
        if buy_flag == 0:
            flag_entry_condition = 0
            
            for j in user_entry_condition:
                
                variable = compare(j.condition , datapoints[j.first_parameter][i], datapoints[j.first_parameter][i-1],datapoints[j.second_parameter][i] , datapoints[j.second_parameter][i-1])
#                print(str(datapoints[j.first_parameter][i]) + j.condition + " " + str())
                if variable == False:
                    flag_entry_condition = 1
                    break
            if flag_entry_condition == 0: 
                buy_flag = 1
                back.investment.append(qty*datapoints['close'][i])
                back.entry_date.append(datapoints['ltt'][i])
                f.write("%.3f %.3f %s" % (datapoints['close'][i], datapoints['0'][i], datapoints['ltt'][i]))
        else:
            flag_exit_condition = 0
            
            for j in user_exit_condition:
                if not compare(j.condition , datapoints[j.first_parameter][i],datapoints[j.first_parameter][i-1],datapoints[j.second_parameter][i] , datapoints[j.second_parameter][i-1]):
                    flag_exit_condition = 1
                    break
            if flag_exit_condition == 0:
                buy_flag = 0
                back.sell.append(qty*datapoints['close'][i])
                back.exit_date.append(datapoints['ltt'][i])
                profit = back.sell[-1] - back.investment[-1]
                back.profit = back.profit + profit
                back.transaction.append(profit)
                if profit >= 0:
                    back.pos += 1
                else:
                    back.neg += 1
                
                f.write("\t %.3f %s %.3f\n" % (datapoints['close'][i], datapoints['ltt'][i], profit))
    f.close()
    return back

def main(entry_condition , exit_condition):    
    #sorting out relevant datapoints        
    data = {}
    with open('backtest/3.txt') as json_file:
        data = json.load(json_file)
        
    pltPnts = data['data']['pltPnts']
    tiOut = data['data']['tiOut']
    
    datapoints = {}
    for key in pltPnts.keys():
        datapoints[key] = pltPnts[key]
    for index in range(0, len(tiOut)):
        datapoints[str(index)] = tiOut[index]['rsltSet'][0]['vals']
    
    datapoints[''] = "None"
    #taking entry conditions from the user
    user_entry_condition = []
    user_exit_condition = []
    
    for i in range(0,len(entry_condition[0])):
        temp = query()
        user_entry_condition.append(temp)
        user_entry_condition[i].first_parameter = entry_condition[0][i]
        user_entry_condition[i].condition = entry_condition[1][i]
        user_entry_condition[i].second_parameter = entry_condition[2][i]
      
    for i in range(0,len(exit_condition[0])):
        temp = query()
        user_exit_condition.append(temp)
        user_exit_condition[i].first_parameter = exit_condition[0][i]
        user_exit_condition[i].condition = exit_condition[1][i]
        user_exit_condition[i].second_parameter = exit_condition[2][i]

    f = open("temp.txt" , "w")    
    for i in range(0,len(datapoints['open'])):
        f.write("%.3f %.3f %.3f %s\n" %(datapoints['open'][i], datapoints['close'][i] , datapoints['0'][i] , datapoints['ltt'][i]))
    f.close()
        
    
    
    back = backtest(user_entry_condition, user_exit_condition , datapoints , 1)
    return back