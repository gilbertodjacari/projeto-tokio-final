
from django.urls import path
from . import views 
from core import views
from .views import sucesso

app_name = 'core'  # Define the namespace

urlpatterns = [
    path('registar/', views.registar_cliente, name='registar_cliente'),
    path('autenticar/', views.autenticar_cliente, name='autenticar_cliente'),
    path('sair/', views.sair_cliente, name='sair_cliente'),
    path('pesquisa/', views.pesquisa_veiculos, name='pesquisa_veiculos'),
    path('reservar/<int:veiculo_id>/', views.reservar_veiculo, name='reservar_veiculo'),
    path('lista_reservas/', views.lista_reservas, name='lista_reservas'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('alterar_reserva/<int:reserva_id>/', views.alterar_reserva, name='alterar_reserva'),
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('categorias/', views.ver_todas_categorias, name='ver_todas_categorias'),
    path('carros/categoria/<str:categoria>/', views.ver_veiculos_por_categoria, name='ver_carros_por_categoria'),
    path('veiculos/', views.todos_veiculos, name='todos_veiculos'),
    path('sucesso/', views.sucesso, name='sucesso'),

]




  
