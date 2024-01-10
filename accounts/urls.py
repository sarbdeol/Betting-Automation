from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_account/', views.add_account, name='add_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('execute/', views.execute, name='execute'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('get_account_choices/', views.get_account_choices, name='get_account_choices'),
    path('json-data/', views.json_data, name='json_data'),
    path('betway-json-data/', views.json_data, name='json_data'),
    path('submit/', views.submit_data, name='submit_data'),
]


