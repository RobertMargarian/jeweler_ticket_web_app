from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class CompanyOwnerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a company owner."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner:
            return redirect('orders:order-list')
        return super().dispatch(request, *args, **kwargs)
    

class EmployeeRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an employee."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employee:
            return redirect('orders:order-list')
        return super().dispatch(request, *args, **kwargs)