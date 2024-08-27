from flask import Blueprint, render_template, request, redirect, url_for, flash
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
            flash('Email ou senha incorretos.', 'error')
            return redirect(url_for('login.login'))
    
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
            flash('As senhas devem ser iguais', 'error')
            return redirect(url_for('login.createAccount'))
        
        userNomeExist = db.session.query(User).filter_by(userNome=userNome).first()
        if userNomeExist:
            flash('Nome em uso', 'error')
            return redirect(url_for('login.createAccount'))
        
        userEmailExist = db.session.query(User).filter_by(userEmail=userEmail).first()
        if userEmailExist:
            flash('Email em uso', 'error')
            return redirect(url_for('login.createAccount'))

        newUser = User(
            userNome = userNome,
            userEmail = userEmail,
            userSenha = userSenha
        )

        db.session.add(newUser)
        db.session.commit()
        flash('Conta criada com sucesso', 'success')

        login_user(newUser)
    return redirect(url_for('login.login'))


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))