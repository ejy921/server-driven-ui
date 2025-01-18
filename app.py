# Few concerns:
# - Object-oriented route?
# - pass cursor as argument, or it's okay?

from flask import Flask, jsonify
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
CREATE_ORDERS = """CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, name TEXT);"""
CREATE_WORKFLOWS = """CREATE TABLE IF NOT EXISTS workflows (id SERIAL PRIMARY KEY, name TEXT);"""

INSERT_CUSTOMER = """INSERT INTO customers (customer_id, name, email, address) VALUES (%s, %s, %s, %s) RETURNING customer_id;"""
INSERT_PRODUCT = """INSERT INTO products (product_id, name, price) VALUES (%s, %s, %s) RETURNING product_id;"""
INSERT_ORDER = """INSERT INTO orders (customer_id, payment_method, total_price) VALUES (%s, %s, %s) RETURNING order_id;""" 
INSERT_WORKFLOW = """INSERT INTO workflowsteps (order_id, customer_id, payment_method, total_price) VALUES (%s, %s, %s, %s) RETURNING workflow_id;"""

GET_CUSTOMERS = """SELECT * FROM customers"""
GET_PRODUCTS = """SELECT * FROM products"""
GET_CUSTOMER = """SELECT * FROM customers WHERE customer_id = %s"""
GET_PRODUCT = """SELECT * FROM products WHERE product_id = %s"""

UPDATE_CUSTOMER = """UPDATE customers
                SET {fields_to_update}
                WHERE customer_id = %s""" 
UPDATE_PRODUCT = """UPDATE products
                SET {fields_to_update}
                WHERE product_id = %s"""

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
    else:
        print("Cannot identify object type")
        return None

    try:
        # serialize to JSON if value is dictionary (customer address)
        for field, value in object_data.items():
            if isinstance(value, dict):
                object_data[field] = json.dumps(value)

        cursor.execute(get, (object_data[f"{object}_id"],))
        results = cursor.fetchone() # results from PostgreSQL: the keys of the data (e.g. name, email, price, etc.)

        # if object already exists
        if results:
            names_column = [description[0] for description in cursor.description]
            updates = []
            update_values = []

            for field, value in object_data.items():
                # if field in JSON is not equal to object_id and if the value is not equal to 
                if field not in [f"{object}_id"] and value != results[names_column.index(field)]:
                    updates.append(f"{field} = %s")
                    update_values.append(value)

            if updates:
                update_query = update.format(fields_to_update=",".join(updates))
                update_values.append(results[0]) # append object_id
                cursor.execute(update_query, tuple(update_values))
                print(f"Object {object_data['name']} ({object_data[f"{object}_id"]}) updated.")
            else:
                print(f"No changes for object {object_data['name']} ({object_data[f"{object}_id"]}).")

        else:
            # insert object if not exist
            cursor.execute(insert, tuple(object_data.values()))
            entity_id = cursor.fetchone()[0]
            print(f"{object} {object_data['name']} inserted with ID {entity_id}.")  
        
        conn.commit()
        
    except Exception as e:
        print(f"Error inserting object {e}")
        conn.rollback()
        return None
    
# parse through json and insert
def json_to_db(json_file):
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


json_to_db("schema.json")


@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        cursor.execute(GET_PRODUCTS)
        products = cursor.fetchall()
        # format products as dictionary
        product_list = [
            {"index": idx, "id": row[0], "name": row[1], "price": float(row[2])}
            for idx, row in enumerate(products)
        ]

        return jsonify(product_list), 200 # HTML code for successful request
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
print(get_products())




    
