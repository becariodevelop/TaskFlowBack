Proyecto diseñado en django rest framework para taskflow

La base de datos correspondiente es PostgreSQL v17, es necesario crear un esquema llamado "bitacora_agencia_digital" mismo que contendrá las tablas


# Pasos para crear el entorno virtual necesario para el backend

pasos para crear el entorno virtual

pip freeze > dependencias.txt

# Crear el entorno virtual

Python -m venv venv

# Activar el entorno virtual en Windows

venv/Scripts/actívate

# Actualizar pip en el entorno virtual

python -m pip install --upgrade pip

# Ejecutar el proyecto para observar las dependencias necesarias

Python manage.py check

# Activar la ejecución de scripts en sistema Windows si es necesario
# Abrir power Shell como administrador y escribir el siguiente comando

Get-ExecutionPolicy -List

# Generará la siguiente salida: 

        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser       Undefined
 LocalMachine       Undefined

# Cambiar current user con el siguiente comando: 

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

## Ya se puede crear el entorno virtual de Python

# Ejecutar el proyecto y ver las dependencias faltantes

python manage.py check

## Instalar las dependencias

python -m pip install --upgrade pip

pip install Django==5.2.4
pip install django-cors-headers==4.7.0
pip install djangorestframework==3.16.0
pip install psycopg==3.2.9
pip install psycopg-binary==3.2.9
pip install pycparser==2.22
pip install python-dotenv==1.1.1

pip                       25.2

# Verificar 

py manage.py check

# Ejecutar migraciones

py manage.py migrate

#Ejecutar servidor de desarrollo

python manage.py runserver

# Generar archivo requirements

pip freeze > requirements.txt
