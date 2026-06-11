from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost:3306/crmdb")
try:
    connection = engine.connect()
    print("✅ MySQL Connected Successfully")
    connection.close()

except Exception as e:
    print("❌ Connection Failed")
    print(e)