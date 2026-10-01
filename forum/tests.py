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
        response = self.client.post(
            reverse('forum:create_response', args=[self.thread.id]),
            {'content': 'Anonymous reply'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_create_response_rejects_get(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('forum:create_response', args=[self.thread.id]),
        )

        self.assertEqual(response.status_code, 405)

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

    def test_anonymous_visitors_are_prompted_to_log_in(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'Log in')
        self.assertNotContains(response, 'Submit Response')

    def test_authenticated_visitors_see_reply_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, 'Submit Response')

    def test_thread_detail_post_does_not_create_reply(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {'content': 'Wrong endpoint'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Response.objects.count(), 0)


class ForumContentEscapingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='escape-user',
            password='test-password',
        )
        category = Category.objects.create(name='Safety')
        self.thread = Thread.objects.create(
            category=category,
            title='Markup test',
            content='<script>alert("thread")</script>\nSecond line',
            author=self.user,
        )
        Response.objects.create(
            thread=self.thread,
            author=self.user,
            content='<img src=x onerror=alert("reply")>\nReply line',
        )

    def test_thread_content_is_escaped_but_line_breaks_are_preserved(self):
        response = self.client.get(
            reverse('forum:view_thread', args=[self.thread.id]),
        )

        self.assertContains(
            response,
            '&lt;script&gt;alert(&quot;thread&quot;)&lt;/script&gt;',
        )
        self.assertNotContains(response, '<script>alert("thread")</script>')
        self.assertContains(response, '<br>Second line')

    def test_response_content_is_escaped(self):
        response = self.client.get(
            reverse('forum:view_thread', args=[self.thread.id]),
        )

        self.assertContains(
            response,
            '&lt;img src=x onerror=alert(&quot;reply&quot;)&gt;',
        )
        self.assertNotContains(response, '<img src=x onerror=alert("reply")>')


class ForumThreadManagementTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username='owner', password='password')
        self.other_user = user_model.objects.create_user(username='other', password='password')
        self.staff = user_model.objects.create_user(
            username='moderator',
            password='password',
            is_staff=True,
        )
        self.category = Category.objects.create(name='Ownership')
        self.thread = Thread.objects.create(
            category=self.category,
            title='Original title',
            content='Original content',
            author=self.owner,
        )

    def test_owner_can_edit_thread(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('forum:edit_thread', args=[self.thread.id]),
            {
                'title': 'Updated title',
                'content': 'Updated content',
                'category': self.category.id,
            },
        )

        self.assertRedirects(
            response,
            reverse('forum:view_thread', args=[self.thread.id]),
        )
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'Updated title')

    def test_non_owner_cannot_edit_thread(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('forum:edit_thread', args=[self.thread.id]))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_edit_thread(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse('forum:edit_thread', args=[self.thread.id]))

        self.assertEqual(response.status_code, 200)

    def test_delete_requires_post_and_owner_can_delete(self):
        self.client.force_login(self.owner)

        get_response = self.client.get(reverse('forum:delete_thread', args=[self.thread.id]))
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(Thread.objects.filter(pk=self.thread.id).exists())

        post_response = self.client.post(reverse('forum:delete_thread', args=[self.thread.id]))
        self.assertRedirects(post_response, reverse('forum:thread_list'))
        self.assertFalse(Thread.objects.filter(pk=self.thread.id).exists())

    def test_non_owner_cannot_delete_thread(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('forum:delete_thread', args=[self.thread.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Thread.objects.filter(pk=self.thread.id).exists())

    def test_staff_can_delete_thread(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse('forum:delete_thread', args=[self.thread.id]))

        self.assertRedirects(response, reverse('forum:thread_list'))
        self.assertFalse(Thread.objects.filter(pk=self.thread.id).exists())

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('forum:edit_thread', args=[self.thread.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_management_controls_only_show_for_owner_or_staff(self):
        detail_url = reverse('forum:view_thread', args=[self.thread.id])

        self.client.force_login(self.owner)
        owner_response = self.client.get(detail_url)
        self.assertContains(owner_response, 'Edit Thread')
        self.assertContains(owner_response, 'Delete Thread')

        self.client.force_login(self.other_user)
        other_response = self.client.get(detail_url)
        self.assertNotContains(other_response, 'Edit Thread')
        self.assertNotContains(other_response, 'Delete Thread')


class ForumResponseManagementTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username='reply-owner', password='password')
        self.other_user = user_model.objects.create_user(username='reply-other', password='password')
        self.staff = user_model.objects.create_user(
            username='reply-moderator',
            password='password',
            is_staff=True,
        )
        category = Category.objects.create(name='Response ownership')
        self.thread = Thread.objects.create(
            category=category,
            title='Response permissions',
            content='Testing response ownership.',
            author=self.owner,
        )
        self.response = Response.objects.create(
            thread=self.thread,
            author=self.owner,
            content='Original response',
        )
        self.thread_url = reverse('forum:view_thread', args=[self.thread.id])

    def test_owner_can_edit_response(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse('forum:edit_response', args=[self.response.id]), {'content': 'Updated response'})

        self.assertRedirects(response, self.thread_url)
        self.response.refresh_from_db()
        self.assertEqual(self.response.content, 'Updated response')

    def test_non_owner_cannot_edit_response(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('forum:edit_response', args=[self.response.id]))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_edit_response(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse('forum:edit_response', args=[self.response.id]))

        self.assertEqual(response.status_code, 200)

    def test_owner_delete_requires_post(self):
        self.client.force_login(self.owner)

        get_response = self.client.get(reverse('forum:delete_response', args=[self.response.id]))
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(Response.objects.filter(pk=self.response.id).exists())

        post_response = self.client.post(reverse('forum:delete_response', args=[self.response.id]))
        self.assertRedirects(post_response, self.thread_url)
        self.assertFalse(Response.objects.filter(pk=self.response.id).exists())

    def test_non_owner_cannot_delete_response(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('forum:delete_response', args=[self.response.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Response.objects.filter(pk=self.response.id).exists())

    def test_staff_can_delete_response(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse('forum:delete_response', args=[self.response.id]))

        self.assertRedirects(response, self.thread_url)
        self.assertFalse(Response.objects.filter(pk=self.response.id).exists())

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('forum:edit_response', args=[self.response.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_response_controls_only_show_for_owner_or_staff(self):
        self.client.force_login(self.owner)
        owner_response = self.client.get(self.thread_url)
        self.assertContains(owner_response, 'Edit Response')
        self.assertContains(owner_response, 'Delete Response')

        self.client.force_login(self.other_user)
        other_response = self.client.get(self.thread_url)
        self.assertNotContains(other_response, 'Edit Response')
        self.assertNotContains(other_response, 'Delete Response')


class ForumThreadListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='list-user',
            password='password',
        )
        self.category = Category.objects.create(name='Forum index')
        self.url = reverse('forum:thread_list')

    def test_empty_forum_has_clear_empty_state(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'No forum threads have been posted yet.')
        self.assertContains(response, 'Log in')
        self.assertNotContains(response, 'Create New Thread')

    def test_authenticated_empty_forum_offers_create_thread(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, 'Create New Thread')

    def test_thread_list_uses_annotated_response_count(self):
        thread = Thread.objects.create(
            category=self.category,
            title='Counted thread',
            content='Count replies without per-row count queries.',
            author=self.user,
        )
        Response.objects.create(thread=thread, author=self.user, content='One')
        Response.objects.create(thread=thread, author=self.user, content='Two')

        response = self.client.get(self.url)

        self.assertContains(response, 'Counted thread')
        self.assertContains(response, self.category.name)
        self.assertContains(response, '<td>2</td>', html=True)

    def test_thread_list_paginates_twenty_threads_per_page(self):
        for number in range(21):
            Thread.objects.create(
                category=self.category,
                title=f'Thread {number:02d}',
                content='Pagination test',
                author=self.user,
            )

        first_page = self.client.get(self.url)
        second_page = self.client.get(self.url, {'page': 2})

        self.assertEqual(len(first_page.context['page_obj']), 20)
        self.assertEqual(len(second_page.context['page_obj']), 1)
        self.assertContains(first_page, 'Page 1 of 2')
        self.assertContains(second_page, 'Page 2 of 2')
