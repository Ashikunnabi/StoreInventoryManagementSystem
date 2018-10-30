from django import forms


class WorkerInputForm(forms.Form):

    cost_per_unit = forms.FloatField(
        required=False, initial=0, min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )
    previous_balance = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8', 'readonly': 'readonly'}
        )
    )
    purchase = forms.IntegerField(
        required=False,initial=0, min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8', 'onchange': 'purchaseItem()', 'onkeyup': 'purchaseItem()'}
        )
    )
    issued = forms.IntegerField(
        required=False,initial=0, min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8', 'onchange': 'issuedItem()', 'onkeyup': 'issuedItem()'}
        )
    ) 
    ending_balance = forms.IntegerField(
        initial=0, min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8', 'readonly':'readonly'}
        )
    )   
    issued_to = forms.CharField(
        required=False,
        max_length=50, help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )
    comments = forms.CharField(
        required=False,
        max_length=100, help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-8', 'placeholder': 'Write within 100 letters'}
        )
    )

