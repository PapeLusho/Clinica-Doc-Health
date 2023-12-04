from django.contrib import admin
from .models import *

# Register your models here.

# class EspecialidadAdmin(admin.ModelAdmin):
#     list_display = ['id','nombre']


# class SucursalAdmin(admin.ModelAdmin):
#     list_display = ['id','nombre','direccion','telefono']

# class PacienteAdmin(admin.ModelAdmin):
#     list_display = ['rut','usuario','nombre','fecha_nacimiento',"telefono"]

# class MedicoAdmin(admin.ModelAdmin):
#     list_display = ['rut','usuario','nombre','sucursal',"especialidad",'telefono']


# class CitaAdmin(admin.ModelAdmin):
#     list_display = ['id','rut_medico','rut_paciente','dia','hora','estado']



# admin.site.register(Especialidad, EspecialidadAdmin)
# admin.site.register(Sucursal, SucursalAdmin)
# admin.site.register(Paciente, PacienteAdmin)
# admin.site.register(Medico, MedicoAdmin)
# admin.site.register(Cita_Medica, CitaAdmin)
