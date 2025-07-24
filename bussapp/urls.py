from django.urls import path
from . import views 

urlpatterns = [
    path('home',views.home,name='home'),
    path('add_vehicle',views.add_vehicle,name='add_vehicle'),
    path('enter_data',views.enter_data,name='enter_data'),
    path('view_records',views.view_records,name='view_records'),
    path('vehicle_list',views.vehicle_list,name='vehicle_list'),
    path('update_vehicle',views.update_vehicle,name='update_vehicle'),
    path('delete_vehicle',views.delete_vehicle,name='delete_vehicle'),
    path('update_record',views.update_record,name='update_record'),
    path('delete_record',views.delete_record,name='delete_record'),
    path('multiple_records_delete',views.multiple_records_delete,name='multiple_records_delete'),
    path('multiple_vehicles_delete',views.multiple_vehicles_delete,name='multiple_vehicles_delete'),
    path('',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('search',views.search,name='search'),
    path('vehicle_search',views.vehicle_search,name='vehicle_search'),
    path('records_pdf_download_view',views.records_pdf_download_view,name='records_pdf_download_view'),
    path('records_generate_pdf', views.records_generate_pdf, name='records_generate_pdf'),
    path('records_generate_excel', views.records_generate_excel, name='records_generate_excel'),
    path('vehicles_pdf_download_view',views.vehicles_pdf_download_view,name='vehicles_pdf_download_view'),
    path('vehicles_generate_pdf', views.vehicles_generate_pdf, name='vehicles_generate_pdf'),
    path('vehicles_generate_excel', views.vehicles_generate_excel, name='vehicles_generate_excel'),
]