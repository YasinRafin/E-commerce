# Flask E-commerce Backend

A Flask-based e-commerce backend system with user authentication, product management, shopping cart, and order processing capabilities.

## Features

- User Authentication (JWT)
  - Registration
  - Login
  - Protected endpoints
  - Logout
- Product & Category Management
  - CRUD operations
  - Filtering & Pagination
- Shopping Cart System
  - Add/Update/Remove items
  - View cart with total
- Checkout & Order Management
  - Place orders
  - Stock management
- Pagination & Filtering
  - By category, price, availability

## Setup Instructions
1. Clone the repository
   ```
   git clone git@github.com:YasinRafin/Registration_API.git
   cd Registration_API
   code .
   ``` 

2. Create a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with:
   ```
   DATABASE_URL=postgresql://user:password@localhost/ecommerce
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```
