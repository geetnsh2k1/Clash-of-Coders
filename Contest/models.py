from django.db import models
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
from Profile.models import Profile
from django.core.validators import FileExtensionValidator

# Create your models here.
def content_file_name(instance, filename):
    return '/'.join(['Submissions', instance.Contest_Name, instance.Profile.User.username,  filename])

class Submission(models.Model):
    Contest_Name = models.CharField(max_length=50, null=False)
    
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Profile')
    
    Output = models.FileField(upload_to=content_file_name, validators=[FileExtensionValidator(allowed_extensions=['zip'])], null=False)
    
    Time = models.DateTimeField(auto_now_add=True, null=True)
    
    Score = models.CharField(max_length=100, default="0")
    
    Previous = models.TextField(default="No previous submission.")

    def __str__(self):
        return self.Profile.User.username + ' - ' + self.Contest_Name + ' - ' + self.Score

def problem_file_path(instance, filename):
    return '/'.join([instance.Name, 'Problem',  filename])

def check_file_path(instance, filename):
    return '/'.join([instance.Name, 'Check_File',  filename])

def dataset_file_path(instance, filename):
    return '/'.join([instance.Name, 'Dataset',  filename])

class Contest(models.Model):
    Name = models.CharField(max_length=50, null=False, validators=[RegexValidator("[A-Za-z]{1}[A-Za-z0-9@#&*! ]{2,49}", "Contest name must only contain alpha-numeric characters, @, #, &, * and ! only and must start with alphabet only and can be only upto 50 words.", "Contest name must only contain alpha-numeric characters, @, #, &, * and ! only and must start with alphabet only and can be only upto 50 words.")])
    
    Released = models.DateTimeField(auto_now_add=True)
    
    Start = models.DateTimeField(null=False)
    
    # as soon as contest is created, duration is stored in this variable
    Duration = models.CharField(max_length=20, blank=False)
    
    End = models.DateTimeField(null=False)
    
    Contenders = models.ManyToManyField(Profile, related_name='Contenders', null=True, blank=True)
    
    Problem = models.FileField(upload_to=problem_file_path, null=False)
    
    Check = models.FileField(upload_to=check_file_path, null=False)
    
    Dataset = models.FileField(upload_to=dataset_file_path, validators=[FileExtensionValidator(allowed_extensions=['zip'])], null=False)
    
    Status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Name+" - "+str(self.End)

    def Time_Span(self):
        return self.End-self.Start