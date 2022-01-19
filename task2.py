import os
from datetime import date
# from safe_schedule import SafeScheduler
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UKAligners.settings")
import django
django.setup()

import schedule
import time
from portfolioApp.models import Income, RepeatIncome, RepeatExpense, Expense

def job():
	if date.today().day == 1:
		ri=RepeatIncome.objects.all()
		for r in ri:
			Date=r.Date
			Title=r.Title
			Category=r.Category
			Account=r.Account
			Amount=r.Amount
			Status=r.Status
			Note=r.Note
			Repeat=r.Repeat
			RepeatStatus=r.RepeatStatus
			income=Income(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note,Repeat=Repeat,RepeatStatus=RepeatStatus)
			print(income)
			income.save()

		re = RepeatExpense.objects.all()
		for r in re:
			Date=r.Date
			Title=r.Title
			Category=r.Category
			Account=r.Account
			Amount=r.Amount
			Status=r.Status
			Note=r.Note
			expense=Expense(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note)
			expense.save()
		print("Data Entered")

def entries():
	print("Starting to add data")
	schedule.every().day.at("00:00").do(job)
	while True:
		schedule.run_pending()
		time.sleep(1)

print("Hello I am working")
entries()