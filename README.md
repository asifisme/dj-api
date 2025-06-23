# xApi

Personal Portfolio & E-Commerce API Server

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

**xApi** is a modular, production-ready RESTful API server built with Django and Django REST Framework. It is designed for personal portfolios, e-commerce platforms, and content management systems. The project emphasizes security, scalability, maintainability, and developer experience.

---

## Features

- **User Authentication & Authorization:** JWT-based authentication, registration, login, and permissions management
- **Product Catalog:** CRUD for products, categories, meta tags, images, and wishlists
- **Article & Blog Management:** CRUD for articles, categories, meta tags, and images
- **Shopping Cart & Orders:** Cart, cart items, orders, and order items management
- **Payment Processing:** Stripe and PayPal integration
- **Ledger & Transactions:** Financial transaction and journal entry tracking
- **Messaging:** Real-time in-app messaging and notifications (WebSocket support)
- **Admin Tools:** User profile management, mail sending
- **Role-Based Access Control:** Fine-grained permissions for users, staff, and superusers
- **Filtering, Searching, Pagination:** Powerful query, search, and navigation tools
- **Logging:** Application, request, access, error, and security logs
- **Extensible Modular Structure:** Easily add new features or apps
- **Interactive API Docs:** Swagger and Redoc auto-generated documentation

---

## Project Structure

```
xApi/           # Django project configuration, settings, root URLs
Admin/          # Admin tools, user profile management, mail
Article/        # Article, category, meta tag, image management
Authentication/ # User authentication, registration, profile
Cart/           # Shopping cart, cart items, orders, order items
Ledger/         # Ledger and transaction management
Message/        # In-app messaging, notifications (WebSocket)
Payment/        # Payment processing (Stripe, PayPal)
Product/        # Product, category, meta tag, image, wishlist
core/           # Shared utilities, permissions, pagination, middleware
media/          # Uploaded media files (articles, product images, etc.)
logs/           # Application, request, access, error, security logs
db.sqlite3      # SQLite database (default, can be replaced)
Dockerfile      # Containerization
requirements.txt# Python dependencies
manage.py       # Django management script
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- (Optional) Docker & Docker Compose

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd xApi
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Docker (Recommended for Production)

1. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

---

## API Usage

- All endpoints are prefixed with `/api/v1/`
- Interactive API docs available at `/swagger/` (Swagger UI) and `/redoc/` (Redoc)
- Authentication required for write operations (JWT)
- Each app provides RESTful endpoints (see app-specific docs or browse `/swagger/`)

### Example Endpoints

- **Authentication:** `/api/v1/auth/login/`, `/api/v1/auth/register/`
- **Products:** `/api/v1/product/`, `/api/v1/product-category/`, `/api/v1/wishlist-product/`
- **Articles:** `/api/v1/articles/`, `/api/v1/art-categories/`
- **Cart:** `/api/v1/cart/`, `/api/v1/order/`
- **Payments:** `/api/v1/payments/`, `/api/v1/paypal/`, `/api/v1/stripe/success/`
- **Ledger:** `/api/v1/ledger/`
- **Messaging:** `/api/v1/message/`

### Filtering, Search, and Pagination

- **Filtering:** `?q=<uid>` (e.g., `/api/v1/product/?q=1234`)
- **Search:** `?search=keyword` (e.g., `/api/v1/articles/?search=django`)
- **Pagination:** `?page=2` (responses include `count`, `next`, `previous`, `results`)

---

## Interactive API Documentation

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Testing

Run all tests:

```bash
python manage.py test
```

---

## Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

Please follow PEP8 and write clear, well-documented code. Add tests for new features.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions, issues, or feature requests, please open an issue or contact the maintainer.

---
