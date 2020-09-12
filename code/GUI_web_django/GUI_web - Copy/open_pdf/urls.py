from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from open_pdf import views

app_name = 'open_pdf'

urlpatterns = [
    path('view_pdf/',views.view_pdf,name='view_pdf'),
    path('annotate_pdf/',views.annotate_pdf,name='annotate_pdf'),
]