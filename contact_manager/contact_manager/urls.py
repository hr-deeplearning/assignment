from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ContactViewSet
from app.urls import urlpatterns as app_urls

# router = DefaultRouter()
# router.register(r"contacts", ContactViewSet)
# router.register(r"persons", PersonViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/", include(router.urls)),
    path("api/", include("app.urls")),  # new
]
