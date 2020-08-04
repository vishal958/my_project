from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name='login'),
    #url('^', include('django.contrib.auth.urls')),
]