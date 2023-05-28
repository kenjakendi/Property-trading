# Repository setup
1. Install new Python interpreter.
2. Create a venv:
```
python -m venv ./venv
```
3. Activate venv:
```
# On Linux:
source ./venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```
4. Install necessary libraries:
```
python -m pip install -r requirements.txt
```
5. Apply migrations (if needed):
```
python manage.py makemigrations
python manage.py migrate
```
6. Start server:
```
python manage.py runserver
```
