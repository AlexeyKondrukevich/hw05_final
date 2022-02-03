from http import HTTPStatus

from django.test import Client, TestCase


class URLSTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_and_tech_pages(self):
        adresses = ["/about/author/", "/about/tech/"]

        for adress in adresses:  # Act
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_urls_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/about/author/": "about/author.html",
            "/about/tech/": "about/tech.html",
        }

        for address, template in templates_url_names.items():  # Act
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
