from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from .models import LabWork, Patient,User,PatientProposedTreatment, DentistProfile,Referral,TreatmentRequestFile,ImageUploadAdmin,Payment,Income,Expense,IncomeExpenseTitle,IncomeExpenseCategory,LabWork,Order,RepeatExpense,RepeatIncome
from django.contrib.auth.forms import UserCreationForm
from .forms import DentistProfileForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import schedule
import time
from tasks import entries
# Create your views here.

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        #Patients
        totalpatientscount=Patient.objects.count()
        newpatientscount=Patient.objects.filter(Status="New").count()
        acceptedpatientscount=Patient.objects.filter(Status="Accepted").count()
        reviewpatientscount=Patient.objects.filter(Status="Review").count()
        declinedpatientscount=Patient.objects.filter(Status="Declined").count()
        ohpatientscount=Patient.objects.filter(Status="On Hold").count()
        wapatientscount=Patient.objects.filter(InternalStatus="Waiting Acceptance").count()
        tdvpatientscount=Patient.objects.filter(InternalStatus="3D View").count()
        mppatientscount=Patient.objects.filter(InternalStatus="Model Production").count()
        arpatientscount=Patient.objects.filter(InternalStatus="Aligners Ready").count()
        tcpatientscount=Patient.objects.filter(InternalStatus="TC").count()
        archivedpatientcount=Patient.objects.filter(InternalStatus="Archived").count()
        #Referrals
        reftotalcount=Referral.objects.count()
        refnewcount=Referral.objects.filter(Status="New").count()
        refconsultationscount=Referral.objects.filter(TreatmentPlan="Consultation").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()
        refimplantscount=Referral.objects.filter(TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        reforthodonticscount=Referral.objects.filter(TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        refrootcanalcount=Referral.objects.filter(TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        refcrownnveneerscount=Referral.objects.filter(TreatmentPlan="Crown").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()      
        refdeclinedcount=Referral.objects.filter(Status="Declined").count()       
        reftccount=Referral.objects.filter(Status="TC").count()       
    else:
        #Patients
        totalpatientscount=Patient.objects.filter(Dentist=request.user).count()
        newpatientscount=Patient.objects.filter(Dentist=request.user,Status="New").count()
        acceptedpatientscount=Patient.objects.filter(Dentist=request.user,Status="Accepted").count()
        reviewpatientscount=Patient.objects.filter(Dentist=request.user,Status="Review").count()
        declinedpatientscount=Patient.objects.filter(Dentist=request.user,Status="Declined").count()
        ohpatientscount=Patient.objects.filter(Dentist=request.user,Status="On Hold").count()
        wapatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Waiting Acceptance").count()
        tdvpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="3D View").count()
        mppatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Model Production").count()
        arpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Aligners Ready").count()
        tcpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="TC").count()
        archivedpatientcount=Patient.objects.filter(InternalStatus="Archived").count()
        #Referrals
        reftotalcount=Referral.objects.filter(Dentist=request.user).count()
        refnewcount=Referral.objects.filter(Dentist=request.user,Status="New").count()
        refconsultationscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Consultation").exclude(Status="Declined").exclude(Status="New").count()
        refimplantscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").count()       
        reforthodonticscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").count()       
        refrootcanalcount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").count()       
        refcrownnveneerscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Crown and Veneers").exclude(Status="Declined").exclude(Status="New").count()              
        refdeclinedcount=Referral.objects.filter(Dentist=request.user,Status="Declined").count()       
        reftccount=Referral.objects.filter(Dentist=request.user,Status="TC").count()       

    context={
        'dashboard':'active',
        'totalpatientscount':totalpatientscount,
        'acceptedpatientscount':acceptedpatientscount,
        'newpatientscount':newpatientscount,
        'ohpatientscount':ohpatientscount,
        'reviewpatientscount':reviewpatientscount,
        'declinedpatientscount':declinedpatientscount,
        'reftotalcount':reftotalcount,
        'refnewcount':refnewcount,
        'refconsultationscount':refconsultationscount,
        'refimplantscount':refimplantscount,
        'reforthodonticscount':reforthodonticscount,
        'refrootcanalcount':refrootcanalcount,
        'refcrownnveneerscount':refcrownnveneerscount,
        'refdeclinedcount':refdeclinedcount,
        'reftccount':reftccount,
        'wapatientscount':wapatientscount,
        'tdvpatientscount':tdvpatientscount,
        'arpatientscount':arpatientscount,
        'tcpatientscount':tcpatientscount,
        'mppatientscount':mppatientscount,
        'archivedpatientcount':archivedpatientcount,
    }
    return render(request,'dashboard.html',context)

# Patients
@login_required(login_url='login')
def patients(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.order_by("PatientName")
    else:
        mypatients=Patient.objects.filter(Dentist=request.user).order_by("PatientName")
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patients.html',context)

@login_required(login_url='login')
def patientaccepted(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(Status="Accepted").order_by("PatientName")  
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.Status="On"
            editpatient.save()              
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,Status="Accepted").order_by("PatientName")      
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientaccepted.html',context)

@login_required(login_url='login')
def patientarchived(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="Archived").order_by("PatientName")
    context={
        'patients':'active',
        'mypatients':mypatients,
    }
    return render(request,'patientarchived.html',context)

@login_required(login_url='login')
def patientmp(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="Model Production").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()        
    context={
        'patients':'active',
        'mypatients':mypatients,
    }
    return render(request,'patientmp.html',context)

@login_required(login_url='login')
def patientnew(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(Status="New").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status="On"
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,Status="New").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientnew.html',context)

@login_required(login_url='login')
def patientoh(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(Status="On Hold").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,Status="On Hold").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.save()        
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientoh.html',context)

@login_required(login_url='login')
def patientreview(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(Status="Review").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,Status="Review").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.save()    
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientreview.html',context)

@login_required(login_url='login')
def patientdeclined(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(Status="Declined").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,Status="Declined").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientdeclined.html',context)

@login_required(login_url='login')
def patientwa(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="Waiting Acceptance").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    else:
        mypatients=Patient.objects.filter(Dentist=request.user,InternalStatus="Waiting Acceptance").order_by("PatientName")    
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patientwa.html',context)

@login_required(login_url='login')
def patienttdv(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="3D View").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }

    return render(request,'patienttdv.html',context)

@login_required(login_url='login')
def patientar(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="Aligners Ready").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }
    return render(request,'patientar.html',context)

