# TSTR

## Initial project
```
1. setup virtual environment >=python3.6
2. pip install -r requirements.txt
```

## Work with project
```
1. python manage.py makemigrations tstr_app
2. python manage.py migrate
3. python manage.py runserver
```

## Set up Database
```
1. sudo su - postgres
2. psql
3. CREATE DATABASE tstr;

Optionally:
4. CREATE USER myprojectuser WITH PASSWORD 'password';
5. GRANT ALL PRIVILEGES ON DATABASE tstr TO myprojectuser;
```
