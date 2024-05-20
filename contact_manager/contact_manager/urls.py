from django.contrib import admin
from django.urls import path, include

# router = DefaultRouter()
# router.register(r"contacts", ContactViewSet)
# router.register(r"persons", PersonViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/", include(router.urls)),
    path("api/", include("app.urls")),  # new
]
