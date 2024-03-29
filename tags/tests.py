from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from .models import Tag
from transactions.models import Transaction
from faker import Faker
import random
from users.tests import create_user_with_token


class TagListViewTest(APITestCase):
    """
    Classe desenvolvida para testar listagem de tags
    """

    def setUp(self) -> None:
        tag1 = Tag.objects.create(tag_name="Alimentacao", sub_tag_name="ifood")
        tag2 = Tag.objects.create(tag_name="Saude", sub_tag_name="academia")

    def test_tag_list(self):
        URL = reverse("tag-list")

        response = self.client.get(URL)

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = f"Verifique se a paginação está sendo feita corretamente"

        for expected_key in expected_pagination_keys:
            self.assertIn(expected_key, response.json().keys(), msg)

        results_len = response.json()["count"]
        expected_len = 2

        msg = "Verifique se a paginação está retornando apenas dois items de cada vez"

        self.assertEqual(expected_len, results_len, msg)

        expected_keys = {"id", "tag_name", "sub_tag_name"}

        msg = f"Verifique se o serializer foi configurado para retornar os campos corretamente"

        for key in expected_keys:
            first_data = response.json()["results"][0].keys()

            self.assertIn(key, first_data, msg)


class TagCreateViewTest(APITestCase):
    """
    Classe desenvolvida para testar criação de tags
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, cls.credencial = create_user_with_token()

    def setUp(self) -> None:
        fake = Faker()

        tag1 = Tag.objects.create(tag_name="Saude", sub_tag_name="academia")

        Transaction.objects.create(
            name=f"Transferência enviada pelo Pix - {fake.name()}",
            value=round(random.uniform(1, 1000), 2),
            status="Done",
            type="Expense",
            created_at=f"2024-02-10",
            year_month_reference=f"2024-02",
            tag=tag1,
        )

    def test_tag_creation_success(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Done",
            "type": "Income",
            "tag": {"tag_name": "Alimentacao", "sub_tag_name": "mercado"},
            "created_at": "2023-01-09",
            "year_month_reference": "2023-01",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, transaction_data, format="json")

        expected_data = {
            "id": 2,
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": "107.19",
            "status": "Done",
            "tag": {
                "id": 2,
                "tag_name": "Alimentacao",
                "sub_tag_name": "Mercado",
            },
            "type": "Income",
            "created_at": "2023-01-09",
        }

        expected_status_code = status.HTTP_201_CREATED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_tag_creation_without_required_fields(self):
        URL = reverse("transaction-list-create")

        transaction_data = {
            "name": "Transferência Recebida - FULANO - •••.111.111-•• - Easynvest",
            "description": "investimento",
            "value": 107.19,
            "status": "Done",
            "type": "Income",
            "tag": {},
            "created_at": "2023-01-09",
            "year_month_reference": "2023-01",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, data=transaction_data, format="json")

        expected_data = {
            "tag": {
                "tag_name": ["This field is required."],
                "sub_tag_name": ["This field is required."],
            }
        }

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se a mensagem de erro está de acordo"

        self.assertEqual(expected_data, response.json(), msg)


class TagDetailViewTest(APITestCase):
    """
    Classe desenvolvida para testar atualização de tags
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, cls.credencial = create_user_with_token()

    def setUp(self) -> None:
        fake = Faker()

        tag1 = Tag.objects.create(tag_name="Saude", sub_tag_name="academia")

        Transaction.objects.create(
            name=f"Transferência enviada pelo Pix - {fake.name()}",
            value=round(random.uniform(1, 1000), 2),
            status="Done",
            type="Expense",
            created_at=f"2024-02-10",
            year_month_reference=f"2024-02",
            user=self.user,
            tag=tag1,
        )

    def test_update_tag_by_id_success(self):
        transaction = Tag.objects.create(
            tag_name="Assinaturas",
            sub_tag_name="Amaonz",
        )

        URL = reverse("tag-detail", kwargs={"pk": transaction.pk})

        transaction_data = {
            "sub_tag_name": "amazon",
        }

        response = self.client.patch(URL, transaction_data, format="json")

        expected_data = {
            "id": transaction.pk,
            "tag_name": "Assinaturas",
            "sub_tag_name": "amazon",
        }

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_update_tag_by_id_invalid(self):
        URL = reverse("tag-detail", kwargs={"pk": 100})

        response = self.client.patch(URL)

        expected_status_code = status.HTTP_404_NOT_FOUND

        msg = f"Verifique se o status code está conforme o solicitado {expected_status_code}"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {"detail": "Not found."}

        msg = "Verifique se está retornando a mensagem de erro correta"

        self.assertEqual(expected_data, response.json(), msg)
