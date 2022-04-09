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

con = sqlite3.connect('/home/pi/bhl/bhl_gnioki/interface/interface/db.sqlite3')
con.row_factory = sqlite3.Row
cursor = con.cursor()
con.commit()
cursor.execute("SELECT name FROM sqlite_master;")
con.commit()
print(cursor.fetchall())
cursor.close()
con.close()