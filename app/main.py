from flask import render_template, request, redirect, session, jsonify
import dao
from app import app, login
from flask_login import login_user







@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=False)
