from rest_framework import viewsets, renderers
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer, UserSignUpSerializers
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Prefetch
from app.models import ContactPhone
from app.permissions import IsOwner
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
from rest_framework import status


class SignUpAPIView(APIView):
    """
    This view is used for the create user
    """

    def post(self, request, format=None):

        try:
            data = request.data
            email = data.get("email", None)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            password = data.get("password", None)

            params = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
            }
            serializer = UserSignUpSerializers(data=params)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(serializer.data["password"])
                user.save()
            else:
                return Response(
                    {"status": False, "msg": str(serializer.error_messages)}
                )

            return Response(
                {"status": True, "message": "User hass been created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as val_err:
            return Response({"staus": False, "message": str(val_err)})


class LoginAPIView(APIView):
    """
    This API is used for login user
    """

    def post(self, request, formate=None):

        try:
            data = request.data
            email = data.get("email", None)
            password = data.get("password", None)

            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "status": True,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            return Response({"status": False})

        except Exception as val_err:
            return Response({"status": False, "message": str(val_err)})


# class ContactViewSet(viewsets.ModelViewSet):
#    queryset = Contact.objects.all()
#    serializer_class = ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # @action(
    #     detail=True,
    #     renderer_classes=[renderers.JSONRenderer],
    # )
    # def list(self, request, *args, **kwargs):
    #     instances = Contact.objects.prefetch_related(
    #         Prefetch("phones", queryset=ContactPhone.objects.filter(is_deleted=False))
    #     ).distinct()
    #     serializer = self.get_serializer(instances)
    #     return Response(serializer.data)

    @action(
        detail=True,
        renderer_classes=[renderers.JSONRenderer],
    )
    def retrieve(self, request, pk, *args, **kwargs):
        instance = (
            Contact.objects.filter(pk=pk)
            .prefetch_related(
                Prefetch(
                    "phones", queryset=ContactPhone.objects.filter(is_deleted=False)
                )
            )
            .first()
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        renderer_classes=[renderers.JSONRenderer],
    )
    def search_contacts(self, request, *args, **kwargs):
        user = request.user
        filter_contact = request.query_params.get("filter_word", None)
        ContactsObject = Contact.objects
        condition1 = Q(created_user=user)
        query = Q()
        if filter_contact:
            query = Q(fullname__contains=filter_contact)
            query.add(Q(phones__number__contains=filter_contact), Q.OR)
        instances = (
            ContactsObject.filter(condition1 & query)
            .prefetch_related(
                Prefetch(
                    "phones", queryset=ContactPhone.objects.filter(is_deleted=False)
                )
            )
            .distinct()
        )

        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
