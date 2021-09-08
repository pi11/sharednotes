from django.forms import ModelForm

from .models import Note

class AddPageForm(ModelForm):
    class Meta:
        model = Note
        fields = ("title", )
        
