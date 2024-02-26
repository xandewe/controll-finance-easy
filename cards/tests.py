from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from users.tests import create_user_with_token
import random
from .models import Card, CreditCardDetail


class CardListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, cls.credencial = create_user_with_token(True)
        cls.user_common1, cls.user_common1_credential = create_user_with_token(
            username="neto", password="neto123"
        )
        cls.user_common2, cls.user_common2_credential = create_user_with_token(
            username="ronaldo", password="ronaldo123"
        )

    def setUp(self) -> None:
        users_list = (
            self.user_common1,
            self.user_common2,
        )

        for user in users_list:
            detail_data = {
                "due_date": round(random.uniform(1, 30)),
                "closing_date": round(random.uniform(1, 30)),
            }

            detail = CreditCardDetail(**detail_data)

            card_data = {
                "card_name": "Nubank",
                "category": "Credit",
                "card_detail": detail,
                "user": user,
            }

            Card.objects.create(**card_data)

        for user in users_list:
            card_data = {"card_name": "Nubank", "category": "Account", "user": user}
            Card.objects.create(**card_data)

    def test_credit_card_creation_success(self):
        URL = reverse("card-list-create")

        card_data = {
            "card_name": "Nubank",
            "category": "Credit",
            "card_detail": {"due_date": 27, "closing_date": 3},
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, card_data, format="json")

        expected_status_code = status.HTTP_201_CREATED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": response.json()["id"],
            "card_name": "Nubank",
            "category": "Credit",
            "card_detail": {
                "closing_date": 3,
                "due_date": 27,
                "id": response.json()["card_detail"]["id"],
                "updated_at": response.json()["card_detail"]["updated_at"],
            },
        }

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_account_card_creation_success(self):
        URL = reverse("card-list-create")

        card_data = {
            "card_name": "Nubank",
            "category": "Account",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, card_data, format="json")

        expected_status_code = status.HTTP_201_CREATED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": response.json()["id"],
            "card_name": "Nubank",
            "category": "Account",
            "card_detail": None,
        }

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_card_creation_without_token(self):
        URL = reverse("card-list-create")

        card_data = {
            "card_name": "Nubank",
            "category": "Account",
        }

        response = self.client.post(URL, card_data, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {"detail": "Authentication credentials were not provided."}

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_card_creation_with_category_invalid(self):
        URL = reverse("card-list-create")

        card_data = {
            "card_name": "Nubank",
            "category": "Other",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, card_data, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {"category": ['"Other" is not a valid choice.']}

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_card_creation_without_required_fields(self):
        URL = reverse("card-list-create")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.post(URL, data={}, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "card_name": ["This field is required."],
            "category": ["This field is required."],
        }

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_cards_list(self):
        URL = reverse("card-list-create")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.credencial)
        response = self.client.get(URL)

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = f"Verifique se a paginação está sendo feita corretamente"

        for expected_key in expected_pagination_keys:
            self.assertIn(expected_key, response.json().keys(), msg)

        results_len = response.json()["count"]
        expected_len = 4

        msg = "Verifique se a paginação está retornando apenas seis items de cada vez"

        self.assertEqual(expected_len, results_len, msg)

        expected_keys = {
            "id",
            "card_name",
            "category",
            "card_detail",
        }

        msg = f"Verifique se o serializer foi configurado para retornar os campos corretamente"

        for key in expected_keys:
            result_keys = response.json()["results"][0].keys()
            first_data = result_keys

            self.assertIn(key, first_data, msg)
