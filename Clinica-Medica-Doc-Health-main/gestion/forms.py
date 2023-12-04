from django import forms
import re
from django.core.exceptions import ValidationError

class RutField(forms.CharField):
    rut = forms.CharField(
        label='Ingresa tu RUT completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def validate_rut(self, rut):
        if len(rut) != 9:
            raise forms.ValidationError("El RUT debe tener 9 caracteres.", code='invalid_length')

        # Extraer el dígito verificador del RUT ingresado
        provided_verifier = rut[-1]
        rut_without_verifier = rut[:8]

        reversed_rut = rut_without_verifier[::-1]
        factors = [2, 3, 4, 5, 6, 7]
        total = 0
        for i, digit in enumerate(reversed_rut):
            total += int(digit) * factors[i % 6]

        remainder = total % 11

        if remainder == 0:
            calculated_digit = 0
        elif remainder == 1:
            calculated_digit = 'K'
        else:
            calculated_digit = 11 - remainder

        if str(calculated_digit) != provided_verifier:
            raise forms.ValidationError("El dígito verificador ingresado no es válido.", code='invalid_verifier')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        self.validate_rut(rut)

        return int(rut[:8])

def validate_rut( rut):
        if len(rut) != 9:
            raise forms.ValidationError("El RUT debe tener 9 caracteres.", code='invalid_length')

        provided_verifier = rut[-1]
        rut_without_verifier = rut[:8]

        reversed_rut = rut_without_verifier[::-1]
        factors = [2, 3, 4, 5, 6, 7]
        total = 0
        for i, digit in enumerate(reversed_rut):
            total += int(digit) * factors[i % 6]

        remainder = total % 11

        if remainder == 0:
            calculated_digit = '0'
        elif remainder == 1:
            calculated_digit = 'K'
        else:
            calculated_digit = str(11 - remainder)

        if calculated_digit != provided_verifier:
            raise forms.ValidationError("El dígito verificador ingresado no es válido.", code='invalid_verifier')


class PacienteForm(forms.Form):
    rut = RutField(label="Rut",validators=[validate_rut],widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ej: 266212321'}),required=True)
    nombre = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ej: Juan'}))
    apellido = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Ej: Pérez'}))
    usuario = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: usuario123'}))
    email = forms.EmailField(max_length=300, required=True,widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: usuario@example.com'}))
    contraseña = forms.CharField(max_length=300,min_length=5, required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 5 dígitos'}))
    confirmar_contraseña = forms.CharField(max_length=300, min_length=5, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'}))
    direccion = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 556 Paicaví, Concepción'}))
    telefono = forms.IntegerField(max_value=999999999 , min_value=1,required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 982617201'}))




class MedicoForm(forms.Form):
    rut = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control '}))

    
    sucursal_id = forms.ChoiceField(
        choices=(
            (1, 'Santa Juana'),
            (2, 'San Pedro'),
            (3, 'Concepcion'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    especialidad_id = forms.ChoiceField(
        choices=(
            (1, 'Odontología'),
            (2, 'Cardiología'),
            (3, 'Anestesiología'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    nombre = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control '}))
    apellido = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control '}))
    usuario = forms.CharField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control '}))
    email = forms.EmailField(max_length=300, required=True,widget=forms.TextInput(attrs={'class': 'form-control '}))
    contraseña = forms.CharField(max_length=300,widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)



class LoginPacienteForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=300, required=True)
    contraseña = forms.CharField(max_length=300,widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
