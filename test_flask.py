from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Setup below copied from demo code
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample users."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast")
        user2 = User(first_name="Test2First", last_name="Test2Last")
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test that list of /users gives list of users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)
            self.assertIn('Test2Last', html)

    def test_show_user(self):
        """Test detail page for user with no posts"""
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirst TestLast</h1>', html)
            self.assertIn('<li>TestFirst TestLast has not posted anything yet</li>', html)

    def test_new_user_post(self):
        """Test post new user info"""
        with app.test_client() as client:
            resp = client.post('users/new', 
                               data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'image_url': ''})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_new_user_follow_redirect(self):
        """Test post new user info"""
        with app.test_client() as client:
            resp = client.post('users/new', 
                               data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'image_url': ''},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>NewFirst NewLast</h1>', html)

    def test_delete_user(self):
        """Test deletion of user"""
        with app.test_client() as client:
            resp = client.post(f'users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('TestFirst', html)
            self.assertIn('Test2Last', html)

class PostViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample posts."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()

        post1 = Post(title='Test1', content='Test content 1.', user_id=user.id)
        post2 = Post(title='Test2', content='Test content 2.', user_id=user.id)
        tag = Tag(name='silly tag')
        db.session.add_all([post1, post2, tag])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        """Test that homepage redirects"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)
            self.assertIn('Test content 2.', html)
    def test_user_detail(self):
        """Test that users detail gives list of posts"""
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/posts/1">Test1</a>', html)
            self.assertIn('<a href="/posts/2">Test2</a>', html)

    def test_show_post(self):
        """Test detail page for post"""
        with app.test_client() as client:
            resp = client.get("posts/2")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test2</h1>', html)
            self.assertIn('<p>Test content 2.</p>', html)

    def test_new_post_form(self):
        """Test new post form shows tag option"""
        with app.test_client() as client:
            resp = client.get('/users/1/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('silly tag', html)

    def test_new_post_post(self):
        """Test post new post"""
        with app.test_client() as client:
            resp = client.post('users/1/posts/new', 
                               data={'title': 'NewTitle', 'content': 'This is new.'})

            self.assertEqual(resp.status_code, 302)

    def test_new_post_follow_redirect(self):
        """Test post new post, follow redirect"""
        with app.test_client() as client:
            resp = client.post('users/1/posts/new', 
                               data={'title': 'NewTitle', 'content': 'This is new.'},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/posts/3">NewTitle</a>', html)

    def test_delete_post(self):
        """Test deletion of post"""
        with app.test_client() as client:
            resp = client.post(f'posts/2/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test2', html)
            self.assertIn('<a href="/posts/1">Test1</a>', html)

class TagViewsTestsCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add sample posts."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()

        post1 = Post(title='Test1', content='Test content 1.', user_id=user.id)
        post2 = Post(title='Test2', content='Test content 2.', user_id=user.id)
        tag = Tag(name='silly tag')
        db.session.add_all([post1, post2, tag])
        db.session.commit()

        post1.tags.append(tag)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_tag(self):
        """Test detail page for post"""
        with app.test_client() as client:
            resp = client.get("tags/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>silly tag</h1>', html)
            self.assertIn('<a href="/posts/1">Test1</a>', html)
            self.assertNotIn('Test2', html)

    def test_new_tag_form(self):
        """Test new tag form shows posts titles"""
        with app.test_client() as client:
            resp = client.get('/tags/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test1', html)
            self.assertIn('Test2', html)

    def test_new_tag_post(self):
        """Test add new tag"""
        with app.test_client() as client:
            resp = client.post('tags/new', 
                               data={'name': 'new tag'})

            self.assertEqual(resp.status_code, 302)

    def test_new_tag_follow_redirect(self):
        """Test post new tag, follow redirect"""
        with app.test_client() as client:
            resp = client.post('tags/new', 
                               data={'name': 'new tag'},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/tags/2">new tag</a></li>', html)
            self.assertIn('<h1>Tags</h1>', html)

    def test_delete_tag(self):
        """Test deletion of post"""
        with app.test_client() as client:
            resp = client.post(f'tags/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('silly tag', html)
            self.assertIn('<h1>Tags</h1>', html)