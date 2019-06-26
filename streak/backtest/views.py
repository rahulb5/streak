from django.shortcuts import render
from backtest.main import main
from .models import trade
from django.http import HttpResponseBadRequest
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
    
    var_id = request.session['saved']
    back = trade.objects.get(id = var_id)
    data = {
        'back' : back,        
        }
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
        
        try:
            back = main(user_entry_condition, user_exit_condition)
            back.save()
        except:
            return HttpResponseBadRequest("please fill the fields correctly")
        request.session['saved'] = back.id
        data = {
        'back' : back,        
        }
        
    return render(request , "submit.html" , data)

def details(request):
    var_id = request.session['saved']
    details = trade.objects.get(id = var_id)
    details.summary()
    rang = len(details.exit_date)
    print(rang)
    zippped_list = zip(details.investment, details.entry_date,details.sell,details.exit_date,details.transaction)
    return render(request, 'details.html' , {'detail': details,'zipped_list':zippped_list, 'range' : range(rang)})
