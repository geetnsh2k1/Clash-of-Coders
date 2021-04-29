from django.db import models
from django.contrib.auth.models import User as Usr
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField

# Create your models here.
def profile_file_path(instance, filename):
    return '/'.join(['Profile', instance.User.username, 'Profile_Picture',  filename])

class Profile(models.Model):
    
    Created = models.DateTimeField(auto_now_add=True)
    
    User = models.OneToOneField(Usr, unique=True, on_delete=models.CASCADE, null=False)
    
    Age = models.IntegerField(validators=[RegexValidator("([1]{1}[6-9]{1}|[2-5]{1}[0-9]{1}){1}", "Age must be in the range of 16-59.", "Age must be in the range of 16-59.")], null=False)
    
    Phone = models.IntegerField(validators=[RegexValidator("[1-9]{1}[0-9]{9}", "Enter the phone number without 0 and country code.", "Enter the phone number without 0 and country code.")], null=False)
    
    Image = models.ImageField(upload_to=profile_file_path, default='Default.png')
    
    Nickname = models.CharField(max_length=50, blank=True, default="Nick name")
    
    Status = (
        ('Student', 'Student'),
        ('Professional', 'Professional'),
        ('Decline to answer', 'Decline to answer')
    )
    
    Profession = models.CharField(max_length=20, choices=Status, null=False)
    
    College = models.CharField(max_length=200, blank=True)
    
    Levels = (
        ('amateur', 'Amateur'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advance', 'Advance'),
        ('expert', 'Expert'),
    )
    
    Level = models.CharField(max_length=20, choices=Levels, null=False)
    
    P_Languages = (
        ('C/C++', 'C/C++'),
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('Object-C', 'Objective-C'),
        ('PHP', 'PHP'),
        ('Swift', 'Swift'),
        ('Ruby', 'Ruby'),
        ('Perl', 'Perl'),
        ('Go', 'Go'),
        ('R', 'R'),
        ('Scala', 'Scala')
    )
    
    Languages = MultiSelectField(choices=P_Languages, blank=True)
    
    LinkedIn = models.URLField(max_length=100, blank=True)
    
    GitHub = models.URLField(max_length=100, blank=True)
    
    Rating = models.FloatField(default=0)
    
    Histoty = models.TextField(default="No History")
    
    def __str__(self):
        return self.User.username