# -*- coding: utf-8 -*-

from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blog.models import Post, Category

from django.template.defaultfilters import date as _date
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import markdown

class PostTest(TestCase):
    def test_create_category(self):
        # Create the category
        category = Category()

        # Add attributes
        category.name = 'python'
        category.description = 'The Python programming language'

        # Save it
        category.save()

        # Check we can find it
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category, category)

        # Check attributes
        self.assertEquals(only_category.name, 'python')
        self.assertEquals(only_category.description, 'The Python programming language')

    def teste_create_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # cria o post
        post = Post()
        post.titulo = 'Meu primeiro post'
        post.texto = 'Este é meu primeiro post do blog'
        post.slug = "my-first-post"
        post.pub_data = timezone.now()
        post.author = author
        post.site = site
        post.category = category

        # salva o post no banco de dados
        post.save()

        # verifica se conseguimos encontrá-lo
        todos_os_posts = Post.objects.all()
        um_post = todos_os_posts[0]
        self.assertEqual(um_post, post)

        # verifica os atributos
        self.assertEqual(um_post.titulo, 'Meu primeiro post')
        self.assertEqual(um_post.texto, u'Este é meu primeiro post do blog')
        self.assertEqual(um_post.slug, 'my-first-post')
        self.assertEquals(um_post.site.name, 'example.com')
        self.assertEquals(um_post.site.domain, 'example.com')
        self.assertEqual(um_post.pub_data.day, post.pub_data.day)
        self.assertEqual(um_post.pub_data.month, post.pub_data.month)
        self.assertEqual(um_post.pub_data.year, post.pub_data.year)
        self.assertEqual(um_post.pub_data.hour, post.pub_data.hour)
        self.assertEqual(um_post.pub_data.minute, post.pub_data.minute)
        self.assertEqual(um_post.pub_data.second, post.pub_data.second)
        self.assertEquals(um_post.author.username, 'testuser')
        self.assertEquals(um_post.author.email, 'user@example.com')
        self.assertEquals(um_post.category.name, 'python')
        self.assertEquals(um_post.category.description, 'The Python programming language')

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']
    def test_create_category(self):
        # Log in
        self.client.login(username='teste2', password="teste2")

        # Check response code
        response = self.client.get('/admin/blog/category/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blog/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('adicionado com sucesso' in response.content)

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='teste2', password="teste2")

        # Edit the category
        response = self.client.post('/admin/blog/category/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('modificado com sucesso' in response.content)

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'perl')
        self.assertEquals(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='teste2', password="teste2")

        # Delete the category
        response = self.client.post('/admin/blog/category/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('excluído com sucesso' in response.content)

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)

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

    def test_create_post(self):
        # Log in
        self.client.login(username='teste2', password="teste2")

        # Check response code
        response = self.client.get('/admin/blog/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blog/post/add/', {
            'titulo': 'My first post',
            'texto': 'This is my first post',
            'pub_data_0': '2013-12-28',
            'pub_data_1': '22:00:04',
            'slug': 'my-first-post',
            'site': '1'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('adicionado com sucesso' in response.content)

        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertGreater(len(all_posts), 0)

    def test_edit_post(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.titulo = 'My first post'
        post.texto = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_data = timezone.now()
        post.author = author
        post.site = site
        post.save()

        # Log in
        self.client.login(username='teste2', password="teste2")

        # Edit the post
        response = self.client.post('/admin/blog/post/1/', {
            'titulo': 'My second post',
            'texto': 'This is my second blog post',
            'pub_data_0': '2013-12-28',
            'pub_data_1': '22:00:04',
            'slug': 'my-second-post',
            'site': '1'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('modificado com sucesso' in response.content)

        # Check post amended
        todos_os_posts = Post.objects.all()
        self.assertGreater(len(todos_os_posts), 0)
        um_post = todos_os_posts[0]
        self.assertEquals(um_post.titulo, 'My second post')
        self.assertEquals(um_post.texto, 'This is my second blog post')

    def test_delete_post(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.titulo = 'My first post'
        post.texto = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_data = timezone.now()
        post.site = site
        post.author = author
        post.save()

        # Check new post saved
        todos_os_posts = Post.objects.all()
        self.assertGreater(len(todos_os_posts), 0)

        # Log in
        self.client.login(username='teste2', password="teste2")

        # Delete the post
        response = self.client.post('/admin/blog/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('excluído com sucesso' in response.content)

        # Check post amended
        todos_os_posts = Post.objects.all()
        self.assertEquals(len(todos_os_posts), 0)

class PostViewTest(BaseAcceptanceTest):
    def test_index(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.titulo = 'My first post'
        post.texto = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_data = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        todos_os_posts = Post.objects.all()
        self.assertEquals(len(todos_os_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.titulo in response.content)

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_data.year) in response.content)
        self.assertTrue(_date(post.pub_data, "F").encode('utf-8') in response.content)
        self.assertTrue(str(post.pub_data.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_post_page(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.titulo = 'My first post'
        post.texto = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_data = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        todos_os_posts = Post.objects.all()
        self.assertEquals(len(todos_os_posts), 1)
        um_post = todos_os_posts[0]
        self.assertEquals(um_post, post)

        # Get the post URL
        post_url = um_post.get_absolute_url()

        # Fetch the post
        response = self.client.get(post_url)
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.titulo in response.content)

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.texto).encode() in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_data.year) in response.content)
        self.assertTrue(_date(post.pub_data, "F").encode('utf-8') in response.content)
        self.assertTrue(str(post.pub_data.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_category_page(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.titulo = 'My first post'
        post.texto = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_data = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the category URL
        category_url = post.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.texto).encode() in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_data.year) in response.content)
        self.assertTrue(_date(post.pub_data, "F").encode('utf-8') in response.content)
        self.assertTrue(str(post.pub_data.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEquals(only_page, page)

        # Check data correct
        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'About me')
        self.assertEquals(only_page.content, 'All about me')

        # Get URL
        page_url = only_page.get_absolute_url()

        # Get the page
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)

        # Check title and content in response
        self.assertTrue('About me' in response.content)
        self.assertTrue('All about me' in response.content)