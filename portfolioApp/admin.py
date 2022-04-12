from django.contrib import admin
from .models import Patient,PatientProposedTreatment,DentistProfile,Referral,TreatmentRequestFile,ImageUploadAdmin,Payment,Income,Expense,IncomeExpenseTitle,IncomeExpenseCategory,LabWork,Order,RepeatExpense, RepeatIncome, userType,UpperArchBox,LowerArchBox
# Register your models here.
admin.site.register(Patient)
admin.site.register(PatientProposedTreatment)
admin.site.register(DentistProfile)
admin.site.register(Referral)
admin.site.register(TreatmentRequestFile)
admin.site.register(ImageUploadAdmin)
admin.site.register(Payment)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(IncomeExpenseTitle)
admin.site.register(IncomeExpenseCategory)
admin.site.register(LabWork)
admin.site.register(Order)
# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Querie)
# admin.site.register(Answer)

admin.site.register(RepeatExpense)
admin.site.register(RepeatIncome)

admin.site.register(userType)

admin.site.register(UpperArchBox)
admin.site.register(LowerArchBox)