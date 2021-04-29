from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from urlparams.redirect import param_redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Profile.models import Profile
from Contest.models import Contest, Submission
import json

# Create your views here.
def send_mail(reciever, name):
    MY_ADDRESS = "codecombatjuit@gmail.com"
    PASSWORD = "clashofcoders"

    print(reciever, name)

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()

    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = '''Thank you for your participation.

Dear {name},

We the organizing team want to take a moment of your to thank you for the active participation of yours in our event Code Combat.


Your participation ensured the success of our event.

We hope you enjoyed and we look forward to seeing you at the next events as well.

Thank you for being at the event.


Team CODECOMBAT
while(!(succeed=try()));'''.format(name=name)

    msg['From']=MY_ADDRESS
    msg['To']=reciever
    msg['Subject'] = "Thank you for registering"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    del msg

def sign_in(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
            else:
                res = '@'+username+" doesn't exists."
                messages.error(request, res)
            
            return redirect('home')
        return redirect('home')
    except :
        messages.error(request, 'an unexpected error occured, try again.')
        return redirect('home')

def sign_up(request):
    try:
        if request.method == "POST":
            first_name = request.POST['f_name'].upper()
            last_name = request.POST['l_name'].upper()
            Age = request.POST['age']
            Phone = request.POST['phone']
            username = request.POST['username']
            Email = request.POST['email']
            College = request.POST['college']
            Profession = request.POST['profession']
            Level = request.POST['level']
            password = request.POST['password']
            
            user = authenticate(username=username, email=Email, password=password)
            
            if not user:
                new_user = User.objects.create_user(username=username, email=Email, password=password, first_name=first_name, last_name=last_name)
                new_user.save()
                
                new_profile = Profile.objects.create(User=new_user, Age=Age, Phone=Phone, College=College, Profession=Profession, Level=Level)
                new_profile.save()
                
                send_mail(new_profile.User.email, new_profile.User.first_name+" "+new_profile.User.last_name)
                
                login(request, new_user)
                messages.success(request, "You are now successfully registerd with us.")            

            else:
                res="user already exists."
                messages.error(request, res) 
            
        return redirect('home')
    except :
        messages.error(request, 'an unexpected error occured, try again.')
        return redirect('home')

def sign_out(request):
    logout(request)
    return redirect('home')

def profile_page(request, username):
    try:
        if request.user.username == username:    
            user = User.objects.get(username=username)
            profile = Profile.objects.get(User=user)
            
            data = {}
            data['profile'] = profile 
            if request.user.is_superuser:
                profiles = Profile.objects.all()
                contests = Contest.objects.all()
                submissions = Submission.objects.all()
                
                d = {}
                res = "Contest\n"
                for contest in contests:
                    res += contest.Name+" "
                    res += str(contest.Start)+" "
                    res += str(contest.Status)+"\n"
                    
                res += "\nSubmissions\n"
                for submission in submissions:
                    res += str(submission)+"\n"
                
                res += "\nProfiles\n"
                for profile in profiles:
                    res += str(profile)+"\n"
                
                data['superuser'] = json.dumps(res)
                 
            return render(request, 'profile.html', data)
        return redirect('home')
    except Exception as e:
        print(e)
        messages.error(request, 'an unexpected error occured, try again.')
        return redirect('home')

def update_profile(request, username):
    try:
        if request.method == "POST":
            profile_picture = request.FILES['image']
            if request.user.username == username:    
                user = User.objects.get(username=username)
                profile = Profile.objects.get(User=user)
                profile.Image = profile_picture
                profile.save()
                return param_redirect(request, 'profile', username)
        return redirect('home')
    except :
        messages.error(request, 'an unexpected error occured, try again.')
        return redirect('home')

def upd_profile(request, username):
    try:
        if request.method == "POST":
            if request.user.username == username:
                user = User.objects.get(username=username)
                Nickname = request.POST['nickname'][2:]
                Phone = request.POST['phone'][4:]
                GitHub = request.POST['github']
                LinkedIn = request.POST['linkedin']
                
                if '@ ' not in request.POST['nickname'] or '+91 ' not in request.POST['phone']:
                    messages.error(request, "don't remove @_ from nickname and +91_ from phone number")
                    return param_redirect(request, 'profile', username) 
                
                elif len(Nickname) < 4:
                    messages.error(request, "nickname must be of atleast 4 characters.")
                    return param_redirect(request, 'profile', username)  
                
                elif len(Phone) != 10:
                    messages.error(request, "a valid phone number is of 10 digits.")
                    return param_redirect(request, 'profile', username)  
                
                profile = Profile.objects.get(User=user)
                profile.Nickname = Nickname
                profile.Phone = Phone
                profile.GitHub = GitHub
                profile.LinkedIn = LinkedIn
                profile.save()
                return param_redirect(request, 'profile', username)
        return redirect('home')
    except : return redirect('home')
