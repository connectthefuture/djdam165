# Register your models here.
from django.contrib import admin
import autocomplete_light
from models import ImageUpdate

class ImageUpdateAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ImageUpdate)
admin.site.register(ImageUpdate)


