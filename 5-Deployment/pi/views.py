import json
from .models import profilreco, jobseekerfinal, profilfinal, user_userwise, job_userwise, jobofferfinal,userrecommandation, cv,pfeseekers
from .models import pfejobsuser_userwise, pfecombjobs, pfejob_userwise, pfeprofil, pfejobs_userwise, pferecommend, coursfinal
import pandas as pd
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.forms.models import model_to_dict
from django.http  import JsonResponse, HttpResponse

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def find_user_profile(user_text, profilfinal_data):
    # Create CountVectorizer object to convert text to vectors
    vectorizer = CountVectorizer()

    # Fit the vectorizer to the user text
    vectorizer.fit_transform([user_text])

    # Get the vector for the user text
    user_vector = vectorizer.transform([user_text]).toarray()[0]

    # Compute the cosine similarity between the user vector and each profile vector
    similarity_scores = []
    for index, row in enumerate(profilfinal_data):
        profile_text = row['Title']
        profile_vector = vectorizer.transform([profile_text]).toarray()[0]
        similarity_scores.append(cosine_similarity([user_vector, profile_vector])[0, 1])

    # Find the profile with the highest similarity score
    best_match_index = similarity_scores.index(max(similarity_scores))
    field_string = profilfinal_data[best_match_index]['Field']
    field_string = field_string.replace("'", "")

    return field_string


UserRecommandation = [model_to_dict(obj, fields=["Applicant_ID", "jobID", "CleanTitle", "Score"]) for obj in userrecommandation.objects.all()]

def jobs_UserRecommendation(usrid_list):
    jobs_userwise = [job for job in UserRecommandation if job['Applicant_ID'] in usrid_list]
    joblist = [job['jobID'] for job in jobs_userwise]
    return joblist

ProfileRecommendation = [model_to_dict(obj, fields=["Profil", "jobID", "CleanTitle", "Score"]) for obj in profilreco.objects.all()]

def jobs_Profilecommendation(profil):
    jobs_userwise = [job['jobID'] for job in ProfileRecommendation if job['Profil'] == profil]
    return jobs_userwise


