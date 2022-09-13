from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordChangeDoneView
from articles import views


app_name = "articles"

urlpatterns = [
    path('articles/', views.articles, name='articles'),
    path('articles/<slug:slug>/', views.article_details, name='article_details'),
    path('article/create/', views.add_article, name='add_article'),
    path('article/update/<slug:slug>/', views.update_article, name='update_article'),
    path('article/delete/<slug:slug>/', views.delete_article, name='delete_article'),
    # path('auth/login/', views.user_login, name='login'),
    path('auth/login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('auth/create/', views.create_user, name='register'),
    path('auth/password_change/', \
        PasswordChangeView.as_view(template_name='auth/update_password.html'), name='change_password'),
    path('auth/password_change/done/', \
        PasswordChangeDoneView.as_view(template_name='auth/update_password_done.html'), name='password_change_done'),
]