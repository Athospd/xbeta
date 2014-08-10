# -*- coding: utf-8 -*-

from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blog.models import Post


class PostTeste(TestCase):
    def teste_cria_post(self):
        # cria o post
        post = Post()
        post.titulo = 'Meu primeiro post'
        post.texto = 'Este é meu primeiro post do blog'
        post.pub_data = timezone.now()

        # salva o post no banco de dados
        post.save()

        # verifica se conseguimos encontrá-lo
        todos_os_posts = Post.objects.all()
        self.assertEqual(len(todos_os_posts), 1)
        um_post = todos_os_posts[0]
        self.assertEqual(um_post, post)

        # verifica os atributos
        self.assertEqual(um_post.titulo, 'Meu primeiro post')
        self.assertEqual(um_post.texto, u'Este é meu primeiro post do blog')
        self.assertEqual(um_post.pub_data.day, post.pub_data.day)
        self.assertEqual(um_post.pub_data.month, post.pub_data.month)
        self.assertEqual(um_post.pub_data.year, post.pub_data.year)
        self.assertEqual(um_post.pub_data.hour, post.pub_data.hour)
        self.assertEqual(um_post.pub_data.minute, post.pub_data.minute)
        self.assertEqual(um_post.pub_data.second, post.pub_data.second)

class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Usuário:' in response.content)

        # Log the user in
        self.client.login(username="teste2", password="teste2")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Encerrar sessão' in response.content)

    def test_logout(self):
        # Log in
        self.client.login(username="teste2", password="teste2")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Encerrar sessão' in response.content)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Usuário:' in response.content)