@login_required(login_url='login')
def patienttc(request):
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(InternalStatus="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editpatient=Patient.objects.get(id=id)
            editpatient.Status=request.POST.get('Status')
            editpatient.InternalStatus=request.POST.get('InternalStatus')
            editpatient.save()
    context={
        'patients':'active',
        'mypatients':mypatients,
    }
    return render(request,'patienttc.html',context)

@login_required(login_url='login')
def dentists(request):
    dentists=User.objects.order_by("first_name")
    context={
        'dentists':'active',
        'dentists':dentists,
    }
    return render(request,'dentists.html',context)

@login_required(login_url='login')
def addnewpatient(request):
    treatmentrequestfile=TreatmentRequestFile.objects.order_by('-id')[:1]
    if request.method=="POST":
        Dentist=request.user
        Prescriber=request.POST.get('Prescriber')
        Clinic=request.POST.get('Clinic')
        Email=request.POST.get('Email')
        Telephone=request.POST.get('Telephone')
        PatientName=request.POST.get('PatientName')
        Sex=request.POST.get('Sex')
        TreatmentInPast=request.POST.get('TreatmentInPast')
        Age=request.POST.get('Age')
        Address1=request.POST.get('Address1')
        Address2=request.POST.get('Address2')
        OralScan=request.POST.get('OralScan',default="No")
        Impression=request.POST.get('Impression',default="No")
        UpperJaw=request.FILES.get('UpperJaw',default="images/Logo2.png")
        LowerJaw=request.FILES.get('LowerJaw',default="images/Logo2.png")
        Photo1=request.FILES.get('Photo1',default="images/Logo2.png")
        Photo2=request.FILES.get('Photo2',default="images/Logo2.png")
        Photo3=request.FILES.get('Photo3',default="images/Logo2.png")
        Photo4=request.FILES.get('Photo4',default="images/Logo2.png")
        Treatment=request.POST.get('Treatment',default="No")
        TreatmentRequired=request.POST.get('TreatmentRequired',default="No")
        Aligners=request.POST.get('Aligners')
        TreatmentLimit=request.POST.get('TreatmentLimit')
        Overbite=request.POST.get('Overbite')
        Overjet=request.POST.get('Overjet')
        Expension=request.POST.get('Expension')
        IPR=request.POST.get('IPR')
        Procline=request.POST.get('Procline')
        Distalize=request.POST.get('Distalize')
        UpperMidline=request.POST.get('UpperMidline')
        LoverMidline=request.POST.get('LoverMidline')
        ArchForm=request.POST.get('ArchForm')
        PCrossbite=request.POST.get('PCrossbite')
        Hint1=request.POST.get('Hint1')
        Hint2=request.POST.get('Hint2')
        Hint3=request.POST.get('Hint3')
        DentistNote=request.POST.get('Note')
        Status="New"
        AdminNote="TBA"
        patient=Patient(Dentist=Dentist,Prescriber=Prescriber,Clinic=Clinic,Email=Email,Telephone=Telephone,Address1=Address1,Address2=Address2,PatientName=PatientName,Sex=Sex,TreatmentInPast=TreatmentInPast,Age=Age,OralScan=OralScan,Impression=Impression,UpperJaw=UpperJaw,LowerJaw=LowerJaw,Photo1=Photo1,Photo2=Photo2,Photo3=Photo3,Photo4=Photo4,Treatment=Treatment,TreatmentRequired=TreatmentRequired,Aligners=Aligners,TreatmentLimit=TreatmentLimit,Overbite=Overbite,Overjet=Overjet,Expension=Expension,IPR=IPR,Procline=Procline,Distalize=Distalize,UpperMidline=UpperMidline,LoverMidline=LoverMidline,ArchForm=ArchForm,PCrossbite=PCrossbite,Hint1=Hint1,Hint2=Hint2,Hint3=Hint3,Status=Status,DentistNote=DentistNote,AdminNote=AdminNote)
        patient.save()
        messages.success(request,"Patient has been added successfully!")

    context={
        'dentists':'active',
        'treatmentrequestfile':treatmentrequestfile,
    }
    return render(request,'addnewpatient.html',context)

@login_required(login_url='login')
def patientdetail(request,id):
    patient=Patient.objects.get(id=id)
    proposed=PatientProposedTreatment.objects.filter(Patient=patient).order_by('-id')[:1]
    adminuploads=ImageUploadAdmin.objects.filter(Patient=patient).order_by('-id')[:1]
    if "Proposed" in request.POST:
        ProposedTreatment=request.FILES.get('ProposedTreatment',default="images/Logo2.png")
        Invoice=request.FILES.get('Invoice',default="images/Logo2.png")
        ThreeDViewProposed=request.FILES.get('ThreeDViewProposed',default="images/Logo2.png")
        InternalStatus=request.POST.get('InternalStatus',default="On")
        Proposed=PatientProposedTreatment(ProposedTreatment=ProposedTreatment,Invoice=Invoice,ThreeDViewProposed=ThreeDViewProposed,Patient=patient,user=request.user)
        Proposed.save()
        patient.Admin=request.POST.get('Note')
        patient.save()

    if "UploadImages" in request.POST:
        Image1=request.FILES.get('Image1',default="images/Logo2.png")
        Image2=request.FILES.get('Image2',default="images/Logo2.png")
        Image3=request.FILES.get('Image3',default="images/Logo2.png")
        imageupload=ImageUploadAdmin(Image1=Image1,Image2=Image2,Image3=Image3,Patient=patient,user=request.user)
        imageupload.save()

    if "SubmitStatus" in request.POST:
        patient.Status=request.POST.get('Status')
        patient.save()

    if "SubmitInternalStatus" in request.POST:
        patient.InternalStatus=request.POST.get('InternalStatus')
        patient.save()

    if "SubmitNote" in request.POST:
        if request.user.is_superuser:
            patient.AdminNote=request.POST.get('AdminNote')
            patient.save()
        else:
            patient.DentistNote=request.POST.get('DentistNote')
            patient.save()


    context={
        'patient':patient,
        'proposed':proposed,
        'adminuploads':adminuploads,
    }
    return render(request, 'patientdetail.html', context)

# Referrals
@login_required(login_url='login')
def referrals(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.order_by("PatientName")
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user).order_by("PatientName")
    context={
        'referral':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'referrals.html',context)

@login_required(login_url='login')
def addnewreferral(request):
    if request.method=="POST":
        Dentist=request.user
        DentistName=request.POST.get('DentistName')
        PatientName=request.POST.get('PatientName')
        PatientPhone=request.POST.get('PatientPhone')
        PatientEmail=request.POST.get('PatientEmail')
        ReferralReason=request.POST.get('ReferralReason')
        Status=request.POST.get('Status',default="New")
        referral=Referral(Dentist=Dentist,DentistName=DentistName,PatientName=PatientName,PatientPhone=PatientPhone,PatientEmail=PatientEmail,ReferralReason=ReferralReason,Status=Status)
        referral.save()
        messages.success(request,"Referral has been added successfully!")

    context={
        'referral':'active'
    }
    return render(request,'addnewreferral.html',context)

@login_required(login_url='login')
def referraldetail(request,id):
    referral=Referral.objects.get(id=id)
    
    if "SubmitStatus" in request.POST:
        referral.Status=request.POST.get('Status')
        referral.save()

    context={
        'referral':referral,
    }
    return render(request, 'referraldetail.html', context)

@login_required(login_url='login')
def refnew(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(Status="New").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.TreatmentPlan=request.POST.get('TreatmentPlan')
            editreferral.save()        
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,Status="New").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.TreatmentPlan=request.POST.get('TreatmentPlan')
            editreferral.save()         
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'refnew.html',context)

