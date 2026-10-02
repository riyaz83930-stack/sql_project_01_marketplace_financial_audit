WITH master_summary AS (

    
    --    PHASE 1 — SURFACE EXPLORATION
       

    SELECT
        'Phase 1' AS phase,
        'NULL customer email' AS check_name,
        26 AS affected_rows,
        250 AS total_rows,
        ROUND(26 / 250 * 100, 2) AS affected_percent,
        NULL AS financial_impact,
        'Data completeness issue' AS finding_note

    UNION ALL

    SELECT
        'Phase 1',
        'NULL vendor commission rate',
        4,
        NULL,
        NULL,
        NULL,
        '4 non-suspended vendors have NULL commission_rate'

    UNION ALL

    SELECT
        'Phase 1',
        'Orders with non-positive total_amount',
        192,
        2500,
        ROUND(192 / 2500 * 100, 2),
        NULL,
        'total_amount <= 0'

    UNION ALL

    SELECT
        'Phase 1',
        'Order items with non-positive quantity or item_price',
        164,
        5000,
        ROUND(164 / 5000 * 100, 2),
        NULL,
        'quantity <= 0 OR item_price <= 0'

    UNION ALL

    SELECT
        'Phase 1',
        'Payments with non-positive amount_paid',
        191,
        2301,
        ROUND(191 / 2301 * 100, 2),
        NULL,
        'amount_paid <= 0'

    UNION ALL

    SELECT
        'Phase 1',
        'Products with non-positive unit_price',
        9,
        400,
        ROUND(9 / 400 * 100, 2),
        NULL,
        'unit_price <= 0'

    UNION ALL

    SELECT
        'Phase 1',
        'Vendor payouts with non-positive payout_amount',
        13,
        154,
        ROUND(13 / 154 * 100, 2),
        NULL,
        'payout_amount <= 0'

    UNION ALL

    SELECT
        'Phase 1',
        'Order status case inconsistency',
        NULL,
        2500,
        NULL,
        NULL,
        'Different casing found in status values'


    
    --    PHASE 2 — REFERENTIAL INTEGRITY
       

    UNION ALL

    SELECT
        'Phase 2',
        'Orphan customer_id in orders',
        78,
        2500,
        ROUND(78 / 2500 * 100, 2),
        NULL,
        'customer_id does not exist in customers'

    UNION ALL

    SELECT
        'Phase 2',
        'Orphan order_id in order_items',
        116,
        5000,
        ROUND(116 / 5000 * 100, 2),
        NULL,
        'order_id does not exist in orders'

    UNION ALL

    SELECT
        'Phase 2',
        'Orphan product_id in order_items',
        69,
        5000,
        ROUND(69 / 5000 * 100, 2),
        NULL,
        'product_id does not exist in products'

    UNION ALL

    SELECT
        'Phase 2',
        'Orphan order_id in payments',
        40,
        2301,
        ROUND(40 / 2301 * 100, 2),
        NULL,
        'order_id does not exist in orders'

    UNION ALL

    SELECT
        'Phase 2',
        'Orphan vendor_id in vendor_payouts',
        4,
        154,
        ROUND(4 / 154 * 100, 2),
        NULL,
        'vendor_id does not exist in vendors'


    -- PHASE 3 — DATE LOGIC
       

    UNION ALL

    SELECT
        'Phase 3',
        'Orders before customer signup',
        77,
        2500,
        ROUND(77 / 2500 * 100, 2),
        NULL,
        'order_date < customer signup_date'

    UNION ALL

    SELECT
        'Phase 3',
        'Payments before corresponding order',
        44,
        2301,
        ROUND(44 / 2301 * 100, 2),
        NULL,
        'payment_date < order_date'

    UNION ALL

    SELECT
        'Phase 3',
        'Vendor payouts before vendor signup',
        27,
        154,
        ROUND(27 / 154 * 100, 2),
        NULL,
        'payout_date < vendor signup_date'


    -- PHASE 4 — FINANCIAL RECONCILIATION
       

    UNION ALL

    SELECT
        'Phase 4',
        'Completed orders with payment amount mismatch',
        93,
        1464,
        ROUND(93 / 1464 * 100, 2),
        363717,
        'Expected order amount and recorded payment amount do not reconcile'

    UNION ALL

    SELECT
        'Phase 4',
        'Orders without payment record',
        294,
        2500,
        ROUND(294 / 2500 * 100, 2),
        NULL,
        'No corresponding payment record found'

    UNION ALL

    SELECT
        'Phase 4',
        'Payments without matching order',
        40,
        2301,
        ROUND(40 / 2301 * 100, 2),
        NULL,
        'Same orphan-payment issue identified in Phase 2'

    UNION ALL

    SELECT
        'Phase 4',
        'Duplicate payment records',
        37,
        2301,
        ROUND(37 / 2301 * 100, 2),
        NULL,
        'Potential duplicate payments based on order, amount and date'

    UNION ALL

    SELECT
        'Phase 4',
        'Vendor sales vs payout reconciliation',
        NULL,
        NULL,
        NULL,
        NULL,
        'Full-period reconciliation is unreliable because revenue and payout periods are not consistently aligned'
)

SELECT
    phase,
    check_name,
    affected_rows,
    total_rows,
    affected_percent,
    financial_impact,
    finding_note
FROM master_summary
ORDER BY
    FIELD(phase, 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'),
    affected_percent DESC;