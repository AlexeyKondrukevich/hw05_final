from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()
uidb64 = "Mw"
token = "5xr-9713b923abcdd5a56637"


class UsersPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_users_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            "users/signup.html": reverse("users:signup"),
            "users/password_change_form.html": reverse(
                "users:password_change"
            ),
            "users/password_change_done.html": reverse(
                "users:password_change_done"
            ),
            "users/password_reset_form.html": reverse("users:password_reset"),
            "users/password_reset_done.html": reverse(
                "users:password_reset_done"
            ),
            "users/password_reset_confirm.html": reverse(
                "users:password_reset_confirm",
                kwargs={"uidb64": uidb64, "token": token},
            ),
            "users/password_reset_complete.html": reverse(
                "users:password_reset_complete"
            ),
            "users/logged_out.html": reverse("users:logout"),
            "users/login.html": reverse("users:login"),
        }

        for template, reverse_name in templates_pages_names.items():  # Act
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)
