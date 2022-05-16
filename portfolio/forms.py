from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    surname = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(max_length=50)
    topic = forms.CharField(max_length=120)
    content = forms.CharField(widget=forms.Textarea(attrs={'style': "width: 93%", 'rows': 10}))
    
    
