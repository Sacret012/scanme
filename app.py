from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from utils.dbHelper import get_login, register_user, get_user_nickname

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-own-jwt-secret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'auth'
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1000)
jwt = JWTManager(app)

FLAG = 'fake flag stolen. Try something similar on the production server'
@app.route('/')
@jwt_required(optional=True)
def index():
  try:
    current_user = get_jwt_identity()
    if current_user is None:
      return(redirect(url_for('login')))
    login = current_user['login']
    print(login)
    return render_template('index.html', name= get_user_nickname(login))
  except Exception as e:
    return "Ошибка на сервере :("

@app.route('/check-promocode', methods=['POST'])
@jwt_required()
def check_promocode():
  try:
    promocode = request.json['promocode']
    #на проде промокоды другие, в тестовой бдшке лежит только этот
    # Проверить промокод в базе данных
    if promocode == 'TEST_PROMO':
      message = FLAG
    else:
      message = 'Увы, но вы ничего не выиграли. Купите у нас еще много пельменей и тогда победа будет у вас в руках'

    return jsonify({'message': message})
  except Exception as e:
    return jsonify({'message': "Возникла проблема с проверкой промокода. Попробуйте позже. А пока купите у нас еще пельменей"})

@app.route('/register', methods=['GET', 'POST'])
@jwt_required(optional=True)
def register():
  try:
    current_user = get_jwt_identity()
    if current_user is None:
      if request.method == 'GET':
        return render_template('register.html')
      login = request.form.get('login')
      name = request.form.get('name')
      password = request.form.get('password')
      if (login == None or name == None or password == None):
        return redirect(url_for('register'))
      if (register_user(login, name, password)):
        return (redirect(url_for('login')))
      else:
        return (redirect(url_for('register')))
    else:
      return redirect(url_for('index'))
  except Exception as e:
    return "Проблема с регистрацией :("
   

@app.route('/login', methods=['GET', 'POST'])
@jwt_required(optional=True)
def login():
    try:
      current_user = get_jwt_identity()
      if current_user is None:
        if request.method == 'GET':
          return render_template('login.html')
      
        login = request.form.get('login')
        password = request.form.get('password')
  
        if get_login(login, password):
            new_token = create_access_token(identity={'login': login})
            response = make_response(redirect(url_for('index')))
            response.set_cookie('auth', new_token)
            return response
        else:
          return 'Invalid login or password', 401
      else:
         return redirect(url_for('index'))
    except Exception as e:
       return "error"
    
@app.route('/logout')
def logout():
  response = make_response(redirect(url_for('login')))
  response.set_cookie('auth', "")
  return response


if __name__ == '__main__':
    app.run()
