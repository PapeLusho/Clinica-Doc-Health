from django.shortcuts import render,redirect
from .forms import *
import requests
from django.http import HttpResponse
from requests.exceptions import RequestException
from django.http import HttpResponseBadRequest

PACIENTE_LOGIN = 0
# Create your views here.

def mi_vista(request):
    try:
        api_url = ''
        response = requests.get(api_url)

        if response.status_code == 200:
            mensaje_hello = response.text
            return HttpResponse(f'Mensaje de la API: {mensaje_hello}')
        else:
            return HttpResponse('Error al obtener el mensaje de la API')
    except RequestException as e:
        return HttpResponse(f'Error en la solicitud a la API: {e}')

def home(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    return render(request, 'home.html',{'rut_paciente':rut_paciente})

def cerrar_sesion(request):
    request.session['PACIENTE_LOGIN'] = ''
    return redirect('home')

def registro(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.cleaned_data
            rut = paciente['rut']
            paciente['rut'] = str(rut[:9])

            if paciente['contraseña'] == paciente['confirmar_contraseña']:

                response = requests.post('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/pacientes/add', json=paciente)
                response_data = response.json()
                response2 = requests.get('https://Clinica-Doc-Health.edinsondelgado4.co/api/pacientes/')
                pacientes = response2.json()
                
                for paciente1 in pacientes:
                    if paciente.get('email') == paciente['email']:
                        paciente_rut = paciente1.get('rut')

                        # Almacena el valor del rut en la sesión
                        request.session['PACIENTE_LOGIN'] = paciente_rut

                        if response.status_code == 200:
                            mensaje = "Guardado correctamente"
                            return render(request, 'home.html', {'rut_paciente': paciente_rut,'mensaje':mensaje})
                        else:
                            mensaje = "Error al conectar con la API Flask: " + response_data.get('message', 'Mensaje de error desconocido')
                        return render(request, 'registro.html', {'form': form, 'mensaje': mensaje})
            else:
                # Si las contraseñas no coinciden, muestra un mensaje de error
                form.add_error('confirmar_contraseña', "Las contraseñas no coinciden")
                return render(request, 'registro.html', {'form': form})
        else:
            return render(request, 'registro.html', {'form': form , 'errors': form.errors, 'mensaje': 'formulario invalido'})
    else:
        form = PacienteForm()
        return render(request, 'registro.html', {'form': form,'rut_paciente':rut_paciente})

def registro_medico(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    data = {
        'form':MedicoForm(),
        'rut_paciente':rut_paciente
    }
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():


            medico = form.cleaned_data
            medico['especialidad_id'] = str(medico['especialidad_id'])
            medico['sucursal_id'] = str(medico['sucursal_id'])

            response = requests.post('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/medicos/add', json=medico)
            
            response_data = response.json()

            data['mensaje2'] = response

            if response.status_code == 200:
                data['mensaje'] = "Guardado correctamente en la API Flask"
            else:
                data['mensaje2'] = "Error al conectar con la API Flask: " + response_data.get('message', 'Mensaje de error desconocido')
        else:
            data['mensaje3'] = form.errors
            return render(request, 'registro_medico.html', data)
                
    
    return render(request, 'registro_medico.html', data)


def lista_registro(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    return render(request, 'lista_registro.html',{'rut_paciente':rut_paciente})

def Pacientes(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/pacientes')
    try:
        if response.status_code == 200:
            pacientes = response.json()
            return render(request, 'pacientes.html', {'pacientes': pacientes,'rut_paciente':rut_paciente})
        else:
            return render(request, 'pacientes.html', {'error_msg': 'Error al obtener datos de pacientes'})
    except Exception as ex:
        return render(request, 'pacientes.html', {'error_msg': str(ex)})



def medicos(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/medicos')
    try:
        if response.status_code == 200:
            medicos = response.json()
            return render(request, 'medicos.html', {'medicos': medicos,'rut_paciente':rut_paciente})
        else:
            return render(request, 'medicos.html', {'error_msg': 'Error al obtener datos de medicos'})
    except Exception as ex:
        return render(request, 'medicos.html', {'error_msg': str(ex)})



 

def login(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    data = {
        'form': LoginPacienteForm(),
        'rut_paciente':rut_paciente
    }
    if request.method == 'POST':
        form = LoginPacienteForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            email = user['email']

            try:
                response = requests.post('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/pacientes/login', json=user)
                response2 = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/pacientes/')

                pacientes = response2.json()

                for paciente in pacientes:
                    if paciente.get('email') == email:
                        paciente_rut = paciente.get('rut')

                        request.session['PACIENTE_LOGIN'] = paciente_rut

                        response_data = response.json()
                        data['mensaje'] = response

                        if response.status_code == 200:
                            return render(request, 'home.html', {'rut_paciente': paciente_rut})
                        else:
                            request.session['PACIENTE_LOGIN'] = ''
                            paciente_rut = ''
                            mensaje_error = response_data.get('message', 'Error desconocido')
                            return render(request, 'login.html', {'error_message': mensaje_error,'rut_paciente': paciente_rut,'form': LoginPacienteForm()})
            except Exception as ex:
                request.session['PACIENTE_LOGIN'] = ''
                paciente_rut = ''
                return render(request, 'login.html', {'error_message': str(ex),'data':data,'rut_paciente': paciente_rut})

    return render(request, 'login.html', data)

def agendar_doctor(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/medicos')
    try:
        if response.status_code == 200:
            medicos = response.json()
            return render(request, 'agendar_medico.html', {'medicos': medicos,'rut_paciente':rut_paciente})
        else:
            return render(request, 'agendar_medico.html', {'error_msg': 'Error al obtener datos de medicos'})
    except Exception as ex:
        return render(request, 'agendar_medico.html', {'error_msg': str(ex)})
    

def agendar_cita(request, rut,nombre,apellido):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    nombreMed = nombre
    apellidoMed = apellido
    unique_dates = set() 

    if request.method == 'POST':
        selected_date = request.POST.get('fecha')
        response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/disponibilidad/' + rut )
        for item in response.json():
            date = item.get('fecha')
            if date not in unique_dates:
                unique_dates.add(date)

        disponibilidad = response.json()
        return render(request, 'agendar_cita.html', {'unique_dates': list(unique_dates),'rut_paciente':rut_paciente,'disponibilidad': disponibilidad, 'rut': rut,'nombreMed':nombreMed,'apellidoMed':apellidoMed, 'unique_dates': unique_dates, 'selected_date': selected_date})
    else:
        response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/disponibilidad/' + rut)

        for item in response.json():
            date = item.get('fecha')
            if date not in unique_dates:
                unique_dates.add(date)

        try:
            if response.status_code == 200:
                return render(request, 'agendar_cita.html', {'rut': rut,'nombreMed':nombreMed,'apellidoMed':apellidoMed, 'unique_dates': list(unique_dates)})
            else:
                return render(request, 'agendar_cita.html', {'nombreMed':nombreMed,'apellidoMed':apellidoMed,'error_msg': 'Error al obtener datos de medicos'})
        except Exception as ex:
            return render(request, 'agendar_cita.html', {'nombreMed':nombreMed,'apellidoMed':apellidoMed,'error_msg': str(ex)})

def lista_citas(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/cita_medica/')
    try:
        if response.status_code == 200:
            citas = response.json()
            return render(request, 'citas.html', {'citas': citas ,'rut_paciente':rut_paciente})
        else:
            return render(request, 'citas.html', {'error_msg': 'Error al obtener datos de medicos'})
    except Exception as ex:
        return render(request, 'citas.html', {'error_msg': str(ex)})

def cambiar_cita(request, id):
    if request.method == 'POST':
        estado = request.POST.get('estado')

        response = requests.put('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/cita_medica/cambiar/' + id + '/' + estado)

        if response.status_code == 200:
            return redirect('citas')
        else:
            return HttpResponseBadRequest('Error al cambiar el estado')
    else:
        return HttpResponseBadRequest('Método no permitido')

def agendar_cita2(request, rut_medico, id_disponibilidad):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    if rut_paciente == '':
        return redirect('login')
    else:
        cita = {'rut_medico': rut_medico, 'id_disponibilidad': id_disponibilidad, 'rut_paciente': rut_paciente, 'id_estado': 4}
        response = requests.post('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/cita_medica/add', json=cita)
        response2 = requests.put('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/disponibilidad/cambiar/'+id_disponibilidad+'/'+'False')
        response3 = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/cita_medica/citas/'+ str(rut_paciente) )

        try:
            if response.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
                citas = response3.json()
                return render(request, 'mis_citas.html', {'citas':citas,'rut_paciente': rut_paciente,'msj':'cita programada :)'})
            else:
                return render(request, 'citas.html', {'error_msg': 'Error al agendar la cita'})
        except Exception as ex:
            return render(request, 'citas.html', {'error_msg': str(ex)})

def mis_citas(request):
    rut_paciente = request.session.get('PACIENTE_LOGIN', '')
    response = requests.get('https://Clinica-Doc-Health.edinsondelgado4.repl.co/api/cita_medica/citas/'+ str(rut_paciente) )

    try:
        if response.status_code == 200:
            citas = response.json()
            return render(request, 'mis_citas.html', {'citas':citas,'rut_paciente': rut_paciente})
        else:
            return render(request, 'mis_citas.html', {'error_msg': 'Error al agendar la cita'})
    except Exception as ex:
            return render(request, 'mis_citas.html', {'error_msg': str(ex)})

