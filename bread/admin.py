from django.contrib import admin

from bread.models import Grain, Flour, Leaven, FlourInLeaven, Bread, FlourInBread


admin.site.register(Grain)
admin.site.register(Flour)
admin.site.register(Leaven)
admin.site.register(FlourInLeaven)
admin.site.register(Bread)
admin.site.register(FlourInBread)