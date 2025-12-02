<div align="center">

# GoPizza

### Django-Based Online Food Ordering Platform

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

## Overview

GoPizza is a comprehensive Django web application for online food ordering and restaurant management. The platform provides a complete e-commerce solution with customer-facing features and administrative tools for managing products, orders, and users.

**Key Capabilities:**
- Full-featured product catalog with search and filtering
- Shopping cart and checkout system
- Order management with status tracking
- PDF receipt generation
- Admin dashboard for business operations
- User authentication and authorization

---

## Features

### Customer Interface

**Product Browsing**
- Product catalog with category filtering
- Real-time search functionality
- Product detail pages with images and descriptions
- Availability status display

**Shopping Cart**
- Add products with custom quantities
- View cart total and item breakdown
- Remove items from cart
- Persistent cart storage per user

**Order Management**
- Checkout with delivery address and phone number
- Order confirmation and tracking
- Order history view
- PDF receipt download

**User Accounts**
- Registration with email verification
- Secure login/logout
- Profile information management

### Administrative Interface

**Product Management**
- Create, read, update, delete (CRUD) operations
- Image upload and management
- Category assignment
- Availability toggle

**Order Management**
- View all orders with filtering options
- Update order status (Pending, Accepted, Rejected, Delivered)
- Access customer information
- View order details and totals

**User Management**
- View all registered users
- Reset user passwords
- View user registration dates
- Distinguish between admin and regular users

---

## Technology Stack

**Backend**
- Django 5.0+
- Python 3.11+
- SQLite (development database)
- Django REST Framework (API ready)

**Additional Libraries**
- ReportLab (PDF generation)
- Pillow (image processing)

**Deployment**
- Docker & Docker Compose
- Gunicorn (production server)

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ivasx/GoPizza.git
cd GoPizza

# Build and start containers
docker-compose up --build

# Access application at http://localhost:8000
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/ivasx/GoPizza.git
cd GoPizza

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Access the application at `http://localhost:8000`

---

## Project Structure

```
GoPizza/
├── GoPizza/                  # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── polls/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View controllers
│   ├── forms.py             # Form definitions
│   ├── urls.py              # URL patterns
│   ├── admin.py             # Admin panel config
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── admin/
│   │   └── polls/
│   └── migrations/          # Database migrations
│
├── media/                    # User uploads
│   └── fonts/               # Fonts for PDF generation
├── static/                   # Static files (CSS, JS)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── manage.py                # Django management script
```

---

## Database Schema

### Models

**Category**
- `name` - Category name

**Product**
- `name` - Product name
- `description` - Product description
- `price` - Product price
- `image` - Product image
- `category` - Foreign key to Category
- `available` - Availability status
- `created_at`, `updated_at` - Timestamps

**Cart**
- `user` - One-to-one with User
- `created_at`, `updated_at` - Timestamps

**CartItem**
- `cart` - Foreign key to Cart
- `product` - Foreign key to Product
- `quantity` - Item quantity

**Order**
- `user` - Foreign key to User
- `address` - Delivery address
- `phone` - Contact phone
- `status` - Order status (pending/accepted/rejected/delivered)
- `created_at`, `updated_at` - Timestamps

**OrderItem**
- `order` - Foreign key to Order
- `product` - Foreign key to Product
- `price` - Price at time of order
- `quantity` - Item quantity

---

## URL Structure

### Public URLs
- `/` - Product list (homepage)
- `/product/<id>/` - Product detail page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### Authenticated User URLs
- `/cart/` - Shopping cart
- `/cart/add/` - Add to cart
- `/cart/remove/<id>/` - Remove from cart
- `/order/create/` - Create order
- `/orders/` - Order list
- `/order/<id>/` - Order detail
- `/order/<id>/pdf/` - Download PDF receipt

### Admin URLs (Superuser only)
- `/admin/products/` - Product management
- `/admin/products/create/` - Create product
- `/admin/products/<id>/edit/` - Edit product
- `/admin/products/<id>/delete/` - Delete product
- `/admin/orders/` - Order management
- `/admin/orders/<id>/status/` - Update order status
- `/admin/users/` - User management
- `/admin/users/<id>/change-password/` - Change user password

---

## Configuration

### Settings

Key configurations in `GoPizza/settings.py`:

```python
# Security
SECRET_KEY = 'your-secret-key'  # Change in production
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['*']  # Configure for production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static and Media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication
LOGIN_REDIRECT_URL = 'polls:product_list'
LOGOUT_REDIRECT_URL = 'polls:product_list'
```

### Docker Configuration

`docker-compose.yml`:
```yaml
version: '3.9'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./media:/app/media
    environment:
      - DEBUG=1
```

---

## Usage

### For Customers

1. Browse products on the homepage
2. Use search or category filters to find items
3. Click on products to view details
4. Register or login to add items to cart
5. Review cart and proceed to checkout
6. Enter delivery information
7. Confirm order and download PDF receipt

### For Administrators

1. Login with superuser credentials
2. Access admin panel via navigation menu
3. Manage products (add, edit, delete)
4. View and update order statuses
5. Manage user accounts
6. Reset user passwords if needed

---

## Security Features

- CSRF protection enabled
- Password hashing with Django's default algorithm
- Authentication required for cart and orders
- Role-based access control (superuser checks)
- SQL injection prevention via Django ORM
- XSS protection through template auto-escaping

**Production Checklist:**
- Generate new SECRET_KEY
- Set DEBUG = False
- Configure ALLOWED_HOSTS properly
- Use PostgreSQL or MySQL for production
- Enable HTTPS
- Configure static file serving

---

## PDF Generation

The application includes PDF receipt generation using ReportLab. Receipts include:
- Order number and date
- Customer information
- Delivery address and phone
- Order status
- Itemized product list with quantities and prices
- Total amount

Custom fonts (DejaVu Sans) are supported for internationalization.

---

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

---

## Deployment

### Production Recommendations

1. Use PostgreSQL or MySQL instead of SQLite
2. Configure environment variables for sensitive data
3. Set up proper static file serving (nginx, WhiteNoise)
4. Enable HTTPS with SSL certificates
5. Configure email backend for notifications
6. Set up regular database backups
7. Implement logging and monitoring

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

Please ensure code follows PEP 8 standards and includes appropriate documentation.

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Author

**ivasx**


**Available for:** Freelance Projects | Contract Work | Full-time Opportunities

---

## Support

For issues or questions:
- Open an issue on [GitHub Issues](https://github.com/yourusername/GoPizza/issues)
- Contact via email for commercial inquiries

---

<div align="center">

**GoPizza** - Professional Django E-Commerce Platform

Copyright © 2025. All rights reserved.

</div>