import mysql.connector
from datetime import date

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="" # insert password
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS bacchus_winery")
cursor.execute("USE bacchus_winery")

# Disable foreign key checks to safely drop tables
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

cursor.execute("DROP TABLE IF EXISTS Departments")
cursor.execute("DROP TABLE IF EXISTS Positions")
cursor.execute("DROP TABLE IF EXISTS Employees")
cursor.execute("DROP TABLE IF EXISTS Time_Entries")

cursor.execute("DROP TABLE IF EXISTS Distributors")
cursor.execute("DROP TABLE IF EXISTS Wine_Orders")
cursor.execute("DROP TABLE IF EXISTS Wine_Types")
cursor.execute("DROP TABLE IF EXISTS Harvest_Batch")
cursor.execute("DROP TABLE IF EXISTS Wine_Inventory")
cursor.execute("DROP TABLE IF EXISTS Wine_Order_Details")

cursor.execute("DROP TABLE IF EXISTS Suppliers")
cursor.execute("DROP TABLE IF EXISTS Supply_Orders")
cursor.execute("DROP TABLE IF EXISTS Supply_Types")
cursor.execute("DROP TABLE IF EXISTS Supply_Inventory")
cursor.execute("DROP TABLE IF EXISTS Supply_Order_Details")

cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

##################
# EMPLOYEE TABLES
##################

cursor.execute("""
               CREATE TABLE Departments
               (
                   dept_id   INT PRIMARY KEY,
                   dept_name VARCHAR(40)
               )
               """)

cursor.execute("""
               CREATE TABLE Positions
               (
                   position_id INT PRIMARY KEY,
                   title       VARCHAR(40),
                   min_salary  DECIMAL(10, 2),
                   max_salary  DECIMAL(10, 2),
                   dept_id     INT REFERENCES Departments (dept_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Employees
               (
                   employee_id    INT PRIMARY KEY,
                   first_name     VARCHAR(20),
                   last_name      VARCHAR(20),
                   date_of_birth  VARCHAR(20),
                   street_address VARCHAR(60),
                   city           VARCHAR(40),
                   state          VARCHAR(40),
                   phone_number   VARCHAR(20),
                   manager_id     INT REFERENCES Employees (employee_id),
                   position_id    INT REFERENCES Positions (position_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Time_Entries
               (
                   entry_id     INT PRIMARY KEY,
                   hours_worked DECIMAL(4, 2),
                   work_date    DATE,
                   employee_id  INT REFERENCES Employees (employee_id)
               )
               """)

##############
# WINE TABLES
##############

cursor.execute("""
               CREATE TABLE Distributors
               (
                   distributor_id INT PRIMARY KEY,
                   name           VARCHAR(60),
                   street_address VARCHAR(60),
                   city           VARCHAR(40),
                   state          VARCHAR(40),
                   contact_name   VARCHAR(40),
                   phone_number   VARCHAR(20),
                   email          VARCHAR(40)
               )
               """)

cursor.execute("""
               CREATE TABLE Wine_Orders
               (
                   order_id      INT PRIMARY KEY,
                   order_date    DATE,
                   ship_date     DATE,
                   distributor_id INT REFERENCES Distributors (distributor_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Wine_Types
               (
                   wine_id      INT PRIMARY KEY,
                   type         VARCHAR(60),
                   bottle_price DECIMAL(10, 2)
               )
               """)

cursor.execute("""
               CREATE TABLE Harvest_Batch
               (
                   batch_id          INT PRIMARY KEY,
                   harvest_date      DATE,
                   weight            DECIMAL(10, 2),
                   fermentation_date DATE,
                   wine_id           INT REFERENCES Wine_Types (wine_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Wine_Inventory
               (
                   inv_id      INT PRIMARY KEY,
                   quantity    INT,
                   bottle_date DATE,
                   batch_id    INT REFERENCES Harvest_Batch (batch_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Wine_Order_Details
               (
                   order_detail_id INT PRIMARY KEY,
                   order_quantity  INT,
                   order_id        INT REFERENCES Wine_Orders (order_id),
                   inv_id          INT REFERENCES Wine_Inventory (inv_id)
               )
               """)

