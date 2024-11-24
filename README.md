## Sobre
Projeto em desenvolvimento que consiste em uma aplicação web para criação, consultas e gerenciamento de registros de ocorrências policiais.
As principais tecnologias utilizadas são os frameworks Django (5.1.2) e Bootstrap (5.3.3).

## Execução em Linux
- Faça download e extração dos arquivos
- Acesse a pasta pelo terminal e execute os seguintes comandos:
     - python3 -m venv .venv
     - source .venv/bin/activate
     - pip install -r requirements.txt
     - python3 manage.py makemigrations
     - python3 manage.py migrate
     - python3 manage.py createsuperuser
     - python3 manage.py runserver
- No navegador, acesse o endereço http://127.0.0.1:8000/
- Ao terminar de utilizar, aperte Ctrl + C no terminal e execute o comando deactivate


## Execução em Windows
- Necessário ter o python instalado (https://www.python.org/downloads/windows/)
- Faca o download e extração dos arquivos desse repositório
- Acesse a pasta pelo terminal* e execute os seguintes comandos:
	- python -m venv venv
	- .\venv\scripts\activate
	- pip install -r requirements.txt
	- python manage.py makemigrations
	- python manage.py migrate
	- python manage.py createsuperuser
 - python manage.py shell
 - from report.scripts.populate_incident_types import populate_incident_types
	- python manage.py runserver
- No navegador, acesse o endereço http://127.0.0.1:8000/
- Ao terminar de utilizar, aperte Ctrl + C no terminal e execute o comando deactivate




*Note que, ao extrair, pode ser que duas pastas com o mesmo nome sejam criadas. O caminho correto onde os comandos devem ser executados seria algo como C:\Users\nome\Downloads\GCM-main\GCM-main


