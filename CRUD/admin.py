from django.contrib import admin
from .models import PresionManometrica
from .models import PresionDiferencial
from .models import Temperatura
from .models import FlujoVolumetricoDinamico
from .models import PatronesPresionManometrica

#from .models import Curriculums




# Register your models here.
class PresionManometricaAdmin(admin.ModelAdmin):
  list_display = ("fecha_asignacion", "responsable",)
  
admin.site.register(PresionManometrica, PresionManometricaAdmin)

class PresionDiferencialAdmin(admin.ModelAdmin):
  list_display = (id, "fecha_asignacion", "responsable",)
  
admin.site.register(PresionDiferencial, PresionDiferencialAdmin)
class TemperaturaAdmin(admin.ModelAdmin):
  list_display = (id, "fecha_asignacion", "responsable",)
  
admin.site.register(Temperatura, TemperaturaAdmin)
class FlujoVolumetricoDinamicoAdmin(admin.ModelAdmin):
  list_display = (id, "fecha_asignacion", "responsable",)
  
admin.site.register(FlujoVolumetricoDinamico, FlujoVolumetricoDinamicoAdmin)

class PatronesPresionManometricaAdmin(admin.ModelAdmin):
  list_display = ("patron_identificacion", "patron_marca")
admin.site.register(PatronesPresionManometrica, PatronesPresionManometricaAdmin)

#class CurriculumsAdmin(admin.ModelAdmin):
    #list_display = ("id_asociado", "nombre_asociado")
#admin.site.register(Curriculums, CurriculumsAdmin)
