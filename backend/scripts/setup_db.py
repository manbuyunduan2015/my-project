import pymysql
import bcrypt

conn = pymysql.connect(host='localhost', user='root', password='123456', charset='utf8mb4')
cursor = conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS vehicle_parts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
print('Database created')
cursor.execute('USE vehicle_parts')

tables = [
    '''CREATE TABLE IF NOT EXISTS sys_role (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE,
        role_desc VARCHAR(200),
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS sys_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        real_name VARCHAR(50) NOT NULL,
        password VARCHAR(200) NOT NULL,
        phone VARCHAR(20),
        email VARCHAR(100),
        status INT DEFAULT 1,
        is_deleted INT DEFAULT 0,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS sys_user_role (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        role_id INT NOT NULL,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sys_user(id),
        FOREIGN KEY (role_id) REFERENCES sys_role(id)
    )''',
    '''CREATE TABLE IF NOT EXISTS vehicle_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_code VARCHAR(50) NOT NULL UNIQUE,
        vehicle_name VARCHAR(100) NOT NULL,
        vehicle_model VARCHAR(100),
        brand VARCHAR(50),
        year_model VARCHAR(20),
        engine_model VARCHAR(50),
        description TEXT,
        is_deleted INT DEFAULT 0,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS part_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        part_code VARCHAR(50) NOT NULL UNIQUE,
        part_name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        spec_model VARCHAR(100),
        material VARCHAR(100),
        supplier VARCHAR(100),
        unit VARCHAR(20),
        price DECIMAL(10,2) DEFAULT 0,
        stock_qty INT DEFAULT 0,
        safe_stock INT DEFAULT 0,
        description TEXT,
        is_deleted INT DEFAULT 0,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS vehicle_part_relation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_id INT NOT NULL,
        part_id INT NOT NULL,
        quantity INT DEFAULT 1,
        position_name VARCHAR(100),
        remark TEXT,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle_info(id),
        FOREIGN KEY (part_id) REFERENCES part_info(id),
        UNIQUE KEY uk_vehicle_part (vehicle_id, part_id)
    )''',
]

for sql in tables:
    cursor.execute(sql)
print('All tables created')

# Seed roles
cursor.execute("INSERT IGNORE INTO sys_role (id, role_name, role_desc) VALUES (1, 'admin', '超级管理员')")
cursor.execute("INSERT IGNORE INTO sys_role (id, role_name, role_desc) VALUES (2, 'viewer', '只读用户')")

# Seed admin user
hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt(12)).decode()
cursor.execute(
    "INSERT IGNORE INTO sys_user (id, username, real_name, password, status) VALUES (1, 'admin', '管理员', %s, 1)",
    (hashed,)
)
cursor.execute("INSERT IGNORE INTO sys_user_role (user_id, role_id) VALUES (1, 1)")
conn.commit()
print('Seed data inserted. Admin user: admin/admin123')
conn.close()
