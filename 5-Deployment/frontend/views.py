from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from resume_parser import resumeparse
from pi.models import cv
from django.http  import JsonResponse

# Create your views here.
def jobrecommendation(request):
    return render(request, 'frontend/jobrecommendation.html')

def pferecommendation(request):
    return render(request, 'frontend/pferecommendation.html')

def index(request):
    return render(request, template_name="frontend/index.html")

def upload_file(request):
    file = request.FILES.get("file")

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    print("*************************************")
    media_root = settings.MEDIA_ROOT
    media_path = os.path.join(media_root,filename)
    print("*************************************")
    data = resumeparse.read_file(media_path)
    headline=data['designition']
    skills=data['skills']
    skills_str = ','.join(skills)
    headline_str = ','.join(headline)
    print(headline)
    print(skills)
    print("*************************************")
    if any(term in headline for term in ["student", "intern"]):
        User= "intern"        
    else:
        User= "jobSeeker"

    new_user = cv(user_type=User, allSkills=skills_str, headline=headline_str, filename=filename)
    new_user.save() 
    data = {'user_type': User}
    print(User)
    return JsonResponse(data,  safe=False)

    
   
