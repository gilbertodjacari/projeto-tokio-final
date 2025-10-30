from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q
from datetime import date
from .models import Veiculo 
from datetime import date, timedelta
from .forms import ContatoForm




def base(request):
    return render(request, 'core/base.html')

def pagina_inicial(request):
    veiculos = Veiculo.objects.all()

    for veiculo in veiculos:
        if veiculo.data_ultima_inspecao < date.today() - timedelta(days=365) or \
           veiculo.data_proxima_revisao < date.today():
            veiculo.disponivel = False
            veiculo.save()

    veiculos_disponiveis = Veiculo.objects.filter(disponivel=True)[:6]

    # FORMULÁRIO DE CONTATO
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona ou mostra mensagem de sucesso
            return redirect('core:sucesso') 
    else:
        form = ContatoForm()

    context = {
        'veiculos': veiculos_disponiveis,
        'form': form
    }
    return render(request, 'core/pagina_inicial.html', context)

    
def registar_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from .models import Cliente
            Cliente.objects.create(user=user)
            login(request, user)
            return redirect('pagina_inicial')
    else:
        form = UserCreationForm()
    return render(request, 'core/registar.html', {'form': form})

def autenticar_cliente(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:pagina_inicial')
    else:
        form = AuthenticationForm()
    return render(request, 'core/autenticar.html', {'form': form})

def sair_cliente(request):
    logout(request)
    return redirect('pagina_inicial')
""" 
def pesquisa_veiculos(request):
    from .models import Veiculo
    veiculos = Veiculo.objects.all()
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
   
    categoria = request.GET.get('categoria')
    transmissao = request.GET.get('transmissao')
    tipo = request.GET.get('tipo')
    valor_min = request.GET.get('valor_min')
    valor_max = request.GET.get('valor_max')
    quantidade_pessoas = request.GET.get('quantidade_pessoas')
   
    
    if marca:
        veiculos = veiculos.filter(marca__icontains=marca)
    if modelo:
        veiculos = veiculos.filter(modelo__icontains=modelo)
        
    if categoria:
    veiculos = veiculos.filter(categoria=categoria)
    if transmissao:
        veiculos = veiculos.filter(transmissao=transmissao)
    if tipo:
        veiculos = veiculos.filter(tipo=tipo)
    if valor_min and valor_max:
        veiculos = veiculos.filter(valor_diaria__range=(valor_min, valor_max))
    if quantidade_pessoas:
        veiculos = veiculos.filter(capacidade_pessoas=quantidade_pessoas)

       
    
    return render(request, 'core/pesquisa.html', {'veiculos': veiculos})
     """

def pesquisa_veiculos(request):
    # Inicializa todos os veículos
    veiculos = Veiculo.objects.all()

    # Obtém os parâmetros de pesquisa da URL
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')

    # Filtra apenas se algum parâmetro for informado
    if marca:
        veiculos = veiculos.filter(marca__icontains=marca)
    if modelo:
        veiculos = veiculos.filter(modelo__icontains=modelo)

    # Passa os resultados para o template
    return render(request, 'core/pesquisa.html', {
        'veiculos': veiculos, 
        'marca': marca, 
        'modelo': modelo
    })

@login_required
def reservar_veiculo(request, veiculo_id):
    from .models import Veiculo, Reserva, Cliente  # Import Cliente
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

    try:
        cliente = request.user.cliente  #Tentar obter o Cliente existente
    except Cliente.DoesNotExist:
       # Se o Cliente não existir, crie um
        cliente = Cliente.objects.create(user=request.user)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente  # Usar o Cliente obtido ou criado
            reserva.veiculo = veiculo
            reserva.valor_total = (reserva.data_fim - reserva.data_inicio).days * veiculo.valor_diaria
            reserva.save()
            veiculo.disponivel = False  # Define o veículo como indisponível
            veiculo.save()  # Salva as alterações no veículo
            return redirect('core:lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'core/reservar.html', {'form': form, 'veiculo': veiculo})

@login_required
def lista_reservas(request):
    from .models import Reserva
    reservas = Reserva.objects.filter(cliente=request.user.cliente)
    return render(request, 'core/lista_reservas.html', {'reservas': reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    from .models import Reserva
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user.cliente)
    reserva.cancelada = True
    reserva.save()
    return redirect('core:lista_reservas')

@login_required
def alterar_reserva(request, reserva_id):
    from .models import Reserva
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user.cliente)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.valor_total = (reserva.data_fim - reserva.data_inicio).days * reserva.veiculo.valor_diaria
            reserva.save()
            return redirect('core:lista_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'core/alterar_reserva.html', {'form': form, 'reserva': reserva})



def sair_cliente(request):
    logout(request)
    return redirect(reverse('core:pagina_inicial'))  



def ver_todas_categorias(request):
    categorias = Veiculo._meta.get_field('categoria').choices  # Acessando as opções de categoria
    return render(request, 'core/ver_todas_categorias.html', {'categorias': categorias})


# Exibe todos os veículos para uma categoria específica
def ver_veiculos_por_categoria(request, categoria):
    veiculos = Veiculo.objects.filter(categoria=categoria)  # Filtra os carros pela categoria
    return render(request, 'core/ver_todos_veiculos.html', {'veiculos': veiculos, 'categoria': categoria})


def todos_veiculos(request):
    veiculos = Veiculo.objects.all()  
    return render(request, 'core/ver_todos_veiculos.html', {'veiculos': veiculos})

def sucesso(request):
    return render(request, 'core/sucesso.html')

