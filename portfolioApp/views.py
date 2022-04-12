from optparse import Option
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from .models import LabWork, Patient,User,PatientProposedTreatment, DentistProfile,Referral,TreatmentRequestFile,ImageUploadAdmin,Payment,Income,Expense,IncomeExpenseTitle,IncomeExpenseCategory,LabWork,Order,RepeatExpense,RepeatIncome,UpperArchBox,LowerArchBox
from django.contrib.auth.forms import UserCreationForm
from .forms import DentistProfileForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import schedule
import time
from tasks import entries
from django.http import FileResponse
from django.db.models import Q

# Create your views here.

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_dentist:
        #Patients
        totalpatientscount=Patient.objects.filter(~Q(Progress="New")).count()
        newpatientscount=Patient.objects.filter(Progress="New").count()
        acceptedpatientscount=Patient.objects.filter(Status="Accepted").count()
        reviewpatientscount=Patient.objects.filter(Status="Review").count()
        declinedpatientscount=Patient.objects.filter(Status="Declined").count()
        ohpatientscount=Patient.objects.filter(Status="On Hold").count()
        wapatientscount=Patient.objects.filter(InternalStatus="Waiting Acceptance").count()
        tdvpatientscount=Patient.objects.filter(InternalStatus="3D View").count()
        mppatientscount=Patient.objects.filter(InternalStatus="Model Production").count()
        arpatientscount=Patient.objects.filter(InternalStatus="Aligners Ready").count()
        tcpatientscount=Patient.objects.filter(InternalStatus="TC").count()
        archivedpatientcount=Patient.objects.filter(Action="TC").count()
        #Referrals
        reftotalcount=Referral.objects.distinct().filter(
            Q(Status="In progress") |
            Q(Status="Booked")
            ).count()
        refnewcount=Referral.objects.filter(Status="New").count()
        refconsultationscount=Referral.objects.filter(TreatmentPlan="Consultation").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()
        refimplantscount=Referral.objects.filter(TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        reforthodonticscount=Referral.objects.filter(TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        refrootcanalcount=Referral.objects.filter(TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()       
        refcrownnveneerscount=Referral.objects.filter(TreatmentPlan="Crown").exclude(Status="Declined").exclude(Status="New").exclude(Status="TC").count()      
        refdeclinedcount=Referral.objects.filter(Status="Declined").count()       
        reftccount=Referral.objects.distinct().filter(
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")).count()        
    else:
        #Patients
        totalpatientscount=Patient.objects.distinct().filter(
            Q(Dentist=request.user) &
            ~Q(Progress="New") &
            ~Q(Action="TC")
        ).count()
        newpatientscount=Patient.objects.distinct().filter(
            Q(Dentist=request.user) &
            Q(Progress="New")
        ).count()
        acceptedpatientscount=Patient.objects.filter(Dentist=request.user,Status="Accepted").count()
        reviewpatientscount=Patient.objects.filter(Dentist=request.user,Status="Review").count()
        declinedpatientscount=Patient.objects.filter(Dentist=request.user,Status="Declined").count()
        ohpatientscount=Patient.objects.filter(Dentist=request.user,Status="On Hold").count()
        wapatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Waiting Acceptance").count()
        tdvpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="3D View").count()
        mppatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Model Production").count()
        arpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="Aligners Ready").count()
        tcpatientscount=Patient.objects.filter(Dentist=request.user,InternalStatus="TC").count()
        archivedpatientcount=Patient.objects.distinct().filter(
            Q(Dentist=request.user) &
            Q(Action="TC")
        ).count()
        #Referrals
        reftotalcount=Referral.objects.distinct().filter(
            Q(Dentist=request.user) &
            Q(Status="In progress") |
            Q(Status="Booked")
            ).count()
        refnewcount=Referral.objects.filter(Dentist=request.user,Status="New").count()
        refconsultationscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Consultation").exclude(Status="Declined").exclude(Status="New").count()
        refimplantscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Implant").exclude(Status="Declined").exclude(Status="New").count()       
        reforthodonticscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Orthodontics").exclude(Status="Declined").exclude(Status="New").count()       
        refrootcanalcount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Root Canal").exclude(Status="Declined").exclude(Status="New").count()       
        refcrownnveneerscount=Referral.objects.filter(Dentist=request.user,TreatmentPlan="Crown and Veneers").exclude(Status="Declined").exclude(Status="New").count()              
        refdeclinedcount=Referral.objects.filter(Dentist=request.user,Status="Declined").count()       
        reftccount=Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")).count()     

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
    if request.user.is_admin or request.user.is_dentist:
        if request.POST:
            if request.user.is_admin:
                patientObj = Patient.objects.get(id=request.POST.get('id'))
                patientObj.Stage = request.POST.get('Stage')
                patientObj.Status = request.POST.get('Status')
                patientObj.Action = request.POST.get('Action')
                patientObj.save()
            else:
                patientObj = Patient.objects.get(id=request.POST.get('id'))
                patientObj.Treatment = request.POST.get('Treatment')
                patientObj.Progress = request.POST.get('Progress')
                patientObj.save()

        if request.user.is_admin:
            # mypatients=Patient.objects.order_by("PatientName")
            mypatientsAccept=Patient.objects.distinct().filter(
                Q(Progress__icontains="Accepted") &
                ~Q(Action="TC")
            ).order_by("PatientName")

            mypatientsReview=Patient.objects.distinct().filter(
                Q(Progress__icontains="Review") &
                ~Q(Action="TC")
            ).order_by("PatientName")

            mypatientsDecline=Patient.objects.distinct().filter(
                Q(Progress__icontains="Decline") &
                ~Q(Action="TC")
            ).order_by("PatientName")
            
            mypatientsOn_Hold=Patient.objects.distinct().filter(
                Q(Progress__icontains="On-Hold") &
                ~Q(Action="TC")
            ).order_by("PatientName")
        else:
            # mypatients=Patient.objects.filter(Dentist=request.user).order_by("PatientName")

            mypatientsAccept = Patient.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(Progress__icontains="Accepted") &
                ~Q(Action="TC")
            ).order_by("PatientName")

            mypatientsReview = Patient.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(Progress__icontains="Review")
            ).order_by("PatientName")

            mypatientsDecline = Patient.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(Progress__icontains="Decline") &
                ~Q(Action="TC")
            ).order_by("PatientName")

            mypatientsOn_Hold = Patient.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(Progress__icontains="On-Hold") &
                ~Q(Action="TC")
            ).order_by("PatientName")

        context={
            'patients':'active',
            'mypatientsAccept':mypatientsAccept,
            'mypatientsReview':mypatientsReview,
            'mypatientsDecline':mypatientsDecline,
            'mypatientsOn_Hold':mypatientsOn_Hold
        }

        return render(request,'patients.html',context)
    else:
        return redirect('dashboard')

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
    # if request.user.is_superuser or request.user.is_staff:
    mypatients=Patient.objects.filter(Action="TC").order_by("PatientName")
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
    if request.user.is_admin or request.user.is_dentist: 
        if request.user.is_superuser or request.user.is_staff:
            mypatients=Patient.objects.filter(Progress="New").order_by("-Date")
            if "Save" in request.POST:
                patientObj = Patient.objects.get(id=request.POST.get('id'))
                patientObj.Status = request.POST.get('Status')
                patientObj.Stage = request.POST.get('Stage')
                patientObj.save()
        else:
            mypatients=Patient.objects.filter(Dentist=request.user,Progress="New").order_by("-Date")
            if "Save" in request.POST:
                id=request.POST.get('id')
                editpatient=Patient.objects.get(id=id)
                editpatient.Progress=request.POST.get('Progress')
                editpatient.Treatment=request.POST.get('Treatment')
                editpatient.save()
        context={
            'patients':'active',
            'mypatients':mypatients,
        }
        return render(request,'patientnew.html',context)
    else:
        return redirect('dashboard')

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
        Progress = "New"
        Stage = "New"
        Action = "In progress"
        patient=Patient(Dentist=Dentist,Prescriber=Prescriber,Clinic=Clinic,Email=Email,Telephone=Telephone,Address1=Address1,Address2=Address2,PatientName=PatientName,Sex=Sex,TreatmentInPast=TreatmentInPast,Age=Age,OralScan=OralScan,Impression=Impression,UpperJaw=UpperJaw,LowerJaw=LowerJaw,Photo1=Photo1,Photo2=Photo2,Photo3=Photo3,Photo4=Photo4,Treatment=Treatment,TreatmentRequired=TreatmentRequired,Aligners=Aligners,TreatmentLimit=TreatmentLimit,Overbite=Overbite,Overjet=Overjet,Expension=Expension,IPR=IPR,Procline=Procline,Distalize=Distalize,UpperMidline=UpperMidline,LoverMidline=LoverMidline,ArchForm=ArchForm,PCrossbite=PCrossbite,Hint1=Hint1,Hint2=Hint2,Hint3=Hint3,Status=Status,DentistNote=DentistNote,AdminNote=AdminNote,Progress=Progress,Stage=Stage,Action=Action)
        patient.save()
        UpperArchBoxObj = UpperArchBox.objects.create(patient=patient,name="Model")
        UpperArchBoxObj.save()
        UpperArchBoxObj = UpperArchBox.objects.create(patient=patient,name="Aligner")
        UpperArchBoxObj.save()
        UpperArchBoxObj = UpperArchBox.objects.create(patient=patient,name="Ready")
        UpperArchBoxObj.save()
        UpperArchBoxObj = UpperArchBox.objects.create(patient=patient,name="Material")
        UpperArchBoxObj.save()
        LowerArchBoxObj = LowerArchBox.objects.create(patient=patient,name="Model")
        LowerArchBoxObj.save()
        LowerArchBoxObj = LowerArchBox.objects.create(patient=patient,name="Aligner")
        LowerArchBoxObj.save()
        LowerArchBoxObj = LowerArchBox.objects.create(patient=patient,name="Ready")
        LowerArchBoxObj.save()
        LowerArchBoxObj = LowerArchBox.objects.create(patient=patient,name="Material")
        LowerArchBoxObj.save()
        
        
        messages.success(request,"Patient has been added successfully!")

    context={
        'dentists':'active',
        'treatmentrequestfile':treatmentrequestfile,
    }
    return render(request,'addnewpatient.html',context)

