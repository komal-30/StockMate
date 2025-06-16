import mysql.connector
from mysql.connector import errorcode

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',       # <-- replace with your MySQL username
            password='Komal@325740',   # <-- replace with your MySQL password
            database='inventory_db'            # <-- replace with your MySQL database name
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password is incorrect.")
        else:
            print(err)
        return None

def setup_database():
    conn = create_connection()
    if conn is None:
        print("Connection failed. Setup aborted.")
        return
    cursor = conn.cursor()

    # Create operators table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operators (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
    """)

    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        barcode VARCHAR(255),
        sku VARCHAR(255),
        category VARCHAR(255),
        subcategory VARCHAR(255),
        image_path VARCHAR(255),
        name VARCHAR(255),
        description TEXT,
        tax FLOAT,
        price FLOAT,
        unit VARCHAR(100)
    )
    """)

    # Create goods_receiving table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goods_receiving (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        supplier_name VARCHAR(255),
        quantity FLOAT,
        unit VARCHAR(100),
        rate_per_unit FLOAT,
        total_rate FLOAT,
        tax FLOAT,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # Create sales table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        customer_name VARCHAR(255),
        quantity FLOAT,
        unit VARCHAR(100),
        rate_per_unit FLOAT,
        total_rate FLOAT,
        tax FLOAT,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # Insert two operator users if not exist (MySQL doesn't have INSERT OR IGNORE; use INSERT ... ON DUPLICATE KEY UPDATE)
    cursor.execute("""
    INSERT INTO operators (username, password) VALUES ('operator1', '1234')
    ON DUPLICATE KEY UPDATE username=username
    """)
    cursor.execute("""
    INSERT INTO operators (username, password) VALUES ('operator2', 'abcd')
    ON DUPLICATE KEY UPDATE username=username
    """)

    conn.commit()
    cursor.close()
    conn.close()
