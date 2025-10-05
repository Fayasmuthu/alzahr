from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.forms import models as model_forms
from django.views.generic import DetailView, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
# from django_filters.views import FilterView
# from django_tables2.export.views import ExportMixin
# from django_tables2.views import SingleTableMixin
# from core.models import Employee
# from core.models import Student
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin


class SuperAdminLoginRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied("You must be a superuser to access this page.")
        else:
            # Custom handling for displaying a 403 Forbidden template
            return render(self.request, 'web/404.html', status=403)

def check_access(request, permissions):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.usertype in permissions:
            return True
    return False


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permissions = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        usertype = self.request.user.usertype
        if (
            usertype in ["teacher", "management", "accountant"]
            and not Employee.objects.filter(user=self.request.user).exists()
            or usertype == "student"
            and not Student.objects.filter(user=self.request.user).exists()
        ):
            return self.handle_no_permission()

        if not check_access(request, self.permissions):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

class CustomModelFormMixin:
    exclude = None

    # Rewriting get_form_class to support exclude attribute
    def get_form_class(self):
        model = getattr(self, "model", None)
        if self.exclude:
            exclude = getattr(self, "exclude", None)
            return model_forms.modelform_factory(model, exclude=exclude)
        return super().get_form_class()


class HybridDetailView(SuperAdminLoginRequiredMixin, DetailView):
    template_name = "app/common/object_view.html"


class HybridCreateView(SuperAdminLoginRequiredMixin, CustomModelFormMixin, CreateView):
    template_name = "app/common/object_form.html"
    exclude = ("creator", "is_active")

    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model
        content_type = ContentType.objects.get_for_model(model)
        context["title"] = content_type.model_class()._meta.verbose_name
        return context


class HybridUpdateView(SuperAdminLoginRequiredMixin, CustomModelFormMixin, UpdateView):
    template_name = "app/common/object_form.html"
    exclude = ("creator", "is_active")

    def get_success_url(self):
        return self.object.get_list_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model
        content_type = ContentType.objects.get_for_model(model)
        context["title"] = content_type.model_class()._meta.verbose_name
        return context


class HybridDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    template_name = "app/common/confirm_delete.html"

    def get_success_url(self):
        return self.object.get_list_url()


class HybridListView(SuperAdminLoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView, ListView):
    template_name = "app/common/object_list.html"
    table_pagination = {"per_page": 50}

    def get_export_filename(self, export_format):
        # Customize the export filename if needed
        return f"{self.model.__name__}_export.{export_format}"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model
        content_type = ContentType.objects.get_for_model(model)
        context["title"] = content_type.model_class()._meta.verbose_name_plural
        context[f"is_{content_type.model_class()._meta.verbose_name_plural}"] = True
        return context


class HybridFormView(SuperAdminLoginRequiredMixin, TemplateView):
    template_name = "app/common/object_form.html"


class HybridTemplateView(SuperAdminLoginRequiredMixin, TemplateView):
    template_name = "app/common/object_view.html"


class HybridView(SuperAdminLoginRequiredMixin, View):
    pass


class OpenView(TemplateView):
    pass
