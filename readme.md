# 🍉 HydroMelon API

An intelligent API built with **Django 4.2** and **Python 3.12** to predict the **ripeness level of melon fruit**. Designed for integration with a mobile app to assess melon ripeness in real-time.

## 🚀 Features

- 🔐 User registration & authentication (JWT)
- 🧠 Ripeness level prediction endpoint
- 📊 Fast-RCNN model integration
- 🗃️ Prediction logging & backup
- 🛡️ API Key protection for secured access

## ⚙️ Tech Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- mysql
- JWT Authentication

## 🧪 Local Installation

```bash
git clone git@github.com:fkihai/hydromelon.git
cd hydromelon

# Create virtual environment
python -m venv .djenv
source .djenv/bin/activate  # On Windows: .djenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Run development server
python manage.py runserver
````

## 🔐 API Key Setup (Optional)

In `settings.py`, add:

```python
API_KEY = "your_secret_api_key"
```

Then send the key in request headers:

```
X-API-KEY: your_secret_api_key
```

## 📬 API Endpoints

| Endpoint        | Method | Description            |
| --------------- | ------ | ---------------------- |
| `/api/register` | POST   | Register a new user    |
| `/api/login`    | POST   | Login & retrieve token |
| `/api/predict`  | POST   | Predict melon quality  |
