from django.contrib import admin
from django.apps import apps

models = apps.get_models()

SKIP_MODELS = ('TokenProxy', 'TokenAdmin')

for model in models:
    if model.__name__ not in SKIP_MODELS:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            print(f'{model} already registered')
