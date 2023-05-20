from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render


def dashboard(request):
    powerbi_embed_code =  '<iframe title="finalreport" width="100%" height="1140px" src="https://app.powerbi.com/reportEmbed?reportId=8f0e9279-086b-45be-b774-3501cd6a7527&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730" frameborder="0" allowFullScreen="true"></iframe>'
    
    return render(request, 'dashboard.html', {'powerbi_embed_code': powerbi_embed_code})