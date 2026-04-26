import pymysql
import bcrypt

conn = pymysql.connect(
    host='localhost', user='root', password='123456',
    database='vehicle_parts', charset='utf8mb4'
)
cursor = conn.cursor()

# Clear existing data
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
for table in ['vehicle_part_relation', 'part_info', 'vehicle_info', 'sys_user_role', 'sys_user', 'sys_role']:
    cursor.execute(f'TRUNCATE TABLE {table}')
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

# Seed roles
cursor.execute("INSERT INTO sys_role (id, role_name, role_desc) VALUES (1, 'admin', '超级管理员')")
cursor.execute("INSERT INTO sys_role (id, role_name, role_desc) VALUES (2, 'viewer', '只读用户')")

# Seed admin user
hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt(12)).decode()
cursor.execute(
    "INSERT INTO sys_user (id, username, real_name, password, status) VALUES (1, 'admin', '管理员', %s, 1)",
    (hashed,)
)
viewer_hashed = bcrypt.hashpw(b'viewer123', bcrypt.gensalt(12)).decode()
cursor.execute(
    "INSERT INTO sys_user (id, username, real_name, password, phone, email, status) VALUES (2, 'viewer', '观察员', %s, '13800000002', 'viewer@test.com', 1)",
    (viewer_hashed,)
)
cursor.execute("INSERT INTO sys_user_role (user_id, role_id) VALUES (1, 1)")
cursor.execute("INSERT INTO sys_user_role (user_id, role_id) VALUES (2, 2)")

# Seed vehicles
vehicles = [
    ('VH-001', 'Model 3', 'Model 3 Standard Range', 'Tesla', '2024', 'Electric Motor 3D1/3D2', '特斯拉标准续航版'),
    ('VH-002', 'Model Y', 'Model Y Long Range', 'Tesla', '2024', 'Electric Motor 3D5', '特斯拉长续航版'),
    ('VH-003', '汉EV', '汉 荣耀版', '比亚迪', '2024', 'BYD-476ZQA', '比亚迪汉纯电动'),
    ('VH-004', '秦PLUS', '秦PLUS DM-i', '比亚迪', '2024', 'BYD-472QA', '比亚迪秦插混'),
    ('VH-005', 'BMW 325Li', '3 Series Long Wheelbase', '宝马', '2024', 'B48B20C', '华晨宝马3系长轴'),
    ('VH-006', 'A4L', 'Audi A4L 40 TFSI', '奥迪', '2024', 'DTA', '一汽奥迪A4L'),
]
for v in vehicles:
    cursor.execute(
        "INSERT INTO vehicle_info (vehicle_code, vehicle_name, vehicle_model, brand, year_model, engine_model, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        v
    )

# Seed parts
parts = [
    ('PRT-001', '前刹车片', '制动系统', 'BP-F-001', '陶瓷复合材料', 'Bosch', '套', 350.00, 50, 30, '前轮刹车片套装'),
    ('PRT-002', '后刹车片', '制动系统', 'BP-R-001', '陶瓷复合材料', 'Bosch', '套', 280.00, 45, 30, '后轮刹车片套装'),
    ('PRT-003', '机油滤清器', '过滤系统', 'OF-001', '纸质滤芯', 'Mahle', '个', 45.00, 200, 100, '机油滤芯'),
    ('PRT-004', '空气滤清器', '过滤系统', 'AF-001', '纤维滤纸', 'Mann', '个', 85.00, 150, 80, '空气滤芯'),
    ('PRT-005', '前大灯总成', '照明系统', 'HL-F-L-001', 'LED', 'Hella', '个', 1200.00, 10, 15, '左侧前大灯'),
    ('PRT-006', '前大灯总成', '照明系统', 'HL-F-R-001', 'LED', 'Hella', '个', 1200.00, 8, 15, '右侧前大灯'),
    ('PRT-007', '轮胎', '行走系统', 'TR-225-001', '橡胶', 'Michelin', '条', 850.00, 40, 20, '225/55R18'),
    ('PRT-008', '雨刮片', '附件', 'WB-001', '橡胶+不锈钢', 'Bosch', '对', 120.00, 60, 30, '26寸+18寸'),
    ('PRT-009', '空调滤芯', '过滤系统', 'CF-001', '活性炭', 'Mann', '个', 65.00, 180, 100, '空调系统滤芯'),
    ('PRT-010', '火花塞', '点火系统', 'SP-001', '铱金', 'NGK', '个', 35.00, 300, 150, '铱金火花塞'),
    ('PRT-011', '蓄电池', '电气系统', 'BT-001', '铅酸', 'Varta', '个', 680.00, 15, 10, '12V 60Ah'),
    ('PRT-012', '发电机', '电气系统', 'GN-001', '硅整流', 'Bosch', '个', 1500.00, 5, 8, '14V 150A'),
    ('PRT-013', '水泵', '冷却系统', 'WP-001', '铝合金', 'GMB', '个', 280.00, 20, 15, '发动机水泵'),
    ('PRT-014', '正时皮带', '传动系统', 'TB-001', '橡胶+玻璃纤维', 'Gates', '条', 180.00, 25, 20, '正时皮带套装'),
    ('PRT-015', '减震器', '悬挂系统', 'SH-F-001', '液压油', 'KYB', '个', 450.00, 12, 10, '前减震器'),
]
for p in parts:
    cursor.execute(
        "INSERT INTO part_info (part_code, part_name, category, spec_model, material, supplier, unit, price, stock_qty, safe_stock, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        p
    )

# Seed vehicle-part relations (BOM for VH-001 Tesla Model 3)
relations = [
    (1, 1, 2, '左前轮', '前刹车片套装'),
    (1, 2, 2, '右后轮', '后刹车片套装'),
    (1, 7, 4, '全车', '225/55R18轮胎'),
    (1, 3, 1, '发动机舱', '机油滤芯'),
    (1, 4, 1, '进气系统', '空气滤芯'),
    (1, 5, 1, '左前', 'LED大灯'),
    (1, 6, 1, '右前', 'LED大灯'),
    (1, 8, 2, '前挡风', '雨刮片'),
    (1, 9, 1, '空调系统', '活性炭滤芯'),
    (2, 1, 2, '左前轮', '前刹车片'),
    (2, 7, 4, '全车', '235/50R19轮胎'),
    (3, 1, 2, '前轮', '前刹车片'),
    (3, 3, 1, '发动机舱', '机油滤芯'),
    (4, 8, 2, '前挡风', '雨刮片'),
    (5, 1, 2, '前轮', '前刹车片'),
    (5, 10, 4, '发动机', '铱金火花塞'),
]
for r in relations:
    cursor.execute(
        "INSERT INTO vehicle_part_relation (vehicle_id, part_id, quantity, position_name, remark) VALUES (%s, %s, %s, %s, %s)",
        r
    )

conn.commit()
print(f'Vehicles: {len(vehicles)}')
print(f'Parts: {len(parts)}')
print(f'Relations: {len(relations)}')
print('Users: admin/admin123, viewer/viewer123')
conn.close()
print('Done!')
