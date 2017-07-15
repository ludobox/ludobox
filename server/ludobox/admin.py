#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from flask import url_for
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_security import login_required, current_user, url_for_security

from models import User, Role, db
from security import security

# Create admin
admin = Admin(
    name='Ludobox Admin Panel',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for_security('login', next=request.url))


# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))


# define a context processor for merging flask-admin's template context into the flask-security views.
# @security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
