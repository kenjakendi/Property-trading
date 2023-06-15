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

5. Create folder 'conf' and add 'cfg.conf' with following structure:

```
[APP_CONF]
ganache_url = 
contract_address = 
moralis_api_key =
```

6. Create folders 'media/property_images' for storing property images on server.


7. Apply migrations (if needed):
```
python manage.py makemigrations
python manage.py migrate
```

8. Start server:
```
python manage.py runserver
```
