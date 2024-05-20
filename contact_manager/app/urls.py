from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views


# API endpoints


contact_list = views.ContactViewSet.as_view(
    {"get": "search_contacts", "post": "create"}
)
contact_detail = views.ContactViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

user_singup = views.SignUpAPIView.as_view()
user_login = views.LoginAPIView.as_view()


# person_list = views.PersonViewSet.as_view({"get": "list", "post": "create"})
# person_detail = views.PersonViewSet.as_view(
#     {"get": "retrieve", "put": "update", "delete": "destroy"}
# )

urlpatterns = format_suffix_patterns(
    [
        path("contact/", contact_list, name="contact-list"),
        path("contact/<int:pk>/", contact_detail, name="contact-detail"),
        path("auth/signup", user_singup, name="auth-signup"),
        path("auth/", user_login, name="auth-login"),
        # path("person/", person_list, name="person-list"),
        # path("person/<int:pk>/", person_detail, name="person-detail"),
    ]
)
