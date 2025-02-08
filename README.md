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
   git clone git@github.com:YasinRafin/E-commerce.git
   cd E-commerce
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
## API Endpoints Checking:

1. Authentication:
   - Registration(POST): `http://127.0.0.1:5000/auth/register`
     ```
        {
            "email":
            "name":
            "password":
        }
     ```
   - Login(POST): `http://127.0.0.1:5000/auth/login`
     ```
       {
          "email":
          "password":
       }
     ```
     Will generate an access token
   - Logout(POST): `http://127.0.0.1:5000/auth/logout`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
2. Cart:
   - Get all cart items(GET): `http://127.0.0.1:5000/cart`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
   - Post cart item(POST): `http://127.0.0.1:5000/cart`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     {
        "product_id":,
        "quantity":
     }
     ```
   - Update cart item(PUT): `http://127.0.0.1:5000/cart/<int:cart_item_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
      {
          "quantity":
      }
     ```
   - Delete cart item(DELETE): `http://127.0.0.1:5000/cart/<int:cart_item_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     
     ```
3. Products:
   - Add products(POST): `http://127.0.0.1:5000/products`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     {
          "name":
          "description":
          "price":
          "stock":
          "category_id":
      }
     ```
   - Get all product details(GET): `http://127.0.0.1:5000/products`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```

   - Update any Product details(PUT):  `http://127.0.0.1:5000/products/<int:product_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
         {
          "name":
          "description":
          "price":
      
        }
    ```
  - Delete any product(DELETE): `http://127.0.0.1:5000/products/<int:product_id>`
    ```
    Must provide access token from login in Authorization -> Bearer Token
    
    ```
4. Category:
   - Create category(POST):`http://127.0.0.1:5000/categories`
     ```
     Must provide access token from login in Authorization -> Bearer Token
        {
            "name":
        }
     ```
   - Get all categories(GET): `http://127.0.0.1:5000/categories`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
   - Get category by id(GET): `http://127.0.0.1:5000/categories/<int:category_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
   - Update a category(PUT): `http://127.0.0.1:5000/categories/<int:cateogory_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
         {
            "name":"Pajamas"
         }
     ```
   - Delete a category(DELETE): `http://127.0.0.1:5000/categories/<int:category_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
5. Order:
   - Create a order(POST): `http://127.0.0.1:5000/orders`
     ```
     Must provide access token from login in Authorization -> Bearer Token
        {
            "shipping_address":"6/D, road-23, house-39/40"
        }
     ```
   - Get all orders(GET): `http://127.0.0.1:5000/orders`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
   - Get order by id(GET): `http://127.0.0.1:5000/orders/<int:order_id>`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
   - Cancel a order(POST): `http://127.0.0.1:5000/orders/<int:order_id>/cancel`
     ```
     Must provide access token from login in Authorization -> Bearer Token
     ```
