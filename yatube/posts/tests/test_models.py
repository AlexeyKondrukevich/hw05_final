from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая группа",
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        models = {
            self.group: self.group.title,
            self.post: self.post.text[:15],
        }

        for model, method in models.items():  # Act
            with self.subTest(method=method, model=model):
                self.assertEqual(method, str(model))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым в Post."""
        post = self.post
        field_verboses = {
            "text": "Содержание",
            "pub_date": "Дата публикации",
            "author": "Автор",
            "group": "Группа",
        }

        for field, expected_value in field_verboses.items():  # Act
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым в Post."""
        post = self.post
        field_help_texts = {
            "text": "Введите текст поста",
            "group": "Выберите группу",
        }

        for field, expected_value in field_help_texts.items():  # Act
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
