from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from .models import Tag


class TagListViewTest(APITestCase):
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


class TagDetailViewTest(APITestCase):
    ...
