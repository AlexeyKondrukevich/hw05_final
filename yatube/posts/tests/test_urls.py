from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()

    def test_unexisting_page(self):
        response = self.unauthorized_user.get("/unexisting_page/")  # Act

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Тестовое название группы",
            slug="test_slug",
            description="Тестовое описание группы",
        )

        cls.user_author = User.objects.create_user(username="user_author")
        cls.another_user = User.objects.create_user(username="another_user")

        cls.post = Post.objects.create(
            text="Тестовый текст, тестовый текст",
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.unauthorized_user = Client()
        self.post_author = Client()
        self.post_author.force_login(self.user_author)
        self.authorized_user = Client()
        self.authorized_user.force_login(self.another_user)
        cache.clear()

    def test_unauthorized_user(self):
        """Страницы в списке доступны неавторизованному пользователю."""
        urls = [
            "/",
            "/group/test_slug/",
            "/profile/user_author/",
            f"/posts/{self.post.id}/",
        ]

        for address in urls:  # Act
            with self.subTest(address=address):
                response = self.unauthorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_user(self):
        """Страницы в списке доступны авторизованному пользователю."""
        urls = [
            "/",
            "/create/",
            "/group/test_slug/",
            "/profile/user_author/",
            f"/posts/{self.post.id}/",
        ]

        for address in urls:  # Act
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_exists_at_desired_location(self):
        """Страница /post_edit/ доступна только автору."""
        response = self.post_author.get(f"/posts/{self.post.id}/edit/")  # Act

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_redirects_unauthorized_user_on_auth_login(self):
        """Страница редактирования поста перенаправит анонимного
        пользователя на страницу регистрации.
        """
        response = self.unauthorized_user.get(  # Act
            f"/posts/{self.post.id}/edit/", follow=True
        )

        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.id}/edit/"
        )

    def test_post_comment_redirects_authorized_user_on_post_detail(self):
        """Страница добавления комментария к посту перенаправит авторизованного
        пользователя на страницу информации о посте.
        """
        response = self.authorized_user.post(  # Act
            f"/posts/{self.post.id}/comment/"
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_comment_redirects_unauthorized_user_on_auth_login(self):
        """Страница добавления комментария к посту перенаправит анонимного
        пользователя на страницу регистрации.
        """
        response = self.unauthorized_user.get(  # Act
            f"/posts/{self.post.id}/comment/", follow=True
        )

        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.id}/comment/"
        )

    def test_post_edit_redirects_authorized_user_on_post_detail(self):
        """Страница редактирования поста перенаправит авторизованного
        пользователя на страницу информации о посте.
        """
        response = self.authorized_user.get(  # Act
            f"/posts/{self.post.id}/edit/"
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/": "posts/index.html",
            "/group/test_slug/": "posts/group_list.html",
            "/profile/user_author/": "posts/profile.html",
            "/create/": "posts/create_post.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
            f"/posts/{self.post.id}/edit/": "posts/create_post.html",
        }

        for address, template in templates_url_names.items():  # Act
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)
