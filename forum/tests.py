from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Response, Thread


class ForumResponseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='forum-user',
            password='test-password',
        )
        self.category = Category.objects.create(name='General Solar')
        self.thread = Thread.objects.create(
            category=self.category,
            title='Battery sizing',
            content='How should I size my battery bank?',
            author=self.user,
        )

    def test_create_response_requires_login(self):
        response = self.client.get(
            reverse('forum:create_response', args=[self.thread.id]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_create_response_creates_response_for_thread(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('forum:create_response', args=[self.thread.id]),
            {'content': 'Start with your expected daily energy use.'},
        )

        self.assertRedirects(
            response,
            reverse('forum:view_thread', args=[self.thread.id]),
        )
        saved_response = Response.objects.get()
        self.assertEqual(saved_response.thread, self.thread)
        self.assertEqual(saved_response.author, self.user)
        self.assertEqual(
            saved_response.content,
            'Start with your expected daily energy use.',
        )

    def test_invalid_response_is_not_created(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('forum:create_response', args=[self.thread.id]),
            {'content': ''},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Response.objects.count(), 0)
        self.assertTrue(response.context['form'].errors)


class ForumThreadTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='thread-user',
            password='test-password',
        )
        self.category = Category.objects.create(name='RV Solar')

    def test_create_thread_requires_login(self):
        response = self.client.get(reverse('forum:create_thread'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_authenticated_user_can_create_thread(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('forum:create_thread'),
            {
                'title': 'Panel expansion',
                'content': 'Can I add another panel?',
                'category': self.category.id,
            },
        )

        thread = Thread.objects.get()
        self.assertEqual(thread.author, self.user)
        self.assertEqual(thread.category, self.category)
        self.assertRedirects(
            response,
            reverse('forum:view_thread', args=[thread.id]),
        )
