from django.contrib import admin
from django.urls import path, include
from hostel import settings
from . import views
from .views import allocate_hostel
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup , name="signup"),
    path('signin', views.signin , name="signin"),
    path('signout', views.signout , name="signout"),
    path('create-profile', views.create_profile, name="create_profile"),
    path('allocate-hostel/', allocate_hostel, name='allocate_hostel'),
    path('complaint/create/', views.create_complaint, name='create_complaint'),
    path('activity-log', views.user_activity_log, name='activity_log'),
    path('download/activity-log/', views.download_activity_log, name='download_activity_log'),
    path('community/', views.community, name='community'),
    path('hostelcommunity/', views.hostel_community, name='hostel_community'),
    path('post_message/', views.post_message, name='post_message'),
    path('userprofile/<int:user_id>/', views.userprofile, name='userprofile'),
    path('edit_student/', views.edit_student, name='edit_student'),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)