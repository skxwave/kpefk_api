import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GetGroupsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        with open("groups.json", encoding="utf-8") as file:
            data = json.load(file)
        return Response(
            data={
                "status": "OK",
                "result": data,
            },
            status=status.HTTP_200_OK,
        )
