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


class GetGroupInfoAPIView(APIView):
    def get(self, request, group_number, *args, **kwargs):
        with open("schedule.json", encoding="utf-8") as file:
            data = json.load(file)

        group = data.get("groups", {}).get(group_number)

        if not group:
            return Response(
                data={
                    "status": "NOT_FOUND",
                    "result": "Group not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            data={
                "status": "OK",
                "result": group["info"],
            },
            status=status.HTTP_200_OK,
        )
