from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ManagerUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for views requiring manager user authentication.

    This mixin combines the functionalities of LoginRequiredMixin and
    UserPassesTestMixin
    to ensure that the user is authenticated and has manager privileges before
    accessing the view.

    Attributes:
        login_url (str): The URL to redirect to if the user is not logged in.

    Methods:
        test_func: Checks if the user belongs to the 'manager' group.

    """
    login_url = '/login/'

    def test_func(self):
        """
        Method to test if the user belongs to the 'manager' group.

        Returns:
            bool: True if the user belongs to the 'manager' group, False
            otherwise.

        """
        return self.request.user.groups.filter(name='manager').exists()
