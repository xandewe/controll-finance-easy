from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from faker import Faker
from .models import Transaction
import random


class TransactionListCreateViewTest(APITestCase):
    """
    Classe desenvolvida para testar criação e listagem de transações
    """

    def setUp(self):
        fake = Faker()

        for _ in range(2):
            date = fake.date_this_month().strftime("%Y-%m-%d")

            Transaction.objects.create(
                name=f"Transferência Recebida - {fake.name()}",
                value=round(random.uniform(1, 1000), 2),
                status="Done",
                type="Income",
                created_at=date,
            )

        for _ in range(2):
            date = fake.date_this_month().strftime("%Y-%m-%d")

            Transaction.objects.create(
                name=f"Transferência enviada pelo Pix - {fake.name()}",
                value=round(random.uniform(1, 1000), 2),
                status="Done",
                type="Income",
                created_at=date,
            )

    def test_income_transaction_creation_success(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Done",
            "type": "Income",
            "created_at": "2023-01-09",
        }

        response = self.client.post(URL, transaction_data, format="json")

        expected_data = {
            "id": 5,
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": "107.19",
            "status": "Done",
            "tag": None,
            "type": "Income",
            "created_at": "2023-01-09",
        }

        expected_status_code = status.HTTP_201_CREATED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_transaction_creation_without_required_fields(self):
        URL = reverse("transaction-list-create")

        response = self.client.post(URL, data={}, format="json")

        expected_data = {
            "name": ["This field is required."],
            "value": ["This field is required."],
            "type": ["This field is required."],
            "created_at": ["This field is required."],
        }

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se a mensagem de erro está de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_transaction_creation_with_field_status_invalid(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Other",
            "tag": {"tag_name": "Alimentacao", "sub_tag_name": "mercado"},
            "type": "Income",
            "created_at": "2023-01-09",
        }

        response = self.client.post(URL, transaction_data, format="json")

        expected_data = {
            "status": ['"Other" is not a valid choice.'],
        }

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se a mensagem de erro está de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_transaction_creation_with_field_type_invalid(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Done",
            "tag": {"tag_name": "Alimentacao", "sub_tag_name": "mercado"},
            "type": "Other",
            "created_at": "2023-01-09",
        }

        response = self.client.post(URL, transaction_data, format="json")

        expected_data = {
            "type": ['"Other" is not a valid choice.'],
        }

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se a mensagem de erro está de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_transaction_creation_with_field_tag_name_invalid(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Done",
            "tag": {"tag_name": "alimento", "sub_tag_name": "mercado"},
            "type": "Income",
            "created_at": "2023-01-09",
        }

        response = self.client.post(URL, transaction_data, format="json")

        expected_data = {
            "tag": {"tag_name": ['"alimento" is not a valid choice.']},
        }

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se a mensagem de erro está de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_transaction_list(self):
        URL = reverse("transaction-list-create")

        response = self.client.get(URL)

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = f"Verifique se a paginação está sendo feita corretamente"

        for expected_key in expected_pagination_keys:
            self.assertIn(expected_key, response.json().keys(), msg)

        results_len = len(response.json()["results"])
        expected_len = 4

        msg = "Verifique se a paginação está retornando apenas quatro items de cada vez"

        self.assertEqual(expected_len, results_len, msg)


class TransactionDetailViewTest(APITestCase):
    """
    Classe desenvolvida para testar a busca por id, deleção e atualização de transações
    """

    def setUp(self):
        fake = Faker()

        for _ in range(2):
            date = fake.date_this_month().strftime("%Y-%m-%d")

            Transaction.objects.create(
                name=f"Transferência Recebida - {fake.name()}",
                value=round(random.uniform(1, 1000), 2),
                status="Done",
                type="Income",
                created_at=date,
            )

        for _ in range(2):
            date = fake.date_this_month().strftime("%Y-%m-%d")

            Transaction.objects.create(
                name=f"Transferência enviada pelo Pix - {fake.name()}",
                value=round(random.uniform(1, 1000), 2),
                status="Done",
                type="Income",
                created_at=date,
            )

    def test_get_transaction_by_id_success(self):
        transaction = Transaction.objects.create(
            name=f"Transferência Recebida - Guido Van Rossum",
            value=1000.50,
            status="Done",
            type="Income",
            created_at="2024-01-01",
        )

        URL = reverse("transaction-detail", kwargs={"pk": transaction.pk})

        response = self.client.get(URL)

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": transaction.pk,
            "name": "Transferência Recebida - Guido Van Rossum",
            "description": None,
            "value": "1000.50",
            "tag": None,
            "status": "Done",
            "type": "Income",
            "created_at": "2024-01-01",
        }

        msg = "Verifique se está retornando o mesmo dado buscado por id"

        self.assertEqual(expected_data, response.json(), msg)

    def test_get_transaction_by_id_invalid(self):  
        URL = reverse("transaction-detail", kwargs={"pk": 100})

        response = self.client.get(URL)

        expected_status_code = status.HTTP_404_NOT_FOUND

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "Not found."
        }

        msg = "Verifique se está retornando a mensagem de erro correta"

        self.assertEqual(expected_data, response.json(), msg)
    
    def test_delete_transaction_by_id_success(self):
        transaction = Transaction.objects.create(
            name=f"Transferência Recebida - Guido Van Rossum",
            value=1000.50,
            status="Done",
            type="Income",
            created_at="2024-01-01",
        )

        URL = reverse("transaction-detail", kwargs={"pk": transaction.pk})

        response = self.client.delete(URL)

        expected_status_code = status.HTTP_204_NO_CONTENT

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        response = self.client.get(URL)

        expected_status_code = status.HTTP_404_NOT_FOUND

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}, e se a transação foi de fato deletada"

    def test_delete_transaction_by_id_invalid(self):
        URL = reverse("transaction-detail", kwargs={"pk": 100})

        response = self.client.delete(URL)

        expected_status_code = status.HTTP_404_NOT_FOUND

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "Not found."
        }

        msg = "Verifique se está retornando a mensagem de erro correta"

        self.assertEqual(expected_data, response.json(), msg)

    def test_update_transaction_by_id_success(self):
        transaction = Transaction.objects.create(
            name=f"Transferência Recebida - Gado Rossum",
            value=1000.50,
            status="Done",
            type="Income",
            created_at="2024-01-01",
        )

        URL = reverse("transaction-detail", kwargs={"pk": transaction.pk})

        transaction_data = {
            "name": "Transferência Recebida - Guido Van Rossum",
            "description": "freela",
            "value": 1300.50
        }

        response = self.client.patch(URL, transaction_data, format="json")

        expected_data = {
            "id": 5,
            "name": "Transferência Recebida - Guido Van Rossum",
            "description": "freela",
            "value": "1300.50",
            "status": "Done",
            "tag": None,
            "type": "Income",
            "created_at": "2024-01-01",
        }

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_update_transaction_by_id_invalid(self):
        URL = reverse("transaction-detail", kwargs={"pk": 100})

        response = self.client.patch(URL)

        expected_status_code = status.HTTP_404_NOT_FOUND

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "Not found."
        }

        msg = "Verifique se está retornando a mensagem de erro correta"

        self.assertEqual(expected_data, response.json(), msg)