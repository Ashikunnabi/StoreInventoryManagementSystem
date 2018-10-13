from django import forms


class WorkerInputForm(forms.Form):

    cost_per_unit = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )
    previous_balance = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8', 'readonly': 'readonly'}
        )
    )
    purchase = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )
    issued = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8'}
        )
    ) 
    ending_balance = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-8'}
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

