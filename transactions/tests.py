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
        ...

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

        msg = (
            "\nVerifique se a paginação está retornando apenas quatro items de cada vez"
        )
        self.assertEqual(expected_len, results_len)
