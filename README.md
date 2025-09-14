# Dataharis Backend API

This is the official Django REST API backend for **Dataharis**, a platform that [describe the goal].

## 🚀 Features
# Remission Backend API

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Django Version](https://img.shields.io/badge/django-4.x-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()

## Overview

Remission is a backend API project built with Django and Django REST Framework. It offers:

- **JWT-based Authentication**: Secure user authentication using JSON Web Tokens.
- **User Management**: Registration, login, logout, password reset, and email verification.
- **Stripe Donation Integration**: Users can make one-time or recurring donations via Stripe.
- **Blog Functionality**: CRUD APIs for blogs and posts.
- **Privacy & Terms APIs**: Endpoints to serve privacy policy, terms & conditions, and trust & safety info.
- **Role-based Access Control**: Different access permissions for users and admins.
- **Email Notifications**: OTP verification and password reset via SMTP.

---

## Features

| Feature                    | Description                                  |
|----------------------------|----------------------------------------------|
| JWT Authentication         | Login/logout, token refresh, and cookie support |
| Email OTP Verification     | Secure account verification via email OTP   |
| Password Reset             | Secure forgot/reset password workflow        |
| Stripe Donation Gateway    | Integration with Stripe for payments         |
| Blog Management            | Create, read, update, delete blog posts      |
| Privacy & Terms API        | Fetch privacy policy and terms documents      |
| Clean and Modular Code     | Easy to maintain and extend                   |

---

## Tech Stack

- Python 3.9+
- Django 4.x
- Django REST Framework
- Simple JWT
- Stripe API
- PostgreSQL / SQLite (configurable)
- SMTP Email Backend (for OTP and notifications)

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/remission-backend.git
   cd remission-backend

## 🛠️ Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- Simple JWT
- Stripe API

## 📦 Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/TechbyAbrar/Dataharis-Backends-API.git
cd Dataharis-Backends-API
Create virtual environment and install dependencies:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Create .env file:

env
Copy
Edit
SECRET_KEY=your-secret
DEBUG=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
Run migrations:

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Run server:

bash
Copy
Edit
python manage.py runserver

---

## ✅ 4. Add a `requirements.txt`

Run this to auto-generate:

```bash
pip freeze > requirements.txt
