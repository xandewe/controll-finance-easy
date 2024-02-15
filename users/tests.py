from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserType
from rest_framework_simplejwt.tokens import RefreshToken

User: UserType = get_user_model()


def create_user_with_token(
    user_data: dict = None, is_superuser: bool = False
) -> tuple[UserType, str]:
    """
    Cria um usuário comum e retorna-o juntamente com seu token de acesso JWT.
    Se passado is_superuser, cria um usuário admin
    """
    fake = Faker()

    default_user_data = {
        "username": "cassio",
        "email": fake.unique.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": "cassio123",
    }

    user_data = user_data or default_user_data

    if is_superuser:
        user = User.objects.create_superuser(**user_data)
    else:
        user = User.objects.create_user(**user_data)

    token: RefreshToken = RefreshToken.for_user(user)

    return user, str(token.access_token)


class UserViewTest(APITestCase):
    """
    Classe desenvolvida para testar criação de usuarios
    """

    def setUp(self):
        fake = Faker()

        User.objects.create_user(
            username=fake.unique.name,
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password="1234",
        )

    def test_common_user_creation_success(self):
        URL = reverse("user-create")

        user_data = {
            "first_name": "craque",
            "last_name": "neto",
            "username": "netao",
            "email": "neto@mail.com",
            "password": "123",
        }

        response = self.client.post(URL, user_data, format="json")

        expected_data = {
            "id": 2,
            "first_name": "craque",
            "last_name": "neto",
            "username": "netao",
            "email": "neto@mail.com",
        }

        expected_status_code = status.HTTP_201_CREATED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_user_creation_without_required_fields(self):
        URL = reverse("user-create")

        response = self.client.post(URL, {}, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "username": ["This field is required."],
            "password": ["This field is required."],
        }

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)

    def test_login_success(self):
        URL = reverse("user-login")

        user, _ = create_user_with_token()

        data_login = {
            "username": user.username,
            "password": "cassio123",
        }

        response = self.client.post(URL, data_login, format="json")

        expected_status_code = status.HTTP_200_OK

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        keys_expected = ("refresh", "access")

        for key, _ in response.json().items():
            self.assertIn(key, keys_expected)

    def test_login_failed(self):
        URL = reverse("user-login")

        user, _ = create_user_with_token()

        data_login = {
            "username": user.username,
            "password": "cassio",
        }

        response = self.client.post(URL, data_login, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        msg = f"Verifique se o status code está conforme o solicitado"

        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            'detail': 'No active account found with the given credentials'
        }

        msg = f"Verifique se as informações de retorno de transações estão de acordo"

        self.assertEqual(expected_data, response.json(), msg)