import sqlite3
# # con = sqlite3.connect('db.sqlite3')
# # print(con)
# # print('Connected to database successfully.')
# #
# # cur = con.cursor()
# # cur.execute("SELECT * FROM 'hmi_appointment'")
# #
# # rows = cur.fetchall()
# # for row in rows:
# #     print(row[2])

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())