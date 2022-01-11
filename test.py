import schedule
import time
# from portfolioApp.models import Expense
# Create your views here.
import sqlite3

def job():
	# expenseObj = Expense.objects.create(Date="2022/01/11", Title="T1", Category="C1", Account="A1", Amount="A1", Status="S1", Note="N1", Repeat="r")
	# expenseObj.save()
	try:
		sqliteConnection = sqlite3.connect('db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")

		sqlite_insert_query = """INSERT INTO portfolioApp_expense
							(Date, Title, Category, Account, Amount, Status, Note, Repeat) 
							VALUES 
							('2022-01-11','T1','C1','A1', 'A1', 'S1', 'N1', 'r')"""

		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
		cursor.close()

	except sqlite3.Error as error:
		print("Failed to insert data into sqlite table", error)
	finally:
		if sqliteConnection:
			sqliteConnection.close()
			print("The SQLite connection is closed")


	print("Hello 1 min has passed")

schedule.every(1).minutes.do(job)

while True:
	schedule.run_pending()
	time.sleep(1) 

# job()

# def deleteRecord():
#     try:
#         sqliteConnection = sqlite3.connect('db.sqlite3')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")

#         # Deleting single record now
#         sql_delete_query = """DELETE from portfolioApp_expense where id = 2"""
#         cursor.execute(sql_delete_query)
#         sqliteConnection.commit()
#         print("Record deleted successfully ")
#         cursor.close()

#     except sqlite3.Error as error:
#         print("Failed to delete record from sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")

# deleteRecord()