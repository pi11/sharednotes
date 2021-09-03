from slugify import slugify

from django.db.models.signals import pre_save
from django.db import models


class BaseModel(models.Model):
    added = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
        
class History(BaseModel):
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "{}{}".format(str(self.note), self.added)
    
class Note(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        
def save_history(sender, instance, update_fields=None, **kwargs):
    try:
        old_instance = Note.objects.get(id=instance.id)
    except Note.DoesNotExist:  # to handle initial object creation
        return None

    h = History(note=instance, text=instance.text)
    h.save()

pre_save.connect(save_history, sender=Note)
