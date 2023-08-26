from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class CompanyAdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a company admin."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_role == 2:
            return redirect('orders:order-list')
        return super().dispatch(request, *args, **kwargs)
    

class CompanyOwnerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a company owner."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_role == 1:
            return redirect('orders:order-list')
        return super().dispatch(request, *args, **kwargs)
    

class EmployeeRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an employee."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_role == 3:
            return redirect('orders:order-list')
        return super().dispatch(request, *args, **kwargs)