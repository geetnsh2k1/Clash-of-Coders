from django.shortcuts import render, redirect
from Contest.models import Contest, Submission
from Profile.models import Profile
from django.utils import timezone
from datetime import timedelta
# Create your views here.

def contest(request, Name):
    try:
        data = {}
        contest = Contest.objects.get(Name=Name)
        data['contest'] = contest
        if request.user.is_authenticated:
            profile = Profile.objects.get(User=request.user)
            data['profile'] = profile
            
            if profile not in contest.Contenders.all():
                contest.Contenders.add(profile)
                contest.save()
        
            submissions = Submission.objects.filter(Contest_Name=contest.Name)
            data['submissions'] = sorted(submissions, key=lambda x : (x.Score, contest.End-x.Time, x.Profile.User.username), reverse=True)
            
            months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
            
            E = contest.End+timedelta(hours=5)
            E = E+timedelta(minutes=30)
            end = months[E.month]+" "
            end += str(int(E.day))+", "
            end += str(E.year)+" "
            end += E.strftime("%H:%M:%S")
            
            data['end'] = end
        else : return redirect('home')
        return render(request, 'contest.html', data)
    except :
        return redirect('home')