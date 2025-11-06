# from django.urls import path
# from .views import RegisterView
#
# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrganisationViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'organisations', OrganisationViewSet, basename='organisation')

urlpatterns = [
    path('', include(router.urls)),  # include all router-generated endpoints
]
