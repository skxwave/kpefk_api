import json
import os

from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.schedule.helpers import groups_to_json, main

load_dotenv()

true_password = os.getenv("PASSWORD")


class UpdateScheduleAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get("password", None) == true_password:
            groups_to_json()
            main()
            return Response(
                data={
                    "status": "OK",
                    "message": "schedule updated",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"status": "401", "result": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class GetAllScheduleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        with open("schedule.json", encoding="utf-8") as file:
            data = json.load(file)
        return Response(
            data={
                "status": "OK",
                "result": data,
            },
            status=status.HTTP_200_OK,
        )


class GetGroupScheduleAPIView(APIView):
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
                "result": group,
            },
            status=status.HTTP_200_OK,
        )