################
# SUPPLY TABLES
################

cursor.execute("""
               CREATE TABLE Suppliers
               (
                   supplier_id    INT PRIMARY KEY,
                   name           VARCHAR(60),
                   street_address VARCHAR(60),
                   city           VARCHAR(40),
                   state          VARCHAR(40),
                   contact_name   VARCHAR(40),
                   phone_number   VARCHAR(20),
                   email          VARCHAR(40)
               )
               """)

cursor.execute("""
               CREATE TABLE Supply_Orders
               (
                   order_id      INT PRIMARY KEY,
                   order_date    DATE,
                   expected_date DATE,
                   arrival_date  DATE,
                   supplier_id   INT REFERENCES Suppliers (supplier_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Supply_Types
               (
                   supply_id   INT PRIMARY KEY,
                   name        VARCHAR(60),
                   unit_price  DECIMAL(10, 2),
                   supplier_id INT REFERENCES Suppliers (supplier_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Supply_Inventory
               (
                   inv_id    INT PRIMARY KEY,
                   quantity  INT,
                   supply_id INT REFERENCES Supply_Types (supply_id)
               )
               """)

cursor.execute("""
               CREATE TABLE Supply_Order_Details
               (
                   order_detail_id INT PRIMARY KEY,
                   quantity        INT,
                   order_id        INT REFERENCES Supply_Orders (order_id),
                   inv_id          INT REFERENCES Supply_Inventory (inv_id)
               )
               """)

###################
# EMPLOYEE RECORDS
###################

departments = [
    (1, 'Finance'),
    (2, 'Marketing'),
    (3, 'Production'),
    (4, 'Distribution'),
    (5, 'HR'),
    (6, 'IT')
]
cursor.executemany("INSERT INTO Departments (dept_id, dept_name) VALUES (%s, %s)", departments)

positions = [
    (1, 'Owner', 100000, 200000, None),
    (2, 'Finance Manager', 80000, 100000, 1),
    (3, 'Marketing Manager', 80000, 100000, 2),
    (4, 'Marketing Assistant', 60000, 75000, 2),
    (5, 'Production Manager', 80000, 100000, 3),
    (6, 'Production Lineman', 80000, 100000, 3),
    (7, 'Distribution Manager', 80000, 100000, 4),
]
cursor.executemany("INSERT INTO Positions (position_id, title, min_salary, max_salary, dept_id) VALUES (%s, %s, %s, "
                   "%s, %s)", positions)

