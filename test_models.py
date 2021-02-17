from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing posts and users."""
        Post.query.delete()
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        user = User(first_name="TestFirst", last_name="TestLast")
        self.assertEqual(user.full_name, "TestFirst TestLast")

class PostModelTestCase(TestCase):
    """Tests for model for Posts."""

    def setUp(self):
        """Clean up any existing users/posts."""
        Post.query.delete()
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_post_user(self):
        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()
        post = Post(title='TestTitle', content="This is a test.", user_id='1')
        db.session.add(post)
        db.session.commit()

        self.assertEqual(post.user.first_name, "TestFirst")
        self.assertEqual(post.user.full_name, "TestFirst TestLast")

    def test_pretty_time(self):
        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()
        post = Post(title='TestTitle', content="This is a test.", created_at='2020-12-12 12:12:12.343294', user_id='1')
        db.session.add(post)
        db.session.commit()

        self.assertEqual(post.pretty_datetime, 'Dec 12, 2020 12:12 PM')

class TagModelTestCase(TestCase):
    """Tests for model for Tags."""

    def setUp(self):
        """Clean up any existing posts and users."""
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_post_tag(self):
        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()
        post1 = Post(title='TestTitle1', content="This is a test.", user_id='1')
        post2 = Post(title='TestTitle2', content="This is also a test.", user_id='1')
        tag1 = Tag(name='test_tag1')
        tag2 = Tag(name='test_tag2')
        db.session.add_all([post1, post2, tag1, tag2])
        db.session.commit()
        post1.tags.append(tag1)
        tag2.posts.append(post1)
        post2.tags.append(tag2)
        db.session.commit()

        self.assertEqual(len(post1.tags), 2)
        self.assertEqual(len(post2.tags), 1)
        self.assertEqual(len(tag1.posts), 1)
        self.assertEqual(len(tag2.posts), 2)

