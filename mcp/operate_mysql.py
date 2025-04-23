'''
Author: LinYiHan
Date: 2025-04-16 10:00:28
Description: 
Version: 1.0
'''
import mysql.connector
from mysql.connector import Error
from fastmcp import FastMCP
import json
import os


from mysql.connector import pooling

mysql_mcp_name = "MySQLQueryServer"

mcp = FastMCP(mysql_mcp_name)

def get_mysql_config():
    """
    从JSON文件中读取MySQL配置信息。
    优先查找本目录下的cline_mcp_settings.json，不存在则查找上级.vscode目录。
    """
    # config_path = "D:\GitHubWorkSpace\python_test\.cursor\mcp.json"
    try:
        # with open(config_path, "r", encoding="utf-8") as f:
        #     config = json.load(f)
        # mysql_env = config["mcpServers"][mysql_mcp_name]["env"]
        mysql_env = {
            "API_KEY": "benborla29",
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": "3306",
            "MYSQL_USER": "linyihan",
            "MYSQL_PASS": "a5555550123",
            "MYSQL_DB": "ai_interior_design"
        }
        return {
            "host": mysql_env["MYSQL_HOST"],
            "port": int(mysql_env.get("MYSQL_PORT", 3306)),
            "user": mysql_env["MYSQL_USER"],
            "password": mysql_env["MYSQL_PASS"],
            "database": mysql_env["MYSQL_DB"]
        }
    except Exception as e:
        raise RuntimeError(f"读取MySQL配置失败: {e}")

# 全局连接池
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mcp_pool",
    pool_size=5,
    **get_mysql_config()
)

@mcp.tool()
def execute_mysql_query(sql_query: str, max_rows=100) -> str:    
    """
    执行MySQL查询并返回查询结果字符串。

    Args:
        sql_query (str): SQL查询语句。
        max_rows (int, optional): 最多返回的行数，默认为100。

    Returns:
        str: 查询结果的字符串表示。如果发生数据库错误，返回错误信息。

    Raises:
        无

    """
    try:        
        mysql_config = get_mysql_config()
        connection = mysql.connector.connect(**mysql_config)        
        cursor = connection.cursor(dictionary=True)        
        cursor.execute(sql_query)        
        results = cursor.fetchall()
        result_str = ""
        count = 0
        for row in results:
            if count >= max_rows:
                break
            # row是字典，取前两个字段的值
            values = list(row.values())
            if len(values) >= 6:
                result_str += f"{values[0]}:{values[1]},{values[2]},{values[3]},{values[4]},{values[5]}\n"
            else:
                result_str += f"{values}\n"
            count += 1
        result_str = result_str.rstrip("\n")
        print(result_str) 
        return result_str    
    except Error as e:        
        return f"数据库错误: {e}"
    finally:
        try:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
        except:
            pass

if __name__ == "__main__":
    # execute_mysql_query("SELECT * FROM model")  # 执行简单查询
    mcp.run(transport='stdio')  # 通过标准输入输出通信[6,9](@ref)


