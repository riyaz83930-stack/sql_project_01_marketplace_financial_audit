--  Referential Integrity Audit
-- ═══════════════════════════════════════

-- FINDING ORPHAN ORDERS

SELECT
	COUNT(*)
FROM orders o
LEFT JOIN customers c
	ON o.customer_id=c.customer_id
WHERE c.customer_id IS NULL;

-- FINDING ORPHAN order_id IN ORDER-ITEMS 

SELECT
	COUNT(*)
FROM order_items oi
LEFT JOIN orders o
	ON oi.order_id=o.order_id
WHERE o.order_id IS NULL;

-- FINDING ORPHAN prduct_id IN ORDER-ITEMS 

SELECT
	COUNT(*)
FROM order_items oi
LEFT JOIN products p
	ON oi.product_id=p.product_id
WHERE p.product_id IS NULL;

-- FINDING ORPHAN vendor_id IN PRODUCTS

SELECT
	COUNT(*)
FROM products p
LEFT JOIN vendors v
	ON p.vendor_id=v.vendor_id
WHERE v.vendor_id IS NULL;

-- FINDING ORPHAN order_id IN PAYMENTS

SELECT
	COUNT(*)
FROM payments p
LEFT JOIN orders o
	ON p.order_id=o.order_id
WHERE o.order_id IS NULL;

-- FINDING ORPHAN vendor_id IN VENDOR PAYOUTS

SELECT
	COUNT(*)
FROM vendor_payouts vp
LEFT JOIN vendors v
	ON vp.vendor_id=v.vendor_id
WHERE v.vendor_id IS NULL;





