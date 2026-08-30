"""
============================================================
MESS MANAGEMENT SYSTEM - PYTHON (SQLite) IMPLEMENTATION
Assessment 10: Final Internship Evaluation
============================================================
Run this file directly:
    python mess_management_system.py

It will:
  1. Create an in-memory SQLite database with all tables + relationships
  2. Insert sample data
  3. Run 15 business queries and print the results
  4. Run 3 optimized queries (with indexes added) and show EXPLAIN plans
     before/after so you can see the optimization effect

No external packages needed - only the built-in sqlite3 module.
============================================================
"""

import sqlite3


def get_connection():
    """Creates an in-memory SQLite database connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ============================================================
# 1. TABLE CREATION (schema + relationships)
# ============================================================
SCHEMA = """
CREATE TABLE hostels (
    hostel_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    hostel_name   TEXT NOT NULL,
    warden_name   TEXT
);

CREATE TABLE students (
    student_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    roll_no       TEXT UNIQUE NOT NULL,
    room_no       TEXT,
    hostel_id     INTEGER,
    contact       TEXT,
    email         TEXT,
    FOREIGN KEY (hostel_id) REFERENCES hostels(hostel_id)
);

CREATE TABLE mess_plans (
    plan_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name      TEXT NOT NULL,
    meals_included TEXT,
    monthly_fee    REAL NOT NULL
);

CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    plan_id         INTEGER NOT NULL,
    start_date      TEXT NOT NULL,
    end_date        TEXT,
    status          TEXT CHECK(status IN ('Active','Expired','Cancelled')) DEFAULT 'Active',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (plan_id) REFERENCES mess_plans(plan_id)
);

CREATE TABLE menu_items (
    item_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name        TEXT NOT NULL,
    category         TEXT CHECK(category IN ('Veg','Non-Veg','Dessert','Beverage')) DEFAULT 'Veg',
    cost_per_serving REAL
);

