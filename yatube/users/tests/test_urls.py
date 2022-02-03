from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()
uidb64 = "Mw"
token = "5xr-9713b923abcdd5a56637"


class UsersURLTests(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()
        self.user = User.objects.create_user(username="user")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_getability_of_pages(self):
        """Страницы приложения users доступны пользователям."""
        usertype_and_urls = {
            self.unauthorized_user: "/auth/signup/",
            self.unauthorized_user: "/auth/login/",
            self.authorized_user: "/auth/password_change/",
            self.authorized_user: "/auth/password_change/done/",
            self.authorized_user: "/auth/password_reset/",
            self.authorized_user: "/auth/password_reset/done/",
            self.authorized_user: f"/auth/reset/{uidb64}/{token}/",
            self.authorized_user: "/auth/reset/done/",
            self.authorized_user: "/auth/logout/",
        }

        for usertype, urls in usertype_and_urls.items():  # Act
            with self.subTest(usertype=usertype, urls=urls):
                response = usertype.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_urls_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        pswrd_reset_done_template = "users/password_reset_done.html"
        pswrd_reset_confirm_template = "users/password_reset_confirm.html"
        urls_templates_names = {
            "/auth/signup/": "users/signup.html",
            "/auth/login/": "users/login.html",
            "/auth/password_change/": "users/password_change_form.html",
            "/auth/password_change/done/": "users/password_change_done.html",
            "/auth/password_reset/": "users/password_reset_form.html",
            "/auth/password_reset/done/": pswrd_reset_done_template,
            f"/auth/reset/{uidb64}/{token}/": pswrd_reset_confirm_template,
            "/auth/reset/done/": "users/password_reset_complete.html",
            "/auth/logout/": "users/logged_out.html",
        }

        for urls, template in urls_templates_names.items():  # Act
            with self.subTest(urls=urls):
                response = self.authorized_user.get(urls)
                self.assertTemplateUsed(response, template)
