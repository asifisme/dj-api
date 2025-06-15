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

xApi is a modular RESTful API server built with Django and Django REST Framework. It powers personal portfolios, e-commerce platforms, and content management systems. The project supports user authentication, product management, article publishing, cart and payment processing, and more, following best practices for security, scalability, and maintainability.

---

## Features

- **User Authentication & Authorization**: Secure registration, login, and permissions management
- **Product Catalog**: Manage products, categories, and meta tags with full CRUD support
- **Article & Blog Management**: Publish and organize articles and blog posts
- **Shopping Cart & Orders**: Add to cart, checkout, and order tracking
- **Payment Processing**: Integrate with payment gateways for seamless transactions
- **Role-Based Access Control**: Fine-grained permissions for users, staff, and superusers
- **Filtering, Searching, and Pagination**: Efficiently query and navigate large datasets
- **Extensible Modular Structure**: Easily add new features or apps as your project grows

---

## Project Structure

- `xApi/` – Django project configuration and settings
- `Article/` – Article and blog management
- `Product/` – Product, category, and meta tag management
- `Authentication/` – User authentication and profile management
- `Cart/` – Shopping cart and order logic
- `Payment/` – Payment processing
- `Ledger/` – Ledger and transaction management
- `core/` – Shared utilities, permissions, pagination, and middleware
- `fixtures/` – Data import/export scripts
- `media/` – Uploaded media files
- `logs/` – Application logs

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

### Docker (Optional)

1. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

---

## API Usage

- All endpoints are prefixed with `/api/`
- Authentication is required for write operations
- See each app's documentation for detailed endpoint information

### Filtering, Search, and Pagination

- **Filtering:** Use the `q` parameter to filter by unique identifiers (e.g., `/api/products/?q=<uid>`)
- **Search:** Use the `search` parameter to search across key fields (e.g., `/api/products/?search=sample`)
- **Pagination:** Use the `page` parameter to navigate results (e.g., `/api/products/?page=2`)
- Responses include metadata: `count`, `next`, `previous`, and `results`

---

## Testing

Run all tests:

```bash
python manage.py test
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions, issues, or feature requests, please open an issue or contact the maintainer.
