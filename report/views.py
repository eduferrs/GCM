import csv
import re
from .forms import RecordForm
from .models import Record, Profile, IncidentType
from openpyxl import Workbook
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
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
    not_dispatched_records = Record.objects.filter(is_dispatched=False).order_by('-priority_incident', 'call_date')
    not_finished_records = Record.objects.filter(is_finished=False, is_dispatched=True).order_by('-priority_incident', 'call_date')
    users = User.objects.filter(is_active=True)

    return render(request, 'user_area.html', {
        'not_dispatched_records': not_dispatched_records,
        'not_finished_records': not_finished_records,
        'users': users,
    })



##################################################################### CRIAÇÃO DE REGISTRO
@login_required
def create_record(request):
    if request.method == 'GET':             #Carregamento da pagina
        incident_types = IncidentType.objects.all().order_by('type')
        return render(request, 'create_record.html', {
            'form': RecordForm(),
            'incident_types': incident_types
        })
    else: 
        try:
            form = RecordForm(request.POST)
            if form.is_valid():

                new_record = form.save(commit=False)  #Cria o objeto, mas ainda não salva
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

                new_record.reference_point = apply_default(request.POST.get('reference_point', ""))

                new_record.suspect_haircut_style = apply_default(request.POST.get('suspect_haircut_style', ""))
                new_record.suspect_tatoos = apply_default(request.POST.get('suspect_tatoos', ""))
                new_record.suspect_approximate_age = apply_default(request.POST.get('suspect_approximate_age', ""))
                new_record.suspect_approximate_height = apply_default(request.POST.get('suspect_approximate_height', ""))
                new_record.suspect_description = apply_default(request.POST.get('suspect_description', ""))

                fact_date = request.POST.get('fact_date')
                if fact_date:
                    new_record.fact_date = timezone.datetime.strptime(fact_date, '%Y-%m-%dT%H:%M')
                
                incident_type_value = request.POST.get('type_of_incident')
                if incident_type_value:
                    incident_type, created = IncidentType.objects.get_or_create(type=incident_type_value)
                    new_record.incident_type = incident_type

                new_record.number_of_people_involved = apply_default(request.POST.get('number_of_people_involved', ""))
                new_record.nature_of_the_incident = apply_default(request.POST.get('nature_of_the_incident', ""))
                new_record.vehicle = apply_default(request.POST.get('vehicle', ""))
                new_record.vehicle_model = apply_default(request.POST.get('vehicle_model', ""))
                new_record.vehicle_color = apply_default(request.POST.get('vehicle_color', ""))
                new_record.vehicle_type = apply_default(request.POST.get('vehicle_type', ""))

                new_record.child_involved = 'child_involved' in request.POST
                new_record.is_there_a_firearm = 'is_there_a_firearm' in request.POST
                new_record.are_there_victims = 'are_there_victims' in request.POST
                new_record.ambulance_required = 'ambulance_required' in request.POST
                new_record.priority_incident = 'priority_incident' in request.POST

                new_record.call_date = timezone.localtime(timezone.now())
                new_record.save()

                return redirect('user_area')
               
            else: #Se houver algum erro, recarrega e passa uma mensagem

                incident_types = IncidentType.objects.all().order_by('type')
                
                field_errors = []
                for field, errors in form.errors.items():
                    for error in errors:
                        field_errors.append(f"Campo {field}: {error}")
                
                if field_errors:
                    return render(request, 'create_record.html', {
                        'form': form,
                        'incident_types': incident_types,
                        'field_errors': field_errors
                    })
                else:
                    return render(request, 'create_record.html', {
                        'form': form,
                        'incident_types': incident_types,
                        'error': 'Erro ao tentar registrar!'
                    })

        except ValueError as e:

            incident_types = IncidentType.objects.all().order_by('type')
            return render(request, 'create_record.html', {
                'form': form,
                'incident_types': incident_types,
                'error': f'Ocorreu um erro ao registrar: {str(e)}'
            })
        
        except IntegrityError as e:

            incident_types = IncidentType.objects.all().order_by('type')
            return render(request, 'create_record.html', {
                'form': form,
                'incident_types': incident_types,
                'error': f'Erro de integridade: {str(e)}. Verifique se não há dados duplicados.'
            })
        
        except Exception as e:

            incident_types = IncidentType.objects.all().order_by('type')
            return render(request, 'create_record.html', {
                'form': form,
                'incident_types': incident_types,
                'error': f'Ocorreu um erro inesperado: {str(e)}'
            })


########################################################################## DESPACHAR OCORRENCIA
@login_required
def notdispatched(request):
    
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        record = get_object_or_404(Record, id=record_id)

        incident_dispatch_VTR = request.POST.get('incident_dispatch_VTR')
        response_team = request.POST.get('response_team')

        if incident_dispatch_VTR:
            record.incident_dispatch_VTR = incident_dispatch_VTR
        if response_team:
            record.response_team = response_team

        record.dispatched_by = request.user
        record.dispatch_date = timezone.now()
        record.is_dispatched = True
        record.save()

    return redirect('user_area')

########################################################################## FINALIZAR OCORRENCIA
@login_required
def notfinished(request):
    
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        record = get_object_or_404(Record, id=record_id)

        def apply_default(field_value):
            return field_value.strip() if field_value.strip() else "Não Informado"

        record.ro = 'ro' in request.POST
        record.ri = 'ri' in request.POST
        record.joint_operation = 'joint_operation' in request.POST
        record.police_district = apply_default(request.POST.get('police_district', ""))
        record.bopc = apply_default(request.POST.get('bopc', ""))
        record.police_chief_qra = apply_default(request.POST.get('police_chief_qra', ""))
                
        incident_conclusion_time = request.POST.get('incident_conclusion_time')
        if incident_conclusion_time:
            record.incident_conclusion_time = timezone.datetime.strptime(incident_conclusion_time, '%Y-%m-%dT%H:%M')
                
        record.officer_in_charge = apply_default(request.POST.get('officer_in_charge', ""))

        notification_time = request.POST.get('incident_conclusion_time')
        if notification_time:
            record.notification_time = timezone.datetime.strptime(notification_time, '%Y-%m-%dT%H:%M')
                
        record.officer_in_charge_actions = apply_default(request.POST.get('officer_in_charge_actions', ""))
        record.is_finished = True
        record.finished_by = request.user
        record.save()

    return redirect('user_area')



########################################################################## CONSULTAS
@login_required
def today_records(request):
    today = timezone.localtime(timezone.now()).date()  
    records = Record.objects.filter(call_date__date=today)
    return render(request, 'today_records.html', {'records': records})

@login_required
def all_records(request):
    records = Record.objects.filter(is_finished=True)
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