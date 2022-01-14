import schedule
import time
# from portfolioApp.models import Expense
# Create your views here.
import sqlite3

# def job():
# 	# expenseObj = Expense.objects.create(Date="2022/01/11", Title="T1", Category="C1", Account="A1", Amount="A1", Status="S1", Note="N1", Repeat="r")
# 	# expenseObj.save()
# 	try:
# 		sqliteConnection = sqlite3.connect('db.sqlite3')
# 		cursor = sqliteConnection.cursor()
# 		print("Successfully Connected to SQLite")

# 		sqlite_insert_query = """INSERT INTO portfolioApp_expense
# 							(Date, Title, Category, Account, Amount, Status, Note, Repeat) 
# 							VALUES 
# 							('2022-01-11','T1','C1','A1', 'A1', 'S1', 'N1', 'r')"""

# 		count = cursor.execute(sqlite_insert_query)
# 		sqliteConnection.commit()
# 		print("Record inserted successfully into SqliteDb_expence table ", cursor.rowcount)
# 		cursor.close()

# 	except sqlite3.Error as error:
# 		print("Failed to insert data into expence sqlite table", error)
# 	finally:
# 		if sqliteConnection:
# 			sqliteConnection.close()
# 			print("The SQLite connection is closed")

# 	try:
# 		sqliteConnection = sqlite3.connect('db.sqlite3')
# 		cursor = sqliteConnection.cursor()
# 		print("Successfully Connected to SQLite")

# 		sqlite_insert_query = """INSERT INTO portfolioApp_income
# 							(Date, Title, Category, Account, Amount, Status, Note, Repeat, RepeatStatus) 
# 							VALUES 
# 							('2022-01-11','T1','C1','A1', 'A1', 'S1', 'N1', 'r','off')"""

# 		count = cursor.execute(sqlite_insert_query)
# 		sqliteConnection.commit()
# 		print("Record inserted successfully into SqliteDb_income table ", cursor.rowcount)
# 		cursor.close()

# 	except sqlite3.Error as error:
# 		print("Failed to insert data into sqlite income table", error)
# 	finally:
# 		if sqliteConnection:
# 			sqliteConnection.close()
# 			print("The SQLite connection is closed")


# 	print("Hello 1 min has passed")

# schedule.every(1).minutes.do(job)

# while True:
# 	schedule.run_pending()
# 	time.sleep(1) 

# job()

def deleteRecord():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from portfolioApp_expense where id = 73"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

deleteRecord()


def job():
		try:
			sqliteConnection = sqlite3.connect('db.sqlite3')
			cursor = sqliteConnection.cursor()
			print("Successfully Connected to SQLite")
			
			sqlite_get_query = """SELECT * FROM portfolioApp_repeatexpense"""

			count = cursor.execute(sqlite_get_query)
			for c in count:
				try:
					sqliteConnection2 = sqlite3.connect('db.sqlite3')
					cursor2 = sqliteConnection2.cursor()
					print("Successfully Connected to SQLite")
					print(type(c[1]))
					strDate = str(c[1])
					print(strDate)
					sqlite_insert_query = """INSERT INTO portfolioApp_expense
										(Date, Title, Category, Account, Amount, Status, Note, Repeat) 
										VALUES 
										('{}','{}','{}','{}', '{}', '{}', '{}', '{}')""".format(strDate,c[2],c[3],c[4],c[5],c[6],c[7],c[8])
					print("Query created", sqlite_insert_query)
					count2 = cursor2.execute(sqlite_insert_query)
					print("exicuted")
					sqliteConnection2.commit()
					print("Record inserted successfully into SqliteDb_expence table ", cursor2.rowcount)
					cursor2.close()

				except sqlite3.Error as error:
					print("Failed to insert data into expence sqlite table", error)
				finally:
					if sqliteConnection2:
						sqliteConnection2.close()
						print("The SQLite connection is closed")
					sqliteConnection2.commit()
					print("Record inserted successfully into SqliteDb_expence table ", cursor2.rowcount)
					cursor2.close()
				time.sleep(30)

		except sqlite3.Error as error:
			print("Failed to get data", error)
		finally:
			if sqliteConnection:
				sqliteConnection.close()
				print("The SQLite connection is closed")

		try:
			sqliteConnection = sqlite3.connect('db.sqlite3')
			cursor = sqliteConnection.cursor()
			print("Successfully Connected to SQLite")
			
			sqlite_get_query = """SELECT * FROM portfolioApp_repeatincome"""

			count = cursor.execute(sqlite_get_query)
			for c in count:
				try:
					sqliteConnection2 = sqlite3.connect('db.sqlite3')
					cursor2 = sqliteConnection2.cursor()
					print("Successfully Connected to SQLite")
					print(type(c[1]))
					strDate = str(c[1])
					print(strDate)
					sqlite_insert_query = """INSERT INTO portfolioApp_income
										(Date, Title, Category, Account, Amount, Status, Note, Repeat, RepeatStatus) 
										VALUES 
										('{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}')""".format(strDate,c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9])
					print("Query created", sqlite_insert_query)
					count2 = cursor2.execute(sqlite_insert_query)
					print("exicuted")
					sqliteConnection2.commit()
					print("Record inserted successfully into SqliteDb_income table ", cursor2.rowcount)
					cursor2.close()

				except sqlite3.Error as error:
					print("Failed to insert data into expence sqlite table", error)
				finally:
					if sqliteConnection2:
						sqliteConnection2.close()
						print("The SQLite connection is closed")
					sqliteConnection2.commit()
					print("Record inserted successfully into SqliteDb_expence table ", cursor2.rowcount)
					cursor2.close()
				time.sleep(30)

		except sqlite3.Error as error:
			print("Failed to get data", error)
		finally:
			if sqliteConnection:
				sqliteConnection.close()
				print("The SQLite connection is closed")