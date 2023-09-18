from django import forms


class TasaEditForm(forms.Form):
    id = forms.CharField(label='id', max_length=2)
    tasa = forms.CharField(label='tasa', max_length=10)
