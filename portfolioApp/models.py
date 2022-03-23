from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

# Dentist
class DentistProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    Clinic= models.CharField(max_length=100,null=True)
    Address1 = models.CharField(max_length=100,null=True)
    Address2 = models.CharField(max_length=100,null=True)
    City = models.CharField(max_length=100,null=True)
    Postcode = models.CharField(max_length=100,null=True)
    Country = models.CharField(max_length=100,null=True)
    def __str__(self):
        return str(self.user)
    
# Patient
class Patient(models.Model):
    Dentist=models.ForeignKey(User,on_delete=models.CASCADE)
    Prescriber=models.CharField(max_length=100,null=True)
    Clinic=models.CharField(max_length=300,null=True)
    Email=models.CharField(max_length=300,null=True)
    Telephone=models.CharField(max_length=300,null=True)
    PatientName=models.CharField(max_length=100,null=True)
    Sex=models.CharField(max_length=100,null=True)
    TreatmentInPast=models.CharField(max_length=100,null=True)
    Age=models.CharField(max_length=100,null=True)
    Address1=models.CharField(max_length=100,null=True)
    Address2=models.CharField(max_length=100,null=True)
    OralScan=models.CharField(max_length=100,null=True)
    Impression=models.CharField(max_length=100,null=True)
    UpperJaw=models.FileField(null=True)
    LowerJaw=models.FileField(null=True)
    Photo1=models.ImageField(null=True)
    Photo2=models.ImageField(null=True)
    Photo3=models.ImageField(null=True)
    Photo4=models.ImageField(null=True)
    Treatment=models.CharField(max_length=50,null=True)
    TreatmentRequired=models.CharField(max_length=50,null=True)
    Aligners=models.CharField(max_length=50,null=True)
    TreatmentLimit=models.CharField(max_length=50,null=True)
    Overbite=models.CharField(max_length=50,null=True)
    Overjet=models.CharField(max_length=50,null=True)
    Expension=models.CharField(max_length=50,null=True)
    IPR=models.CharField(max_length=50,null=True)
    Procline=models.CharField(max_length=50,null=True)
    Distalize=models.CharField(max_length=50,null=True)
    UpperMidline=models.CharField(max_length=50,null=True)
    LoverMidline=models.CharField(max_length=50,null=True)
    ArchForm=models.CharField(max_length=50,null=True)
    PCrossbite=models.CharField(max_length=50,null=True)
    Hint1=models.CharField(max_length=50,null=True)
    Hint2=models.CharField(max_length=50,null=True)
    Hint3=models.CharField(max_length=50,null=True)
    DentistNote=models.TextField(default="Not Added",null=True)
    AdminNote=models.TextField(default="Not Added",null=True)
    Status=models.CharField(max_length=20,default="Pending",null=True,choices=(("Accept","Accept"),("Review","Review"),("Decline","Decline"),("On-Hold","On-Hold")
    ))
    InternalStatus=models.CharField(max_length=30,null=True,default="On")
    Date=models.DateField(auto_now_add=True)
    file=models.FileField(null=True)
    def __str__(self):
        return str(self.id) + "  |  " + self.PatientName + "  |  " + str(self.Date) 
    
class PatientProposedTreatment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    Patient=models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    ProposedTreatment=models.FileField(null=True)
    ThreeDViewProposed=models.FileField(null=True)
    Invoice=models.FileField(null=True)
    Time=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.Patient) + " | " + self.user.username + " | " + str(self.Time)

class ImageUploadAdmin(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    Patient=models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    Image1=models.FileField()
    Image2=models.FileField()
    Image3=models.FileField()
    Time=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.Patient) + " | " + self.user.username + " | " + str(self.Time)

class TreatmentRequestFile(models.Model):
    File=models.FileField()
    
# Referral
class Referral(models.Model):
    Dentist=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    DentistName=models.CharField(max_length=50,null=True)
    PatientName=models.CharField(max_length=50)
    PatientPhone=models.CharField(max_length=20)
    PatientEmail=models.CharField(max_length=40)
    ReferralReason=models.CharField(max_length=60,default="Consultation",null=True,choices=(("Consultation","Consultation"),("Implant","Implant"),("Orthodontics","Orthodontics"),("Root Canal Treatment","Root Canal Treatment"),("Implant","Crown and Veneers")
    ))
    Status=models.CharField(max_length=40,default="In Progress",null=True,choices=(("Inprogress","Inprogress"),("Accepted","Accepted"),("TC","TC"),("Declined","Declined")
    ))
    BookedOn=models.CharField(max_length=40,null=True)
    TreatmentPlan=models.CharField(max_length=80,null=True)
    Note=models.CharField(max_length=150,null=True)
    Stage=models.CharField(max_length=150,null=True)
    Date=models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.id) + "  |  " + self.PatientName + "  |  " + str(self.Date) 

# Payment
class Payment(models.Model):
    Date=models.DateField()
    User=models.CharField(max_length=50)
    PatientName=models.CharField(max_length=50)
    Dentist=models.CharField(max_length=50)
    Scheme=models.CharField(max_length=50)
    PaymentMethod=models.CharField(max_length=50)
    Amount=models.FloatField()
    Status=models.CharField(max_length=50,default="Pending")

    def __str__(self):
        return str(self.Date) + " | " + self.User + " | " + self.PatientName