@login_required(login_url='login')
def refconsultations(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(TreatmentPlan="Consultation").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.TreatmentPlan=request.POST.get('TreatmentPlan')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()           
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Consultation").exclude(Status="New").exclude(Status="TC").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.TreatmentPlan=request.POST.get('TreatmentPlan')
            editreferral.save()      
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'refconsultations.html',context)

@login_required(login_url='login')
def refimplants(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save() 
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()         
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'refimplants.html',context)

@login_required(login_url='login')
def reforthodontics(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()  
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'reforthodontics.html',context)

@login_required(login_url='login')
def refrootcanals(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()      
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'refrootcanals.html',context)

@login_required(login_url='login')
def refcrowns(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(TreatmentPlan="Crown").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Crown").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").order_by("PatientName")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.BookedOn=request.POST.get('BookedOn')
            editreferral.Stage=request.POST.get('Stage')
            editreferral.Note=request.POST.get('Note')
            editreferral.save()      
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }
    return render(request,'refcrowns.html',context)

@login_required(login_url='login')
def refdeclined(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(Status="Declined").order_by("PatientName")
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,Status="Declined").order_by("PatientName")
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'refdeclined.html',context)

@login_required(login_url='login')
def reftc(request):
    if request.user.is_superuser or request.user.is_staff:
        myreferrals=Referral.objects.filter(Status="TC").order_by("PatientName")
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,Status="TC").order_by("PatientName")
    context={
        'referrals':'active',
        'myreferrals':myreferrals,
    }

    return render(request,'reftc.html',context)

# Search Results
@login_required(login_url='login')
def patientsearchresults(request):
    patientsearchquery=request.GET['PatientSearchQuery']
    if request.user.is_superuser or request.user.is_staff:
        mypatients=Patient.objects.filter(PatientName__icontains=patientsearchquery).order_by("-PatientName")
    else:
        mypatients=Patient.objects.filter(PatientName__icontains=patientsearchquery,Dentist=request.user).order_by("-PatientName")
    patientname=patientsearchquery
    context={
        'patients':'active',
        'mypatients':mypatients,
        'patientname':patientname,
    }
    return render(request,'patientsearchresults.html',context)

