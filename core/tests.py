from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Veiculo, Cliente, Reserva, FormaPagamento, Contato
from django.test import TestCase, Client
from django.urls import reverse, resolve
from core import views

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testeuser', password='senha123')
        self.cliente, _ = Cliente.objects.get_or_create(user=self.user, defaults={
            'telefone': '912345678',
            'endereco': 'Rua Teste'
        })

        self.veiculo = Veiculo.objects.create(
            marca='Toyota',
            modelo='Yaris',
            categoria='Pequeno',
            transmissao='Manual',
            tipo_veiculo='Carro',
            capacidade_pessoas=4,
            imagem='veiculos/teste.jpg',
            valor_diaria=35.50,
            data_ultima_revisao=date.today() - timedelta(days=180),
            data_proxima_revisao=date.today() + timedelta(days=180),
            data_ultima_inspecao=date.today() - timedelta(days=300),
            disponivel=True
        )

        self.forma_pagamento = FormaPagamento.objects.create(tipo='Cartão')

    def test_veiculo_str(self):
        self.assertEqual(str(self.veiculo), 'Toyota Yaris')

    def test_cliente_str(self):
        self.assertEqual(str(self.cliente), self.user.get_full_name())

    def test_reserva_criacao(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=2),
            valor_total=71.00,
            forma_pagamento=self.forma_pagamento
        )
        self.assertEqual(str(reserva), f"Reserva de {self.veiculo} por {self.cliente}")
        self.assertFalse(reserva.cancelada)

    def test_forma_pagamento_str(self):
        self.assertEqual(str(self.forma_pagamento), 'Cartão')

    def test_contato_criacao(self):
        contato = Contato.objects.create(
            nome='João Silva',
            email='joao@example.com',
            mensagem='Gostaria de saber mais sobre os carros.'
        )
        self.assertEqual(str(contato), 'João Silva - joao@example.com')


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')
        self.cliente, _ = Cliente.objects.get_or_create(user=self.user, defaults={
            'telefone': '12345',
            'endereco': 'Rua X'
        })
        self.client = Client()
        self.client.login(username='teste', password='senha123')

        self.veiculo = Veiculo.objects.create(
            marca="Toyota",
            modelo="Corolla",
            categoria="Médio",
            transmissao="Manual",
            tipo_veiculo="Carro",
            capacidade_pessoas=5,
            imagem="veiculos/carro.jpg",
            valor_diaria=100,
            data_ultima_revisao=date.today() - timedelta(days=30),
            data_proxima_revisao=date.today() + timedelta(days=30),
            data_ultima_inspecao=date.today(),
            disponivel=True
        )

        self.pagamento = FormaPagamento.objects.create(tipo='Dinheiro')

    def test_pagina_inicial_status_code(self):
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)

    def test_sucesso_status_code(self):
        response = self.client.get(reverse('core:sucesso'))
        self.assertEqual(response.status_code, 200)

    def test_todos_veiculos_view(self):
        response = self.client.get(reverse('core:todos_veiculos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.veiculo.marca)

    def test_ver_veiculos_por_categoria(self):
        response = self.client.get(reverse('core:ver_carros_por_categoria', args=[self.veiculo.categoria]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.veiculo.modelo)

    def test_reservar_veiculo_view(self):
        response = self.client.post(reverse('core:reservar_veiculo', args=[self.veiculo.id]), {
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=2),
            'forma_pagamento': self.pagamento.id
        })
        self.assertEqual(response.status_code, 302)
        self.veiculo.refresh_from_db()
        self.assertFalse(self.veiculo.disponivel)
        self.assertTrue(Reserva.objects.exists())

    def test_lista_reservas_view(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=3),
            valor_total=300,
            forma_pagamento=self.pagamento
        )
        response = self.client.get(reverse('core:lista_reservas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.veiculo.marca)

    def test_cancelar_reserva(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=2),
            valor_total=200,
            forma_pagamento=self.pagamento
        )
        response = self.client.get(reverse('core:cancelar_reserva', args=[reserva.id]))
        self.assertRedirects(response, reverse('core:lista_reservas'))
        reserva.refresh_from_db()
        self.assertTrue(reserva.cancelada)

    def test_alterar_reserva(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=2),
            valor_total=200,
            forma_pagamento=self.pagamento
        )
        response = self.client.post(reverse('core:alterar_reserva', args=[reserva.id]), {
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=5),
            'forma_pagamento': self.pagamento.id
        })
        self.assertRedirects(response, reverse('core:lista_reservas'))
        reserva.refresh_from_db()
        self.assertEqual(reserva.valor_total, 500)

    def test_pesquisa_veiculos(self):
        response = self.client.get(reverse('core:pesquisa_veiculos'), {'marca': 'Toyota'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')
