import importlib

from django.contrib.auth.models import Group, User
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase
from django.urls import reverse
from pytils.translit import slugify

from .constants import DEFENDER_SLUGS, DEFENDERS_CATEGORIES
from .models import Blog, CategoryBlog
from .templatetags.user_app_tags import get_blog_category_for_menu

EMPTY_STATE_TEXT = 'Готуємо оновлення'
MENU_TITLE = 'ЗАХИСНИКАМ ТА ЗАХИСНИЦЯМ'
MIN_SEED_TEXT_LENGTH = 100
SEED_MIGRATION_NAME = '0005_seed_defenders_categories'
SEED_MIGRATION_MODULE = f'user_app.migrations.{SEED_MIGRATION_NAME}'


def detail_url(blog: Blog) -> str:
    """Return the public detail URL of a blog post."""
    return reverse('user_app:blog_single_view', kwargs={
        'slug_category': blog.category.slug,
        'id': blog.id,
        'slug': blog.slug,
    })


def run_seed() -> None:
    """Run the seed function on historical models, as migrate does."""
    module = importlib.import_module(SEED_MIGRATION_MODULE)
    state = MigrationExecutor(connection).loader.project_state(
        ('user_app', SEED_MIGRATION_NAME))
    module.seed_defenders(state.apps, None)


class DefendersConstantsTests(TestCase):
    def test_has_seven_categories_in_requested_order(self) -> None:
        titles = [title for _, title in DEFENDERS_CATEGORIES]

        self.assertEqual(titles, [
            'Обслуговування без черги',
            'Кабінет ветерана',
            'Медичні послуги та реабілітація',
            'ЕКОПФО',
            'Соціальні програми та пільги',
            'Підтримка родин військових',
            'Корисні ресурси та гарячі лінії',
        ])

    def test_slugs_match_model_slugify(self) -> None:
        # CategoryBlog.save() re-slugifies the title, so a mismatch would
        # silently break menu links after any re-save from the admin.
        for slug, title in DEFENDERS_CATEGORIES:
            with self.subTest(slug=slug):
                self.assertEqual(slug, slugify(title))

    def test_migration_copy_matches_constants(self) -> None:
        module = importlib.import_module(SEED_MIGRATION_MODULE)

        frozen = [(s, t) for s, t, _ in module.DEFENDERS_POSTS]

        self.assertEqual(frozen, list(DEFENDERS_CATEGORIES))


class DefendersSeedMigrationTests(TestCase):
    def test_each_category_exists_with_one_seed_post(self) -> None:
        for slug, title in DEFENDERS_CATEGORIES:
            with self.subTest(slug=slug):
                category = CategoryBlog.objects.get(slug=slug)
                self.assertEqual(category.title, title)
                self.assertEqual(
                    Blog.objects.filter(category=category).count(), 1)

    def test_seed_posts_have_text_and_valid_slug(self) -> None:
        for slug in DEFENDER_SLUGS:
            with self.subTest(slug=slug):
                blog = Blog.objects.get(category__slug=slug)
                self.assertGreater(len(blog.text), MIN_SEED_TEXT_LENGTH)
                self.assertEqual(blog.slug, slugify(blog.title))

    def test_seed_is_idempotent(self) -> None:
        categories_before = CategoryBlog.objects.count()
        blogs_before = Blog.objects.count()

        run_seed()

        self.assertEqual(CategoryBlog.objects.count(), categories_before)
        self.assertEqual(Blog.objects.count(), blogs_before)

    def test_seed_does_not_add_post_to_category_with_manager_content(
            self) -> None:
        category = CategoryBlog.objects.get(slug=DEFENDER_SLUGS[0])
        Blog.objects.filter(category=category).delete()
        Blog.objects.create(category=category, title='Manager post', text='x')

        run_seed()

        titles = list(
            Blog.objects.filter(category=category).values_list(
                'title', flat=True))
        self.assertEqual(titles, ['Manager post'])


class DefendersPagesTests(TestCase):
    def test_every_category_page_shows_seed_post(self) -> None:
        for slug in DEFENDER_SLUGS:
            with self.subTest(slug=slug):
                response = self.client.get(
                    reverse('user_app:blogs_view', kwargs={'slug': slug}))
                blog = Blog.objects.get(category__slug=slug)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, blog.title)
                self.assertNotContains(response, EMPTY_STATE_TEXT)

    def test_seed_post_detail_page_opens(self) -> None:
        for slug in DEFENDER_SLUGS:
            with self.subTest(slug=slug):
                blog = Blog.objects.get(category__slug=slug)

                response = self.client.get(detail_url(blog))

                self.assertEqual(response.status_code, 200)

    def test_blank_line_separates_paragraphs(self) -> None:
        category = CategoryBlog.objects.get(slug=DEFENDER_SLUGS[0])
        blog = Blog.objects.create(
            category=category, title='Two paragraphs',
            text='First paragraph.\n\nSecond <b>paragraph</b>.')

        response = self.client.get(detail_url(blog))

        self.assertContains(response, '<p>First paragraph.</p>', html=True)
        self.assertContains(
            response, '<p>Second &lt;b&gt;paragraph&lt;/b&gt;.</p>',
            html=True)


class DefendersMenuTests(TestCase):
    def test_home_page_renders_submenu_with_all_links_in_order(self) -> None:
        response = self.client.get(reverse('user_app:home_view'))
        content = response.content.decode()

        self.assertContains(response, MENU_TITLE)
        positions = []
        for slug, title in DEFENDERS_CATEGORIES:
            with self.subTest(slug=slug):
                url = reverse('user_app:blogs_view', kwargs={'slug': slug})
                self.assertContains(response, f'href="{url}"')
                self.assertContains(response, title.upper())
                positions.append(content.index(f'href="{url}"'))
        self.assertEqual(positions, sorted(positions))

    def test_submenu_toggle_declares_popup(self) -> None:
        response = self.client.get(reverse('user_app:home_view'))

        self.assertContains(response, 'aria-haspopup="true"')

    def test_barrier_free_menu_excludes_defenders_categories(self) -> None:
        slugs = {item['slug'] for item in get_blog_category_for_menu()}

        self.assertFalse(slugs & set(DEFENDER_SLUGS))


class DefendersManagerControlsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        group = Group.objects.create(name='manager')
        cls.manager = User.objects.create_user('mgr')
        cls.manager.groups.add(group)
        cls.blog = Blog.objects.get(category__slug=DEFENDER_SLUGS[0])

    def test_manager_sees_edit_delete_and_add(self) -> None:
        self.client.force_login(self.manager)

        detail = self.client.get(detail_url(self.blog))
        listing = self.client.get(
            reverse('user_app:blogs_view', kwargs={'slug': DEFENDER_SLUGS[0]}))

        self.assertContains(
            detail, reverse('update_blog', kwargs={'pk': self.blog.pk}))
        self.assertContains(
            detail, reverse('delete_blog', kwargs={'pk': self.blog.pk}))
        self.assertContains(listing, reverse('add_blog'))

    def test_visitor_does_not_see_manager_controls(self) -> None:
        detail = self.client.get(detail_url(self.blog))

        self.assertNotContains(
            detail, reverse('update_blog', kwargs={'pk': self.blog.pk}))
        self.assertNotContains(
            detail, reverse('delete_blog', kwargs={'pk': self.blog.pk}))

    def test_manager_can_open_update_form(self) -> None:
        self.client.force_login(self.manager)

        response = self.client.get(
            reverse('update_blog', kwargs={'pk': self.blog.pk}))

        self.assertEqual(response.status_code, 200)