# Payment
class Income(models.Model):
    Date=models.DateField()
    Title=models.CharField(max_length=50)
    Category=models.CharField(max_length=50)
    Account=models.CharField(max_length=50)
    Amount=models.FloatField()
    Status=models.CharField(max_length=20,null=True)
    Note=models.TextField()
    Repeat=models.CharField(max_length=20,null=True)
    RepeatStatus=models.CharField(max_length=20,null=True,default="On")

    def __str__(self):
        return str(self.Date) + " | " + self.Title + " | " + self.Category
  
class Expense(models.Model):
    Date=models.DateField()
    Title=models.CharField(max_length=50)
    Category=models.CharField(max_length=50)
    Account=models.CharField(max_length=50)
    Amount=models.FloatField()
    Status=models.CharField(max_length=20,null=True)
    Note=models.TextField()
    Repeat=models.CharField(max_length=20,null=True)


    def __str__(self):
        return str(self.Date) + " | " + self.Title + " | " + self.Category

class IncomeExpenseTitle(models.Model):
    Title=models.CharField(max_length=50)

    def __str__(self):
        return self.Title

class IncomeExpenseCategory(models.Model):
    Category=models.CharField(max_length=50)

    def __str__(self):
        return self.Category
  
# Labs  
class LabWork(models.Model):
    date=models.DateField(auto_now_add=True)
    PatientName=models.CharField(max_length=100)
    PatientID=models.CharField(max_length=100,null=True)
    Dentist=models.CharField(max_length=100)
    Scheme=models.CharField(max_length=100)
    Lab=models.CharField(max_length=100)
    Type=models.CharField(max_length=50,null=True)
    Quantity=models.CharField(max_length=50,null=True)
    Note=models.CharField(max_length=50,null=True)
    Stage=models.CharField(max_length=40,null=True)
    Status=models.CharField(max_length=40,null=True)
    DateArriving=models.CharField(max_length=20,null=True)
    Arrived=models.CharField(max_length=40,null=True)
    Fee=models.FloatField()
    PaidDate=models.CharField(max_length=20,null=True)
    TC=models.CharField(max_length=20,null=True,default=" ")
    def __str__(self):
        return self.PatientName + " | " + str(self.date)
    
# Orders  
class Order(models.Model):
    Date=models.DateField()
    user=models.CharField(max_length=40,null=True)
    Item=models.CharField(max_length=100,null=True)
    Category=models.CharField(max_length=100)
    OrderBy=models.CharField(max_length=100)
    Supplier=models.CharField(max_length=100)
    Quantity=models.CharField(max_length=50,null=True)
    Fee=models.FloatField(null=True)
    NewDate=models.DateField(null=True)
    Arrived=models.CharField(max_length=20,null=True)
    Returned=models.CharField(max_length=20,null=True)
    Note=models.CharField(max_length=200,null=True)
    Status=models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.Item + " | " + str(self.Date)
  


# class Post(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     Title=models.CharField(max_length=150)
#     slug = models.SlugField(unique=True,null=True,blank=True)
#     Meta_Tags = models.CharField(max_length=200,)
#     Description=models.TextField()
#     Category=models.CharField(max_length=50)
#     Body=RichTextUploadingField()
#     Date=models.DateField(auto_now_add=True)   
#     Views=models.IntegerField(default=0,null=True)
#     Likes=models.IntegerField(default=0,null=True)
#     Dis_Likes=models.IntegerField(default=0,null=True)
#     CommentsCounts=models.IntegerField(default=0,null=True)
#     def __str__(self):
#         return self.Title + " | " + str(self.Date)

# def createslug(instance,new_slug=None):
#     slug=slugify(instance.Title)
#     if new_slug is not None:
#         slug=new_slug
#     qs = Post.objects.filter(slug=slug).order_by("-id")
#     exists=qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug,qs.first().id)
#         return createslug(instance,new_slug=new_slug)
#     return slug
# def pre_save_post_receiver(sender,instance,*args, **kwargs):
#     if not instance.slug:
#         instance.slug=createslug(instance)
# pre_save.connect(pre_save_post_receiver,Post)

# class Comment(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     Post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
#     Body=models.TextField(null=True)
#     Time=models.DateTimeField(auto_now_add=True,null=True)
#     def __str__(self):
#         return str(self.Post) + " | "  + self.Body + " | " + self.user.username + " | " + str(self.Time)        

class RepeatExpense(models.Model):
    Date=models.DateField()
    Title=models.CharField(max_length=50)
    Category=models.CharField(max_length=50)
    Account=models.CharField(max_length=50)
    Amount=models.FloatField()
    Status=models.CharField(max_length=20,null=True)
    Note=models.TextField()
    Repeat=models.CharField(max_length=20,null=True)


    def __str__(self):
        return str(self.Date) + " | " + self.Title + " | " + self.Category

class RepeatIncome(models.Model):
    Date=models.DateField()
    Title=models.CharField(max_length=50)
    Category=models.CharField(max_length=50)
    Account=models.CharField(max_length=50)
    Amount=models.FloatField()
    Status=models.CharField(max_length=20,null=True)
    Note=models.TextField()
    Repeat=models.CharField(max_length=20,null=True)
    RepeatStatus=models.CharField(max_length=20,null=True,default="On")

    def __str__(self):
        return str(self.Date) + " | " + self.Title + " | " + self.Category