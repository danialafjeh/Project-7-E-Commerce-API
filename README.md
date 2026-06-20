# َAbout Project
# 🛒 E-Commerce REST API

A fully featured E-Commerce REST API built with Django REST Framework.

This project provides a complete backend solution for an online shopping platform including user management, product catalog, shopping cart, checkout process, address management, and order tracking.

---

# 🚀 Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication (Simple JWT)
* DRF Spectacular (Swagger / OpenAPI)
* Django Filter
* RESTful API Design

---

# 🔐 Authentication

Authentication is implemented using JWT tokens.

Features:

* User Registration
* User Login
* Access Token
* Refresh Token
* Protected Endpoints
* Role-Based Permissions

---

# 👤 User Management

Features:

* User Registration
* User Profile Retrieval
* User Profile Update
* User Search
* User Ordering
* Admin User Management

Special behavior:

* A shopping cart is automatically created when a new user registers.

---

# 📦 Product Management

Features:

* Product Listing
* Product Details
* Product Creation
* Product Update
* Product Deletion
* Product Image Upload
* Product Search
* Product Filtering
* Product Ordering

Supported filters:

* Category
* Brand

Supported ordering:

* Price
* Creation Date
* Last Update Date

Supported search fields:

* Product Name
* Brand Name
* Category Name

---

# 🏷️ Categories & Brands

Products are organized using:

* Categories
* Brands

Relationships are implemented using Foreign Keys.

---

# 🛒 Shopping Cart System

Features:

* View Cart
* Add Product To Cart
* Remove Product From Cart
* Search User Carts (Admin)
* Paginated Cart Listing

Special behavior:

* Duplicate products are automatically merged.
* Product quantity is increased instead of creating duplicate cart items.

---

# 📍 Address Management

Features:

* Create Address
* Retrieve Address
* Update Address
* Delete Address
* Search Addresses
* Ordering Addresses

Users can manage multiple shipping addresses.

---

# 📑 Order Management

Features:

* Checkout
* View Orders
* Search Orders (Admin)
* Change Order Status (Admin)
* Paginated Order Listing

Supported order statuses:

* WAITING
* PREPARING
* SHIPPING
* DELIVERED
* CANCELED

---

# 💳 Checkout System

The checkout process performs:

* Shopping Cart Validation
* Address Validation
* Stock Validation
* Order Creation
* Order Item Creation
* Inventory Update: After the checkout process is completed, the stock quantity of the selected products will decrease by the quantity specified in the order.
* Cart Cleanup

Additional features:

* Atomic Database Transactions
* Historical Price Storage
* Sale Price Support
* Stock Quantity Management
  
The checkout process guarantees data consistency using:

```python
transaction.atomic()
```

---

# 📄 Order Items

Each order stores:

* Product
* Quantity
* Purchase Price

Historical pricing is preserved even if product prices change later.

---

# 📤 File Upload Support

Product images are uploaded using:

* Multipart Requests
* Form Data

Supported through:

* MultiPartParser
* FormParser

---

# 🔎 Search Functionality

Implemented using DRF SearchFilter.

Available on:

* Users
* Products
* Addresses
* Orders
* Carts

---

# 🎯 Filtering

Implemented using Django Filter Backend.

Supported product filters:

* Category
* Brand

Example:

```http
GET /products/?brand=1
GET /products/?category=2
```

---

# 📊 Ordering

Implemented using DRF OrderingFilter.

Examples:

```http
GET /products/?ordering=price
GET /products/?ordering=-created_at
```

---

# 📄 Pagination

Implemented using:

```python
PageNumberPagination
```

Available on:

* Orders
* Carts

---

# 🧩 API Architecture

This project heavily utilizes:

* ModelViewSet
* ViewSet
* Routers

Architecture distribution:

* ~90% ModelViewSet + Routers
* ~10% Custom ViewSets

This significantly reduces boilerplate code while maintaining flexibility for custom business logic.

---

# 🔒 Permissions

Permission system is implemented using:

* AllowAny
* IsAuthenticated
* IsAdminUser

Examples:

### Public Endpoints

* Product List
* Product Details
* User Registration

### Authenticated Users

* Profile Management
* Cart Management
* Checkout
* Address Management

### Administrators

* Product Management
* User Management
* Order Status Management
* Search Endpoints
* Administrative Listings

---

# 📚 API Documentation

Interactive API documentation is available through:

* Swagger UI
* OpenAPI Schema

Powered by:

```text
drf-spectacular
```

---

# ⚙️ Database

Database engine:

```text
PostgreSQL
```

The project is designed around relational database principles and uses efficient model relationships for all business entities.

---

# 🎉 Main Features Summary

✅ JWT Authentication

✅ PostgreSQL Database

✅ Product Management

✅ Shopping Cart System

✅ Checkout Workflow

✅ Order Management

✅ Address Management

✅ Image Upload

✅ Search

✅ Filtering

✅ Ordering

✅ Pagination

✅ Swagger Documentation

✅ Nested Serializers

✅ Role-Based Permissions

✅ Atomic Transactions

✅ Inventory Management

✅ Historical Price Tracking