@login_required(login_url='login')
def patientdetail(request,id):
    patient=Patient.objects.get(id=id)
    adminuploads=ImageUploadAdmin.objects.filter(Patient=patient).order_by('-id')[:1]
    if "Proposed" in request.POST:
        ProposedTreatment=request.FILES.get('ProposedTreatment')
        Invoice=request.FILES.get('Invoice')
        ThreeDViewProposed=request.FILES.get('ThreeDViewProposed')
        try:
            proposed_objs=PatientProposedTreatment.objects.get(Patient=patient, user=request.user)
            if ProposedTreatment:
                proposed_objs.ProposedTreatment = ProposedTreatment
            if ThreeDViewProposed:
                proposed_objs.ThreeDViewProposed = ThreeDViewProposed
            if Invoice:
                proposed_objs.Invoice = Invoice
            proposed_objs.save()

        except:
            proposed_objs=PatientProposedTreatment(ProposedTreatment=ProposedTreatment,Invoice=Invoice,ThreeDViewProposed=ThreeDViewProposed,Patient=patient,user=request.user)
            proposed_objs.save()
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
    if "lineAmount" in request.POST:
        amount = request.POST.get('line1Length')
        if int(amount) > 0 and int(amount) < 16:
            patient.UpperArch = amount
            patient.save()
    
    if "lineAmount2" in request.POST:
        amount = request.POST.get('line2Length')
        if int(amount) > 0 and int(amount) < 16:
            patient.LowerArch = amount
            patient.save()

    if "line1" in request.POST:
        UpperArchModelBoxObj = UpperArchBox.objects.get(patient=patient, name="Model")
        UpperArchAlignerBoxObj = UpperArchBox.objects.get(patient=patient, name="Aligner")
        UpperArchReadyBoxObj = UpperArchBox.objects.get(patient=patient, name="Ready")
        UpperArchMaterialBoxObj = UpperArchBox.objects.get(patient=patient, name="Material")
        Modelstage1 = request.POST.get('Modelstage1')
        Modelstage2 = request.POST.get('Modelstage2')
        Modelstage3 = request.POST.get('Modelstage3')
        Modelstage4 = request.POST.get('Modelstage4')
        Modelstage5 = request.POST.get('Modelstage5')
        Modelstage6 = request.POST.get('Modelstage6')
        Modelstage7 = request.POST.get('Modelstage7')
        Modelstage8 = request.POST.get('Modelstage8')
        Modelstage9 = request.POST.get('Modelstage9')
        Modelstage10 = request.POST.get('Modelstage10')
        Modelstage11 = request.POST.get('Modelstage11')
        Modelstage12 = request.POST.get('Modelstage12')
        Modelstage13 = request.POST.get('Modelstage13')
        Modelstage14 = request.POST.get('Modelstage14')
        Modelstage15 = request.POST.get('Modelstage15')
        if Modelstage1 == "on":
            UpperArchModelBoxObj.stage1 = True
        else:
            UpperArchModelBoxObj.stage1 = False
        if Modelstage2 == "on":
            UpperArchModelBoxObj.stage2 = True
        else:
            UpperArchModelBoxObj.stage2 = False
        if Modelstage3 == "on":
            UpperArchModelBoxObj.stage3 = True
        else:
            UpperArchModelBoxObj.stage3 = False
        if Modelstage4 == "on":
            UpperArchModelBoxObj.stage4 = True
        else:
            UpperArchModelBoxObj.stage4 = False
        if Modelstage5 == "on":
            UpperArchModelBoxObj.stage5 = True
        else:
            UpperArchModelBoxObj.stage5 = False
        if Modelstage6 == "on":
            UpperArchModelBoxObj.stage6 = True
        else:
            UpperArchModelBoxObj.stage6 = False
        if Modelstage7 == "on":
            UpperArchModelBoxObj.stage7 = True
        else:
            UpperArchModelBoxObj.stage7 = False
        if Modelstage8 == "on":
            UpperArchModelBoxObj.stage8 = True
        else:
            UpperArchModelBoxObj.stage8 = False
        if Modelstage9 == "on":
            UpperArchModelBoxObj.stage9 = True
        else:
            UpperArchModelBoxObj.stage9 = False
        if Modelstage10 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False 
        if Modelstage11 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False
        if Modelstage12 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False
        if Modelstage13 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False 
        if Modelstage14 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False 
        if Modelstage15 == "on":
            UpperArchModelBoxObj.stage10 = True 
        else:
            UpperArchModelBoxObj.stage10 = False    
        UpperArchModelBoxObj.save()  
            #************************************************ Aligners
        if request.POST.get('Alignerstage1') == "on":
            UpperArchAlignerBoxObj.stage1 = True
        else:
            UpperArchAlignerBoxObj.stage1 = False
        if request.POST.get('Alignerstage2') == "on":
            UpperArchAlignerBoxObj.stage2 = True
        else:
            UpperArchAlignerBoxObj.stage2 = False
        if request.POST.get('Alignerstage3') == "on":
            UpperArchAlignerBoxObj.stage3 = True
        else:
            UpperArchAlignerBoxObj.stage3 = False
        if request.POST.get('Alignerstage4') == "on":
            UpperArchAlignerBoxObj.stage4 = True
        else:
            UpperArchAlignerBoxObj.stage4 = False
        if request.POST.get('Alignerstage5') == "on":
            UpperArchAlignerBoxObj.stage5 = True
        else:
            UpperArchAlignerBoxObj.stage5 = False
        if request.POST.get('Alignerstage6') == "on":
            UpperArchAlignerBoxObj.stage6 = True
        else:
            UpperArchAlignerBoxObj.stage6 = False
        if request.POST.get('Alignerstage7') == "on":
            UpperArchAlignerBoxObj.stage7 = True
        else:
            UpperArchAlignerBoxObj.stage7 = False
        if request.POST.get('Alignerstage8') == "on":
            UpperArchAlignerBoxObj.stage8 = True
        else:
            UpperArchAlignerBoxObj.stage8 = False
        if request.POST.get('Alignerstage9') == "on":
            UpperArchAlignerBoxObj.stage9 = True
        else:
            UpperArchAlignerBoxObj.stage9 = False
        if request.POST.get('Alignerstage10') == "on":
            UpperArchAlignerBoxObj.stage10 = True
        else:
            UpperArchAlignerBoxObj.stage10 = False
        if request.POST.get('Alignerstage11') == "on":
            UpperArchAlignerBoxObj.stage11 = True
        else:
            UpperArchAlignerBoxObj.stage11 = False
        if request.POST.get('Alignerstage12') == "on":
            UpperArchAlignerBoxObj.stage12 = True
        else:
            UpperArchAlignerBoxObj.stage12 = False
        if request.POST.get('Alignerstage13') == "on":
            UpperArchAlignerBoxObj.stage13 = True
        else:
            UpperArchAlignerBoxObj.stage13 = False
        if request.POST.get('Alignerstage14') == "on":
            UpperArchAlignerBoxObj.stage14 = True
        else:
            UpperArchAlignerBoxObj.stage14 = False
        if request.POST.get('Alignerstage15') == "on":
            UpperArchAlignerBoxObj.stage15 = True
        else:
            UpperArchAlignerBoxObj.stage15 = False
        UpperArchAlignerBoxObj.save()
            #************************************************ Ready
        if request.POST.get('Readystage1') == "on":
            UpperArchReadyBoxObj.stage1 = True
        else:
            UpperArchReadyBoxObj.stage1 = False
        if request.POST.get('Readystage2') == "on":
            UpperArchReadyBoxObj.stage2 = True
        else:
            UpperArchReadyBoxObj.stage2 = False
        if request.POST.get('Readystage3') == "on":
            UpperArchReadyBoxObj.stage3 = True
        else:
            UpperArchReadyBoxObj.stage3 = False
        if request.POST.get('Readystage4') == "on":
            UpperArchReadyBoxObj.stage4 = True
        else:
            UpperArchReadyBoxObj.stage4 = False
        if request.POST.get('Readystage5') == "on":
            UpperArchReadyBoxObj.stage5 = True
        else:
            UpperArchReadyBoxObj.stage5 = False
        if request.POST.get('Readystage6') == "on":
            UpperArchReadyBoxObj.stage6 = True
        else:
            UpperArchReadyBoxObj.stage6 = False
        if request.POST.get('Readystage7') == "on":
            UpperArchReadyBoxObj.stage7 = True
        else:
            UpperArchReadyBoxObj.stage7 = False
        if request.POST.get('Readystage8') == "on":
            UpperArchReadyBoxObj.stage8 = True
        else:
            UpperArchReadyBoxObj.stage8 = False
        if request.POST.get('Readystage9') == "on":
            UpperArchReadyBoxObj.stage9 = True
        else:
            UpperArchReadyBoxObj.stage9 = False
        if request.POST.get('Readystage10') == "on":
            UpperArchReadyBoxObj.stage10 = True
        else:
            UpperArchReadyBoxObj.stage10 = False
        if request.POST.get('Readystage11') == "on":
            UpperArchReadyBoxObj.stage11 = True
        else:
            UpperArchReadyBoxObj.stage11 = False
        if request.POST.get('Readystage12') == "on":
            UpperArchReadyBoxObj.stage12 = True
        else:
            UpperArchReadyBoxObj.stage12 = False
        if request.POST.get('Readystage13') == "on":
            UpperArchReadyBoxObj.stage13 = True
        else:
            UpperArchReadyBoxObj.stage13 = False
        if request.POST.get('Readystage14') == "on":
            UpperArchReadyBoxObj.stage14 = True
        else:
            UpperArchReadyBoxObj.stage14 = False
        if request.POST.get('Readystage15') == "on":
            UpperArchReadyBoxObj.stage15 = True
        else:
            UpperArchReadyBoxObj.stage15 = False
        UpperArchReadyBoxObj.save()
        #************************************************ Material
        if request.POST.get('Materialstage1') == "on":
            UpperArchMaterialBoxObj.stage1 = True
        else:
            UpperArchMaterialBoxObj.stage1 = False
        if request.POST.get('Materialstage2') == "on":
            UpperArchMaterialBoxObj.stage2 = True
        else:
            UpperArchMaterialBoxObj.stage2 = False
        if request.POST.get('Materialstage3') == "on":
            UpperArchMaterialBoxObj.stage3 = True
        else:
            UpperArchMaterialBoxObj.stage3 = False
        if request.POST.get('Materialstage4') == "on":
            UpperArchMaterialBoxObj.stage4 = True
        else:
            UpperArchMaterialBoxObj.stage4 = False
        if request.POST.get('Materialstage5') == "on":
            UpperArchMaterialBoxObj.stage5 = True
        else:
            UpperArchMaterialBoxObj.stage5 = False
        if request.POST.get('Materialstage6') == "on":
            UpperArchMaterialBoxObj.stage6 = True
        else:
            UpperArchMaterialBoxObj.stage6 = False
        if request.POST.get('Materialstage7') == "on":
            UpperArchMaterialBoxObj.stage7 = True
        else:
            UpperArchMaterialBoxObj.stage7 = False
        if request.POST.get('Materialstage8') == "on":
            UpperArchMaterialBoxObj.stage8 = True
        else:
            UpperArchMaterialBoxObj.stage8 = False
        if request.POST.get('Materialstage9') == "on":
            UpperArchMaterialBoxObj.stage9 = True
        else:
            UpperArchMaterialBoxObj.stage9 = False
        if request.POST.get('Materialstage10') == "on":
            UpperArchMaterialBoxObj.stage10 = True
        else:
            UpperArchMaterialBoxObj.stage10 = False
        if request.POST.get('Materialstage11') == "on":
            UpperArchMaterialBoxObj.stage11 = True
        else:
            UpperArchMaterialBoxObj.stage11 = False
        if request.POST.get('Materialstage12') == "on":
            UpperArchMaterialBoxObj.stage12 = True
        else:
            UpperArchMaterialBoxObj.stage12 = False
        if request.POST.get('Materialstage13') == "on":
            UpperArchMaterialBoxObj.stage13 = True
        else:
            UpperArchMaterialBoxObj.stage13 = False
        if request.POST.get('Materialstage14') == "on":
            UpperArchMaterialBoxObj.stage14 = True
        else:
            UpperArchMaterialBoxObj.stage14 = False
        if request.POST.get('Materialstage15') == "on":
            UpperArchMaterialBoxObj.stage15 = True
        else:
            UpperArchMaterialBoxObj.stage15 = False
        UpperArchMaterialBoxObj.save()
    if "line2" in request.POST:
        LowerArchModelBoxObj = LowerArchBox.objects.get(patient=patient, name="Model")
        LowerArchAlignerBoxObj = LowerArchBox.objects.get(patient=patient, name="Aligner")
        LowerArchReadyBoxObj = LowerArchBox.objects.get(patient=patient, name="Ready")
        LowerArchMaterialBoxObj = LowerArchBox.objects.get(patient=patient, name="Material")
        Modelstage1 = request.POST.get('Modelstage1')
        Modelstage2 = request.POST.get('Modelstage2')
        Modelstage3 = request.POST.get('Modelstage3')
        Modelstage4 = request.POST.get('Modelstage4')
        Modelstage5 = request.POST.get('Modelstage5')
        Modelstage6 = request.POST.get('Modelstage6')
        Modelstage7 = request.POST.get('Modelstage7')
        Modelstage8 = request.POST.get('Modelstage8')
        Modelstage9 = request.POST.get('Modelstage9')
        Modelstage10 = request.POST.get('Modelstage10')
        Modelstage11 = request.POST.get('Modelstage11')
        Modelstage12 = request.POST.get('Modelstage12')
        Modelstage13 = request.POST.get('Modelstage13')
        Modelstage14 = request.POST.get('Modelstage14')
        Modelstage15 = request.POST.get('Modelstage15')
        if Modelstage1 == "on":
            LowerArchModelBoxObj.stage1 = True
        else:
            LowerArchModelBoxObj.stage1 = False
        if Modelstage2 == "on":
            LowerArchModelBoxObj.stage2 = True
        else:
            LowerArchModelBoxObj.stage2 = False
        if Modelstage3 == "on":
            LowerArchModelBoxObj.stage3 = True
        else:
            LowerArchModelBoxObj.stage3 = False
        if Modelstage4 == "on":
            LowerArchModelBoxObj.stage4 = True
        else:
            LowerArchModelBoxObj.stage4 = False
        if Modelstage5 == "on":
            LowerArchModelBoxObj.stage5 = True
        else:
            LowerArchModelBoxObj.stage5 = False
        if Modelstage6 == "on":
            LowerArchModelBoxObj.stage6 = True
        else:
            LowerArchModelBoxObj.stage6 = False
        if Modelstage7 == "on":
            LowerArchModelBoxObj.stage7 = True
        else:
            LowerArchModelBoxObj.stage7 = False
        if Modelstage8 == "on":
            LowerArchModelBoxObj.stage8 = True
        else:
            LowerArchModelBoxObj.stage8 = False
        if Modelstage9 == "on":
            LowerArchModelBoxObj.stage9 = True
        else:
            LowerArchModelBoxObj.stage9 = False
        if Modelstage10 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False 
        if Modelstage11 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False
        if Modelstage12 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False
        if Modelstage13 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False 
        if Modelstage14 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False 
        if Modelstage15 == "on":
            LowerArchModelBoxObj.stage10 = True 
        else:
            LowerArchModelBoxObj.stage10 = False    
        LowerArchModelBoxObj.save()  
            #************************************************ Aligners
        if request.POST.get('Alignerstage1') == "on":
            LowerArchAlignerBoxObj.stage1 = True
        else:
            LowerArchAlignerBoxObj.stage1 = False
        if request.POST.get('Alignerstage2') == "on":
            LowerArchAlignerBoxObj.stage2 = True
        else:
            LowerArchAlignerBoxObj.stage2 = False
        if request.POST.get('Alignerstage3') == "on":
            LowerArchAlignerBoxObj.stage3 = True
        else:
            LowerArchAlignerBoxObj.stage3 = False
        if request.POST.get('Alignerstage4') == "on":
            LowerArchAlignerBoxObj.stage4 = True
        else:
            LowerArchAlignerBoxObj.stage4 = False
        if request.POST.get('Alignerstage5') == "on":
            LowerArchAlignerBoxObj.stage5 = True
        else:
            LowerArchAlignerBoxObj.stage5 = False
        if request.POST.get('Alignerstage6') == "on":
            LowerArchAlignerBoxObj.stage6 = True
        else:
            LowerArchAlignerBoxObj.stage6 = False
        if request.POST.get('Alignerstage7') == "on":
            LowerArchAlignerBoxObj.stage7 = True
        else:
            LowerArchAlignerBoxObj.stage7 = False
        if request.POST.get('Alignerstage8') == "on":
            LowerArchAlignerBoxObj.stage8 = True
        else:
            LowerArchAlignerBoxObj.stage8 = False
        if request.POST.get('Alignerstage9') == "on":
            LowerArchAlignerBoxObj.stage9 = True
        else:
            LowerArchAlignerBoxObj.stage9 = False
        if request.POST.get('Alignerstage10') == "on":
            LowerArchAlignerBoxObj.stage10 = True
        else:
            LowerArchAlignerBoxObj.stage10 = False
        if request.POST.get('Alignerstage11') == "on":
            LowerArchAlignerBoxObj.stage11 = True
        else:
            LowerArchAlignerBoxObj.stage11 = False
        if request.POST.get('Alignerstage12') == "on":
            LowerArchAlignerBoxObj.stage12 = True
        else:
            LowerArchAlignerBoxObj.stage12 = False
        if request.POST.get('Alignerstage13') == "on":
            LowerArchAlignerBoxObj.stage13 = True
        else:
            LowerArchAlignerBoxObj.stage13 = False
        if request.POST.get('Alignerstage14') == "on":
            LowerArchAlignerBoxObj.stage14 = True
        else:
            LowerArchAlignerBoxObj.stage14 = False
        if request.POST.get('Alignerstage15') == "on":
            LowerArchAlignerBoxObj.stage15 = True
        else:
            LowerArchAlignerBoxObj.stage15 = False
        LowerArchAlignerBoxObj.save()
            #************************************************ Ready
        if request.POST.get('Readystage1') == "on":
            LowerArchReadyBoxObj.stage1 = True
        else:
            LowerArchReadyBoxObj.stage1 = False
        if request.POST.get('Readystage2') == "on":
            LowerArchReadyBoxObj.stage2 = True
        else:
            LowerArchReadyBoxObj.stage2 = False
        if request.POST.get('Readystage3') == "on":
            LowerArchReadyBoxObj.stage3 = True
        else:
            LowerArchReadyBoxObj.stage3 = False
        if request.POST.get('Readystage4') == "on":
            LowerArchReadyBoxObj.stage4 = True
        else:
            LowerArchReadyBoxObj.stage4 = False
        if request.POST.get('Readystage5') == "on":
            LowerArchReadyBoxObj.stage5 = True
        else:
            LowerArchReadyBoxObj.stage5 = False
        if request.POST.get('Readystage6') == "on":
            LowerArchReadyBoxObj.stage6 = True
        else:
            LowerArchReadyBoxObj.stage6 = False
        if request.POST.get('Readystage7') == "on":
            LowerArchReadyBoxObj.stage7 = True
        else:
            LowerArchReadyBoxObj.stage7 = False
        if request.POST.get('Readystage8') == "on":
            LowerArchReadyBoxObj.stage8 = True
        else:
            LowerArchReadyBoxObj.stage8 = False
        if request.POST.get('Readystage9') == "on":
            LowerArchReadyBoxObj.stage9 = True
        else:
            LowerArchReadyBoxObj.stage9 = False
        if request.POST.get('Readystage10') == "on":
            LowerArchReadyBoxObj.stage10 = True
        else:
            LowerArchReadyBoxObj.stage10 = False
        if request.POST.get('Readystage11') == "on":
            LowerArchReadyBoxObj.stage11 = True
        else:
            LowerArchReadyBoxObj.stage11 = False
        if request.POST.get('Readystage12') == "on":
            LowerArchReadyBoxObj.stage12 = True
        else:
            LowerArchReadyBoxObj.stage12 = False
        if request.POST.get('Readystage13') == "on":
            LowerArchReadyBoxObj.stage13 = True
        else:
            LowerArchReadyBoxObj.stage13 = False
        if request.POST.get('Readystage14') == "on":
            LowerArchReadyBoxObj.stage14 = True
        else:
            LowerArchReadyBoxObj.stage14 = False
        if request.POST.get('Readystage15') == "on":
            LowerArchReadyBoxObj.stage15 = True
        else:
            LowerArchReadyBoxObj.stage15 = False
        LowerArchReadyBoxObj.save()
        #************************************************ Material
        if request.POST.get('Materialstage1') == "on":
            LowerArchMaterialBoxObj.stage1 = True
        else:
            LowerArchMaterialBoxObj.stage1 = False
        if request.POST.get('Materialstage2') == "on":
            LowerArchMaterialBoxObj.stage2 = True
        else:
            LowerArchMaterialBoxObj.stage2 = False
        if request.POST.get('Materialstage3') == "on":
            LowerArchMaterialBoxObj.stage3 = True
        else:
            LowerArchMaterialBoxObj.stage3 = False
        if request.POST.get('Materialstage4') == "on":
            LowerArchMaterialBoxObj.stage4 = True
        else:
            LowerArchMaterialBoxObj.stage4 = False
        if request.POST.get('Materialstage5') == "on":
            LowerArchMaterialBoxObj.stage5 = True
        else:
            LowerArchMaterialBoxObj.stage5 = False
        if request.POST.get('Materialstage6') == "on":
            LowerArchMaterialBoxObj.stage6 = True
        else:
            LowerArchMaterialBoxObj.stage6 = False
        if request.POST.get('Materialstage7') == "on":
            LowerArchMaterialBoxObj.stage7 = True
        else:
            LowerArchMaterialBoxObj.stage7 = False
        if request.POST.get('Materialstage8') == "on":
            LowerArchMaterialBoxObj.stage8 = True
        else:
            LowerArchMaterialBoxObj.stage8 = False
        if request.POST.get('Materialstage9') == "on":
            LowerArchMaterialBoxObj.stage9 = True
        else:
            LowerArchMaterialBoxObj.stage9 = False
        if request.POST.get('Materialstage10') == "on":
            LowerArchMaterialBoxObj.stage10 = True
        else:
            LowerArchMaterialBoxObj.stage10 = False
        if request.POST.get('Materialstage11') == "on":
            LowerArchMaterialBoxObj.stage11 = True
        else:
            LowerArchMaterialBoxObj.stage11 = False
        if request.POST.get('Materialstage12') == "on":
            LowerArchMaterialBoxObj.stage12 = True
        else:
            LowerArchMaterialBoxObj.stage12 = False
        if request.POST.get('Materialstage13') == "on":
            LowerArchMaterialBoxObj.stage13 = True
        else:
            LowerArchMaterialBoxObj.stage13 = False
        if request.POST.get('Materialstage14') == "on":
            LowerArchMaterialBoxObj.stage14 = True
        else:
            LowerArchMaterialBoxObj.stage14 = False
        if request.POST.get('Materialstage15') == "on":
            LowerArchMaterialBoxObj.stage15 = True
        else:
            LowerArchMaterialBoxObj.stage15 = False
        LowerArchMaterialBoxObj.save() 

    try:
        proposed=PatientProposedTreatment.objects.get(Patient=patient, user=request.user)
    except:
        proposed = "None"

    UpperArchBoxObj = UpperArchBox.objects.filter(patient=patient)
    LowerArchBoxObj = LowerArchBox.objects.filter(patient=patient)
    context={
        'patient':patient,
        'UpperArchBox':UpperArchBoxObj,
        'LowerArchBox':LowerArchBoxObj,
        'proposed':proposed,
        'adminuploads':adminuploads,
    }
    return render(request, 'patientdetail.html', context)

