# # view.py
# from django.shortcuts import render
# from rest_framework import generics, status
# from rest_framework.response import Response
# from .serializers import RegisterSerializer
#
#
# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'registration.html')
#
#     def post(self, request, *args, **kwargs):
#         # Print request data for debugging
#         print(request.data)
#
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=False):
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             # Print validation errors for debugging
#             print(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound

from .models import Organisation, User
from .serializers import (
    OrganisationBaseSerializer,
    OrganisationDetailSerializer,
    UserBaseSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
)


class SerializerByActionMixin:
    serializer_action_classes = {}

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, super().get_serializer_class())


class OrganisationViewSet(SerializerByActionMixin, viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializer_action_classes = {
        "list": OrganisationBaseSerializer,
        "retrieve": OrganisationDetailSerializer,
        "create": OrganisationDetailSerializer,
        "update": OrganisationDetailSerializer,
        "partial_update": OrganisationDetailSerializer,
    }

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError({"error": f"Organisation creation failed: {str(e)}"})


class UserViewSet(SerializerByActionMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializer_action_classes = {
        "list": UserBaseSerializer,
        "retrieve": UserDetailSerializer,
        "create": UserCreateSerializer,
        "update": UserDetailSerializer,
        "partial_update": UserDetailSerializer,
    }

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError({"error": f"User creation failed: {str(e)}"})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_verified = True
            user.save()
            return Response({"status": "user verified"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound({"error": "User not found"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
