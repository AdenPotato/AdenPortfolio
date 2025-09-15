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