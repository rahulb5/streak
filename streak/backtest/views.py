from django.shortcuts import render
from backtest.main import main
from django.http import HttpResponse
#from .main import trade

# Create your views here.
class query:
    def __init__ (self):
        self.first_parameter = ""
        self.condition = ""
        self.second_parameter = "" 

def indicator(parameter_list):
    for i in range(0,len(parameter_list)):
        if parameter_list[i] == 'SMA 14':
            parameter_list[i] = '0'
        elif parameter_list[i] == 'SMA 100':
            parameter_list[i] = '1'

def get_data(request):        
    return render(request, 'get_data.html' , {})

def submit(request):
    
    if request.method == 'POST': 
        user_entry_condition = []
        user_exit_condition = []
        user_entry_condition.append(request.POST.getlist('entry parameter'))
        user_entry_condition.append(request.POST.getlist('entry condtion'))
        user_entry_condition.append(request.POST.getlist('second_entry_parameter'))
        
        user_exit_condition.append(request.POST.getlist('exit parameter'))
        user_exit_condition.append(request.POST.getlist('exit condition'))
        user_exit_condition.append(request.POST.getlist('second exit parameter'))
        
        indicator(user_entry_condition[0])
        indicator(user_entry_condition[2])
        indicator(user_exit_condition[0])
        indicator(user_exit_condition[2])
        
        print(user_entry_condition)
        back = main(user_entry_condition, user_exit_condition)
        back.summary() 
        print("cgchc")
        
        data = {
        'back' : back,        
        }
        
    return render(request , "submit.html" , data)