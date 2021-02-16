from unittest import TestCase

from app import app
from models import db, User

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
        """Add sample user."""

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

    def test_homepage_redirect(self):
        """Test that homepage redirects"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_homepage_follow_redirect(self):
        """Test that homepage redirects to user list"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)
            self.assertIn('Test2Last', html)

    def test_list_users(self):
        """Test that list of /users gives list of users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)
            self.assertIn('Test2Last', html)

    def test_show_user(self):
        """Test detail page for user"""
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirst TestLast</h1>', html)

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