@login_required(login_url='login')
def referralsearchresults(request): 
    referralsearchquery=request.GET['ReferralSearchQuery']
    if request.user.is_superuser or request.user.is_staff:  
        myreferrals=Referral.objects.filter(PatientName__icontains=referralsearchquery).order_by("-PatientName")
    else:
        myreferrals=Referral.objects.filter(PatientName__icontains=referralsearchquery,Dentist=request.user).order_by("-PatientName")
    referralname=referralsearchquery
    context={
        'referrals':'active',        
        'myreferrals':myreferrals,
        'referralname':referralname,
    }
    return render(request,'referralsearchresults.html',context)

@login_required(login_url='login')
def reportsearchresults(request):
    reportsearchquery=request.GET['ReportSearchQuery']
    date=reportsearchquery
    cashsum= Payment.objects.filter(PaymentMethod="Cash",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    card11sum= Payment.objects.filter(PaymentMethod="Card11",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    card14sum= Payment.objects.filter(PaymentMethod="Card14",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    banktransfersum= Payment.objects.filter(PaymentMethod="Bank Transfer",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    loansum= Payment.objects.filter(PaymentMethod="Loan",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    total=cashsum+card11sum+card14sum+banktransfersum+loansum
    context={
        'payment':'active',
        'cashsum':cashsum,
        'card11sum':card11sum,
        'card14sum':card14sum,
        'banktransfersum':banktransfersum,
        'loansum':loansum,
        'date':date ,
        'total':total,

    }
    return render(request,'reportsearchresults.html',context)

@login_required(login_url='login')
def incomeexpensesearchresult(request):
    StartDate=request.GET['IncomeExpenseStartDateQuery']
    EndDate=request.GET['IncomeExpenseEndDateQuery']
    Account=request.GET['IncomeExpenseAccountQuery']
    date=datetime.now().strftime("%Y-%m-%d")
    if Account=="All":    
        incomereport=Income.objects.filter(Status="Approved",Date__range=[StartDate,EndDate]).order_by('-Date')   
        incometotal= Income.objects.filter(Status="Approved",Date__range=[StartDate,EndDate]).aggregate(Sum('Amount')).get('Amount__sum') or 0
        expensereport=Expense.objects.filter(Status="Approved",Date__range=[StartDate,EndDate]).order_by('-Date')   
        expensetotal= Expense.objects.filter(Status="Approved",Date__range=[StartDate,EndDate]).aggregate(Sum('Amount')).get('Amount__sum') or 0
        total=incometotal-expensetotal
    else:
        incomereport=Income.objects.filter(Status="Approved",Date__range=[StartDate,EndDate],Account=Account).order_by('-Date')   
        incometotal= Income.objects.filter(Status="Approved",Date__range=[StartDate,EndDate],Account=Account).aggregate(Sum('Amount')).get('Amount__sum') or 0
        expensereport=Expense.objects.filter(Status="Approved",Date__range=[StartDate,EndDate],Account=Account).order_by('-Date')   
        expensetotal= Expense.objects.filter(Status="Approved",Date__range=[StartDate,EndDate],Account=Account).aggregate(Sum('Amount')).get('Amount__sum') or 0
        total=incometotal-expensetotal            

    context={
        'payment':'active',
        'incomereport':incomereport,
        'expensereport':expensereport,
        'date':date,
        'incometotal':incometotal,
        'expensetotal':expensetotal,
        'total':total,
        'StartDate':StartDate,
        'EndDate':EndDate,
    }


    return render(request,'incomeexpensesearchresult.html',context)

@login_required(login_url='login')
def paymentfullsearchresultsbypatient(request):
    if "PatientReportSearchQuery" in request.GET:
        date="All Time"
        patientreportsearchquery=request.GET['PatientReportSearchQuery']
        allpayments=Payment.objects.filter(PatientName=patientreportsearchquery).order_by('-Date')
        total= Payment.objects.filter(PatientName=patientreportsearchquery).aggregate(Sum('Amount')).get('Amount__sum') or 0
    if "DateReportSearchQuery" in request.GET:
        datereportsearchquery=request.GET['DateReportSearchQuery']
        date=datereportsearchquery
        allpayments=Payment.objects.filter(Date=datereportsearchquery).order_by('-PatientName')
        total= Payment.objects.filter(Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    if "DentistReportSearchQuery" in request.GET:
        date="All Time"
        dentistreportsearchquery=request.GET['DentistReportSearchQuery']
        allpayments=Payment.objects.filter(Dentist=dentistreportsearchquery).order_by('-Date')
        total= Payment.objects.filter(Dentist=dentistreportsearchquery).aggregate(Sum('Amount')).get('Amount__sum') or 0
    
    context={
        'payment':'active',
        'allpayments':allpayments,
        'date':date,
        'total':total,
    }   
    return render(request,'paymentfullsearchresultsbypatient.html',context) 

# Reception
@login_required(login_url='login')
def addpayment(request): 
    user=request.user
    date=datetime.now().strftime("%Y-%m-%d")
    if request.method=="POST":
        Date=request.POST.get('Date')
        User=request.POST.get('user')
        PatientName=request.POST.get('PatientName')
        Dentist=request.POST.get('Dentist')
        Scheme=request.POST.get('Scheme')
        PaymentMethod=request.POST.get('PaymentMethod')
        Amount=request.POST.get('Amount',default="0")
        payment=Payment(Date=Date,User=User,PatientName=PatientName,Dentist=Dentist,Scheme=Scheme,PaymentMethod=PaymentMethod,Amount=Amount)
        payment.save()
        messages.success(request,"Payment has been added successfully!")

    context={
        'payment':'active',        
        'user':user,
        'date':date,
    }
    return render(request,'addpayment.html',context)

@login_required(login_url='login')
def paymentdailyreport(request):
    date=datetime.now().strftime("%Y-%m-%d")
    cashsum= Payment.objects.filter(Date=date,PaymentMethod="Cash").aggregate(Sum('Amount')).get('Amount__sum') or 0
    card11sum= Payment.objects.filter(Date=date,PaymentMethod="Card11").aggregate(Sum('Amount')).get('Amount__sum') or 0
    card14sum= Payment.objects.filter(Date=date,PaymentMethod="Card14").aggregate(Sum('Amount')).get('Amount__sum') or 0
    banktransfersum= Payment.objects.filter(Date=date,PaymentMethod="Bank Transfer").aggregate(Sum('Amount')).get('Amount__sum') or 0
    loansum= Payment.objects.filter(Date=date,PaymentMethod="Loan").aggregate(Sum('Amount')).get('Amount__sum') or 0
    total=cashsum+card11sum+card14sum+banktransfersum+loansum
    context={
        'payment':'active',
        'cashsum':cashsum,
        'card11sum':card11sum,
        'card14sum':card14sum,
        'banktransfersum':banktransfersum,
        'loansum':loansum,
        'date':date ,
        'total':total,

    }
    return render(request,'paymentdailyreport.html',context)


@login_required(login_url='login')
def paymentfullreport(request):
    date=datetime.now().strftime("%Y-%m-%d")
    StartDate=date
    EndDate=date
    allpayments=Payment.objects.filter(Date=date,Status="Pending").order_by('-Date')   
    total= Payment.objects.filter(Date=date,Status="Pending").order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0
    if "ChangePatientName" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.PatientName=request.POST.get('PatientName')
        editpayments.save() 
    if "Dentist" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.Dentist=request.POST.get('Dentist')
        editpayments.save()  
    if "Scheme" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.Scheme=request.POST.get('Scheme')
        editpayments.save()    
    if "PaymentMethod" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.PaymentMethod=request.POST.get('PaymentMethod')
        editpayments.save()      
    if "ChangeAmount" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.Amount=request.POST.get('Amount')
        editpayments.save()                            
    if "Archive" in request.POST:
        id=request.POST.get('id')
        editpayments=Payment.objects.get(id=id)
        editpayments.Status="Archived"
        editpayments.save()  

    context={
        'payment':'active',
        'allpayments':allpayments,
        'date':date,
        'total':total,
        'StartDate':StartDate,
        'EndDate':EndDate,

    }
    return render(request,'paymentfullreport.html',context)

@login_required(login_url='login')
def paymentfullreportarchived(request):
    date=datetime.now().strftime("%Y-%m-%d")
    StartDate=date
    EndDate=date
    allpayments=Payment.objects.filter(Date=date,Status="Archived").order_by('-Date')   
    total= Payment.objects.filter(Date=date,Status="Archived").order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0
    if "Search" in request.GET:
        StartDate=request.GET['StartDate']
        EndDate=request.GET['EndDate']
        Dentist=request.GET['Dentist']
        Scheme=request.GET['Scheme']
        if Dentist == "All" and Scheme != "All":
            allpayments=Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Scheme=Scheme).order_by("-Date")        
            total= Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Scheme=Scheme).order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0
        elif Scheme == "All" and Dentist != "All":
            allpayments=Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Dentist=Dentist).order_by("-Date")        
            total= Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Dentist=Dentist).order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0
        elif Scheme=="All" and Dentist=="All":
            allpayments=Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate]).order_by("-Date")        
            total= Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate]).order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0            
        else:
            allpayments=Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Dentist=Dentist,Scheme=Scheme).order_by("-Date")        
            total= Payment.objects.filter(Status="Archived",Date__range=[StartDate,EndDate],Dentist=Dentist,Scheme=Scheme).order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0

    context={
        'payment':'active',
        'allpayments':allpayments,
        'date':date,
        'total':total,
        'StartDate':StartDate,
        'EndDate':EndDate,

    }
    return render(request,'paymentfullreportarchived.html',context)