# All named employees included, meeting the minimum of 6 entries
employees = [
    (1, 'Stan', 'Bacchus', date(1980, 1, 15).isoformat(), '123 Fake St', 'Sonoma', 'CA', '707-111-1111', None, 1),
    (2, 'Davis', 'Bacchus', date(1982, 2, 15).isoformat(), '234 Fake St', 'Sonoma', 'CA', '707-222-2222', None, 1),
    (3, 'Janet', 'Collins', date(1984, 3, 15).isoformat(), '345 Unreal St', 'Sonoma', 'CA', '707-333-3333', 1, 2),
    (4, 'Roz', 'Murphy', date(1986, 4, 15).isoformat(), '456 Sham St', 'Sonoma', 'CA', '707-444-4444', 2, 3),
    (5, 'Bob', 'Ulrich', date(1988, 5, 15).isoformat(), '567 Phony St', 'Sonoma', 'CA', '707-555-5555', 4, 4),
    (6, 'Henry', 'Doyle', date(1990, 6, 15).isoformat(), '678 Hoax St', 'Sonoma', 'CA', '707-666-6666', 1, 5),
    (7, 'Maria', 'Costanza', date(1992, 7, 15).isoformat(), '789 Fraud St', 'Sonoma', 'CA', '707-777-7777', 2, 7)
]
cursor.executemany("INSERT INTO Employees (employee_id, first_name, last_name, date_of_birth, street_address, city, "
                   "state, phone_number, manager_id, position_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   employees)

# this table has the potential to be HUGE. I am adding 1 entry a quarter for each employee to save time
time_entries = [
    (1, 8, date(2025, 1, 1).isoformat(), 1),
    (2, 8.25, date(2025, 4, 1).isoformat(), 1),
    (3, 9, date(2025, 7, 1).isoformat(), 1),
    (4, 6, date(2025, 10, 1).isoformat(), 1),
    (5, 10, date(2025, 1, 1).isoformat(), 2),
    (6, 7.5, date(2025, 4, 1).isoformat(), 2),
    (7, 8.5, date(2025, 5, 1).isoformat(), 2),
    (8, 9, date(2025, 10, 1).isoformat(), 2),
    (9, 11, date(2025, 1, 1).isoformat(), 3),
    (10, 8, date(2025, 4, 1).isoformat(), 3),
    (11, 8, date(2025, 7, 1).isoformat(), 3),
    (12, 8, date(2025, 10, 1).isoformat(), 3),
    (13, 7.5, date(2025, 1, 1).isoformat(), 4),
    (14, 8, date(2025, 4, 1).isoformat(), 4),
    (15, 8, date(2025, 7, 1).isoformat(), 4),
    (16, 9.75, date(2025, 10, 1).isoformat(), 4),
    (17, 8, date(2025, 1, 1).isoformat(), 5),
    (18, 8, date(2025, 4, 1).isoformat(), 5),
    (19, 10, date(2025, 7, 1).isoformat(), 5),
    (20, 8, date(2025, 10, 1).isoformat(), 5),
    (21, 8, date(2025, 1, 1).isoformat(), 6),
    (22, 8, date(2025, 4, 1).isoformat(), 6),
    (23, 7.75, date(2025, 7, 1).isoformat(), 6),
    (24, 8, date(2025, 10, 1).isoformat(), 6),
    (25, 8, date(2025, 1, 1).isoformat(), 7),
    (26, 9, date(2025, 4, 1).isoformat(), 7),
    (27, 8, date(2025, 7, 1).isoformat(), 7),
    (28, 10, date(2025, 10, 1).isoformat(), 7),
]
cursor.executemany("INSERT INTO Time_Entries (entry_id, hours_worked, work_date, employee_id) VALUES (%s, %s, %s, %s)",
                   time_entries)

###############
# WINE RECORDS
###############

distributors = [
    (1, 'Wine Plus', '987 Fake St', 'Sonoma', 'CA', "Al Anderson", '707-123-4567', 'al@fake.com'),
    (2, 'Wine Lovers', '876 False St', 'Sonoma', 'CA', "Bill Benson", '707-234-5678', 'bill@fake.com'),
    (3, 'Wine Drinkers', '765 Fraud St', 'Sonoma', 'CA', "Charles Clinton", '707-345-6789', 'charles@fake.com'),
    (4, 'Wine Enthusiasts', '654 Hoax St', 'Sonoma', 'CA', "Devon Davis", '707-456-7890', 'devon@fake.com'),
    (5, 'Wine Depot', '543 Dummy St', 'Sonoma', 'CA', "Edward Ellis", '707-567-8901', 'edward@fake.com'),
    (6, 'Wines-r-us', '432 Feign St', 'Sonoma', 'CA', "Frank Freeman", '707-678-9012', 'frank@fake.com')
]
cursor.executemany("INSERT INTO Distributors (distributor_id, name, street_address, city, state, contact_name, "
                   "phone_number, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", distributors)

wine_orders = [
    (1, date(2025, 1, 1).isoformat(), date(2025, 1, 7).isoformat(), 1),
    (2, date(2025, 2, 1).isoformat(), date(2025, 2, 7).isoformat(), 1),
    (3, date(2025, 3, 1).isoformat(), date(2025, 3, 7).isoformat(), 2),
    (4, date(2025, 4, 1).isoformat(), date(2025, 4, 7).isoformat(), 2),
    (5, date(2025, 5, 1).isoformat(), date(2025, 5, 7).isoformat(), 3),
    (6, date(2025, 6, 1).isoformat(), date(2025, 6, 7).isoformat(), 3),
    (7, date(2025, 7, 1).isoformat(), date(2025, 7, 7).isoformat(), 4),
    (8, date(2025, 8, 1).isoformat(), date(2025, 8, 7).isoformat(), 4),
    (9, date(2025, 9, 1).isoformat(), date(2025, 9, 7).isoformat(), 5),
    (10, date(2025, 10, 1).isoformat(), date(2025, 10, 7).isoformat(), 5),
    (11, date(2025, 11, 1).isoformat(), date(2025, 11, 7).isoformat(), 6),
    (12, date(2025, 12, 1).isoformat(), date(2025, 12, 7).isoformat(), 6)
]
cursor.executemany("INSERT INTO Wine_Orders(order_id, order_date, ship_date, distributor_id) VALUES (%s, %s, %s, %s)",
                   wine_orders)

# The case study specifies the vineyard has the following grapes
wines_types = [
    (1, 'Merlot', 15.99),
    (2, 'Cabernet', 18.50),
    (3, 'Chablis', 12.75),
    (4, 'Chardonnay', 14.25)
]
cursor.executemany("INSERT INTO Wine_Types (wine_id, type, bottle_price) VALUES (%s, %s, %s)", wines_types)

harvest_batch = [
    (1, date(2024, 1, 1).isoformat(), 1000, date(2024, 1, 15).isoformat(), 1),
    (2, date(2024, 2, 1).isoformat(), 1000, date(2024, 2, 15).isoformat(), 1),
    (3, date(2024, 3, 1).isoformat(), 1000, date(2024, 3, 15).isoformat(), 2),
    (4, date(2024, 4, 1).isoformat(), 1000, date(2024, 4, 15).isoformat(), 2),
    (5, date(2024, 5, 1).isoformat(), 1000, date(2024, 5, 15).isoformat(), 3),
    (6, date(2024, 6, 1).isoformat(), 1000, date(2024, 6, 15).isoformat(), 4)
]
cursor.executemany("INSERT INTO Harvest_Batch (batch_id, harvest_date, weight, fermentation_date, wine_id) VALUES (%s, "
                   "%s, %s, %s, %s)", harvest_batch)

wine_inv = [
    (1, 700, date(2024, 2, 25).isoformat(), 1),
    (2, 800, date(2024, 3, 25).isoformat(), 1),
    (3, 600, date(2024, 4, 25).isoformat(), 2),
    (4, 900, date(2024, 5, 25).isoformat(), 2),
    (5, 1000, date(2024, 6, 25).isoformat(), 3),
    (6, 400, date(2024, 7, 25).isoformat(), 4)
]
cursor.executemany("INSERT INTO Wine_Inventory (inv_id, quantity, bottle_date, batch_id) VALUES (%s, %s, %s, %s)",
                   wine_inv)

wine_order_details = [
    (1, 50, 1, 1),
    (2, 60, 1, 3),
    (3, 80, 2, 1),
    (4, 40, 2, 2),
    (5, 50, 3, 1),
    (6, 50, 3, 4),
    (7, 100, 4, 5),
    (8, 50, 4, 3),
    (9, 25, 5, 2),
    (10, 70, 5, 1),
    (11, 50, 6, 4),
    (12, 80, 6, 1)
]
cursor.executemany("INSERT INTO Wine_Order_Details (order_detail_id, order_quantity, order_id, inv_id) VALUES (%s, %s, "
                   "%s, %s)", wine_order_details)

#################
# SUPPLY RECORDS
#################

# The case study specifies the vineyard has the following suppliers
suppliers = [
    (1, 'BottleCo', '147 Fake St', 'Sonoma', 'CA', 'Allen Fuller', '707-147-2583', 'allen@unreal.com'),
    (2, 'LabelWorks', '258 Fake St', 'Sonoma', 'CA', 'Barry Hanson', '707-472-5836', 'barry@unreal.com'),
    (3, 'Vats&Tubes', '369 Fake St', 'Sonoma', 'CA', 'Courtney Dawson', '707-725-8369', 'courtney@unreal.com')
]
cursor.executemany("INSERT INTO Suppliers (supplier_id, name, street_address, city, state, contact_name, "
                   "phone_number, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", suppliers)

supply_orders = [
    (1, date(2025, 1, 1).isoformat(), date(2025, 1, 14).isoformat(), date(2025, 1, 15).isoformat(), 1),
    (2, date(2025, 2, 1).isoformat(), date(2025, 2, 14).isoformat(), date(2025, 2, 9).isoformat(), 1),
    (3, date(2025, 3, 1).isoformat(), date(2025, 3, 14).isoformat(), date(2025, 3, 7).isoformat(), 2),
    (4, date(2025, 4, 1).isoformat(), date(2025, 4, 14).isoformat(), date(2025, 4, 12).isoformat(), 3),
    (5, date(2025, 5, 1).isoformat(), date(2025, 5, 14).isoformat(), date(2025, 5, 5).isoformat(), 2),
    (6, date(2025, 6, 1).isoformat(), date(2025, 6, 14).isoformat(), date(2025, 6, 14).isoformat(), 3),
]
cursor.executemany("INSERT INTO Supply_Orders (order_id, order_date, expected_date, arrival_date, supplier_id) VALUES ("
                   "%s, %s, %s, %s, %s)", supply_orders)

supply_types = [
    (1, '375ml bottle', .8, 1),
    (2, 'cork', .25, 1),
    (3, 'label', .03, 1),
    (4, 'box', .8, 6),
    (5, 'vat', .8, 3000),
    (6, 'tubing', .8, 100),
]
cursor.executemany("INSERT INTO Supply_Types (supply_id, name, unit_price, supplier_id) VALUES (%s, %s, %s, %s)",
                   supply_types)

supply_inv = [
    (1, 20000, 1),
    (2, 20000, 2),
    (3, 25000, 3),
    (4, 10000, 4),
    (5, 20, 5),
    (6, 500, 6)
]
cursor.executemany("INSERT INTO Supply_Inventory (inv_id, quantity, supply_id) VALUES (%s, %s, %s)", supply_inv)

supply_order_details = [
    (1, 5000, 1, 1),
    (2, 5000, 1, 2),
    (3, 1000, 2, 2),
    (4, 1000, 2, 1),
    (5, 5000, 3, 3),
    (6, 10, 4, 5),
    (7, 1000, 5, 4),
    (8, 100, 6, 6),
]
cursor.executemany("INSERT INTO Supply_Order_Details (order_detail_id, quantity, order_id, inv_id) VALUES (%s, %s, %s, "
                   "%s)", supply_order_details)

# Commit changes
conn.commit()


# Function to print all rows from a table
def print_table(name):
    cursor.execute(f"SELECT * FROM {name}")
    rows = cursor.fetchall()
    print(f"\n{name}:")
    for row in rows:
        print(row)


# Print all tables
for table_name in ["Departments", "Positions", "Employees", "Time_Entries", "Distributors", "Wine_Orders",
                   "Wine_Types", "Harvest_Batch", "Wine_Inventory", "Wine_Order_Details", "Suppliers",
                   "Supply_Orders", "Supply_Types", "Supply_Inventory", "Supply_Order_Details"]:
    print_table(table_name)

# Close connection
cursor.close()
conn.close()
