# QuickCart

QuickCart is a Django REST API skeleton for OTP-based authentication and user profile management for a commerce app.

## Features
- Phone-number based custom user model with JWT auth via SimpleJWT.
- OTP request and verification endpoints that issue 6-digit codes, valid for 5 minutes and logged to the console in development.
- Auto-creation of users on first OTP verification; profile retrieval/update for name, email, and preferred_categories.
- SQLite database by default for fast local setup; JSON-only responses via Django REST Framework.

## Requirements
- Python 3.10+ (tested with Django 3.2.25)
- pip or pipenv/poetry for dependency management
- SQLite (bundled)

## Setup
1. Create and activate a virtual environment:
   - Windows: `python -m venv .venv && .\.venv\Scripts\activate`
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies:
   `pip install "Django==3.2.25" djangorestframework djangorestframework-simplejwt`
3. Apply migrations:
   `python manage.py migrate`
4. Run the API:
   `python manage.py runserver`
5. (Optional) Create a superuser if you want admin access:
   `python manage.py createsuperuser`

## API quickstart
### Request an OTP
POST `/api/auth/request-otp/`
```json
{"phone": "+15551234567"}
```
Response: `{"message": "OTP sent"}` with the OTP printed to the console in development.

### Verify an OTP and get a token
POST `/api/auth/verify-otp/`
```json
{"phone": "+15551234567", "otp": "123456"}
```
Creates the user if missing, marks `verification_status` as `verified`, and returns:
```json
{"access": "<jwt-access-token>"}
```

### Read your profile
GET `/api/user/profile` with header `Authorization: Bearer <jwt-access-token>`
Returns the user's profile including fields like `phone`, `name`, `email`, `preferred_categories`, `verification_status`, `total_orders`, and `lifetime_value`.

### Update your profile
PUT `/api/user/profile` with the same Authorization header.
Body example:
```json
{"name": "Alex Shopper", "email": "alex@example.com", "preferred_categories": ["electronics", "groceries"]}
```
Immutable fields such as `phone`, `verification_status`, `total_orders`, and `lifetime_value` are read-only.

## Notes
- Development settings keep `DEBUG=True` and an inline `SECRET_KEY`; set environment variables and harden settings before production.
- OTPs are stored in the database and expire after 5 minutes; SMS delivery is stubbed by printing to the console.