CREATE TABLE daily_menu (
    menu_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_date   TEXT NOT NULL,
    meal_type   TEXT CHECK(meal_type IN ('Breakfast','Lunch','Snacks','Dinner')) NOT NULL,
    item_id     INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

CREATE TABLE attendance (
    attendance_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    attendance_date TEXT NOT NULL,
    meal_type       TEXT CHECK(meal_type IN ('Breakfast','Lunch','Snacks','Dinner')) NOT NULL,
    present         INTEGER DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE payments (
    payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    amount          REAL NOT NULL,
    payment_date    TEXT NOT NULL,
    payment_mode    TEXT CHECK(payment_mode IN ('Cash','Card','UPI','NetBanking')) DEFAULT 'UPI',
    status          TEXT CHECK(status IN ('Paid','Pending','Failed')) DEFAULT 'Paid',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

CREATE TABLE staff (
    staff_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    role      TEXT CHECK(role IN ('Cook','Helper','Manager','Cleaner')) NOT NULL,
    contact   TEXT,
    salary    REAL
);

CREATE TABLE feedback (
    feedback_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id    INTEGER NOT NULL,
    feedback_date TEXT NOT NULL,
    meal_type     TEXT CHECK(meal_type IN ('Breakfast','Lunch','Snacks','Dinner')) NOT NULL,
    rating        INTEGER CHECK(rating BETWEEN 1 AND 5),
    comments      TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE suppliers (
    supplier_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    contact       TEXT,
    address       TEXT
);

CREATE TABLE inventory (
    inventory_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name     TEXT NOT NULL,
    quantity      REAL NOT NULL,
    unit          TEXT,
    reorder_level REAL DEFAULT 10
);

CREATE TABLE purchase_orders (
    po_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id   INTEGER NOT NULL,
    item_name     TEXT NOT NULL,
    quantity      REAL NOT NULL,
    order_date    TEXT NOT NULL,
    delivery_date TEXT,
    cost          REAL NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);
"""


# ============================================================
# 2. SAMPLE DATA
# ============================================================
def insert_sample_data(conn):
    cur = conn.cursor()

    cur.executemany(
        "INSERT INTO hostels (hostel_name, warden_name) VALUES (?, ?)",
        [
            ("Hostel A", "Mr. Ramesh Kumar"),
            ("Hostel B", "Mrs. Sunita Rao"),
        ],
    )

    cur.executemany(
        """INSERT INTO students (name, roll_no, room_no, hostel_id, contact, email)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            ("Arjun Mehta", "CS101", "A101", 1, "9876543210", "arjun@example.com"),
            ("Priya Sharma", "CS102", "A102", 1, "9876543211", "priya@example.com"),
            ("Rahul Verma", "CS103", "B201", 2, "9876543212", "rahul@example.com"),
            ("Sneha Iyer", "CS104", "B202", 2, "9876543213", "sneha@example.com"),
            ("Karan Joshi", "CS105", "A103", 1, "9876543214", "karan@example.com"),
        ],
    )

    cur.executemany(
        "INSERT INTO mess_plans (plan_name, meals_included, monthly_fee) VALUES (?, ?, ?)",
        [
            ("Basic Plan", "Breakfast,Lunch,Dinner", 3000.00),
            ("Premium Plan", "Breakfast,Lunch,Snacks,Dinner", 4000.00),
        ],
    )

    cur.executemany(
        """INSERT INTO subscriptions (student_id, plan_id, start_date, end_date, status)
           VALUES (?, ?, ?, ?, ?)""",
        [
            (1, 1, "2026-07-01", "2026-07-31", "Expired"),
            (1, 1, "2026-08-01", None, "Active"),
            (2, 2, "2026-08-01", None, "Active"),
            (3, 1, "2026-08-01", None, "Active"),
            (4, 2, "2026-08-01", None, "Active"),
            (5, 1, "2026-08-01", None, "Active"),
        ],
    )

    cur.executemany(
        "INSERT INTO menu_items (item_name, category, cost_per_serving) VALUES (?, ?, ?)",
        [
            ("Idli Sambar", "Veg", 25.00),
            ("Chicken Curry", "Non-Veg", 60.00),
            ("Veg Fried Rice", "Veg", 40.00),
            ("Gulab Jamun", "Dessert", 15.00),
            ("Masala Chai", "Beverage", 10.00),
        ],
    )

    cur.executemany(
        "INSERT INTO daily_menu (menu_date, meal_type, item_id) VALUES (?, ?, ?)",
        [
            ("2026-08-25", "Breakfast", 1),
            ("2026-08-25", "Lunch", 3),
            ("2026-08-25", "Dinner", 2),
            ("2026-08-26", "Breakfast", 1),
            ("2026-08-26", "Lunch", 2),
            ("2026-08-26", "Dinner", 3),
            ("2026-08-26", "Snacks", 5),
        ],
    )

    cur.executemany(
        """INSERT INTO attendance (student_id, attendance_date, meal_type, present)
           VALUES (?, ?, ?, ?)""",
        [
            (1, "2026-08-25", "Breakfast", 1),
            (1, "2026-08-25", "Lunch", 1),
            (1, "2026-08-25", "Dinner", 0),
            (2, "2026-08-25", "Breakfast", 1),
            (2, "2026-08-25", "Lunch", 1),
            (3, "2026-08-25", "Lunch", 1),
            (3, "2026-08-25", "Dinner", 1),
            (4, "2026-08-25", "Breakfast", 1),
            (5, "2026-08-25", "Dinner", 1),
        ],
    )

    cur.executemany(
        """INSERT INTO payments (student_id, subscription_id, amount, payment_date, payment_mode, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (1, 1, 3000.00, "2026-07-01", "UPI", "Paid"),
            (1, 2, 3000.00, "2026-08-01", "UPI", "Paid"),
            (2, 3, 4000.00, "2026-08-02", "Card", "Paid"),
            (3, 4, 3000.00, "2026-08-01", "Cash", "Pending"),
            (4, 5, 4000.00, "2026-08-03", "NetBanking", "Paid"),
            (5, 6, 3000.00, "2026-08-01", "UPI", "Failed"),
        ],
    )

    cur.executemany(
        "INSERT INTO staff (name, role, contact, salary) VALUES (?, ?, ?, ?)",
        [
            ("Suresh Nair", "Cook", "9000011111", 18000.00),
            ("Lakshmi Devi", "Cook", "9000011112", 17000.00),
            ("Manoj Singh", "Manager", "9000011113", 25000.00),
            ("Geeta Bai", "Cleaner", "9000011114", 12000.00),
        ],
    )

    cur.executemany(
        """INSERT INTO feedback (student_id, feedback_date, meal_type, rating, comments)
           VALUES (?, ?, ?, ?, ?)""",
        [
            (1, "2026-08-25", "Breakfast", 4, "Good taste"),
            (2, "2026-08-25", "Breakfast", 5, "Excellent"),
            (3, "2026-08-25", "Lunch", 3, "Average, needs more variety"),
            (4, "2026-08-25", "Dinner", 2, "Too spicy"),
            (5, "2026-08-25", "Dinner", 4, "Nice"),
        ],
    )

    cur.executemany(
        "INSERT INTO suppliers (supplier_name, contact, address) VALUES (?, ?, ?)",
        [
            ("Fresh Farms Pvt Ltd", "9123456780", "Chennai, TN"),
            ("Grain Traders Co.", "9123456781", "Vellore, TN"),
        ],
    )

    cur.executemany(
        "INSERT INTO inventory (item_name, quantity, unit, reorder_level) VALUES (?, ?, ?, ?)",
        [
            ("Rice", 50.00, "kg", 20),
            ("Wheat Flour", 8.00, "kg", 15),
            ("Cooking Oil", 25.00, "litre", 10),
            ("Vegetables", 5.00, "kg", 10),
        ],
    )

    cur.executemany(
        """INSERT INTO purchase_orders (supplier_id, item_name, quantity, order_date, delivery_date, cost)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (1, "Vegetables", 50.00, "2026-08-20", "2026-08-22", 2500.00),
            (2, "Rice", 100.00, "2026-08-18", "2026-08-20", 6000.00),
            (1, "Cooking Oil", 30.00, "2026-08-15", "2026-08-17", 3600.00),
        ],
    )

    conn.commit()


# ============================================================
# Helper to run + pretty-print a query
# ============================================================
def run_query(conn, title, sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")
    print(" | ".join(columns))
    print("-" * 70)
    if not rows:
        print("(no rows)")
    for row in rows:
        print(" | ".join(str(v) for v in row))


def show_explain(conn, label, sql, params=()):
    cur = conn.cursor()
    cur.execute(f"EXPLAIN QUERY PLAN {sql}", params)
    plan = cur.fetchall()
    print(f"\n-- {label} --")
    for step in plan:
        print(step)


# ============================================================
# 3. 15 BUSINESS QUERIES
# ============================================================
def run_business_queries(conn):
    run_query(conn, "Q1: Students with their hostel name", """
        SELECT s.name, s.roll_no, h.hostel_name
        FROM students s
        JOIN hostels h ON s.hostel_id = h.hostel_id
    """)

    run_query(conn, "Q2: Students with an active subscription", """
        SELECT s.name, sub.plan_id, sub.start_date, sub.status
        FROM students s
        JOIN subscriptions sub ON s.student_id = sub.student_id
        WHERE sub.status = 'Active'
    """)

    run_query(conn, "Q3: Total revenue collected in August 2026", """
        SELECT SUM(amount) AS total_revenue
        FROM payments
        WHERE status = 'Paid'
          AND strftime('%m', payment_date) = '08'
          AND strftime('%Y', payment_date) = '2026'
    """)

    run_query(conn, "Q4: Students with Pending/Failed payments", """
        SELECT s.name, p.amount, p.status
        FROM payments p
        JOIN students s ON p.student_id = s.student_id
        WHERE p.status IN ('Pending','Failed')
    """)

    run_query(conn, "Q5: Average feedback rating per meal type", """
        SELECT meal_type, ROUND(AVG(rating), 2) AS avg_rating
        FROM feedback
        GROUP BY meal_type
        ORDER BY avg_rating DESC
    """)

    run_query(conn, "Q6: Attendance percentage per student", """
        SELECT s.name,
               SUM(a.present) AS meals_attended,
               COUNT(*) AS total_meals_logged,
               ROUND(SUM(a.present) * 100.0 / COUNT(*), 2) AS attendance_pct
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        GROUP BY s.student_id, s.name
    """)

    run_query(conn, "Q7: Meal-wise headcount on 2026-08-25", """
        SELECT meal_type, COUNT(*) AS total_present
        FROM attendance
        WHERE attendance_date = '2026-08-25' AND present = 1
        GROUP BY meal_type
    """)

    run_query(conn, "Q8: Total expenditure per supplier", """
        SELECT sup.supplier_name, SUM(po.cost) AS total_spent
        FROM purchase_orders po
        JOIN suppliers sup ON po.supplier_id = sup.supplier_id
        GROUP BY sup.supplier_id, sup.supplier_name
        ORDER BY total_spent DESC
    """)

    run_query(conn, "Q9: Revenue generated per mess plan", """
        SELECT mp.plan_name, SUM(p.amount) AS total_revenue
        FROM payments p
        JOIN subscriptions sub ON p.subscription_id = sub.subscription_id
        JOIN mess_plans mp ON sub.plan_id = mp.plan_id
        WHERE p.status = 'Paid'
        GROUP BY mp.plan_id, mp.plan_name
    """)

    run_query(conn, "Q10: Inventory items below reorder level", """
        SELECT item_name, quantity, reorder_level
        FROM inventory
        WHERE quantity < reorder_level
    """)

    run_query(conn, "Q11: Staff count and salary expense per role", """
        SELECT role, COUNT(*) AS staff_count, SUM(salary) AS total_salary_expense
        FROM staff
        GROUP BY role
    """)

    run_query(conn, "Q12: Menu items served on 2026-08-26", """
        SELECT dm.meal_type, mi.item_name, mi.category
        FROM daily_menu dm
        JOIN menu_items mi ON dm.item_id = mi.item_id
        WHERE dm.menu_date = '2026-08-26'
    """)

    run_query(conn, "Q13: Students belonging to 'Hostel A'", """
        SELECT s.name, s.room_no
        FROM students s
        JOIN hostels h ON s.hostel_id = h.hostel_id
        WHERE h.hostel_name = 'Hostel A'
    """)

    run_query(conn, "Q14: Highest-rated meal type overall", """
        SELECT meal_type, ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY meal_type
        ORDER BY avg_rating DESC
        LIMIT 1
    """)

    run_query(conn, "Q15: Payment collected vs outstanding by mode", """
        SELECT payment_mode,
               SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) AS collected,
               SUM(CASE WHEN status IN ('Pending','Failed') THEN amount ELSE 0 END) AS outstanding
        FROM payments
        GROUP BY payment_mode
    """)


# ============================================================
# 4. QUERY OPTIMIZATION (3 QUERIES)
# ============================================================
def run_optimizations(conn):
    cur = conn.cursor()

    print("\n\n" + "#" * 70)
    print("QUERY OPTIMIZATION SECTION")
    print("#" * 70)

    # ---------- Optimization 1: Q4 ----------
    q4 = """
        SELECT s.name, p.amount, p.status
        FROM payments p
        JOIN students s ON p.student_id = s.student_id
        WHERE p.status IN ('Pending','Failed')
    """
    show_explain(conn, "Q4 BEFORE index (full table scan expected)", q4)

    cur.execute("CREATE INDEX idx_payments_status ON payments(status)")
    cur.execute("CREATE INDEX idx_payments_student_id ON payments(student_id)")

    show_explain(conn, "Q4 AFTER index (uses idx_payments_status)", q4)
    run_query(conn, "Optimization 1 - Q4 result (students w/ pending or failed payments)", q4)

    # ---------- Optimization 2: Q6 ----------
    q6 = """
        SELECT s.name,
               SUM(a.present) AS meals_attended,
               COUNT(*) AS total_meals_logged,
               ROUND(SUM(a.present) * 100.0 / COUNT(*), 2) AS attendance_pct
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        GROUP BY s.student_id, s.name
    """
    show_explain(conn, "Q6 BEFORE index", q6)

    cur.execute("CREATE INDEX idx_attendance_student_date ON attendance(student_id, attendance_date)")

    show_explain(conn, "Q6 AFTER composite index on (student_id, attendance_date)", q6)
    run_query(conn, "Optimization 2 - Q6 result (attendance % per student)", q6)

    # ---------- Optimization 3: Q9 ----------
    q9 = """
        SELECT mp.plan_name, SUM(p.amount) AS total_revenue
        FROM payments p
        JOIN subscriptions sub ON p.subscription_id = sub.subscription_id
        JOIN mess_plans mp ON sub.plan_id = mp.plan_id
        WHERE p.status = 'Paid'
        GROUP BY mp.plan_id, mp.plan_name
    """
    show_explain(conn, "Q9 BEFORE index", q9)

    cur.execute("CREATE INDEX idx_subscriptions_plan_id ON subscriptions(plan_id)")
    cur.execute("CREATE INDEX idx_payments_subscription_id ON payments(subscription_id)")

    show_explain(conn, "Q9 AFTER indexes on subscriptions.plan_id and payments.subscription_id", q9)
    run_query(conn, "Optimization 3 - Q9 result (revenue per mess plan)", q9)


# ============================================================
# MAIN
# ============================================================
def main():
    conn = get_connection()
    conn.executescript(SCHEMA)
    insert_sample_data(conn)

    print("\n" + "#" * 70)
    print("15 BUSINESS QUERIES")
    print("#" * 70)
    run_business_queries(conn)

    run_optimizations(conn)

    conn.close()


if __name__ == "__main__":
    main()