from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersFormTests(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()

    def test_valid_form_creates_user(self):
        """Валидная форма создает запись нового пользователя."""
        users_count = User.objects.count()
        form_data = {
            "first_name": "Firstname",
            "last_name": "Lastname",
            "username": "username",
            "email": "test_test@test.com",
            "password1": "qwsqdedfwr34343sadadf-qwe",
            "password2": "qwsqdedfwr34343sadadf-qwe",
        }

        response = self.unauthorized_user.post(  # Act
            reverse("users:signup"), data=form_data, follow=True
        )

        self.assertRedirects(response, reverse("posts:index"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name="Firstname",
                last_name="Lastname",
                username="username",
                email="test_test@test.com",
            ).exists()
        )
