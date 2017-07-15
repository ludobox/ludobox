#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ludobox.models import db
from ludobox import create_app

def confirm_choice():
    confirm = raw_input("Are you sure you want to erase all data ? : Yes or No [y/n] ?")
    if confirm != 'y' and confirm != 'n':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()
    elif confirm == 'y' :
        return True
    elif confirm == 'n' :
        return False

if __name__ == '__main__':
    if confirm_choice():
        app=create_app()
        with app.app_context():
            db.drop_all()
        print "Tables dropped."
