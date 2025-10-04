from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    
    # Portfolio URLs
    path('portfolio/<int:id>/', views.portfolio_detail, name='portfolio-detail'),
    path('portfolio/<int:id>/update/', views.portfolio_update, name='portfolio-update'),
    
    # Project URLs
    path('portfolio/<int:portfolio_id>/projects/', views.project_list, name='project-list'),
    path('portfolio/<int:portfolio_id>/project/create/', views.project_create, name='project-create'),
    path('project/<int:id>/', views.project_detail, name='project-detail'),
    path('project/<int:id>/update/', views.project_update, name='project-update'),
    path('project/<int:id>/delete/', views.project_delete, name='project-delete'),
    
    # Student URLs
    path('students/', views.student_list, name='student-list'),
    path('student/<int:id>/', views.student_detail, name='student-detail'),
    
    # Admin
    path('admin/', admin.site.urls),
]
    