from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import BlogPost
from .views import generate_summary


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


class BlogListPaginationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='pagination-author',
            password='test-password',
        )
        self.url = reverse('blog:home')

    @patch('blog.views.generate_summary', return_value='Summary')
    def test_empty_blog_has_clear_empty_state(self, _summary):
        response = self.client.get(self.url)

        self.assertContains(response, 'No blog posts have been published yet.')

    @patch('blog.views.generate_summary', return_value='Summary')
    def test_blog_list_paginates_ten_posts_per_page(self, _summary):
        for number in range(11):
            BlogPost.objects.create(
                title=f'Post {number:02d}',
                content='Solar content.',
                author=self.user,
            )

        first_page = self.client.get(self.url)
        second_page = self.client.get(self.url, {'page': 2})

        self.assertEqual(len(first_page.context['blog_posts']), 10)
        self.assertEqual(len(second_page.context['blog_posts']), 1)
        self.assertContains(first_page, 'Page 1 of 2')
        self.assertContains(first_page, '?page=2')
        self.assertContains(second_page, 'Page 2 of 2')
        self.assertContains(second_page, '?page=1')


class BlogPostManagementTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username='post-owner', password='password')
        self.other_user = user_model.objects.create_user(username='post-other', password='password')
        self.staff = user_model.objects.create_user(
            username='post-staff',
            password='password',
            is_staff=True,
        )
        self.post = BlogPost.objects.create(
            title='Managed post',
            content='Managed content.',
            keywords='solar, batteries',
            author=self.owner,
        )

    def test_detail_displays_plain_text_keywords_as_badges(self):
        response = self.client.get(reverse('blog:blog_detail', args=[self.post.pk]))

        self.assertContains(response, 'solar')
        self.assertContains(response, 'batteries')

    def test_owner_can_edit_post(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('blog:edit_blog_post', args=[self.post.pk]),
            {
                'title': 'Updated post',
                'content': 'Updated content.',
                'keywords': 'updated',
            },
        )

        self.assertRedirects(response, reverse('blog:blog_detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated post')

    def test_non_owner_cannot_edit_post(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('blog:edit_blog_post', args=[self.post.pk]))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_edit_post(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse('blog:edit_blog_post', args=[self.post.pk]))

        self.assertEqual(response.status_code, 200)

    def test_owner_delete_requires_post(self):
        self.client.force_login(self.owner)
        delete_url = reverse('blog:delete_blog_post', args=[self.post.pk])

        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(BlogPost.objects.filter(pk=self.post.pk).exists())

        post_response = self.client.post(delete_url)
        self.assertRedirects(post_response, reverse('blog:home'))
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_non_owner_cannot_delete_post(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('blog:delete_blog_post', args=[self.post.pk]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_staff_can_delete_post(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse('blog:delete_blog_post', args=[self.post.pk]))

        self.assertRedirects(response, reverse('blog:home'))
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_management_controls_only_show_for_owner_or_staff(self):
        detail_url = reverse('blog:blog_detail', args=[self.post.pk])

        self.client.force_login(self.owner)
        owner_response = self.client.get(detail_url)
        self.assertContains(owner_response, 'Edit Post')
        self.assertContains(owner_response, 'Delete Post')

        self.client.force_login(self.other_user)
        other_response = self.client.get(detail_url)
        self.assertNotContains(other_response, 'Edit Post')
        self.assertNotContains(other_response, 'Delete Post')


class BlogRuntimeTests(TestCase):
    def test_summary_does_not_require_external_tokenizer_data(self):
        summary = generate_summary(
            'First sentence. Second sentence! Third sentence?',
            sentences_count=2,
        )

        self.assertEqual(summary, 'First sentence. Second sentence!')

    def test_summary_handles_text_without_terminal_punctuation(self):
        self.assertEqual(generate_summary('Solar power basics', 2), 'Solar power basics')

    def test_blog_home_rejects_post(self):
        response = self.client.post(reverse('blog:home'))

        self.assertEqual(response.status_code, 405)

    def test_blog_detail_rejects_post(self):
        user = get_user_model().objects.create_user(username='method-author', password='password')
        post = BlogPost.objects.create(title='Read only', content='Content.', author=user)

        response = self.client.post(reverse('blog:blog_detail', args=[post.pk]))

        self.assertEqual(response.status_code, 405)
