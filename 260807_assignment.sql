-- 문항1
-- 요구사항1
CREATE DATABASE shopping_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE shopping_db;

-- 요구사항2
CREATE TABLE tb_users(
    user_id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id)
);

-- 요구사항3
CREATE TABLE tb_products(
    product_id INT AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    price INT NOT NULL DEFAULT 0,
    stock_quantity INT NOT NULL DEFAULT 0,
    PRIMARY KEY(product_id)
);

-- 요구사항4
ALTER TABLE tb_users ADD COLUMN phone VARCHAR(20);

-- 문항2
-- 요구사항1
INSERT INTO tb_users(username, email, phone)
    VALUES('김유비', 'yoobee@naver.com', '010-1111-1111'),
        ('이관우', 'guanwoo@naver.com', '010-2222-2222'),
        ('최장비', 'jangbee@google.com', '010-3333-3333');

-- 요구사항2
INSERT INTO tb_products(product_name, price, stock_quantity)
    VALUES
        ('무선 마우스', 25000, 50),
        ('기계식 키보드', 89000, 30),
        ('4K 모니터', 350000, 10),
        ('USB 허브', 15000, 100);
INSERT INTO tb_users(username, email, phone)
    VALUES
        ('김철수', 'chulsoo@test.com', '010-5555-5555');

-- 요구사항3
SELECT *
FROM tb_users
WHERE email = 'chulsoo@test.com';

UPDATE tb_users
SET phone = '010-1234-5678'
WHERE email = 'chulsoo@test.com';

-- 요구사항4
SELECT *
FROM tb_products
WHERE product_name = 'USB 허브';

DELETE
FROM tb_products
WHERE product_name = 'USB 허브';

-- 문항3
-- 요구사항1
SELECT DISTINCT product_name, stock_quantity
FROM tb_products;

-- 요구사항2
SELECT product_name, price
FROM tb_products
ORDER BY price DESC;

-- 요구사항3
SELECT *
FROM tb_users
ORDER BY user_id DESC
LIMIT 2;