# Income and Expense
@login_required(login_url='login')
def adminaddincome(request): 
    date=datetime.now().strftime("%Y-%m-%d")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    category=IncomeExpenseCategory.objects.all().order_by('Category')
    if request.method=="POST":
        Date=request.POST.get('Date')
        Title=request.POST.get('Title')
        Category=request.POST.get('Category')
        Account=request.POST.get('Account')
        Amount=request.POST.get('Amount',default=0)
        Status="Pending"
        Note=request.POST.get('Note')
        Repeat=request.POST.get('Repeat')
        RepeatStatus="On"
        income=Income(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note,Repeat=Repeat,RepeatStatus=RepeatStatus)
        income.save()
        if not IncomeExpenseTitle.objects.filter(Title=Title).exists():
            newtitle=IncomeExpenseTitle(Title=Title)
            newtitle.save()
        if not IncomeExpenseCategory.objects.filter(Category=Category).exists():
            newcategory=IncomeExpenseCategory(Category=Category)
            newcategory.save()
        messages.success(request,"Income has been added successfully!")

    context={
        'payment':'active',       
        'date':date,
        'title':title,
        'category':category,
    }
    return render(request,'adminaddincome.html',context)

@login_required(login_url='login')
def adminaddexpense(request): 
    date=datetime.now().strftime("%Y-%m-%d")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    category=IncomeExpenseCategory.objects.all().order_by('Category')
    if request.method=="POST":
        Date=request.POST.get('Date')
        Title=request.POST.get('Title')
        Category=request.POST.get('Category')
        Account=request.POST.get('Account')
        Amount=request.POST.get('Amount',default=0)
        Status="Pending"
        Note=request.POST.get('Note')

        expense=Expense(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note)
        expense.save()
        if not IncomeExpenseTitle.objects.filter(Title=Title).exists():
            newtitle=IncomeExpenseTitle(Title=Title)
            newtitle.save()
        if not IncomeExpenseCategory.objects.filter(Category=Category).exists():
            newcategory=IncomeExpenseCategory(Category=Category)
            newcategory.save()
            
        messages.success(request,"Espense has been added successfully!")

    context={
        'payment':'active',       
        'date':date,
        'title':title,
        'category':category,
    }
    return render(request,'adminaddexpense.html',context)

