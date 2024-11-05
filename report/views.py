import csv
import re
from .forms import RecordForm
from .models import Record, Profile
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'home.html')


################################################## CADASTRO
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['email'] == request.POST['email_confirm']:

            if not re.fullmatch(r'\d+', request.POST['re']):
                return render(request, 'signup.html', {
                    "error": "O RE deve conter apenas números!"
                })

            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'signup.html', {
                    "error": "Este e-mail já está em uso. Tente um diferente."
                })

            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    is_active=False
                )
                user.save()

                profile = Profile.objects.create(
                    user=user,                      # Associando user e profile
                    re=request.POST['re']
                )
                profile.save()

                return render(request, 'signin.html', {
                    'user_created': 'Usuário criado com sucesso! É necessário que o administrador forneça permissão antes de acessar.'
                })
            
            except Exception as e:
                return render(request, 'signup.html', {
                    "error": "Erro ao criar usuário! Nome de usuário ou RE já existe."
                })

        return render(request, 'signup.html', {
            "error": "Senhas ou e-mails divergentes!"
        })

######################################################### LOGIN
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    
    else:
        username_or_email = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            username = username_or_email
        
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Usuário sem permissão de acesso! Contate o administrador.'
                })
        except User.DoesNotExist:
            pass 
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuário e/ou senha incorreto(s)'
            })
        else:
            login(request, user)
            return redirect('user_area')

#################################################################### LOGOUT
@login_required
def sair(request):
    logout(request)
    return redirect('home')


##################################################################### PAG. APOS LOGIN
@login_required
def user_area(request):
    today = timezone.now().date()
    records = Record.objects.filter(call_date__date=today)  
    return render(request, 'user_area.html', {'records': records})


##################################################################### CRIAÇÃO DE REGISTRO
@login_required
def create_record(request):
    if request.method == 'GET':                         
        return render(request, 'create_record.html', {
            'form' : RecordForm
        })
    else:
        try:
            form = RecordForm(request.POST)
            new_record = form.save(commit=False)
            new_record.user = request.user

            def apply_default(field_value):
                return field_value.strip() if field_value.strip() else "Não Informado"

            new_record.caller_name = apply_default(request.POST.get('caller_name', ""))
            new_record.caller_phone = apply_default(request.POST.get('caller_phone', ""))
            new_record.caller_zip_code = apply_default(request.POST.get('caller_zip_code', ""))
            new_record.caller_neighborhood = apply_default(request.POST.get('caller_neighborhood', ""))
            new_record.caller_street = apply_default(request.POST.get('caller_street', ""))
            new_record.caller_house_number = apply_default(request.POST.get('caller_house_number', ""))
            new_record.is_caller_part_of = 'is_caller_part_of' in request.POST
            new_record.is_caller_wating = 'is_caller_wating' in request.POST
            new_record.call_date = timezone.now()

            new_record.save()
            return render(request, 'create_record.html', {
                'form' : RecordForm,
                'success' : 'Registro criado com sucesso!'
            })
        
        except ValueError:                      
            return render(request, 'create_record.html', {
                'form' : RecordForm,
                'error' : 'Erro ao registrar! Algum campo não foi preenchido corretamente'
            })


########################################################################## CONSULTAS
@login_required
def today_records(request):
    today = timezone.now().date()  
    records = Record.objects.filter(call_date__date=today)
    return render(request, 'today_records.html', {'records': records})

@login_required
def all_records(request):
    records = Record.objects.all()
    return render(request, 'all_records.html', {'records': records})


######################################################################## EXPORTAÇÕES
@login_required
def export_records_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registros_gcm.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow([       #cabeçalho
        'solicitante',
        'telefone',
        'cep_do_solicitante',
        'bairro_do_solicitante',
        'rua_do_solicitante',
        'numero_casa_do_solicitante',
        'parte_da_ocorrencia',
        'esperando_no_local',
        'data_hora_fato',
        'data_chamada',
        'plantonista'])
    

    for record in Record.objects.all():
        record.is_caller_part_of = 'Sim' if record.is_caller_part_of else 'Não'
        record.is_caller_wating = 'Sim' if record.is_caller_wating else 'Não'

        ###Formatação das datas
        if record.fact_date:
            fact_date = record.fact_date.replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        else:
            fact_date = ''
        
        if record.call_date:
            call_date = record.call_date.replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        else:
            call_date = ''
        
        plantonista = f"{record.user.first_name} {record.user.last_name}" if record.user else ''

        writer.writerow([
            record.caller_name,
            record.caller_phone,
            record.caller_zip_code,
            record.caller_neighborhood,
            record.caller_street,
            record.caller_house_number,
            record.is_caller_part_of,
            record.is_caller_wating,
            fact_date,
            call_date,
            plantonista])
    return response


@login_required
def export_records_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="registros_gcm.xlsx"'
    
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Registros'
    
    sheet.append([          #cabeçalho
        'solicitante',
        'telefone',
        'cep_do_solicitante',
        'bairro_do_solicitante',
        'rua_do_solicitante',
        'numero_casa_do_solicitante',
        'parte_da_ocorrencia',
        'esperando_no_local',
        'data_hora_fato',
        'data_chamada',
        'plantonista'])
    
    for record in Record.objects.all():

        record.is_caller_part_of = 'Sim' if record.is_caller_part_of else 'Não'
        record.is_caller_wating = 'Sim' if record.is_caller_wating else 'Não'

        ###Formatação das datas
        #replace(tzinfo=None) é para remoção do fuso horário.
        if record.fact_date:
            fact_date = record.fact_date.replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        else:
            fact_date = ''
        
        if record.call_date:
            call_date = record.call_date.replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        else:
            call_date = ''
    
        plantonista = f"{record.user.first_name} {record.user.last_name}" if record.user else ''

        sheet.append([
            record.caller_name,
            record.caller_phone,
            record.caller_zip_code,
            record.caller_neighborhood,
            record.caller_street,
            record.caller_house_number,
            record.is_caller_part_of,
            record.is_caller_wating,
            fact_date,
            call_date,
            plantonista])

    workbook.save(response)
    return response