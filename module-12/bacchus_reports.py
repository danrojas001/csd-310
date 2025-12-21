import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # insert password
    database="bacchus_winery"
)

cursor = conn.cursor()

print("\n========== SUPPLY DELIVERY REPORT ==========")

# Query expected/actual delivery dates
deliveries = """
             SELECT
                 S.name,
                 O.order_id,
                 O.expected_date,
                 O.arrival_date,
                 DATEDIFF(O.expected_date, O.arrival_date) AS difference
             FROM
                 supply_orders AS O
                     INNER JOIN
                 suppliers AS S
                 ON
                     O.supplier_id = S.supplier_id
             ORDER BY
                 O.order_id
             """

cursor.execute(deliveries)
supply_delivery_data = cursor.fetchall()
for name, order_id, expected_date, arrival_date, difference in supply_delivery_data:
    if difference < 0:
        print(f"Supplier: {name} | Order_id: {order_id} | Expected date: {expected_date} | Arrival date: "
              f"{arrival_date} | Late by {abs(difference)} days")
    elif difference == 0 :
        print(f"Supplier: {name} | Order_id: {order_id} | Expected date: {expected_date} | Arrival date: "
              f"{arrival_date} | On Schedule")
    else:
        print(f"Supplier: {name} | Order_id: {order_id} | Expected date: {expected_date} | Arrival date: "
              f"{arrival_date} | Early by {difference} days")
print("========== SUPPLY DELIVERY REPORT ==========\n")



print("\n========== WINE SALES REPORT ==========")

# Query total wine sales
total_sales = """
              SELECT
                  wt.type AS wine_type,
                  wt.bottle_price,
                  COALESCE(SUM(wod.order_quantity), 0) AS total_bottles,
                  COALESCE(SUM(wod.order_quantity * wt.bottle_price), 0) AS total_revenue
              FROM Wine_Types wt
                       LEFT JOIN Harvest_Batch hb ON hb.wine_id = wt.wine_id
                       LEFT JOIN Wine_Inventory wi ON wi.batch_id = hb.batch_id
                       LEFT JOIN Wine_Order_Details wod ON wod.inv_id = wi.inv_id
              GROUP BY wt.type, wt.bottle_price
              ORDER BY wt.type; \
              """

cursor.execute(total_sales)
wine_sales = cursor.fetchall()

print("--- Wine Revenue ---")
for row in wine_sales:
    wine_type, price, total_bottles, total_revenue = row
    print(f"{wine_type} | Price: ${price:.2f} | Total Sold: {total_bottles} bottles | Total Revenue: ${total_revenue:.2f}")


print("\n--- Underperforming Wines ---")
for wine_type, price, total_bottles, total_revenue in wine_sales:
    if total_bottles == 0:
        print(f"{wine_type} is underperforming with {total_bottles} bottles sold.")

# Query showing which distributor bought which wine
distributor = """
              SELECT
                  d.name AS distributor,
                  wt.type AS wine_name,
                  SUM(wod.order_quantity) AS total_bought
              FROM Distributors d
                       JOIN Wine_Orders wo ON d.distributor_id = wo.distributor_id
                       JOIN Wine_Order_Details wod ON wo.order_id = wod.order_id
                       JOIN Wine_Inventory wi ON wod.inv_id = wi.inv_id
                       JOIN Harvest_Batch hb ON wi.batch_id = hb.batch_id
                       JOIN Wine_Types wt ON hb.wine_id = wt.wine_id
              GROUP BY d.name, wt.type
              ORDER BY d.name, wt.type; \
              """
cursor.execute(distributor)
dist_data = cursor.fetchall()

print("\n--- Distributor Wine Purchases ---")
for distributor, wine_name, total_bought in dist_data:
    print(f"{distributor} bought {total_bought} bottles of {wine_name}")
print("========== WINE SALES REPORT ==========\n")



print("\n========== EMPLOYEE WORK HOURS REPORT ==========")

# Query total hours per employee for each quarter
hours = """
        SELECT
            e.first_name,
            e.last_name,
            CONCAT(YEAR(te.work_date), '-Q', QUARTER(te.work_date)) AS quarter,
            SUM(te.hours_worked) AS total_hours
        FROM Employees e
                 LEFT JOIN Time_Entries te ON e.employee_id = te.employee_id
        GROUP BY e.employee_id, quarter
        ORDER BY e.employee_id, quarter; \
        """

cursor.execute(hours)
hours_data = cursor.fetchall()

print("--- Hours Worked Per Employee Each Quarter ---")
for first_name, last_name, quarter, total_hours in hours_data:
    print(f"{first_name} {last_name} | {quarter} | Hours Worked: {total_hours}")
print("========== EMPLOYEE WORK HOURS REPORT ==========")


cursor.close()
conn.close()
