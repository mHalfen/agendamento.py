from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db
from models import User

login_bp = Blueprint('login', __name__)

lm = LoginManager()

@lm.user_loader
def userLoader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user


@login_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        userEmail = request.form['userEmailForm']
        userSenha = request.form['userSenhaForm']

        user = db.session.query(User).filter_by(userEmail=userEmail, userSenha=userSenha).first()

        if not user:
            return 'Email ou senha incorretos.'
    
        login_user(user)
        return redirect(url_for('home.home'))


@login_bp.route('/login/createAccount', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'GET':
        return render_template('login_createAccount.html')
    
    elif request.method == 'POST':
        userNome = request.form['userNomeForm']
        userEmail = request.form['userEmailForm']
        userSenha = request.form['userSenhaForm']
        userSenhaConfirm = request.form['userSenhaConfirmForm']

        if userSenha != userSenhaConfirm:
            return 'As senhas devem ser iguals.'

        newUser = User(
            userNome = userNome,
            userEmail = userEmail,
            userSenha = userSenha
        )

        db.session.add(newUser)
        db.session.commit()

        login_user(newUser)
    return redirect(url_for('login.login'))


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))