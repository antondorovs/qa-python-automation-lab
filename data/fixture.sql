-- Intentionally imperfect e-commerce data for QA checks.
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    status TEXT NOT NULL,
    amount NUMERIC NOT NULL
);
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    status TEXT NOT NULL
);

INSERT INTO users VALUES
    (1, 'Anna Smith', 'anna@example.com'),
    (2, 'Brian Miller', 'brian@example.com'),
    (3, 'Alex Smith', 'ANNA@example.com');
INSERT INTO orders VALUES
    (1, 1, 'PAID', 120.50),
    (2, 2, 'PAID', 35.00),
    (3, 99, 'NEW', 50.00),
    (4, 3, 'NEW', -10.00);
INSERT INTO payments VALUES
    (1, 1, 'SUCCESS');
