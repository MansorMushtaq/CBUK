from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'covid_19'  # Optional but helpful for namespacing

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('cases/', views.cases, name='cases'),
    # path('news/', views.news, name='news'),
    # Add more paths as needed for your COVID-19 app
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('newrecord/', views.new_record, name='newrecord'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('get_death_data/', views.get_death_data, name='get_death_data'),
     path('logout/', views.user_logout, name='logout'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])