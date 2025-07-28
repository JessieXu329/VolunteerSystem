from django import forms
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'phone', 'notes']
        labels = {
            'name': '姓名',
            'phone': '电话',
            'notes': '备注',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }