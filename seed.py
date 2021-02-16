from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

user1 = User(first_name='Allison', last_name='Applebee', image_url='https://cdn.pixabay.com/photo/2014/09/07/21/58/woman-438399_960_720.jpg')
user2 = User(first_name='Barry', last_name='Bumble', image_url='https://cdn.pixabay.com/photo/2015/03/03/20/42/man-657869_960_720.jpg')
user3 = User(first_name='Coral', last_name='Cho')

db.session.add_all([user1, user2, user3])
db.session.commit()

post1 = Post(title='First Post', content='This is my first post.', user_id=1)
post2 = Post(title='Second Post', content='And I did it again.', user_id=1)
post3 = Post(title='Different Post', content="I'm not Allison.", user_id=2)
post4 = Post(title='Post Again', content="I like to be different.", user_id=2)
post5 = Post(title='Third Post', content='And I made yet another.', user_id=1)

db.session.add_all([post1, post2, post3, post4, post5])
db.session.commit()