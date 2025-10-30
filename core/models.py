from django.db import models
from django.contrib.auth.models import User

class Veiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
        ('SUV', 'SUV'),
        ('Luxo', 'Luxo'),
    ])
    transmissao = models.CharField(max_length=20, choices=[
        ('Automático', 'Automático'),
        ('Manual', 'Manual'),
    ])
    tipo_veiculo = models.CharField(max_length=20, choices=[
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
    ])
    capacidade_pessoas = models.IntegerField()
    imagem = models.ImageField(upload_to='veiculos/')
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    data_ultima_revisao = models.DateField()
    data_proxima_revisao = models.DateField()
    data_ultima_inspecao = models.DateField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()

class Reserva(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Correct!
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True)
    data_reserva = models.DateTimeField(auto_now_add=True)
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva de {self.veiculo} por {self.cliente}"

class FormaPagamento(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)  # Armazena a data/hora do envio

    def __str__(self):
        return f"{self.nome} - {self.email}"
