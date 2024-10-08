from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm

User = get_user_model()


class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    template_name = "registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:articles')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user_obj"
    paginate_related_by = 3


class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'user_password_change.html'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})
