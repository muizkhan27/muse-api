# musetax-api
### Setup
- The API is built using Django Rest Framework (DRF)
- Make sure you have python 3.10+ installed in your system
- Clone the repo on your local
- Navigate to the directory containing manage.py
- Create a python virtual environment:
```
python3 -m venv venv
```
- Activate the virtual environment:
```
source venv/bin/activate
```
- Install requirements:
```
pip install -r requirements.txt
```
- Ask a member for the environment variables mentioned in `.env.example`
- Create a `.env` file in directory where settings.py lies and place the env variables there
- Create a postgres database on your local and replace the following environment variables in the `.env` file
```
check .env.example file for env variable names
```
- Run migrations using
```
python manage.py migrate
```
- Run the server using:
```
python manage.py runserver
```
- The server is up now on http://127.0.0.1:8000
