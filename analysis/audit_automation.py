import os
import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================


DB_PASSWORD = os.getenv("DB_PASSWORD")
engine = create_engine(
    f"mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/project_01_financial_audit"
)



# ============================================================
# 2. OUTPUT FOLDERS
# ============================================================

OUTPUT_DIR = "outputs"
DETAIL_DIR = os.path.join(OUTPUT_DIR, "detailed_findings")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DETAIL_DIR, exist_ok=True)


# ============================================================
# 3. AUDIT CHECKS
# ============================================================

def check_orphan_customer_orders():

    query = text("""
        SELECT o.*
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM orders
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_orphan_order_items():

    query = text("""
        SELECT oi.*
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM order_items
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_orphan_product_items():

    query = text("""
        SELECT oi.*
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM order_items
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_orphan_payments():

    query = text("""
        SELECT p.*
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM payments
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_orphan_vendor_payouts():

    query = text("""
        SELECT vp.*
        FROM vendor_payouts vp
        LEFT JOIN vendors v
            ON vp.vendor_id = v.vendor_id
        WHERE v.vendor_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM vendor_payouts
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


# ============================================================
# PHASE 3 — DATE LOGIC
# ============================================================

def check_orders_before_signup():

    query = text("""
        SELECT
            o.order_id,
            o.customer_id,
            o.order_date,
            c.signup_date
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_date < c.signup_date
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM orders
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_payments_before_order():

    query = text("""
        SELECT
            p.payment_id,
            p.order_id,
            p.payment_date,
            o.order_date,
            p.amount_paid
        FROM payments p
        JOIN orders o
            ON p.order_id = o.order_id
        WHERE p.payment_date < o.order_date
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM payments
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


def check_payout_before_vendor_signup():

    query = text("""
        SELECT
            vp.payout_id,
            vp.vendor_id,
            vp.payout_date,
            v.signup_date,
            vp.payout_amount
        FROM vendor_payouts vp
        JOIN vendors v
            ON vp.vendor_id = v.vendor_id
        WHERE vp.payout_date < v.signup_date
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM vendor_payouts
    """)

    affected_data = pd.read_sql(query, engine)
    total_rows = pd.read_sql(total_query, engine).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


# ============================================================
# PHASE 4 — FINANCIAL RECONCILIATION
# ============================================================

def check_completed_order_payment_mismatch():

    query = text("""
        SELECT
            o.order_id,
            o.total_amount AS expected_amount,
            p.amount_paid AS actual_amount,
            ABS(o.total_amount - p.amount_paid) AS difference
        FROM orders o
        JOIN payments p
            ON o.order_id = p.order_id
        WHERE o.status = 'Completed'
        AND o.total_amount <> p.amount_paid
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM orders
        WHERE status = 'Completed'
    """)

    impact_query = text("""
        SELECT
            COALESCE(
                SUM(ABS(o.total_amount - p.amount_paid)),
                0
            ) AS financial_impact
        FROM orders o
        JOIN payments p
            ON o.order_id = p.order_id
        WHERE o.status = 'Completed'
        AND o.total_amount <> p.amount_paid
    """)

    affected_data = pd.read_sql(query, engine)

    total_rows = pd.read_sql(
        total_query,
        engine
    ).iloc[0, 0]

    financial_impact = pd.read_sql(
        impact_query,
        engine
    ).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": float(financial_impact)
    }


def check_orders_without_payment():

    query = text("""
        SELECT
            o.order_id,
            o.customer_id,
            o.order_date,
            o.total_amount,
            o.status
        FROM orders o
        LEFT JOIN payments p
            ON o.order_id = p.order_id
        WHERE p.order_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM orders
    """)

    impact_query = text("""
        SELECT
            COALESCE(SUM(o.total_amount), 0) AS financial_impact
        FROM orders o
        LEFT JOIN payments p
            ON o.order_id = p.order_id
        WHERE p.order_id IS NULL
    """)

    affected_data = pd.read_sql(query, engine)

    total_rows = pd.read_sql(
        total_query,
        engine
    ).iloc[0, 0]

    financial_impact = pd.read_sql(
        impact_query,
        engine
    ).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": float(financial_impact)
    }


def check_payments_without_order():

    query = text("""
        SELECT p.*
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM payments
    """)

    impact_query = text("""
        SELECT
            COALESCE(SUM(p.amount_paid), 0) AS financial_impact
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)

    affected_data = pd.read_sql(query, engine)

    total_rows = pd.read_sql(
        total_query,
        engine
    ).iloc[0, 0]

    financial_impact = pd.read_sql(
        impact_query,
        engine
    ).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": float(financial_impact)
    }


def check_duplicate_payments():

    query = text("""
        WITH duplicate_payments AS (
            SELECT
                p.*,
                ROW_NUMBER() OVER (
                    PARTITION BY
                        order_id,
                        amount_paid
                    ORDER BY
                        payment_date,
                        payment_id
                ) AS rn
            FROM payments p
        )
        SELECT *
        FROM duplicate_payments
        WHERE rn > 1
    """)

    total_query = text("""
        SELECT COUNT(*) AS total_rows
        FROM payments
    """)

    affected_data = pd.read_sql(query, engine)

    total_rows = pd.read_sql(
        total_query,
        engine
    ).iloc[0, 0]

    affected_rows = len(affected_data)

    affected_percent = (
        affected_rows / total_rows * 100
        if total_rows else 0
    )

    return {
        "affected_data": affected_data,
        "affected_rows": affected_rows,
        "total_rows": total_rows,
        "affected_percent": round(affected_percent, 2),
        "financial_impact": None
    }


# ============================================================
# 4. REGISTER ALL CHECKS
# ============================================================

AUDIT_CHECKS = [

    ("Phase 2", "Orphan customer_id in orders",
    check_orphan_customer_orders),

    ("Phase 2", "Orphan order_id in order_items",
    check_orphan_order_items),

    ("Phase 2", "Orphan product_id in order_items",
    check_orphan_product_items),

    ("Phase 2", "Orphan order_id in payments",
    check_orphan_payments),

    ("Phase 2", "Orphan vendor_id in vendor_payouts",
    check_orphan_vendor_payouts),

    ("Phase 3", "Orders before customer signup",
    check_orders_before_signup),

    ("Phase 3", "Payments before corresponding order",
    check_payments_before_order),

    ("Phase 3", "Vendor payouts before vendor signup",
    check_payout_before_vendor_signup),

    ("Phase 4", "Completed order payment mismatch",
    check_completed_order_payment_mismatch),

    ("Phase 4", "Orders without payment",
    check_orders_without_payment),

    ("Phase 4", "Payments without corresponding order",
    check_payments_without_order),

    ("Phase 4", "Duplicate payments",
    check_duplicate_payments)
]


# ============================================================
# 5. MASTER AUDIT FUNCTION
# ============================================================

def run_audit():

    summary = []

    error_log = []

    for phase, check_name, check_function in AUDIT_CHECKS:

        print(f"Running: {check_name}")

        try:

            result = check_function()

            affected_data = result["affected_data"]

            affected_rows = result["affected_rows"]

            total_rows = result["total_rows"]

            affected_percent = result["affected_percent"]

            financial_impact = result["financial_impact"]


            # --------------------------------------------
            # SAVE DETAILED FINDINGS
            # --------------------------------------------

            safe_name = (
                check_name
                .lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            detailed_file = os.path.join(
                DETAIL_DIR,
                f"{safe_name}.csv"
            )

            affected_data.to_csv(
                detailed_file,
                index=False
            )


            # --------------------------------------------
            # MASTER SUMMARY
            # --------------------------------------------

            summary.append({

                "phase": phase,

                "check_name": check_name,

                "affected_rows": affected_rows,

                "total_rows": total_rows,

                "affected_percent": affected_percent,

                "financial_impact": financial_impact

            })


            print(
                f"Completed → "
                f"{affected_rows} affected rows"
            )


        except Exception as e:

            error_message = {
                "phase": phase,
                "check_name": check_name,
                "error": str(e)
            }

            error_log.append(error_message)

            print(
                f"ERROR → {check_name}: {e}"
            )

            continue


    # ========================================================
    # MASTER SUMMARY DATAFRAME
    # ========================================================

    summary_df = pd.DataFrame(summary)


    summary_file = os.path.join(
        OUTPUT_DIR,
        "master_audit_summary.csv"
    )

    summary_df.to_csv(
        summary_file,
        index=False
    )


    # ========================================================
    # ERROR LOG
    # ========================================================

    if error_log:

        error_df = pd.DataFrame(error_log)

        error_file = os.path.join(
            OUTPUT_DIR,
            "audit_error_log.csv"
        )

        error_df.to_csv(
            error_file,
            index=False
        )

    else:

        print("No audit errors found.")


    return summary_df


# ============================================================
# 6. RUN AUDIT
# ============================================================

if __name__ == "__main__":

    summary_df = run_audit()

    print("\n========================================")
    print("AUDIT COMPLETED")
    print("========================================")

    print(summary_df)

    print("\nMaster summary:")
    print(
        os.path.join(
            OUTPUT_DIR,
            "master_audit_summary.csv"
        )
    )

    print("\nDetailed findings:")
    print(DETAIL_DIR)


    