# Referrals
@login_required(login_url='login')
def referrals(request):

    if request.method=="POST":

        referral_obj = Referral.objects.get(id=request.POST.get('id'))
        referral_obj.Stage = request.POST.get('Stage')
        referral_obj.Status = request.POST.get('Status')
        referral_obj.save()

    if request.user.is_superuser or request.user.is_staff:
        implant_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Implant") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        orthodontics_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Orthodontics") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        root_canal_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Root Canal") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        crown_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Crown") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")
        print("Otho",orthodontics_referral.count())
        print("crown",crown_referral.count(),"********************")
    else:
        implant_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Implant") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        orthodontics_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Orthodontics") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        root_canal_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Root Canal") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        crown_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Crown") &
                Q(Status="In progress") |
                Q(Status="Booked")
            ).order_by("PatientName")

        # consultation_referral = Referral.objects.distinct().filter(
        #         Q(Dentist=request.user) &
        #         Q(ReferralReason="Consultation") &
        #         Q(Status="In progress")
        #     ).order_by("PatientName")

    context={
        'referral':'active',
        'implant_referral': implant_referral,
        'orthodontics_referral': orthodontics_referral,
        'root_canal_referral': root_canal_referral,
        'crown_referral': crown_referral,
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
            editreferral.ReferralReason=request.POST.get('ReferralReason')
            editreferral.save()        
    else:
        myreferrals=Referral.objects.filter(Dentist=request.user,Status="New").order_by("-Date")
        if "Save" in request.POST:
            id=request.POST.get('id')
            editreferral=Referral.objects.get(id=id)
            editreferral.Status=request.POST.get('Status')
            editreferral.ReferralReason=request.POST.get('ReferralReason')
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
        implant_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Implant") &
                ~Q(Status="In progress") &
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        orthodontics_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Orthodontics") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        root_canal_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Root Canal") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        crown_referral = Referral.objects.distinct().filter(
                Q(ReferralReason="Crown") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")
    else:
        implant_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Implant") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        orthodontics_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Orthodontics") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        root_canal_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Root Canal") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")

        crown_referral = Referral.objects.distinct().filter(
                Q(Dentist=request.user) &
                Q(ReferralReason="Crown") &
                ~Q(Status="In progress")&
                ~Q(Status="New")&
                ~Q(Status="Booked")
            ).order_by("PatientName")
    context={
        'referrals':'active',
        'implant_referral':implant_referral,
        'orthodontics_referral':orthodontics_referral,
        'root_canal_referral': root_canal_referral,
        'crown_referral': crown_referral
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
    BACS= Payment.objects.filter(PaymentMethod="BACS",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    finance= Payment.objects.filter(PaymentMethod="Finance",Date=date).aggregate(Sum('Amount')).get('Amount__sum') or 0
    total=cashsum+card11sum+card14sum+BACS+finance
    context={
        'payment':'active',
        'cashsum':cashsum,
        'card11sum':card11sum,
        'card14sum':card14sum,
        'BACS':BACS,
        'finance':finance,
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
    if not request.user.is_dentist:
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
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def paymentdailyreport(request):
    if not request.user.is_dentist:
        date=datetime.now().strftime("%Y-%m-%d")
        cashsum= Payment.objects.filter(Date=date,PaymentMethod="Cash").aggregate(Sum('Amount')).get('Amount__sum') or 0
        card11sum= Payment.objects.filter(Date=date,PaymentMethod="Card11").aggregate(Sum('Amount')).get('Amount__sum') or 0
        card14sum= Payment.objects.filter(Date=date,PaymentMethod="Card14").aggregate(Sum('Amount')).get('Amount__sum') or 0
        BACS= Payment.objects.filter(Date=date,PaymentMethod="BACS").aggregate(Sum('Amount')).get('Amount__sum') or 0
        finance= Payment.objects.filter(Date=date,PaymentMethod="Finance").aggregate(Sum('Amount')).get('Amount__sum') or 0
        total=cashsum+card11sum+card14sum+BACS+finance
        context={
            'payment':'active',
            'cashsum':cashsum,
            'card11sum':card11sum,
            'card14sum':card14sum,
            'BACS':BACS,
            'finance':finance,
            'date':date ,
            'total':total,

        }
        return render(request,'paymentdailyreport.html',context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def paymentfullreport(request):
    if not request.user.is_dentist:
        date=datetime.now().strftime("%Y-%m-%d")
        StartDate=date
        EndDate=date
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
            if editpayments.PaymentMethod == "Cash":
                try:
                    incomeObj = Income.objects.get(Date=editpayments.Date,Title="CASH")
                    incomeObj.Amount += editpayments.Amount
                    incomeObj.save()
                except:
                    incomeObj = Income(Date=editpayments.Date, Title="CASH", Category="CASH-UP", Account = "MB-CASH", Status="Pending", Amount=editpayments.Amount)
                    incomeObj.save()
            elif editpayments.PaymentMethod == "Card11":
                try:
                    incomeObj = Income.objects.get(Date=editpayments.Date,Title="Card11")
                    incomeObj.Amount += editpayments.Amount
                    incomeObj.save()
                except:
                    incomeObj = Income(Date=editpayments.Date, Title="Card11", Category="CASH-UP", Account = "BEHNAM LTD", Status="Pending", Amount=editpayments.Amount)
                    incomeObj.save()
            elif editpayments.PaymentMethod == "Card14":
                try:
                    incomeObj = Income.objects.get(Date=editpayments.Date,Title="Card14")
                    incomeObj.Amount += editpayments.Amount
                    incomeObj.save()
                except:
                    incomeObj = Income(Date=editpayments.Date, Title="Card14", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayments.Amount)
                    incomeObj.save()
            elif editpayments.PaymentMethod == "BACS":
                try:
                    incomeObj = Income.objects.get(Date=editpayments.Date,Title="BACS")
                    incomeObj.Amount += editpayments.Amount
                    incomeObj.save()
                except:
                    incomeObj = Income(Date=editpayments.Date, Title="BACS", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayments.Amount)
                    incomeObj.save() 
            elif editpayments.PaymentMethod == "Finance":
                try:
                    incomeObj = Income.objects.get(Date=editpayments.Date,Title="Finance")
                    incomeObj.Amount += editpayments.Amount
                    incomeObj.save()
                except:
                    incomeObj = Income(Date=editpayments.Date, Title="Finance", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayments.Amount)
                    incomeObj.save() 
                

            editpayments.Status="Archived"
            editpayments.save() 

        if "Archive_All" in request.POST:
            editpayments=Payment.objects.all()
            for editpayment in editpayments:
                if editpayment.Status =="Pending":
                    editpayment.Status="Archived"
                    editpayment.save()
                    if editpayment.PaymentMethod == "Cash":
                        try:
                            incomeObj = Income.objects.get(Date=editpayment.Date,Title="CASH")
                            incomeObj.Amount += editpayment.Amount
                            incomeObj.save()
                        except:
                            incomeObj = Income(Date=editpayment.Date, Title="CASH", Category="CASH-UP", Account = "MB-CASH", Status="Pending", Amount=editpayment.Amount)
                            incomeObj.save()
                    elif editpayment.PaymentMethod == "Card11":
                        try:
                            incomeObj = Income.objects.get(Date=editpayment.Date,Title="Card11")
                            incomeObj.Amount += editpayment.Amount
                            incomeObj.save()
                        except:
                            incomeObj = Income(Date=editpayment.Date, Title="Card11", Category="CASH-UP", Account = "BEHNAM LTD", Status="Pending", Amount=editpayment.Amount)
                            incomeObj.save()
                    elif editpayment.PaymentMethod == "Card14":
                        try:
                            incomeObj = Income.objects.get(Date=editpayment.Date,Title="Card14")
                            incomeObj.Amount += editpayment.Amount
                            incomeObj.save()
                        except:
                            incomeObj = Income(Date=editpayment.Date, Title="Card14", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayment.Amount)
                            incomeObj.save() 
                    elif editpayment.PaymentMethod == "BACS":
                        try:
                            incomeObj = Income.objects.get(Date=editpayment.Date,Title="BACS")
                            incomeObj.Amount += editpayment.Amount
                            incomeObj.save()
                        except:
                            incomeObj = Income(Date=editpayment.Date, Title="BACS", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayment.Amount)
                            incomeObj.save()
                        
                    elif editpayment.PaymentMethod == "Finance":
                        try:
                            incomeObj = Income.objects.get(Date=editpayment.Date,Title="Finance")
                            incomeObj.Amount += editpayment.Amount
                            incomeObj.save()
                        except:
                            incomeObj = Income(Date=editpayment.Date, Title="Finance", Category="CASH-UP", Account = "MBDENTAL LTD", Status="Pending", Amount=editpayment.Amount)
                            incomeObj.save()
                        

        allpayments=Payment.objects.filter(Date=date,Status="Pending").order_by('-Date')   
        total= Payment.objects.filter(Date=date,Status="Pending").order_by('-Date').aggregate(Sum('Amount')).get('Amount__sum') or 0
        context={
            'payment':'active',
            'allpayments':allpayments,
            'date':date,
            'total':total,
            'StartDate':StartDate,
            'EndDate':EndDate,

        }
        return render(request,'paymentfullreport.html',context)
    else:
        return redirect('dashboard')

def saveincome(request,id):
    incomeObj = Income.objects.get(id=id)
    incomeObj.Status = "Approved"
    incomeObj.save()
    return redirect('account')

def saveexpense(request,id):
    expenseObj = Expense.objects.get(id=id)
    expenseObj.Status = "Approved"
    expenseObj.save()
    return redirect('account')


@login_required(login_url='login')
def paymentfullreportarchived(request):
    if request.user.is_admin:
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
    else:
        return redirect('dashboard')

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

def account(request):
    if request.user.is_admin:
        incomereport=Income.objects.distinct().filter(
            Q(Date__month=datetime.now().month) &
            Q(Date__year=datetime.now().year)
            ).order_by('-Date')

        expensereport=Expense.objects.distinct().filter(
            Q(Date__month=datetime.now().month) &
            Q(Date__year=datetime.now().year)
            ).order_by('-Date')
        context={
            'payment':'active',
            'incomereport':incomereport,
            'expensereport':expensereport
        }
        return render(request,'account.html',context)
    else:
        return redirect('dashboard')

def deleteincome(request,id):
    incomedata=Income.objects.get(id=id)
    incomedata.delete()
    return redirect('account')

def deleteexpense(request,id):
    expensedata=Expense.objects.get(id=id)
    expensedata.delete()
    return redirect('account')

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
    return redirect('account')
    
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
    return redirect('account')
    

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
    if request.user.is_admin:
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
    else:
        return redirect('dashboard')

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
                user.is_dentist = True
                user.save()
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
    if request.user.is_admin:
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
            messages.success(request,"Expense has been added successfully!")
        context={
            'payment':'active',       
            'date':date,
            'title':title,
            'category':category,
        }
        return render(request, 'repeatExpense.html',context)
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def repeatIncome(request):
    if request.user.is_admin:
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
    else:
        return redirect('dashboard')

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

def file_download(request,id):
    patientObj = Patient.objects.get(id=id)
    path = patientObj.file
    print(path,"*******************")
    return FileResponse(open("media/"+str(path), 'rb'))
