from django.contrib import admin
from .models import Items
from .models import Ingrdesc
from .models import IngredientsInItems
from .models import Ingrko2Eng

admin.site.register(Items)
admin.site.register(Ingrdesc)
admin.site.register(IngredientsInItems)
admin.site.register(Ingrko2Eng)