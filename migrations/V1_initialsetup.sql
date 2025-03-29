-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(250) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(250) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Insert initial data
INSERT INTO users (fio, email, password, is_admin) 
VALUES 
    ('Admin', 'admin@shop.ru', 'QWEasd123', TRUE),
    ('User', 'user@shop.ru', 'password', FALSE);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
);

INSERT INTO products(name, description, price)
VALUES 
    ('Product name 1', 'Product description 1', 100),
    ('Product name 2', 'Product description 2', 200);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    products INTEGER[] NOT NULL,
    order_price INTEGER NOT NULL
);

CREATE TABLE user_2_cart(
    id INTEGER PRIMARY KEY NOT NULL,
    product_id INTEGER NOT NULL,
    name VARCHAR(250) NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
);

CREATE TABLE invalidtoken(
    token TEXT,
    exp BIGINT NOT NULL
);