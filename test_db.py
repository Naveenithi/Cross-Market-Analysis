import mysql.connector

try:
    conn = mysql.connector.connect(
        host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",          # change if using TiDB
        user="2E7RXmh1PwAwo6G.root",
        password="7oxoP3UUnvifoJrR",  # replace with your MySQL password
        database="cross_market"
    )

    print("✅ Connected successfully!")

    conn.close()

except Exception as e:
    print("❌ Connection Failed")
    print("Error:", e)