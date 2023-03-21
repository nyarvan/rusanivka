from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ManagerUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/login/'
    
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
