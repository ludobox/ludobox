from ludobox.models import db, Role

db.create_all()

# create default roles
user_role = Role(name='user')
super_user_role = Role(name='superuser')
db.session.add(user_role)
db.session.add(super_user_role)
db.session.commit()
