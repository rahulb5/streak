from django.shortcuts import render
from .models import dataform

# Create your views here.
def homepage(request):
    form = dataform()
    context = {
        'form': form,        
    }
    
    return render(request, "main/home.html", context)

def input_data(request):
    form = dataform()
    text = None
    if request.method == "POST":
        form = dataform(request.POST)
        if form.is_valid():
            text = form.cleaned_data['first_parameter']
            print(text)
            form = dataform()
    
    context = {
        'form' : form,
        'text' : text,        
    }
    
    return render(request, "main/input_data.html" , context)