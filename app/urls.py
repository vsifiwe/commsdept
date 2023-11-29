from django.urls import path
from .views import (
    email_registration,
    create_ticket,
    get_my_tickets,
    add_followup,
    get_ticket,
    get_queries_by_dept,
    change_dept,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", email_registration, name="email_registration"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create/", create_ticket, name="create_ticket"),
    path("mytickets/", get_my_tickets, name="get_my_tickets"),
    path("followup/", add_followup, name="update_ticket"),
    path("ticket/<int:id>/", get_ticket, name="get_single_ticket"),
    path("queries-dept/", get_queries_by_dept, name="get_queries_by_dept"),
    path("change-dept/", change_dept, name="change-dept"),
]
