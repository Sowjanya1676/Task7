import mysql.connector
import pandas as pd
import matplotlib as plt

# Step 1: Connect to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',         # Replace with your MySQL username
    password='purna',  # Replace with your MySQL password
    database='CU'   # Replace with your database name
)

cursor = connection.cursor()

# Step 2: Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS online_sale (
    orderID INT,
    product VARCHAR(50),
    quantity INT,
    price VARCHAR(50)
)
"""
cursor.execute(create_table_query)
print("Table created successfully (if not already present).")

# Step 3: Insert new records into the table
insert_query = "INSERT INTO online_sale (orderID, product, quantity, price) VALUES (%s,%s, %s, %s)"
data=[(1,'Apple', 10, 0.5),
(2,'Banana', 20, 0.3),
(3,'Apple', 5, 0.5),
(4,'Orange', 7, 0.6),
(5,'Banana', 15, 0.3)
]

cursor.executemany(insert_query, data)
connection.commit()
print(cursor.rowcount, "record(s) inserted successfully.")
# Step 4: Query data from the table and write it to a CSV file
query = "SELECT product,sum(quantity) as total_qty,sum(quantity*price) as revenue FROM online_sale group by product"
cursor.execute(query)
# Fetch all data from the query
result = cursor.fetchall()
print("select is executed")
df=pd.read_sql(query, connection) 
print("sales summary:")
print(df)
# Step 5: Plot a basic bar chart of revenue by product
df.plot(kind='bar', x='product', y='revenue', legend=False, color='orange')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")  # Optional: save the chart as an image
plt.show()

# Step 6: Close the connection
connection.close()
