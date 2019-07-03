from django.shortcuts import render
from backtest.models import conditions
from .models import live_model, results
from .deploy import deployed
from django.shortcuts import redirect
#from .deploy import deployed

def truncate(request):
    print("this was truncated")
    try:
        live_results_id = request.session['live_results']
    except: 
        return redirect('http://127.0.0.1:8000/get_data/submit')
    live_results = results.objects.get(id = live_results_id)
    live_results.delete()
    temp_id = request.session['temp_id']
    temp = live_model.objects.get(id = temp_id)
    temp.buy_flag = 0
    temp.save()
    return redirect('http://127.0.0.1:8000/get_data/submit')

# Create your views here.
def deploy(request):
    
    entry_id = request.session['entry_conditions']
    exit_id = request.session['exit_conditions']
    temp_id = request.session['temp_id']
    live_results_id = request.session['live_results']
    
    entry_condition = conditions.objects.get(id = entry_id)
    exit_condition = conditions.objects.get(id = exit_id)
    temp = live_model.objects.get(id = temp_id)
    live_results = results.objects.get(id = live_results_id)
    
    deployed(entry_condition, exit_condition, temp, live_results)
    zipped_list1 = zip(live_results.buy_price, live_results.buy_time )
    zipped_list2 = zip(live_results.exit_price, live_results.exit_time, live_results.profit)
    
    content = {'zipped_list1': zipped_list1, 'zipped_list2' : zipped_list2}
    
    return render(request, 'deploy.html' , content)
