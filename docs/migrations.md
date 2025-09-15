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