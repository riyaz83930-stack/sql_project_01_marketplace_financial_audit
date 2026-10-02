
---

# `findings_report.md`

```markdown
# Marketplace Financial Data Quality Audit — Findings Report

## 1. Executive Summary

The audit was performed to check the quality and reliability of marketplace customer, order, payment and vendor financial data.

The audit covered data quality, referential integrity, date logic and financial reconciliation.

Several issues were found across the database.

The most important findings were related to invalid financial values, broken table relationships, missing payments and mismatches between completed orders and payments.

The audit also showed that vendor revenue and payout periods are not always aligned, so direct all-time comparisons should be treated carefully.

---

## 2. Data Reviewed

The database contains:

| Table | Rows |
|---|---:|
| customers | 250 |
| orders | 2,500 |
| order_items | 5,000 |
| products | 400 |
| payments | 2,301 |
| vendors | 60 |
| vendor_payouts | 154 |

---

## 3. Phase 1 — Surface-Level Data Quality

The first stage checked NULL values, invalid numeric values and text inconsistencies.

### Main findings

- `customers.email`: 26 NULL values, which is 10.40% of customers.
- `orders.total_amount <= 0`: 192 records, 7.68%.
- `order_items`: 164 records had quantity or item_price less than or equal to zero, 3.28%.
- `payments.amount_paid <= 0`: 191 records, 8.30%.
- `products.unit_price <= 0`: 9 records, 2.25%.
- `vendor_payouts.payout_amount <= 0`: 13 records, 8.44%.
- Inconsistent casing was also found in `orders.status`.

These findings show that the data contains both missing information and financially invalid values that should be reviewed before using the data for reporting.

---

## 4. Phase 2 — Referential Integrity

The next step checked whether foreign-key type relationships were valid.

| Check | Affected Rows | Affected % |
|---|---:|---:|
| Orphan customer_id in orders | 78 | 3.12% |
| Orphan order_id in order_items | 116 | 2.32% |
| Orphan product_id in order_items | 69 | 1.38% |
| Orphan order_id in payments | 40 | 1.74% |
| Orphan vendor_id in vendor_payouts | 4 | 2.60% |

These records indicate that some relationships between tables are broken or cannot be matched to the expected parent record.

The affected records should be reviewed before using these relationships for reporting or financial analysis.

---

## 5. Phase 3 — Date Logic

Three important chronological checks were performed.

| Check | Affected Rows | Affected % |
|---|---:|---:|
| Orders before customer signup | 77 | 3.08% |
| Payments before corresponding order | 44 | 1.91% |
| Vendor payouts before vendor signup | 27 | 17.53% |

The vendor payout check has the highest affected percentage among these date checks.

These records do not by themselves explain why the dates are incorrect. They only show that the expected chronological relationship is not satisfied.

---

## 6. Phase 4 — Financial Reconciliation

### Completed Orders vs Payments

There were 1,464 completed orders.

Out of these:

- 1,371 had matching payment amounts.
- 93 had payment mismatches.
- Mismatch rate: 6.35%.

For the 93 mismatched completed orders:

- Expected order amount: ₹1,419,687
- Actual payment amount: ₹1,055,970
- Reconciliation difference: ₹363,717

The ₹363,717 figure represents the difference identified between the two datasets.

It should not automatically be treated as confirmed loss, fraud or unpaid money without further business validation.

---

### Orders Without Payment

294 orders did not have a payment record.

This represents:

**11.76% of all 2,500 orders.**

This is important because an order without a payment record can affect revenue reporting and payment reconciliation.

However, the data alone does not establish whether these orders were unpaid, cancelled later, paid through another process or simply missing a payment record.

---

### Payments Without Corresponding Order

40 payment records did not have a corresponding order.

This represents:

**1.74% of all 2,301 payments.**

These records should be investigated because they cannot currently be connected to a valid order.

---

### Duplicate Payments

37 duplicate payment records were identified based on the duplicate-payment check.

These records require business validation before being treated as confirmed double charges.

A duplicate-looking payment record does not automatically mean that a customer was charged twice.

---

## 7. Vendor Revenue vs Payouts

Vendor-level reconciliation was also performed by comparing completed sales with vendor payouts.

The analysis showed several different situations:

- Some vendors had completed revenue higher than payouts.
- Some vendors had no payout records.
- Some vendors had NULL revenue values.
- Some vendors had negative revenue values.

A direct comparison cannot always be treated as a payout problem because the vendor table contains `commission_rate`, and commission can explain part of the difference.

More importantly, revenue and payout date ranges were not always aligned.

For some vendors, sales covered a longer or different period than the available payout records.

Because of this, all-time revenue vs all-time payout is not always a fair comparison.

The result should therefore be treated as a reconciliation and data-coverage issue unless the business confirms the expected payout period and calculation rules.

---

## 8. Important SQL/Data Issue Found During Analysis

One important technical issue was join fan-out.

When orders, order_items, products, vendors and vendor_payouts are joined together before aggregation, the same financial values can appear multiple times.

This can make SUM() produce an inflated result.

The correct approach is to calculate the revenue side and payout side separately at the required grain and then compare them.

This was important because the goal of the project was not just to find numbers, but to make sure the numbers themselves were trustworthy.

---

## 9. Main Areas Requiring Attention

The audit highlighted four major areas:

### Data Validity

Invalid or zero financial values exist in several tables.

### Relationship Quality

Several records cannot be linked to the expected parent records.

### Date Consistency

Some business events occur before the dates that should logically come before them.

### Financial Reconciliation

Payment gaps and order-payment mismatches require further investigation.

---

## 10. Recommendations

1. Validate required customer, order, product and vendor relationships before loading data into reporting tables.

2. Add validation rules for financial fields such as quantity, price, payment amount and payout amount.

3. Standardize status values and text formatting during data ingestion.

4. Add checks to prevent impossible date sequences.

5. Reconcile completed orders and payments regularly.

6. Investigate orders without payments and payments without orders separately.

7. Define the exact vendor payout calculation and payout period before comparing revenue with payouts.

8. Keep automated data-quality checks as part of the regular reporting pipeline.

---

## 11. Conclusion

The audit found multiple data-quality and financial-reconciliation issues across the marketplace database.

The main value of the project was not only identifying these records, but separating actual data problems from situations where the data was incomplete or the comparison itself could be misleading.

The final SQL checks and Python automation make the audit repeatable and provide detailed CSV outputs for further investigation.