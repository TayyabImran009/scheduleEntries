from celery import shared_task
import schedule
import time
from portfolioApp.models import Income, RepeatIncome, RepeatExpense, Expense

def job():
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

@shared_task(name="entries")
def entries():
	schedule.every(1).minutes.do(job)

	while True:
		schedule.run_pending()
		time.sleep(1)
