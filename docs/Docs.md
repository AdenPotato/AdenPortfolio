# Admin
Admin doesn't work instantly. First create a super user in manage.py
```python
python3 manage.py createsuperuser
```

asks for username, email, and password. - now can login

To register student model in admin panel you put this in admin.py
```python
from django.contrib import admin
from portfolio_app.models import Student


admin.site.register(Student)
```

# migrations
migrations from [Here](https://docs.djangoproject.com/en/5.2/topics/migrations/)
Migrations are simple as to migrate a model you can do it with runnign commands from manage.py

```python
python3 manage.py makemigrations
```
- that makes the actual migrations for the models, no matter if they are removed
or added

```python
python3 manage.py migrate
```
That does the actual migrations into the app

# superuser

create the super user with this command, asks for stuff that is needed for user

```bash
python3 manage.py createsuperuser
```