@login_required(login_url='login')
def incomeandexpensereport(request):
    date=datetime.now().strftime("%Y-%m-%d")
    StartDate=date
    EndDate=date
    incomereport=Income.objects.filter(Status="Pending").order_by('-Date')   
    incometotal= Income.objects.filter(Status="Pending").aggregate(Sum('Amount')).get('Amount__sum') or 0
    expensereport=Expense.objects.filter(Status="Pending").order_by('-Date')   
    expensetotal= Expense.objects.filter(Status="Pending").aggregate(Sum('Amount')).get('Amount__sum') or 0
    total=incometotal-expensetotal
    context={
        'payment':'active',
        'incomereport':incomereport,
        'expensereport':expensereport,
        'date':date,
        'incometotal':incometotal,
        'expensetotal':expensetotal,
        'total':total,
        'StartDate':StartDate,
        'EndDate':EndDate,
    }
    return render(request,'incomeandexpensereport.html',context)

def incomeandexpenserepeat(request): 
    incomem=Income.objects.filter(RepeatStatus="On",Repeat="Monthly").exclude(Repeat="No Repeat").order_by('-Date','-Repeat') 
    incomeq=Income.objects.filter(RepeatStatus="On",Repeat="Quarterly").exclude(Repeat="No Repeat").order_by('-Date','-Repeat') 
    incomey=Income.objects.filter(RepeatStatus="On",Repeat="Yearly").exclude(Repeat="No Repeat").order_by('-Date','-Repeat') 
    date=datetime.now().strftime("%Y-%m-%d")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    category=IncomeExpenseCategory.objects.all().order_by('Category')
    if "Repeat" in request.POST:
        Date=request.POST.get('Date')
        Title=request.POST.get('Title')
        Category=request.POST.get('Category')
        Account=request.POST.get('Account')
        Amount=request.POST.get('Amount',default=0)
        Status="Pending"
        Note=request.POST.get('Note')
        Repeat=request.POST.get('Repeat')
        RepeatStatus="Off"
        incomeadded=Income(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note,Repeat=Repeat,RepeatStatus=RepeatStatus)
        incomeadded.save()
        if not IncomeExpenseTitle.objects.filter(Title=Title).exists():
            newtitle=IncomeExpenseTitle(Title=Title)
            newtitle.save()
        if not IncomeExpenseCategory.objects.filter(Category=Category).exists():
            newcategory=IncomeExpenseCategory(Category=Category)
            newcategory.save()
        messages.success(request,"Income has been repeated successfully!")

    context={
        'payment':'active',       
        'date':date,
        'incomem':incomem,
        'incomeq':incomeq,
        'incomey':incomey,
        'title':title,
        'category':category,
    }
    return render(request,'incomeandexpenserepeat.html',context)


def incomeandexpensereportapproved(request):
    date=datetime.now().strftime("%Y-%m-%d")
    StartDate=date
    EndDate=date    
    incomereport=Income.objects.filter(Status="Approved").order_by('-Date')   
    incometotal= Income.objects.filter(Status="Approved").aggregate(Sum('Amount')).get('Amount__sum') or 0
    expensereport=Expense.objects.filter(Status="Approved").order_by('-Date')   
    expensetotal= Expense.objects.filter(Status="Approved").aggregate(Sum('Amount')).get('Amount__sum') or 0
    total=incometotal-expensetotal
    context={
        'payment':'active',
        'incomereport':incomereport,
        'expensereport':expensereport,
        'date':date,
        'incometotal':incometotal,
        'expensetotal':expensetotal,
        'total':total,
        'StartDate':StartDate,
        'EndDate':EndDate,        
    }
    return render(request,'incomeandexpensereportapproved.html',context)

def deleteincome(request,id):
    incomedata=Income.objects.get(id=id)
    incomedata.delete()
    return redirect('incomeandexpensereport')

def deleteexpense(request,id):
    expensedata=Expense.objects.get(id=id)
    expensedata.delete()
    return redirect('incomeandexpensereport')

def editincome(request,id):
    date=datetime.now().strftime("%Y-%m-%d")
    incomedata=Income.objects.get(id=id)
    if "UpdateIncome" in request.POST:
        incomedata.Title=request.POST.get('Title')
        incomedata.save()

    context={
        'incomedata':incomedata,
        'date':date
    }
    return render(request,'editincome.html',context)

