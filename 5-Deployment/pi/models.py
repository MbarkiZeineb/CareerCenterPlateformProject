from django.db import models


class profilfinal(models.Model):
    Field = models.TextField(max_length=1000000)
    Technologies = models.TextField(max_length=1000000)
    Company = models.TextField(max_length=1000000)
    Location = models.TextField(max_length=1000000) 
    Title = models.TextField(max_length=1000000) 
    Text = models.TextField(max_length=1000000) 


class profilreco(models.Model):
    Profil = models.TextField(max_length=1000000)
    jobID = models.IntegerField()
    CleanTitle = models.TextField(max_length=1000000)
    Score = models.FloatField(max_length=1000000)

class jobseekerfinal(models.Model):
    ApplicantId	= models.IntegerField()
    headline = models.TextField(max_length=1000000)
    fullName =	models.TextField(max_length=1000000)
    cluster = models.TextField(max_length=1000000)
    allSkills = models.TextField(max_length=1000000)
    Text = models.TextField(max_length=1000000)


class jobofferfinal(models.Model):
    jobID = models.IntegerField()
    companyName = models.TextField(max_length=1000000)
    jobTitle = models.TextField(max_length=1000000)
    jobLocation = models.TextField(max_length=1000000)
    postedAt = models.TextField(max_length=1000000)
    jobDescription = models.TextField(max_length=1000000)
    workplaceType = models.TextField(max_length=1000000)
    jobType = models.TextField(max_length=1000000)
    Skills_Description = models.TextField(max_length=1000000)
    summaryDescription = models.TextField(max_length=1000000)
    CleanTitle = models.TextField(max_length=1000000)
    cluster = models.TextField(max_length=1000000)
    City = models.TextField(max_length=1000000)
    State = models.TextField(max_length=1000000)
    Country = models.TextField(max_length=1000000)
    title = models.TextField(max_length=1000000)
    cluster1 = models.TextField(max_length=1000000)
    Text = models.TextField(max_length=1000000)
   

    
class userrecommandation(models.Model):
    Applicant_ID = models.IntegerField()
    jobID = models.IntegerField()
    CleanTitle = models.TextField(max_length = 1000000)
    Score = models.FloatField(max_length=10000)
    
class coursfinal(models.Model):
    course_title = models.TextField(max_length = 1000000)
    url = models.TextField(max_length = 1000000)
    level = models.TextField(max_length = 1000000)
    Skills = models.TextField(max_length = 1000000)

class user_userwise(models.Model):
    ApplicantID = models.IntegerField()
    headline = models.TextField(max_length = 1000000)
    allSkills = models.TextField(max_length = 1000000)

class job_userwise(models.Model):
    jobID = models.IntegerField()
    CleanTitle = models.TextField(max_length = 1000000)
    Skills_Description = models.TextField(max_length = 1000000)
    jobLocation = models.TextField(max_length = 1000000)    
    jobType = models.TextField(max_length = 1000000)    
    workplaceType = models.TextField(max_length = 1000000)    

class cv(models.Model):
    headline = models.TextField(max_length = 1000000)
    user_type = models.TextField(max_length = 1000000)
    allSkills = models.TextField(max_length = 1000000)
    filename = models.TextField(max_length = 1000000)
###Recommended jobs###

class recommended_jobs(models.Model):
    jobID = models.IntegerField()
    CleanTitle = models.TextField(max_length = 1000000)
    Skills_Description = models.TextField(max_length = 1000000)
    Country = models.TextField(max_length = 1000000)    
    jobType = models.TextField(max_length = 1000000)    
    workplaceType = models.TextField(max_length = 1000000)    
###End Recommended jobs


###########PFE####
class pfeuser(models.Model):
    ApplicantID = models.IntegerField()
    headline = models.TextField(max_length = 1000000)
    fullName = models.TextField(max_length = 1000000)
    allSkills = models.TextField(max_length = 1000000)
    cluster = models.TextField(max_length = 1000000)
    Text = models.TextField(max_length = 1000000)

class pfeprofil(models.Model):
    
    jobID = models.IntegerField()
    Topic = models.TextField(max_length = 1000000)
    Field = models.TextField(max_length = 1000000)
    Technologies = models.TextField(max_length = 1000000)
    Location = models.TextField(max_length = 1000000)
    Duration = models.TextField(max_length = 1000000)
    Company = models.TextField(max_length = 1000000)

class pfecombjobs(models.Model): 
    jobID = models.IntegerField()
    Description = models.TextField(max_length = 1000000)
    Duration = models.TextField(max_length = 1000000)
    Technologies = models.TextField(max_length = 1000000)
    Topic = models.TextField(max_length = 1000000)
    Trainees = models.TextField(max_length = 1000000)
    Location = models.TextField(max_length = 1000000)
    Field = models.TextField(max_length = 1000000)
    Company = models.TextField(max_length = 1000000)
    Cluster = models.TextField(max_length = 1000000)
    Text = models.TextField(max_length = 1000000)
    
class pferecommend(models.Model):
    Applicant_ID = models.IntegerField()
    jobID = models.IntegerField()
    Topic = models.TextField(max_length = 1000000)
    Score = models.FloatField(max_length = 1000000)

class pfejobs_userwise(models.Model):
    Profil = models.TextField(max_length = 1000000)
    jobID = models.IntegerField()
    Topic = models.TextField(max_length = 1000000)
    Score = models.TextField(max_length = 1000000)

class pfejobsuser_userwise(models.Model):
    ApplicantID = models.IntegerField()
    headline = models.TextField(max_length = 1000000)
    allSkills = models.TextField(max_length = 1000000)
    
class pfejob_userwise(models.Model):
    jobID = models.IntegerField()
    Technologies = models.TextField(max_length = 1000000)
    Field = models.TextField(max_length = 1000000)
    Topic = models.TextField(max_length = 1000000) 

class pfeseekers(models.Model):
    ApplicantID = models.IntegerField()
    headline = models.TextField(max_length = 1000000)
    fullName = models.TextField(max_length = 1000000)
    allSkills = models.TextField(max_length = 1000000)
    cluster = models.TextField(max_length = 1000000)
    Text = models.TextField(max_length = 1000000)
    