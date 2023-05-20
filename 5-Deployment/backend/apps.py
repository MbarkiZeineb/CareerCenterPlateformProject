from django.contrib.admin.apps import AdminConfig
from django.apps import AppConfig

class  BackendConfig(AdminConfig):
    default_site = 'backend.admin.BackendAdminArea'
    
class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