def editexpense(request,id):
    date=datetime.now().strftime("%Y-%m-%d")
    expensedata=Expense.objects.get(id=id)
    if "UpdateIncome" in request.POST:
        expensedata.Title=request.POST.get('Title')
        expensedata.save()

    context={
        'expensedata':expensedata,
        'date':date
    }
    return render(request,'editexpense.html',context)


def updateincome(request,id):
    date=datetime.now().strftime("%Y-%m-%d")
    incomedata=Income.objects.get(id=id)
    incomedata.Date=date
    incomedata.Title=request.POST.get('Title')
    incomedata.Category=request.POST.get('Category')
    incomedata.Account=request.POST.get('Account')
    incomedata.Amount=request.POST.get('Amount')
    incomedata.Status=request.POST.get('Status')
    incomedata.Note=request.POST.get('Note')
    incomedata.save()
    return redirect('incomeandexpensereport')
    
def updateexpense(request,id):
    date=datetime.now().strftime("%Y-%m-%d")
    expensedata=Expense.objects.get(id=id)
    expensedata.Date=date
    expensedata.Title=request.POST.get('Title')
    expensedata.Category=request.POST.get('Category')
    expensedata.Account=request.POST.get('Account')
    expensedata.Amount=request.POST.get('Amount')
    expensedata.Status=request.POST.get('Status')
    expensedata.Note=request.POST.get('Note')
    expensedata.save()
    return redirect('incomeandexpensereport')
    

# Labs
@login_required(login_url='login')
def addnewlab(request):
    date=datetime.now().strftime("%Y-%m-%d")    
    if request.method=="POST":
        PatientName=request.POST.get('PatientName')
        PatientID=request.POST.get('PatientID')
        Dentist=request.POST.get('Dentist')
        Scheme=request.POST.get('Scheme')
        Lab=request.POST.get('Lab')
        Type=request.POST.get('Type')
        Quantity=0
        Note=""
        Stage=request.POST.get('Stage')
        DateArriving=request.POST.get('DateArriving')
        Status="Pending"
        Arrived="No"
        Fee=0.00
        PaidDate="00/00/0000"
        TC=" "
        labwork=LabWork(date=date,PatientName=PatientName,PatientID=PatientID,Dentist=Dentist,Scheme=Scheme,Lab=Lab,Type=Type,Quantity=Quantity,Note=Note,Stage=Stage,DateArriving=DateArriving,Status=Status,Arrived=Arrived,Fee=Fee,TC=TC)
        labwork.save()
        messages.success(request,"Lab Work has been added successfully!")
    context={
        'labs':'active',
        'date':date,
    }
    return render(request,'addnewlab.html',context)

@login_required(login_url='login')
def labspending(request):
    labwork=LabWork.objects.filter(Status="Pending").order_by("PatientName")
    if "Save" in request.POST:
        id=request.POST.get('id')
        editlab=LabWork.objects.get(id=id)
        editlab.PatientName=request.POST.get('PatientName')
        editlab.PatientID=request.POST.get('PatientID')
        editlab.Dentist=request.POST.get('Dentist')
        editlab.Scheme=request.POST.get('Scheme')
        editlab.Lab=request.POST.get('Lab')
        editlab.Type=request.POST.get('Type')
        editlab.Quantity=request.POST.get('Quantity')
        editlab.Note=request.POST.get('Note')
        editlab.Arrived=request.POST.get('Arrived')
        editlab.Stage=request.POST.get('Stage')
        editlab.TC=request.POST.get('TC')
        if request.user.is_superuser:
            editlab.Fee=request.POST.get('Fee')
            editlab.PaidDate=request.POST.get('PaidDate')
        editlab.DateArriving=request.POST.get('DateArriving')
        editlab.save()                                      

    if "Archive" in request.POST:
        id=request.POST.get('id')
        editlab=LabWork.objects.get(id=id)
        editlab.Status="Archived"
        editlab.save()  
    context={
        'labs':'active',
        'labwork':labwork,
    }

    return render(request,'labspending.html',context)

@login_required(login_url='login')
def labsarchived(request):
    labwork=LabWork.objects.filter(Status="Archived").order_by("PatientName")
    sum= LabWork.objects.filter(Status="Archived").aggregate(Sum('Fee')).get('Fee__sum') or 0

    if "Approve" in request.POST:
        id=request.POST.get('id')
        editlab=LabWork.objects.get(id=id)
        editlab.Status="Approved"
        editlab.save()
    
    if "Search" in request.GET:
        StartDate=request.GET['StartDate']
        EndDate=request.GET['EndDate']
        Dentist=request.GET['Dentist']
        Scheme=request.GET['Scheme']
        Lab=request.GET['Lab']
        labwork=LabWork.objects.filter(Status="Archived",PaidDate__range=[StartDate,EndDate],Dentist=Dentist,Scheme=Scheme,Lab=Lab).order_by("PatientName")        
        sum= LabWork.objects.filter(Status="Archived",PaidDate__range=[StartDate,EndDate],Dentist=Dentist,Scheme=Scheme,Lab=Lab).aggregate(Sum('Fee')).get('Fee__sum') or 0

    context={
        'labs':'active',
        'labwork':labwork,
        'sum':sum,
    }

    return render(request,'labsarchived.html',context)

