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


class ForumThreadDetailReplyTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='detail-user',
            password='test-password',
        )
        category = Category.objects.create(name='Off-grid')
        self.thread = Thread.objects.create(
            category=category,
            title='Inverter advice',
            content='Which inverter should I use?',
            author=self.user,
        )
        self.url = reverse('forum:view_thread', args=[self.thread.id])

    def test_anonymous_visitors_can_read_threads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inverter advice')

    def test_anonymous_post_redirects_to_login_without_creating_reply(self):
        response = self.client.post(
            self.url,
            {'content': 'Unauthenticated reply'},
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
            fetch_redirect_response=False,
        )
        self.assertEqual(Response.objects.count(), 0)

    def test_authenticated_post_creates_reply(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {'content': 'Use the simultaneous load and surge ratings.'},
        )

        self.assertRedirects(response, self.url)
        self.assertEqual(Response.objects.count(), 1)
        self.assertEqual(Response.objects.get().author, self.user)

    def test_invalid_authenticated_post_preserves_errors(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {'content': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Response.objects.count(), 0)
