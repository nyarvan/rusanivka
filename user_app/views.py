from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView, TemplateView
from .models import Department, Doctor, Administration, CategoryBlog, Blog, BlogImage
from .forms import FormContact


class HomepageView(ListView):
    """
    A view to display the homepage with a list of departments and
    some featured doctors.

    Attributes:
        template_name (str): The template to render for this view.
        context_object_name (str): The name of the context variable containing
        the list of departments.

    Methods:
        get_queryset(): Retrieve the queryset of departments.
        get_context_data(): Get additional context data for the template.
    """

    template_name = 'home.html'
    context_object_name = 'departments'

    def get_queryset(self):
        """
        Get the queryset of departments ordered by their numbers.

        Returns:
            queryset: Departments ordered by their numbers.
        """
        return Department.objects.all().order_by('number')

    def get_context_data(self, **kwargs):
        """
        Get the additional context data.

        Returns:
            dict: Additional context data.
        """
        context = super().get_context_data(**kwargs)

        # Add queryset of visible doctors who are not managers,
        # ordered randomly, limited to four instances
        context['doctors'] = Doctor.objects.filter(
            is_visible=True, is_manager=False).order_by('?')[:4]

        return context


class AdministrationView(ListView):
    """
    A view to display the list of administrators.

    Attributes:
        template_name (str): The template to render for this view.
        context_object_name (str): The name of the context variable containing
    the list of administrators.
    Methods:
        get_queryset(): Retrieve the queryset of administrators.
    """

    template_name = 'administration.html'
    context_object_name = 'admins'

    def get_queryset(self):
        """
        Get the queryset of administrators.

        Returns:
            queryset: Administrators ordered by their position.
        """
        return Administration.objects.all().order_by('position')


class DepartmentView(ListView):
    """
    A view to display the details of a department and its doctors.

    Attributes:
        template_name (str): The template to render for this view.
        context_object_name (str): The name of the context variable containing
    the list of doctors.

    Methods:
        get_queryset(): Retrieve the queryset of doctors for
    the specified department.
        get_context_data(): Get additional context data for the template.
    """

    template_name = 'ambulant.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        """
        Get the queryset of doctors for the specified department.

        Returns:
            queryset: Doctors for the specified department, ordered by whether
        they are managers and their positions.
        """
        department_id = self.kwargs.get('id')
        return Doctor.objects.filter(
            department=department_id, is_visible=True).order_by(
                '-is_manager', 'post')

    def get_context_data(self, **kwargs):
        """
        Get the additional context data for the template.

        Returns:
            dict: Additional context data, including the department and
        invisible doctors.
        """
        department_id = self.kwargs.get('id')
        context = super().get_context_data(**kwargs)
        # Add the department to the context
        context['department'] = get_object_or_404(Department, id=department_id)
        # Add invisible doctors of the department to the context
        context['unvisible_doctor'] = Doctor.objects.filter(
                                        is_visible=False,
                                        department=department_id)
        return context


class DrugsView(TemplateView):
    """
    DrugsView displays the drugs.html template.

    This class is used to handle requests related to displaying the page
    with information about drugs. It inherits from TemplateView, making it
    easy to render an HTML template.

    Attributes:
    ----------
    template_name : str
        The name of the template to be rendered.

    Methods:
    -------
    get_context_data(**kwargs):
        Returns the context data to be used in the drugs.html template.
    """

    template_name = 'drugs.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data to be used in the template.

        Parameters:
        ----------
        **kwargs : dict
            Additional context parameters.

        Returns:
        ----------
        dict
            The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        return context


class BlogsView(ListView):
    """
    A view to display a list of blogs filtered by category.

    Attributes:
        template_name (str): The template to render for this view.
        context_object_name (str): The name of the context variable containing
        the list of blogs.
        paginate_by (int): Number of blogs per page.

    Methods:
        get_queryset(): Retrieve the queryset of blogs filtered by category.
        get_context_data(**kwargs: Any) -> dict[str, Any]: Add extra
        context data to be used in the template.
    """

    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        """
        Get the queryset of blogs filtered by category slug.

        Returns:
            queryset: Blogs ordered by their creation date.
        """
        return Blog.objects.filter(
            category__slug=self.kwargs.get('slug')).order_by('-create')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Add extra context data to be used in the template.

        Returns:
            dict: Context data including the blog category.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            CategoryBlog, slug=self.kwargs.get('slug'))
        return context


class BlogDetailView(DetailView):
    """
    A view to display details of a single blog.

    Attributes:
        template_name (str): The template to render for this view.
        context_object_name (str): The name of the context variable containing
        the blog object.
        model (Model): The model class for the blog object.

    Methods:
        get_object(): Retrieve the blog object based on the URL parameters.
        get_context_data(**kwargs): Add extra context data to be used
        in the template.
    """

    template_name = 'blog_single.html'
    context_object_name = 'blog'
    model = Blog

    def get_object(self):
        """
        Retrieve the blog object based on the URL parameters.

        Returns:
            Blog: The blog object matching the provided parameters.
        """
        return get_object_or_404(
            Blog,
            id=self.kwargs.get('id'),
            slug=self.kwargs.get('slug'),
            category__slug=self.kwargs.get('slug_category')
        )

    def get_context_data(self, **kwargs):
        """
        Add extra context data to be used in the template.

        Returns:
            dict: Context data including images related to the blog.
        """
        context = super().get_context_data(**kwargs)
        context['images'] = BlogImage.objects.filter(blog=self.get_object())
        return context


class ContactView(FormView):
    """
    A view to handle contact form submissions.

    Attributes:
        form_class (Form): The form class used for contact form submission.
        template_name (str): The template to render for this view.
        success_url (str): The URL to redirect to after successful
        form submission.

    Methods:
        form_valid(form): Handle form submission when it is valid.
    """

    form_class = FormContact
    template_name = 'contact.html'
    success_url = '/'

    def form_valid(self, form):
        """
        Handle form submission when it is valid.

        Parameters:
            form (Form): The validated form object containing
            the submitted data.

        Returns:
            HttpResponseRedirect: Redirect to the success URL after saving
            the form data.
        """
        form.save()
        return super(ContactView, self).form_valid(form)


class DocumentView(TemplateView):
    """
    A view to display a document template.

    Attributes:
        template_name (str): The template to render for this view.
    """

    template_name = 'statut.html'
