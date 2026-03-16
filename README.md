# AIAPI

A Django-based REST API for AI model management and user interaction. This project provides a comprehensive backend for handling user authentication, API key management, rate limiting, and AI model request processing.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [License](#license)

## ✨ Features

- **User Authentication**: Secure user registration and login with password hashing
- **API Key Management**: Generate and manage API keys for programmatic access
- **Rate Limiting**: Configurable rate limits per user (requests per minute/day)
- **Multi-Model Support**: Support for various AI models (e.g., Gemma3)
- **Request Tracking**: Log all API requests with prompt, response, and token usage
- **Usage Statistics**: Track user request counts and token consumption
- **Django REST Framework**: Modern REST API with serializers and viewsets
- **Custom User Model**: Extended user model with custom authentication

## 📁 Project Structure

```
AIAPI/
├── backend/
│   ├── User/                    # User management app
│   │   ├── models.py           # User model and authentication
│   │   ├── serializer.py       # User and login serializers
│   │   ├── CustomUserManager.py # Custom user manager
│   │   ├── admin.py            # Django admin configuration
│   │   ├── apps.py             # App configuration
│   │   └── migrations/         # Database migrations
│   ├── API/                     # API endpoints app
│   │   ├── views.py            # API views/endpoints
│   │   ├── urls.py             # URL routing
│   │   └── apps.py             # App configuration
│   ├── communication/          # Communication/request handling
│   │   ├── migrations/         # Database migrations
│   │   └── apps.py             # App configuration
│   ├── models.py               # Shared data models
│   ├── settings.py             # Django settings
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
├── README.md                   # This file
└── env/                        # Virtual environment (not committed)
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YanisBelkacemi/AIAPI.git
   cd AIAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Django settings**
   - Update `backend/settings.py` with your database configuration
   - Set appropriate SECRET_KEY and DEBUG settings

5. **Run migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

## ⚙️ Configuration

### Database
Configure your database in `backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # or postgresql, mysql, etc.
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Environment Variables
Create a `.env` file in the project root with:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

## 🚀 Usage

### Start the Development Server
```bash
cd backend
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### Create a Superuser
```bash
python manage.py createsuperuser
```

### Admin Panel
Access the Django admin at `http://localhost:8000/admin/`

## 📡 API Endpoints

### User Management
- `POST /api/register` - Register a new user
- `POST /api/login` - User login

### API Endpoints
- `GET /api/` - Get API information
- `POST /api/request` - Submit an AI model request

## 🗄️ Models

### Users
- `username` - Unique username
- `email` - User email address
- `password` - Hashed password
- `is_active` - Account status
- `created_at` - Account creation timestamp
- `UserInputID` - Unique input identifier
- `UserOutputID` - Unique output identifier

### ApiKeys
- `user` - Foreign key to Users
- `key_prefix` - Key prefix for identification
- `key_hash` - Hashed API key
- `name` - Key name/description
- `revoked` - Revocation status
- `is_active` - Active status
- `created_at` - Creation timestamp
- `last_used` - Last usage timestamp

### Models (AI Models)
- `name` - Model name (e.g., Gemma3)
- `provider` - AI provider
- `version_model` - Model version
- `max_tokens` - Maximum token limit
- `created_at` - Creation timestamp

### Requests
- `user` - Foreign key to Users
- `api_key` - Foreign key to ApiKeys
- `model` - Foreign key to Models
- `prompt` - User prompt/query
- `response` - AI response
- `tokens_used` - Tokens consumed
- `status` - Request status
- `created_at` - Request timestamp

### RateLimits
- `api_key` - Foreign key to ApiKeys
- `requests_per_minute` - RPM limit
- `requests_per_day` - Daily limit

### UsageStats
- `user` - Foreign key to Users
- `date` - Usage date
- `requests_count` - Number of requests
- `tokens_used` - Total tokens consumed

## 📦 Dependencies

Key dependencies include:
- Django 5.2.12
- Django REST Framework
- python-nanoid (for ID generation)
- Python standard library modules

## 📝 Notes

- The project uses Django's custom user model for extended functionality
- Password hashing is handled by Django's built-in authentication
- User IDs are generated using the nanoid library for uniqueness


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Yanis Belkacemi**
- GitHub: [@YanisBelkacemi](https://github.com/YanisBelkacemi)
