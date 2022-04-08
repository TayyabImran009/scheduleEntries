from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

# Admin Panel Title
admin.site.site_header="UKALIGNERS Admin Login"
admin.site.site_title="UKALIGNERS Administration"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #Dentists pages
    path('dentists', views.dentists, name='dentists'),
    #Patients pages
    path('patients', views.patients, name='patients'),
    path('addnewpatient', views.addnewpatient, name='addnewpatient'),
    path('patientdetail/<int:id>/', views.patientdetail, name='patientdetail'),
    path('patientnew', views.patientnew, name='patientnew'),
    path('patientaccepted', views.patientaccepted, name='patientaccepted'),
    path('patientreview', views.patientreview, name='patientreview'),
    path('patientdeclined', views.patientdeclined, name='patientdeclined'),
    path('patientoh', views.patientoh, name='patientoh'),
    path('patienttdv', views.patienttdv, name='patienttdv'),
    path('patientwa', views.patientwa, name='patientwa'),
    path('patientar', views.patientar, name='patientar'),
    path('patienttc', views.patienttc, name='patienttc'),
    path('patientmp', views.patientmp, name='patientmp'),
    path('patientarchived', views.patientarchived, name='patientarchived'),
    #Referrals Pages
    path('referrals', views.referrals, name='referrals'),
    path('refnew', views.refnew, name='refnew'),
    path('addnewreferral', views.addnewreferral, name='addnewreferral'),
    path('referraldetail/<int:id>/', views.referraldetail, name='referraldetail'),
    path('refconsultations', views.refconsultations, name='refconsultations'),
    path('refimplants', views.refimplants, name='refimplants'),
    path('reforthodontics', views.reforthodontics, name='reforthodontics'),
    path('refrootcanals', views.refrootcanals, name='refrootcanals'),
    path('refcrowns', views.refcrowns, name='refcrowns'),
    path('refdeclined', views.refdeclined, name='refdeclined'),
    path('reftc', views.reftc, name='reftc'),
    #SearchResults
    path('patientsearchresults', views.patientsearchresults, name='patientsearchresults'),
    path('referralsearchresults', views.referralsearchresults, name='referralsearchresults'),
    path('paymentfullsearchresultsbypatient', views.paymentfullsearchresultsbypatient, name='paymentfullsearchresultsbypatient'),
    path('incomeexpensesearchresult', views.incomeexpensesearchresult, name='incomeexpensesearchresult'),
    #Payment pages
    path('addpayment', views.addpayment, name='addpayment'),
    path('paymentdailyreport', views.paymentdailyreport, name='paymentdailyreport'),
    path('reportsearchresults', views.reportsearchresults, name='reportsearchresults'),
    path('paymentfullreport', views.paymentfullreport, name='paymentfullreport'),
    path('paymentfullreportarchived', views.paymentfullreportarchived, name='paymentfullreportarchived'),
    path('adminaddincome', views.adminaddincome, name='adminaddincome'),
    path('adminaddexpense', views.adminaddexpense, name='adminaddexpense'),
    path('incomeandexpensereport', views.incomeandexpensereport, name='incomeandexpensereport'),
    path('incomeandexpenserepeat', views.incomeandexpenserepeat, name='incomeandexpenserepeat'),
    path('incomeandexpensereportapproved', views.incomeandexpensereportapproved, name='incomeandexpensereportapproved'),
    path('deleteincome/<int:id>', views.deleteincome, name='deleteincome'),

    path('account', views.account, name='account'),

    path('saveincome/<int:id>', views.saveincome, name='saveincome'),
    path('saveexpense/<int:id>', views.saveexpense, name='saveexpense'),

    path('deleteexpense/<int:id>', views.deleteexpense, name='deleteexpense'),
    path('editincome/<int:id>', views.editincome, name='editincome'),
    path('editexpense/<int:id>', views.editexpense, name='editexpense'),
    path('editincome/updateincome/<int:id>', views.updateincome, name='updateincome'),
    path('editexpense/updateexpense/<int:id>', views.updateexpense, name='updateexpense'),
    #Accounts pages
    path('login', views.loginuser, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logoutuser, name='logout'),
    #Labs pages
    path('addnewlab', views.addnewlab, name='addnewlab'),
    path('labspending', views.labspending, name='labspending'),
    path('labsarchived', views.labsarchived, name='labsarchived'),
    #Order pages
    path('addorder', views.addorder, name='addorder'),
    path('orders', views.orders, name='orders'),
    path('ordersarchived', views.ordersarchived, name='ordersarchived'),
        

    #cdeditor
    path('ckeditor',include('ckeditor_uploader.urls')),


    path('repeatExpense/',views.repeatExpense, name="repeatExpense"),
    path('repeatIncome/', views.repeatIncome, name="repeatIncome"),
    path('startScript/', views.startScript, name="startScript"),

    path('file_download/<int:id>/', views.file_download, name="file_download"),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="restPassword/restPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="restPassword/passwordRestSend.html"),
          name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="restPassword/newPssword.html"),
          name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="restPassword/passwordResetComplete.html"),
          name="password_reset_complete"),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
