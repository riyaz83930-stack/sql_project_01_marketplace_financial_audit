# Marketplace Financial Data Quality Audit

## Project Overview

This project is a SQL and Python based data quality audit of a marketplace financial database.

The main goal was to check whether the data is reliable enough for reporting and financial analysis.

Instead of only looking at totals, I checked the data from different angles like missing values, invalid values, broken relationships, date problems, payment mismatches and vendor payout reconciliation.

The project was done using MySQL, SQL and Python.

---

## Business Problem

A marketplace depends on different tables for customers, orders, products, payments and vendor payouts.

If these tables contain incorrect or inconsistent data, reports and financial numbers can also become unreliable.

For example:

- An order can have a customer_id which does not exist.
- A payment can exist without a valid order.
- A payment date can be before the order date.
- An order total can be different from the payment amount.
- Vendor payouts may not match completed sales.
- Negative or zero financial values can appear in the data.

The purpose of this audit was to identify these problems and quantify their impact where it was meaningful.

---

## Database

Database used:

`project_01_financial_audit`

Main tables:

- customers
- orders
- order_items
- products
- payments
- vendors
- vendor_payouts

---

## Audit Approach

The audit was divided into five main phases.

### Phase 1 — Surface-Level Exploration

First I checked the basic quality of the data.

This included:

- Row counts
- NULL values and NULL percentage
- Zero and negative financial values
- Distinct values in important text columns
- Status and text inconsistencies
- Basic data quality problems

This phase was mainly used to understand where the problems were before doing deeper checks.

### Phase 2 — Referential Integrity

Next I checked whether the relationships between tables were valid.

I checked for orphan records such as:

- Orders with missing customers
- Order items with missing orders
- Order items with missing products
- Payments with missing orders
- Vendor payouts with missing vendors

These checks help identify broken relationships between the tables.

### Phase 3 — Date Logic

I checked whether important dates followed the expected business sequence.

Examples:

- Order before customer signup
- Payment before the corresponding order
- Vendor payout before vendor signup

These records may indicate data-entry problems, incorrect dates or other data issues.

### Phase 4 — Financial Reconciliation

This was the main financial part of the audit.

I checked:

- Completed order amount vs payment amount
- Orders without payment
- Payments without an order
- Duplicate payment records
- Vendor completed sales vs vendor payouts

Financial differences were quantified only where the calculation made business sense.

A difference in two financial fields was not automatically treated as fraud or loss.

### Phase 5 — Consolidation

Finally, the findings were combined into a master audit summary.

The summary contains:

- Audit check
- Affected rows
- Total rows
- Affected percentage
- Financial impact where applicable
- Finding notes
- Severity

This makes the individual SQL checks easier to review together.

---

## Python Automation

After completing the SQL checks, I used Python to automate the audit process.

Python is mainly used for:

- Connecting to MySQL
- Running the audit queries
- Reading results with Pandas
- Saving detailed findings as CSV files
- Creating the master audit summary
- Handling errors without stopping the complete audit

The SQL queries contain the actual audit logic and financial calculations.

Python mainly handles execution, output and reporting.

Database credentials are not hardcoded in the script. The database password is read from an environment variable.

---

## Project Structure

```text
marketplace-financial-data-quality-audit/
│
├── README.md
├── findings_report.md
│
├── data/
│   └── schema.sql
│
├── queries/
│   ├── phase_1_surface_exploration.sql
│   ├── phase_2_referential_integrity.sql
│   ├── phase_3_date_logic.sql
│   ├── phase_4_financial_reconciliation.sql
│   └── phase_5_consolidation.sql
│
├── analysis/
│   └── audit_automation.py
│
└── outputs/
    ├── master_audit_summary.csv
    ├── audit_error_log.csv
    └── detailed_findings/