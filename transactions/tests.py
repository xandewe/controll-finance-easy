from rest_framework.test import APITestCase


class TransactionListCreateViewTest(APITestCase):
    """
    Classe desenvolvida para testar criação e listagem de transações
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/transactions/"

    def test_transaction_creation(self):
        transaction_data = {
            
        }

    def test_transaction_list(self):
        ...
