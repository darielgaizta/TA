from rest_framework.response import Response

class ResponseBuilder:
    @staticmethod
    def respondWithMessage(status: int, message: str):
        return Response(data={'message': message}, status=status)