# Orders
@login_required(login_url='login')
def addorder(request):
    Date=datetime.now().strftime("%Y-%m-%d")    
    if request.method=="POST":
        Item=request.POST.get('Item')
        Category=request.POST.get('Category')
        Status="Pending"
        Arrived="No"
        Fee=0.00
        order=Order(Date=Date,user=request.user,Item=Item,Category=Category,Status=Status,Arrived=Arrived,Fee=Fee)
        order.save()
        messages.success(request,"Order has been added successfully!")

    context={
        'orders':'active',
        'Date':Date,
    }
    return render(request,'addorder.html',context)

@login_required(login_url='login')
def orders(request):
    order=Order.objects.filter(Status="Pending").order_by("Date")
    if "AddOrderBy" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.OrderBy=request.POST.get('OrderBy')
        editorder.save()
    if "AddSupplier" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Supplier=request.POST.get('Supplier')
        editorder.save()
    if "AddQuantity" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Quantity=request.POST.get('Quantity')
        editorder.save()
    if "AddFee" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Fee=request.POST.get('Fee')
        editorder.save()
    if "AddNewDate" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.NewDate=request.POST.get('NewDate')
        editorder.save()
    if "Arrived" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Arrived=request.POST.get('Arrived')
        editorder.save()                    
    if "Returned" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Returned=request.POST.get('Returned')
        editorder.save()                    
    if "AddNote" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Note=request.POST.get('Note')
        editorder.save()          
    if "Archive" in request.POST:
        id=request.POST.get('id')
        editorder=Order.objects.get(id=id)
        editorder.Status="Archived"
        editorder.save()          
                           
    context={
        'orders':'active',
        'order':order,
    }

    return render(request,'orders.html',context)

@login_required(login_url='login')
def ordersarchived(request):
    order=Order.objects.filter(Status="Archived").order_by("Date")
    context={
        'orders':'active',
        'order':order,
    }

    return render(request,'ordersarchived.html',context)


# Account
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method=='POST':
            username= request.POST.get('username')
            password= request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,"Incorrect Username or Password!")
        context={

        }
        return render(request,'login.html',context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)

            profile_form=DentistProfileForm(request.POST)
            
            if form.is_valid() and profile_form.is_valid():
                user=form.save()
                
                profile=profile_form.save(commit=False)
                profile.user=user
                profile.save()

                user=form.cleaned_data.get("username")
                messages.error(request,"Registration Successful")
                return redirect('login')
        else:
            form=CreateUserForm()
            profile_form=DentistProfileForm()
        context={
            'form':form,
            'profile_form':profile_form,
        }
        return render(request,'signup.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

    return render(request,'login.html',context)

    # Format date
    date1= "June 8, 2021"
    date2= "08/10/2020"
    date3= ""

    date1_obj= datetime.strptime(date1, '%B %d, %Y')
    date2_obj= datetime.strptime(date2, '%m/%d/%Y')
    


@login_required(login_url='login')
def repeatExpense(request):
    date=datetime.now().strftime("%Y-%m-%d")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    category=IncomeExpenseCategory.objects.all().order_by('Category')
    if request.method=='POST':
        Date=request.POST.get('Date')
        Title=request.POST.get('Title')
        Category=request.POST.get('Category')
        Account=request.POST.get('Account')
        Amount=request.POST.get('Amount',default=0)
        Status="Pending"
        Note=request.POST.get('Note')

        expense=RepeatExpense(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note)
        expense.save()
        if not IncomeExpenseTitle.objects.filter(Title=Title).exists():
            newtitle=IncomeExpenseTitle(Title=Title)
            newtitle.save()
        if not IncomeExpenseCategory.objects.filter(Category=Category).exists():
            newcategory=IncomeExpenseCategory(Category=Category)
            newcategory.save()
    context={
        'payment':'active',       
        'date':date,
        'title':title,
        'category':category,
    }
    return render(request, 'repeatExpense.html',context)

@login_required(login_url='login')
def repeatIncome(request):
    date=datetime.now().strftime("%Y-%m-%d")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    category=IncomeExpenseCategory.objects.all().order_by('Category')
    if request.method=="POST":
        print("******************")
        Date=request.POST.get('Date')
        Title=request.POST.get('Title')
        Category=request.POST.get('Category')
        Account=request.POST.get('Account')
        Amount=request.POST.get('Amount',default=0)
        Status="Pending"
        Note=request.POST.get('Note')
        Repeat=request.POST.get('Repeat')
        RepeatStatus="On"
        income=RepeatIncome(Date=Date,Title=Title,Category=Category,Account=Account,Amount=Amount,Status=Status,Note=Note,Repeat=Repeat,RepeatStatus=RepeatStatus)
        income.save()
        if not IncomeExpenseTitle.objects.filter(Title=Title).exists():
            newtitle=IncomeExpenseTitle(Title=Title)
            newtitle.save()
        if not IncomeExpenseCategory.objects.filter(Category=Category).exists():
            newcategory=IncomeExpenseCategory(Category=Category)
            newcategory.save()
        messages.success(request,"Income has been added successfully!")

    context={
        'payment':'active',       
        'date':date,
        'title':title,
        'category':category,
    }
    return render(request, 'repeatIncome.html',context)

@login_required(login_url='login')
def startScript(request):
    print("Starting")
    entries.delay()
    print("Ending")
    return render(request, 'repeatIncome.html')


def test():
    print("*****************************")
    title=IncomeExpenseTitle.objects.all().order_by('Title')
    for t in title:
        print(t)