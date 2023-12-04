from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('lista_registro', lista_registro, name="lista_registro"),
    path('registro', registro, name="registro"),
    path('registro_medico', registro_medico, name="registro_medico"),
    path('pacientes', Pacientes, name="pacientes"),
    path('medicos', medicos, name="medicos"),
    path('login', login, name="login"),
    path('agendar_cita/<rut>/<nombre>/<apellido>/', agendar_cita, name="agendar_cita"),
    path('agendar_doctor', agendar_doctor, name="agendar_doctor"),
    path('citas', lista_citas, name="citas"),
    path('cambiar_cita/<id>/', cambiar_cita, name="cambiar_cita"),
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion"),
    path('agendar_cita2/<rut_medico>/<id_disponibilidad>/', agendar_cita2, name="agendar_cita2"),
    path('mis_citas', mis_citas, name="mis_citas"),


    path('vista', mi_vista, name="vista"),

]
