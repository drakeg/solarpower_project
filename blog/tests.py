from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import BlogPost


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='blog-author',
            password='test-password',
        )
        self.post = BlogPost.objects.create(
            title='Solar basics',
            content='First sentence. Second sentence. Third sentence.',
            keywords='solar, basics',
            author=self.user,
        )

    @patch('blog.views.generate_summary', return_value='First sentence. Second sentence.')
    def test_home_lists_posts_with_summary_and_keywords(self, _summary):
        response = self.client.get(reverse('blog:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        listed_post = response.context['blog_posts'].object_list[0]
        self.assertEqual(listed_post.summary, 'First sentence. Second sentence.')
        self.assertEqual(listed_post.keywords_list, ['solar', 'basics'])

    def test_blog_detail_displays_post(self):
        response = self.client.get(
            reverse('blog:blog_detail', args=[self.post.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog_post'], self.post)

    def test_create_blog_post_requires_login(self):
        response = self.client.get(reverse('blog:create_blog_post'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_authenticated_user_can_create_blog_post(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('blog:create_blog_post'),
            {
                'title': 'New solar post',
                'content': 'Useful solar content.',
                'keywords': 'solar, testing',
            },
        )

        created = BlogPost.objects.get(title='New solar post')
        self.assertEqual(created.author, self.user)
        self.assertRedirects(
            response,
            reverse('blog:blog_detail', args=[created.pk]),
        )
