from app import db
from app import Posts
from app import Users
from app import Rules
from datetime import datetime
#create the database and the db tables
db.create_all()

db.session.add(Posts(title="Hello2", body="My worh should please go smooth", create_date=datetime.now()))
db.session.add(Rules(crop="Corn", advice="This an goodadvice for you", weather="temperature", weather_condition="equals to", value="21", create_date=datetime.now()))

db.session.commit()