@api_view(['GET'])
def job_recommend(request):
    comb_jobs_df = [model_to_dict(obj, fields=["jobID","companyName","jobTitle","jobLocation","postedAt","jobDescription","workplaceType","jobType","Skills_Description","summaryDescription","CleanTitle","cluster","City","State","Country","title","cluster1","Text"]) for obj in jobofferfinal.objects.all()]
    user = [model_to_dict(obj, fields=["ApplicantId", "headline", "fullName", "allSkills", "Text"]) for obj in jobseekerfinal.objects.all()]
    #Text list user
    text_list_user = [d["Text"] for d in user]

    last_row_applicant = cv.objects.last()
    #last_applicant = model_to_dict(last_row_applicant, fields=["id"])


    #obj = jobseekerfinal.objects.get(ApplicantId=last_applicant['id'])
    obj = last_row_applicant


    #JobSeekerTest
    model_data = model_to_dict(obj, fields=["headline", "allSkills", "filename"])
    uploaded_cv = model_data["filename"]
    profilfinal_data = [model_to_dict(obj, fields=["Field", "Technologies", "Company", "Location", "Title", "Text"]) for obj in profilfinal.objects.all()]
    #HeadLine Applicant=785 ==> BI
    Text=model_data['headline']
    #User Profile
    Profile=find_user_profile(str(Text), profilfinal_data)
    print(Profile)
    #Job Recommendation System
    #collaborative filtering recommender system
    #Users Applicant vector

    tfidf_vectorizer = TfidfVectorizer()

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')

    applicant_vector = tf.fit_transform(text_list_user)
    #New User Score
    #model_data['headline]
    jobS_record_vector = tf.transform([model_data['headline']])
    candidate_cos_similarity = map(lambda x: cosine_similarity(jobS_record_vector, x),applicant_vector)
    candidate_score = list(candidate_cos_similarity)

    top_candidates = sorted(range(len(candidate_score)), key=lambda i: candidate_score[i], reverse=True)[:5]
    print(top_candidates)
    user_userwise.objects.all().delete()

    for i in top_candidates:
        df1 = user_userwise(ApplicantID=user[i]["ApplicantId"], headline=user[i]["headline"], allSkills=user[i]["allSkills"])
        df1.save()
    similar_applicant = [model_to_dict(obj, fields=["ApplicantID", "headline", "allSkills"]) for obj in user_userwise.objects.all()]

    ApplicantList = [d["ApplicantID"] for d in similar_applicant]
    print(ApplicantList)

    #Content-based filtering
    text_list_job = [d["Text"] for d in comb_jobs_df]
    count_vect = CountVectorizer()
    count_comb = count_vect.fit_transform(text_list_job) #fitting and transforming the vector
    user_tfidf_gbade = count_vect.transform([model_data['headline']])
    cos_sim_tfidf_gbade = map(lambda x: cosine_similarity(user_tfidf_gbade, x), count_comb)


    rec1 = list(cos_sim_tfidf_gbade)
    top10_seghe_tfidf = sorted(range(len(rec1)), key = lambda i: rec1[i][0][0], reverse = True)[:10]

    job_userwise.objects.all().delete()

    for i in top10_seghe_tfidf:
        dfcontent = job_userwise(jobID=comb_jobs_df[i]["jobID"], CleanTitle=comb_jobs_df[i]["CleanTitle"], Skills_Description=comb_jobs_df[i]["Skills_Description"], jobLocation=comb_jobs_df[i]["Country"], jobType=comb_jobs_df[i]["jobType"], workplaceType=comb_jobs_df[i]["workplaceType"])
        dfcontent.save()
    df_temp_jobs = [model_to_dict(obj, fields=["jobID", "CleanTitle", "Skills_Description", "jobLocation","jobType"]) for obj in job_userwise.objects.all()]

    ContenttList = [d["jobID"] for d in df_temp_jobs]

    ListUser=jobs_UserRecommendation(ApplicantList)
    ListProfil=jobs_Profilecommendation(Profile)

    result_list = list(set(ContenttList + ListUser +  ListProfil))

    df = pd.DataFrame(comb_jobs_df)

    Job_list = df['jobID'].isin(result_list) 
    df_temp = df[Job_list][["jobID","companyName","jobTitle","jobLocation","postedAt","jobDescription","workplaceType","jobType","Skills_Description","summaryDescription","CleanTitle","City","State","Country"]]
    #df_temp = df[Job_list][['jobID','CleanTitle','Skills_Description','Country',"jobType", "workplaceType"]]
    DfHybrid = df_temp.drop_duplicates()
    json_str = DfHybrid.to_json(orient='records')
    json_str = json_str.replace('\\', '')
    data = json.loads(json_str)

    courses, FinalList = course_recommendation(last_row_applicant, Profile)

   

    data = {"data": data, "courses": courses, "filename": uploaded_cv, "skillss": FinalList}

    return JsonResponse(data, safe=False)




#Courses#
def course_recommendation(last_row_applicant, Profile):
    df1 = [model_to_dict(obj, fields=["ApplicantID", "headline", "allSkills"]) for obj in user_userwise.objects.all()]
    course = [model_to_dict(obj, fields=["course_title", "level", "url", "Skills"]) for obj in coursfinal.objects.all()]
   
    Job_Seeker = model_to_dict(last_row_applicant, fields=["headline", "allSkills"])


    
    #df1 = user_userwise model
    #Job_Seeker_Test = SKILLS1
    SKILLS1 = ", ".join(skill.lower() for skill in Job_Seeker['allSkills'].split())
    df = pd.DataFrame(df1)
    grouped = df.groupby('ApplicantID')['allSkills'].agg(lambda x: ','.join([f.lower() for f in x])).reset_index()
    ColaborativeSkill = ','.join(set(grouped['allSkills'].str.lower().str.split(',').explode().values))
    elements = ColaborativeSkill.split(',')
     # extract elements from the list that are not in string2
    result = [elem for elem in elements if elem not in SKILLS1]

    
    """ get the missing skills of the new jobseeker in comparison to his profil"""
    #Profil = profilfinal_data
    profilfinal_data = [model_to_dict(obj, fields=["Field", "Technologies", "Company", "Location", "Title", "Text"]) for obj in profilfinal.objects.all()]
    Profil = pd.DataFrame(profilfinal_data)
    ProfilSkills = Profil[Profil['Field']==Profile]['Technologies'].apply(lambda x: x.lower()).values
    ProfilSkills = ', '.join(str(skill) for skill in ProfilSkills)

    my_list = ProfilSkills


    # split string1 into a list of elements
    elementsProfil = ProfilSkills.split(',')
    # extract elements from the list that are not in string2
    result2 = [elem for elem in elementsProfil if elem not in SKILLS1]

    FinalList=result2+result
        
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)
    vectorizer.fit_transform(FinalList)
    feature_names = vectorizer.get_feature_names_out()
    SkillsFinal=get_keywords(vectorizer, feature_names,FinalList)
    #To do --> Try to displlay skills final
    tfidf_vect = TfidfVectorizer()
    # Fitting and transforming the vector
    CoursData_title = [d["course_title"] for d in course]
    tfidf_comb = tfidf_vect.fit_transform(CoursData_title) 
    CoursData = pd.DataFrame(course)
    recommended_courses = recommend_courses(CoursData,SkillsFinal)

    recommended_courses = pd.DataFrame(recommended_courses)

    escaped_list = [re.escape(term) for term in my_list]
    search_terms = '|'.join(escaped_list)

    recommended = recommended_courses[~((recommended_courses['level'].str.lower().isin(['beginner', 'Beginner Level'])) & (recommended_courses['course_title'].str.contains(search_terms)))]
    
    

    #Here
    records = recommended.to_dict(orient='records')
    recommended = json.dumps(records)
    recommended = recommended.replace('\\', '')
    recommended = json.loads(recommended)

    return recommended, FinalList



