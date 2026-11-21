"""
URL configuration for NoteBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from views import page_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pwa.urls')),
    path('', page_views.index, name='index'),
    
    path('notes/',page_views.notes,name='notes'),
    path('note_create/',page_views.note_create,name='note_create'),
    path('note_details/<int:noteid>/',page_views.notes_details,name='notes_details'),
    path('note_update/<int:noteid>/',page_views.note_update,name='notes_update'),
    path('note_delete/<int:noteid>/',page_views.note_delete,name='notes_delete'),

    path('register/',page_views.register,name='register'),
    path('otp/',page_views.otp_verification,name='otp'),
    path('login/',page_views.user_login,name='login'),
    path('logout/',page_views.user_logout,name='logout'),

    re_path(r"^.*/$", page_views.page_not_found),

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
