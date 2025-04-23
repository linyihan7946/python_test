'''
Author: LinYiHan
Date: 2025-04-15 21:27:22
Description: 
Version: 1.0
'''
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="linyihan",
        password="a5555550123",
        database="ai_interior_design"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model")  # 执行简单查询
    # 获取全部结果
    results = cursor.fetchall()
    # 按列索引访问
    for row in results:
        print(row) 

    print("数据库连接成功！")
except mysql.connector.Error as err:
    print(f"连接失败：{err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()