def recommend_courses(df, skills):
    # Preprocess the course names to create a corpus of documents
    corpus = df['course_title'].apply(lambda x: ' '.join(x.lower().split()))

    # Convert the corpus into a matrix of TF-IDF features
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # Initialize an empty list to store recommended courses for each skill
    recommended_courses = []

    # Loop over the skills and calculate the cosine similarity with course names
    for skill in skills:
        skill_tfidf = tfidf_vectorizer.transform([' '.join(skill.lower().split())])
        cosine_similarities = cosine_similarity(skill_tfidf, tfidf_matrix).flatten()

        # Sort the courses based on their cosine similarity scores in descending order
        course_indices = cosine_similarities.argsort()[::-1]

        # Append the top 3 courses as recommendations for the current skill
        top_courses = df[['course_title', 'url','level']].iloc[course_indices[:3]]
        recommended_courses.append(top_courses)

    # Concatenate the recommended courses into a single dataframe
    recommended_courses_df = pd.concat(recommended_courses, ignore_index=True)
    recommended_courses_df = recommended_courses_df.drop_duplicates()
    return recommended_courses_df


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature, score
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results
def sort_coo(coo_matrix):
    """Sort a dict with highest score"""
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
def get_keywords(vectorizer, feature_names, doc):
    """Return top k keywords from a doc using TF-IDF method"""

    #generate tf-idf for the given document
    tf_idf_vector = vectorizer.transform(doc)
    
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())

    #extract only TOP_K_KEYWORDS
    TOP_K_KEYWORDS = 20 # top k number of keywords to retrieve in a ranked document
    keywords=extract_topn_from_vector(feature_names,sorted_items,TOP_K_KEYWORDS)
    
    return list(keywords.keys())

    





##End Course#

###########PFE#####

def find_user_profile_pfe(user_text, profile_data):
    # Create CountVectorizer object to convert text to vectors
    vectorizer = CountVectorizer()

    # Fit the vectorizer to the user text
    vectorizer.fit_transform([user_text])

    # Get the vector for the user text
    user_vector = vectorizer.transform([user_text]).toarray()[0]

    # Compute the cosine similarity between the user vector and each profile vector
    similarity_scores = []
    for index, row in enumerate(profile_data):
        profile_text = row['Field']
        profile_vector = vectorizer.transform([profile_text]).toarray()[0]
        similarity_scores.append(cosine_similarity([user_vector, profile_vector])[0, 1])

    # Find the profile with the highest similarity score
    best_match_index = similarity_scores.index(max(similarity_scores))
    field_string = profile_data[best_match_index]['Field']
    field_string = field_string.replace("'", "")
    

    return  field_string


PFEUserRecommandation = [model_to_dict(obj, fields=["Applicant_ID", "jobID", "Topic", "Score"]) for obj in pferecommend.objects.all()]

def pfe_UserRecommendation(usrid_list):
    jobs_userwise = [job for job in UserRecommandation if job['Applicant_ID'] in usrid_list]
    joblist = [job['jobID'] for job in jobs_userwise]
    return joblist

PFEProfileRecommendation = [model_to_dict(obj, fields=["Profil", "jobID", "Topic", "Score"]) for obj in pfejobs_userwise.objects.all()]

def pfe_Profilecommendation(profil):
    jobs_userwise = [job['jobID'] for job in ProfileRecommendation if job['Profil'] == profil]
    return jobs_userwise

