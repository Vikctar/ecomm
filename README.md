# Django E-commerce API

A comprehensive Django REST API service for e-commerce with hierarchical categories, order management, and automated notifications.

## Features

- **Hierarchical Categories**: Support for unlimited depth category trees
- **Product Management**: Full CRUD operations with category associations
- **Order Management**: Complete order processing with inventory management
- **Authentication**: OAuth2/OpenID Connect integration
- **Automated Notifications**: SMS and email notifications for orders
- **Testing**: Unit tests with coverage reporting
- **CI/CD**: GitHub Actions pipeline
- **Containerization**: Docker and Kubernetes support

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Docker (optional)
- Linux (preferred)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecomm
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment setup:
```bash
cp .env.example .env
```

5. Database setup:
```bash
python manage.py migrate
python manage.py setup_categories
python manage.py createsuperuser
```

6. Run the server:
```bash
python manage.py runserver
```

7. Start Celery worker (preferably in another terminal:
```bash
celery -A ecommerce worker --loglevel=info
```

## API Endpoints

### Authentication
- `POST /auth/token/` - Get access token
- `POST /auth/authorize/` - OAuth2 authorization

### Categories
- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create category
- `GET /api/v1/categories/{slug}/` - Get category details
- `GET /api/v1/categories/{slug}/average_price/` - Get average price for category

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{slug}/` - Get product details
- `GET /api/v1/products/?category={slug}` - Filter by category

### Orders
- `GET /api/v1/orders/` - List user orders
- `POST /api/v1/orders/create_order/` - Create new order
- `GET /api/v1/orders/{id}/` - Get order details

## Testing

Run tests and checks using tox:
```bash
tox
```

## Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_categories
```

## Configuration

### OAuth2 Setup

1. Create OAuth2 application in Django admin
2. Configure client credentials in your frontend application
3. Use authorization code flow for user authentication

### SMS Configuration

1. Sign up for Africa's Talking account
2. Get API key and username
3. Configure in environment variables

### Email Configuration

1. Configure SMTP settings in environment
2. Using mailtrap for testing purposes

## Architecture

### Models
- **Category**: Hierarchical category structure using self-referencing foreign key
- **Product**: Products with multiple category associations
- **Customer**: User profile extension
- **Order/OrderItem**: Order management with line items

### Key Features
- **KISS/DRY Principles**: Clean, maintainable code structure
- **Async Processing**: Celery for background tasks
- **Comprehensive Testing**: Unit tests with high coverage
- **Scalable Architecture**: Ready for horizontal scaling
