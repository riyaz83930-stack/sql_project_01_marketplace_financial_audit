
-- SURFACE LEVEL EXPLORATION 

SELECT * FROM customers;

SELECT * FROM orders;

SELECT * FROM order_items;

SELECT * FROM payments;

SELECT * FROM products;

SELECT * FROM vendor_payouts;

SELECT * FROM vendors;




SELECT
COUNT(*) AS orders
FROM orders;

SELECT
COUNT(*) AS paymt
FROM payments;

SELECT
COUNT(*) AS vend_pay
FROM vendor_payouts;

SELECT
COUNT(*) AS vendors
FROM vendors;

SELECT
COUNT(*) AS products
FROM products;

SELECT
COUNT(*) AS orderitems
FROM order_items;

SELECT
COUNT(*) AS customerss
FROM customers;

-- FINDING NULL

SELECT
SUM( email IS NULL) ,
SUM( signup_date IS NULL) 
FROM customers;

SELECT
SUM( order_id IS NULL) ,
SUM( customer_id IS NULL),
SUM( order_date IS NULL),
SUM( status IS NULL),
SUM( total_amount IS NULL)    
FROM orders;


SELECT

SUM( product_id IS NULL),
SUM( item_price IS NULL),
SUM( quantity IS NULL),
SUM( order_id IS NULL)    
FROM order_items;

SELECT

SUM( commission_rate IS NULL)    
FROM vendors
WHERE status !='Suspended';

SELECT
SUM( order_id IS NULL) ,
SUM( payment_status IS NULL),
SUM( amount_paid IS NULL),
SUM( payment_date IS NULL),
SUM( payment_id IS NULL)    
FROM payments;

SELECT
SUM( order_id IS NULL) ,
SUM( customer_id IS NULL),
SUM( order_date IS NULL),
SUM( status IS NULL),
SUM( total_amount IS NULL)    
FROM orders;

SELECT

SUM( vendor_id IS NULL),
SUM( price IS NULL),
SUM( product_name IS NULL),
SUM(product_id IS NULL)    
FROM products;

SELECT
SUM( period_covered IS NULL) ,
SUM( vendor_id IS NULL),
SUM( payout_id IS NULL),
SUM( payout_date IS NULL),
SUM( payout_amount IS NULL)    
FROM vendor_payouts;


-- FINDING ORDER STATUS ANOMALY

SELECT
DISTINCT(status)
FROM orders;


-- FINDING AMOUNT/QUANTITY COLUMN ANOMALY

SELECT
COUNT(*)
FROM orders
WHERE total_amount<=0;


SELECT
COUNT(*) 
FROM order_items
WHERE item_price<=0 OR 
quantity<=0;


SELECT
COUNT(*)
FROM payments
WHERE amount_paid<=0;


SELECT
COUNT(*)
FROM products
WHERE price<=0;

SELECT
COUNT(*)
FROM vendor_payouts
WHERE payout_amount<=0;

SELECT
COUNT(*)
FROM vendors
WHERE total_amount<=0;
