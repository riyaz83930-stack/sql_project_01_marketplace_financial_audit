
-- DATE LOGIC AUDIT


-- FINDING ORDERS MADE BEFORE CUSTOMER SIGNUP DATE 

CREATE VIEW order_customer AS 

SELECT
o.*,
c.customer_id AS c_id,
c.customer_name,
c.email,
c.city,
c.signup_date
FROM orders o
INNER JOIN customers c
	ON o.customer_id=c.customer_id;
    
    
SELECT 
	COUNT(*)
FROM order_customer
WHERE order_date < signup_date;


-- FINDING PAYMENTS  MADE BEFORE ORDER DATE 
CREATE VIEW order_payment AS 
SELECT
	p.*,
    o.order_id AS o_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount
FROM payments p
INNER JOIN orders o
	ON p.order_id=o.order_id;
    
    
SELECT
	COUNT(*)
FROM order_payment 
WHERE payment_date < order_date
;
    
-- FINDING VENDOR PAYOUTS DONE BEFORE VENDORS SIGNUP DATE 

CREATE VIEW vendor_and_payout AS 
SELECT
	vp.payout_id,
    vp.vendor_id AS v_id,
    vp.payout_date,
    vp.payout_amount,
    vp.period_covered,
	v.*
FROM vendor_payouts vp
INNER JOIN  vendors v
	ON vp.vendor_id=v.vendor_id;
    
SELECT 
	COUNT(*)
FROM vendor_and_payout 
WHERE payout_date < signup_date
;


-- RESULT

-- | Check                                    | Affected Rows | Total Relevant Rows | Affected % |
-- | ---------------------------------------- | ------------: | ------------------: | ---------: |
-- | Orders before customer signup date       |        **77** |               2,500 |  **3.08%** |
-- | Payments before corresponding order date |        **44** |               2,301 |  **1.91%** |
-- | Vendor payouts before vendor signup date |        **27** |                 154 | **17.53%** |


