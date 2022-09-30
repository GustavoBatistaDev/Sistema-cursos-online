from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('aulas/<int:id_curso>', views.aulas, name='aulas'),
    path('ver_aula/<int:id>', views.ver_aula, name='ver_aula'),
    path('comentarios/', views.comentarios, name = 'comentarios'),
    path('processa_avaliacao/', views.processa_avaliacao, name = 'processa_avaliacao')
]