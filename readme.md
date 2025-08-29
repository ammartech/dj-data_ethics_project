# Data Ethics Platform

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A comprehensive Django-based platform for managing data ethics, consent, and privacy compliance.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Management Commands](#-management-commands)
- [Internationalization](#-internationalization)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🚀 Overview

The Data Ethics Platform is a Django application designed to help organizations manage data ethics compliance, user consent, privacy policies, and data handling practices in accordance with global regulations like GDPR, CCPA, and more.

## ✨ Features

- **Consent Management**: Track and manage user consent for data processing
- **Privacy Policy Management**: Version-controlled privacy policies
- **Data Request Handling**: Process user data access and deletion requests
- **Multi-language Support**: Arabic, French, and Turkish translations
- **Automated Tasks**: Celery tasks for consent expiry notifications and report generation
- **Responsive Design**: Mobile-friendly interface
- **Admin Dashboard**: Comprehensive administration interface

## 📁 Project Structure

```
data_ethics_project/
├── data_ethics_project/          # Django project settings
│   ├── locale/                   # Translation files
│   │   ├── ar/                   # Arabic translations
│   │   ├── fr/                   # French translations
│   │   └── tr/                   # Turkish translations
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py                 # Celery configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py
├── ethics_app/                   # Main application
│   ├── management/
│   │   └── commands/            # Custom management commands
│   │       ├── clean_expired_data.py
│   │       ├── export_user_data.py
│   │       ├── generate_privacy_report.py
│   │       └── notify_consent_expiry.py
│   ├── migrations/              # Database migrations
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── consent.js
│   │       └── content.js
│   ├── templates/               # HTML templates
│   │   └── ethics_app/
│   │       ├── base.html
│   │       ├── consent_management.html
│   │       ├── data_request.html
│   │       ├── index.html
│   │       └── privacy_policy.html
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration
│   ├── apps.py
│   ├── forms.py                 # Django forms
│   ├── middleware.py            # Custom middleware
│   ├── models.py                # Data models
│   ├── tasks.py                 # Celery tasks
│   ├── tests.py                 # Application tests
│   ├── urls.py                  # App URL routing
│   └── views.py                 # View functions
├── locale/                      # Project-level translations
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
└── requirements.txt             # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/data-ethics-platform.git
   cd data-ethics-platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Compile translation files**
   ```bash
   python manage.py compilemessages
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🚦 Usage

### Starting the Application

1. Ensure all dependencies are installed
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Access the application at `http://localhost:8000`
4. Access the admin interface at `http://localhost:8000/admin`

### Management Commands

The project includes several custom management commands:

- **Clean expired data**: `python manage.py clean_expired_data`
- **Export user data**: `python manage.py export_user_data --user <user_id>`
- **Generate privacy report**: `python manage.py generate_privacy_report`
- **Notify consent expiry**: `python manage.py notify_consent_expiry`

### Celery Tasks

To use the asynchronous task processing:

1. Start Redis (required for Celery):
   ```bash
   redis-server
   ```

2. Start the Celery worker:
   ```bash
   celery -A data_ethics_project worker --loglevel=info
   ```

3. Start the Celery beat scheduler for periodic tasks:
   ```bash
   celery -A data_ethics_project beat --loglevel=info
   ```

## 🔌 API Endpoints

The application provides the following endpoints:

- `/` - Home page
- `/consent/` - Consent management interface
- `/data-request/` - Data request submission
- `/privacy-policy/` - Privacy policy viewer
- `/admin/` - Django admin interface

## 🌍 Internationalization

The application supports multiple languages:

- Arabic (ar)
- French (fr)
- Turkish (tr)

To add new translations:

1. Create or update message files:
   ```bash
   python manage.py makemessages -l <language_code>
   ```

2. Translate the text in the generated `.po` files

3. Compile the translations:
   ```bash
   python manage.py compilemessages
   ```

## 🤝 Contributing

We welcome contributions to the Data Ethics Platform! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new functionality
- Update documentation for new features
- Ensure translations are updated for any user-facing text

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Ammar Yasser Elbedwehy**  
- Email: [elbedwehyammar93@gmail.com](mailto:elbedwehyammar93@gmail.com)  
- LinkedIn: [Ammar Elbedwehy](https://www.linkedin.com/in/ammar-elbedwehy2000/)  
- GitHub: [@ammartech]([https://github.com/ammartech/])  

---

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

**⭐ Star this repo if you found it helpful!**
