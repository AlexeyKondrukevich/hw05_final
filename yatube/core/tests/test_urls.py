from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()

    def test_unexisting_page_uses_correct_template(self):
        response = self.unauthorized_user.get("/unexisting_page/")  # Act

        self.assertTemplateUsed(response, "core/404.html")
