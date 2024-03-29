from rest_framework.exceptions import APIException, status

class InvalidDateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Date invalid, enter a date valid between 1 a 31.'

class UserDoesNotContainsCardException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Card does not belong to the authenticated user.'