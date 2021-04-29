from django.shortcuts import render, redirect, HttpResponse
from Profile.models import Profile
from Contest.models import Contest
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from urlparams.redirect import param_redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth import logout

# Create your views here.
def send_mail(reciever, name):
    MY_ADDRESS = "codecombatjuit@gmail.com"
    PASSWORD = "clashofcoders"

    print(reciever, name)

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()

    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = '''Dear {name},

We are reaching out to thank you for registering to Round 1 : Tech Bingo(Code Combat) .

We will send you a reminder one day before the event.

Please feel free to share the event as our goal is to gather as many talent as possible.

Thank you again, and have great rest of the day,

Team CODE COMBAT
while(!(succeed=try()));'''.format(name=name)

    msg['From']=MY_ADDRESS
    msg['To']=reciever
    msg['Subject'] = "Thank you for registering"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    del msg


def home(request):
    data = {}
    #update
    contest = Contest.objects.all()
    contest = contest[0]
    
    data['register'] = "login to register"
    if request.user.is_authenticated:
        data['register'] = "register"
        profile = Profile.objects.get(User=request.user)
        data['profile'] = profile
        for contender in contest.Contenders.all():
            if contender.User.username == profile.User.username:
                data['register'] = "registered"
    data['contest'] = contest
    data['registered'] = contest.Contenders.all().count() 
    
    data['remaining']=None
    data['upcoming']=False
    data['ongoing']=False
    
    duration = contest.End-contest.Start
    totsec = duration.total_seconds()
    data['c_h'] = int(totsec//3600)
    data['c_m'] = int((totsec%3600)//60)
    
    now = timezone.now()
    diff = contest.Start-now
    
    months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
    
    S = contest.Start+timedelta(hours=5)
    S = S+timedelta(minutes=30)
    
    E = contest.End+timedelta(hours=5)
    E = E+timedelta(minutes=30)
    
    start = months[S.month]+" "
    start += str(int(S.day))+", "
    start += str(S.year)+" "
    start += S.strftime("%H:%M:%S")
    
    end = months[E.month]+" "
    end += str(int(E.day))+", "
    end += str(E.year)+" "
    end += E.strftime("%H:%M:%S")
    
    data['start']=start
    data['end']=end
    
    data['initial'] = start[13:18]
    
    if now > contest.End:
        contest.Status = False
        contest.save()
    elif diff.days == -1:
        # ongoing contests
        data['remaining'] = contest.End-now
        data['ongoing'] = True
    elif diff.days >= 0 and diff.days <= 15:
        # upcoming contests
        data['remaining'] = diff
        data['upcoming'] = True
    elif diff.days < -1:
        # contest is over 
        contest.Status = False
        contest.save()
    
    return render(request, "del_home.html", data)

def register(request, contest):
    contest = Contest.objects.get(Name=contest)
    if request.user.is_authenticated:
        profile = Profile.objects.get(User=request.user)
        contest.Contenders.add(profile)
        send_mail(profile.User.email, profile.User.first_name+" "+profile.User.last_name)
        contest.save()
        messages.success(request, "You have successfully registered for the contest.")
    else:
        messages.error(request, 'You must need to sign in to register for this contest.')    
    return redirect('home')   

def schedule(request):
    return render(request, "schedule.html")
