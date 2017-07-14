from ludobox.models import db, Role
from ludobox import create_app

def create_default_roles():
    # create default roles
    user_role = Role(name='contributor')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

if __name__ == '__main__':
    db.create_all(app=create_app())
    # create_default_roles()
    print "Tables created."
