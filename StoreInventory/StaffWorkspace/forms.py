from django import forms


class WorkerInputForm(forms.Form):
    item_name = forms.CharField(
        max_length=50, help_text='100 characters max.',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control col-md-8'}
        )
    )

