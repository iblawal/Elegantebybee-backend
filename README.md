# ElegantByBee Backend

ElegantByBee Backend is the server-side application that powers the ElegantByBee event planning platform. It handles user requests, business logic, payments, and data management for the frontend application.

This backend is built to support a real-world event planning business, including service management, quote requests, and secure payment processing.

---

## Features

* RESTful API built with Django
* User request and quote handling system
* Payment processing integration
* AI chatbot support for user assistance
* Secure backend architecture
* Scalable and production-ready structure

---

## Tech Stack

Backend Framework

* Python
* Django

Database

* PostgreSQL

Payments

* Stripe (for international transactions)
* Paystack (for local transactions)

Other Integrations

* AI chatbot system

---

## Project Purpose

This backend serves as the core engine of the ElegantByBee platform. It manages client interactions, processes payments, stores business data, and ensures smooth communication between the frontend and external services.

---

## Installation

Clone the repository

git clone https://github.com/iblawal/Elegantbybee-backend.git

Move into the project directory

cd Elegantbybee-backend

Create a virtual environment

python -m venv venv

Activate the virtual environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file and add:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_postgresql_connection
STRIPE_SECRET_KEY=your_stripe_key
PAYSTACK_SECRET_KEY=your_paystack_key

---

## Running the Server

Apply migrations

python manage.py migrate

Start the server

python manage.py runserver

Then open:

http://127.0.0.1:8000

---

## Future Improvements

* Admin dashboard for managing bookings
* Email notification system
* Booking and scheduling system
* API rate limiting and security enhancements
* Deployment with Docker

---

## Author

Lawal Ibrahim

Backend developer focused on building scalable APIs and real-world business solutions.
