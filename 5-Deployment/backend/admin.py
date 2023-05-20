from django.contrib import admin
from .views import dashboard
from django.urls import path

class BackendAdminArea(admin.AdminSite):
    site_header = "Dashboard"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', dashboard),
        ]
        return my_urls + urls

dashboard_site = BackendAdminArea(name="DashboardAdmin")
