from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

user1 = User(first_name='Allison', last_name='Applebee')
user2 = User(first_name='Barry', last_name='Bumble')
user3 = User(first_name='Coral', last_name='Cho')

db.session.add_all([user1, user2, user3])
db.session.commit()