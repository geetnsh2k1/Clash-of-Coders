from django.shortcuts import render, redirect
from Contest.models import Contest, Submission
from Profile.models import Profile
from urlparams.redirect import param_redirect
from django.contrib import messages
from django.utils import timezone
import subprocess, sys
from zipfile import ZipFile

# Create your views here.
def submission(request, Name):
    try:
        contest = Contest.objects.get(Name=Name)
        if timezone.now() > contest.End:
            messages.error(request, "The contest {Name} is over now.".format(Name=Name))
            return redirect('home')
        
        if request.user.is_authenticated:
            if request.method == "POST":
                
                profile = Profile.objects.get(User=request.user)
                
                output = request.FILES['output']
                
                Output = output.open()
                Output = ZipFile(Output, 'r')
                
                Input = contest.Dataset.open()
                Input = ZipFile(Input, 'r')
                
                start = ""
                for file in Input.infolist():
                    temp = file.filename.split('/')
                    temp = temp[0:len(temp)-1]
                    start = '/'.join(temp)
                    start += '/'
                
                data = []
                
                for file in Output.infolist():
                    ip = None
                    try:
                        ip = Input.open(start+file.filename.split('/')[-1], 'r')
                    except :
                        res = file.filename+" name must be same to the name of assigned dataset."
                        messages.error(request, res)
                        break
                    op = Output.open(file.filename, 'r')
                    
                    temp = {}
                    temp['filename'] = file.filename
                    temp['input'] = ip.read().decode('utf-8')
                    temp['output'] = op.read().decode('utf-8')
                    data.append(temp)
                    
                result = subprocess.run(
                [sys.executable, "-c", contest.Check.read().decode('utf-8')], capture_output=True, text=True, 
                input=str(data))
                result = eval(result.stdout)
                
                try:
                    old = Submission.objects.get(Profile=profile, Contest_Name=contest.Name)
                    old.Previous = result['out']
                    old.Output = output
                    if result['total'] > eval(old.Score): old.Score=result['total']
                    old.save() 
                except Exception as e:
                    print(e)
                    new_submission = Submission.objects.create(Contest_Name=Name, Profile=profile, Output=output, Previous=result['out'], Score=result['total'])
                    new_submission.save()
                return param_redirect(request, 'contest', Name)
            else:
                pass
        else : return redirect('home')
    except :
        messages.error(request, 'an unexpected error occured, try to submit it again.')
        return param_redirect(request, 'contest', Name)