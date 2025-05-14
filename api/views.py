from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.db.models import Count, Q
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from datetime import date

from .forms import SignUpForm
from .serializers import UserSerializer, HobbySerializer
from .models import User, Hobby


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, "api/spa/index.html", {})


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class RelativeModelViewSet(viewsets.ModelViewSet):
  def get_serializer_context(self):
    result = super().get_serializer_context()
    result['request'] = None
    return(result)

class UserViewSet(RelativeModelViewSet):
    """
    API endpoint for users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.kwargs.get("pk") == "current":
            return self.request.user

        return super().get_object()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        users_with_shared_hobbies = queryset.annotate(
            shared_hobbies_count=Count(
                "hobbies", filter=Q(hobbies__in=request.user.hobbies.all())
            )
        ).order_by("-shared_hobbies_count")

        min_age = request.query_params.get("min_age")
        max_age = request.query_params.get("max_age")
        today = date.today()

        if min_age:
            min_date_of_birth = date(today.year - int(min_age), today.month, today.day)
            users_with_shared_hobbies = users_with_shared_hobbies.filter(
                date_of_birth__lte=min_date_of_birth
            )
        if max_age:
            max_date_of_birth = date(today.year - int(max_age), today.month, today.day)
            users_with_shared_hobbies = users_with_shared_hobbies.filter(
                date_of_birth__gte=max_date_of_birth
            )

        serializer = self.get_serializer(users_with_shared_hobbies, many=True)

        page = self.paginate_queryset(users_with_shared_hobbies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class HobbyViewSet(RelativeModelViewSet):
    """
    API endpoint for hobbies.
    """

    queryset = Hobby.objects.all().order_by("name")
    serializer_class = HobbySerializer
    permission_classes = [permissions.IsAuthenticated]
