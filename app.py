from flask import Flask
import json
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(host='localhost',
                            database='orderworkflow',
                            user='postgres',
                            password='jinny5527024')



# create cursor obj to interact with db
cursor = conn.cursor()

# SQL commands
INSERT_CUSTOMER = """INSERT INTO customers (customer_id, name, email, address) VALUES (%s, %s, %s, %s) RETURNING id;"""
INSERT_PRODUCT = """INSERT INTO products (product_id name, price) VALUES (%s, %s, %s) RETURNING id;"""

GET_CUSTOMER = """SELECT id FROM customers WHERE email = %s"""
GET_PRODUCT = """SELECT id FROM products WHERE name = %s"""

UPDATE_CUSTOMER = """UPDATE customers
                SET {fields_to_update}
                WHERE customer_id = %s""" 
UPDATE_PRODUCT = """UPDATE products
                SET {fields_to_update}
                WHERE product_id = %s"""


# # insert customer into PostgreSQL, or update if already exists
# def insert_or_update_customer(cust_data):
#     try:
#         cursor.execute(GET_CUSTOMER, cust_data["customer_id"])
#         results = cursor.fetchone()

#         # if customer already exists
#         if results:
#             customer_id, name, email, address = results
#             updates = []
#             update_values = []
#             if cust_data["name"] != name:
#                 updates.append("name = %s")
#                 update_values.append(cust_data["name"])

#             if cust_data["email"] != email:
#                 updates.append("email = %s")
#                 update_values.append(cust_data["email"])
            
#             if cust_data["address"] != json.loads(address):
#                 updates.append("address = %s")
#                 update_values.append(json.dumps(cust_data["address"]))
            
#             if updates:
#                 # Use dynamically generated fields for the update
#                 update_query = UPDATE_CUSTOMER.format(fields_to_update=", ".join(updates))
#                 update_values.append(customer_id)
#                 cursor.execute(update_query, tuple(update_values))
#                 print(f"Customer {cust_data['name']} ({cust_data['customer_id']}) updated.")
#             else:
#                 print(f"No changes for customer {cust_data['name']} ({cust_data['customer_id']}).")

#         else:
#             # insert customer if not exist
#             customer_id = cursor.fetchone()[0]
#             cursor.execute(INSERT_CUSTOMER, 
#                            (cust_data['customer_id'], cust_data["name"], cust_data["email"], json.dumps(cust_data["address"])))
#             print(f"Customer {cust_data['name']} inserted with ID {customer_id}.")   
        
#     except Exception:
#         print("Error inserting customer")
#         conn.rollback()
#         return None
    

# # insert customer into PostgreSQL, or update if already exists
# def insert_or_update_product(product_data):
#     try:
#         cursor.execute(GET_PRODUCT, product_data["product_id"])
#         results = cursor.fetchone()

#         # if customer already exists
#         if results:
#             product_id, name, price = results
#             updates = []
#             update_values = []
#             if product_data["name"] != name:
#                 updates.append("name = %s")
#                 update_values.append(product_data["name"])

#             if product_data["price"] != price:
#                 updates.append("price = %s")
#                 update_values.append(product_data["price"])
            
#             if updates:
#                 # Use dynamically generated fields for the update
#                 update_query = UPDATE_PRODUCT.format(fields_to_update=", ".join(updates))
#                 update_values.append(product_id)
#                 cursor.execute(update_query, tuple(update_values))
#                 print(f"Product {product_data['name']} ({product_data['product_id']}) updated.")
#             else:
#                 print(f"No changes for customer {product_data['name']} ({product_data['product_id']}).")

#         else:
#             # insert product if not exist
#             product_id = cursor.fetchone()[0]
#             cursor.execute(INSERT_PRODUCT, 
#                            (product_data['product_id'], product_data["name"], product_data["price"]))
#             print(f"Customer {product_data['name']} inserted with ID {product_id}.")   
        
#     except Exception:
#         print("Error inserting product")
#         conn.rollback()
#         return None
    

# insert either customer or product into PostgreSQL, or update if already exists
def insert_or_update(object, object_data):
    if object == "customer":
        get = GET_CUSTOMER
        insert = INSERT_CUSTOMER
        update = UPDATE_CUSTOMER
    elif object == "product":
        get = GET_PRODUCT
        insert = INSERT_PRODUCT
        update = UPDATE_PRODUCT

    try:
        cursor.execute(get, object_data[f"{object}_id"])
        results = cursor.fetchone() # results from PostgreSQL: the keys of the data (e.g. name, email, price, etc.)

        # if object already exists
        if results:
            names_column = [description[0] for description in cursor.description]
            updates = []
            update_values = []

            for field, value in object_data.items():
                # if field in JSON is not equal to object_id and if the value is not equal to 
                if field not in [f"{object}_id"] and value != results[field_names.index(field)]:
                    updates.append(f"{field} = %s")
                    update_values.append(value)

    try:
        cursor.execute(GET_CUSTOMER, cust_data["customer_id"])
        results = cursor.fetchone()

        # if customer already exists
        if results:
            customer_id, name, email, address = results
            updates = []
            update_values = []
            if cust_data["name"] != name:
                updates.append("name = %s")
                update_values.append(cust_data["name"])

            if cust_data["email"] != email:
                updates.append("email = %s")
                update_values.append(cust_data["email"])
            
            if cust_data["address"] != json.loads(address):
                updates.append("address = %s")
                update_values.append(json.dumps(cust_data["address"]))
            
            if updates:
                # Use dynamically generated fields for the update
                update_query = UPDATE_CUSTOMER.format(fields_to_update=", ".join(updates))
                update_values.append(customer_id)
                cursor.execute(update_query, tuple(update_values))
                print(f"Customer {cust_data['name']} ({cust_data['customer_id']}) updated.")
            else:
                print(f"No changes for customer {cust_data['name']} ({cust_data['customer_id']}).")

        else:
            # insert customer if not exist
            customer_id = cursor.fetchone()[0]
            cursor.execute(INSERT_CUSTOMER, 
                           (cust_data['customer_id'], cust_data["name"], cust_data["email"], json.dumps(cust_data["address"])))
            print(f"Customer {cust_data['name']} inserted with ID {customer_id}.")   
        
    except Exception:
        print("Error inserting customer")
        conn.rollback()
        return None
    


# parse through json and insert
def json_to_db(json_file, conn, cursor):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    for dataset in data['datasets']:
        if dataset['datasetName'] == 'customers':
            for customer in dataset['fields']:
                customer_id = insert_or_update("customer", customer)
                if customer_id:
                    print(f"Customer {customer['name']} inserted with ID {customer_id}")

        elif dataset['datasetName'] == 'products':
            for product in dataset['fields']:
                product_id = insert_or_update("product", product)
                if product_id:
                    print(f"Product {product['name']} inserted with ID {product_id}")