@api_view(['GET'])
def pfe_recommend(request):


    last_row_applicant = cv.objects.last()
    #last_applicant = model_to_dict(last_row_applicant, fields=["id"])


    #obj = jobseekerfinal.objects.get(ApplicantId=last_applicant['id'])
    obj = last_row_applicant

    #obj = pfeseekers.objects.get(ApplicantID=last_row_applicant)
    #pfeSeekerTest
    model_data = model_to_dict(obj, fields=["headline", "allSkills", "filename"])
    Profil = [model_to_dict(obj, fields=["jobID", "Topic", "Technologies", "Field"]) for obj in pfeprofil.objects.all()]
    Text=model_data['headline']

    user = [model_to_dict(obj, fields=["ApplicantID", "headline", "fullName", "allSkills", "Text"]) for obj in pfeseekers.objects.all()]
    #Text list user
    text_list_user = [d["Text"] for d in user]

    ProfilRedict=find_user_profile_pfe(str(Text), Profil)
    tfidf_vectorizer = TfidfVectorizer()
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    applicant_vector = tf.fit_transform(text_list_user) 

    #New User Score
    #model_data['headline]
    jobS_record_vector = tf.transform([model_data['headline']])
    candidate_cos_similarity = map(lambda x: cosine_similarity(jobS_record_vector, x),applicant_vector)
    candidate_score = list(candidate_cos_similarity)

    top_candidates = sorted(range(len(candidate_score)), key=lambda i: candidate_score[i], reverse=True)[:5]

    pfejobsuser_userwise.objects.all().delete()

    for i in top_candidates:
        df1 = pfejobsuser_userwise(ApplicantID=user[i]["ApplicantID"], headline=user[i]["headline"], allSkills=user[i]["allSkills"])
        df1.save()
    similar_applicant = [model_to_dict(obj, fields=["ApplicantID", "headline", "allSkills"]) for obj in pfejobsuser_userwise.objects.all()]

    ApplicantList = [d["ApplicantID"] for d in similar_applicant]
    print(ApplicantList)


    
#Content recommendation
    comb_jobs_all = [model_to_dict(obj, fields=["jobID", "Description" ,"Duration","Technologies" ,"Topic","Trainees" ,"Location" ,"Field" ,"Company" ,"Cluster" , "Text" ]) for obj in pfecombjobs.objects.all()]
    text_list_jobs = [d["Text"] for d in comb_jobs_all]
    tfidf_vect = TfidfVectorizer()
    tfidf_comb = tfidf_vect.fit_transform(text_list_jobs) 
    user_tfidf_gbade = tfidf_vect.transform([model_data['allSkills']])
    cos_sim_tfidf_gbade = map(lambda x: cosine_similarity(user_tfidf_gbade, x), tfidf_comb)
    pfeList = list(cos_sim_tfidf_gbade)
    top10_seghe_tfidf = sorted(range(len(pfeList)), key = lambda i: pfeList[i], reverse = True)[:10]
    list_scores_seghe_tfidf = [pfeList[i][0][0] for i in top10_seghe_tfidf]

    pfejob_userwise.objects.all().delete()

    for i in top10_seghe_tfidf:
        dfcontent = pfejob_userwise(jobID=comb_jobs_all[i]["jobID"], Technologies=comb_jobs_all[i]["Technologies"], Field=comb_jobs_all[i]["Field"], Topic=comb_jobs_all[i]["Topic"])
        dfcontent.save()
    df_temp_jobs = [model_to_dict(obj, fields=["jobID", "Technologies", "Field", "Topic"]) for obj in pfejob_userwise.objects.all()]

    ContenttList = [d["jobID"] for d in df_temp_jobs]

    #Hybrid recommendation
    ListUser=jobs_UserRecommendation(ApplicantList)
    ListProfil=jobs_Profilecommendation(ProfilRedict)
    result_list = list(set(ListProfil + ListUser + ContenttList))

    df = pd.DataFrame(comb_jobs_all)
    Job_list = df['jobID'].isin(result_list) 
    df_temp = df[Job_list][["jobID","Description","Duration","Technologies","Topic","Trainees","Location","Field","Company"]]
    #df_temp = df[Job_list][['jobID','Topic','Field','Technologies']]
    DfHybrid = df_temp.drop_duplicates()
    json_str = DfHybrid.to_json(orient='records')
    json_str = json_str.replace('\\', '')
    data = json.loads(json_str)

    courses, FinalList = course_recommendation(last_row_applicant, ProfilRedict)
    uploaded_cv = model_data["filename"]
   

    data = {"data": data, "courses": courses,"filename": uploaded_cv, "skillss": FinalList}

    return JsonResponse(data, safe=False)   

#Ajouter selectbox, pour executer l'une des methode lorsque job seeker ou intern seeker