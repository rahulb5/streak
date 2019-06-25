from django import forms

class dataform(forms.Form):
    parameter_choice = (
        (None , 'Parameter'),
        ('open' , 'Open'),
        ('close' , 'Close'),
        ('high' , 'High'),
        ('low' ,'Low'),
        ('0', 'SMA 14'),
        ('1', 'SMA 100'),
        ('numeric' , 'Numeric'),
    )
    condition_choice = (
        (None, 'Condtion'),
        ('greater than' , 'Greater than'),
        ('less than' , 'Less than'),
        ('crossed above' , 'Crossed above'),
        ('crossed below', 'Corssed below'),
        ('equal to' , 'Equal to'),
    )
    first_parameter = forms.CharField(widget=forms.Select(choices=parameter_choice))
    condition = forms.CharField(widget = forms.Select(choices=condition_choice))
    second_parameter = forms.CharField(widget=forms.Select(choices=parameter_choice))
    numeric_value = forms.IntegerField()
    

