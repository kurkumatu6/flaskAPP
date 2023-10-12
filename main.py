from flask import Flask, render_template, url_for, request, redirect,flash, get_flashed_messages, session
from dbController import *
from random import choice, randint
import string
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = "asiopdfjoiaspdoifjapsoid"
menu = [ {"name":"Главная","url": "/"},{"name":"Вход","url": "/log"}, {"name":"Регистрация","url": "/reg"}]

link_types = ['Публичная','Общего доступа','Приватная']
linkTypes = getAllLinkTypes()





def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route("/")
def index():
    menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"}, {"name": f"{session.get('user')}", "url": "/profile"}]
    return render_template('index.html',linkTypes = linkTypes, menu=menu, menuauth= menuauth)

@app.route("/linksChange", methods = ["POST"])
def linksChange():
    if request.method == "POST":
        url = request.form["link"]
        castom_url = request.form.get('nickname', None)
        linkType = request.form["link_type"]

        if castom_url != None :
            if( serchLinkForName(castom_url) != None):
                flash("Введите другой псевдоним", category="error")
                return redirect("/", code=302)
        else:
            castom_url = generate_short_id(randint(8, 13))

        if url == "":
            flash("Вы не ввели ссылку для сокращения", category="error")
            return redirect("/", code=302)
        login = session.get("user")

        if login == None:
            rez = createLink(url, castom_url, 'NULL', linkType)
            if rez:
                short_url = request.host_url + castom_url
                flash(short_url, category="url")
        else:
            user_id = serchUser(login)
            rez = createLink(url, castom_url, user_id, linkType)
            if rez:
                short_url = request.host_url + castom_url
                flash(short_url, category="url")



        return redirect("/", code=302)

@app.route('/<short_id>')
def redirect_url(short_id):
    link = serchLink(short_id)
    if link != None:
        if link[1] == link_types[0]:
            updateCountOnLink(short_id)
            return redirect(link[0])

        if link[1] == link_types[1]:

            if session.get('auth') == None:
                session['short_id'] = short_id
                return redirect(f"/log/general/{short_id}", code=302)

            updateCountOnLink(short_id)
            return redirect(link[0])

        if link[1] == link_types[2]:

            if session.get('auth') == None:
                session['short_id'] = short_id
                return redirect(f"/log/general/{short_id}", code=302)

            login = session.get("user")
            user_id = serchUser(login)
            if user_id[0] != link[2]:
                session['short_id'] = short_id
                return redirect(f"/log/general/{short_id}", code=302)

            updateCountOnLink(short_id)
            return redirect(link[0])


    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route('/log/general/<short_id>')
def redirect_general_url(short_id):
    link = serchLink(short_id)
    if link != None:

        if link[1] == link_types[1]:

            if session.get('auth') == None:
                menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"},
                            {"name": f"{session.get('user')}", "url": "/profile"}]
                return render_template('logCH.html', menu=menu, menuauth=menuauth)
        if link[1] == link_types[2]:

            if session.get('auth') == None:
                menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"},
                            {"name": f"{session.get('user')}", "url": "/profile"}]
                return render_template('logCH.html', menu=menu, menuauth=menuauth)

            login = session.get("user")
            user_id = serchUser(login)
            if user_id[0] != link[2]:
                menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"},
                            {"name": f"{session.get('user')}", "url": "/profile"}]
                return render_template('logCH.html', menu=menu, menuauth=menuauth)


    else:
        flash('Invalid URL')
        return redirect(url_for('index'))
    return redirect("/", code=302)


@app.route("/log")
def login():
    # if request.method == "POST":
    #     print(request.form)
    menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"}, {"name": f"{session.get('user')}", "url": "/profile"}]
    return render_template('log.html', menu=menu, menuauth= menuauth)

@app.route("/log/obr", methods = ["POST"])
def loginOBR():
    if request.method == "POST":
        user = authUser(request.form['login'], request.form['password'])
        if(user):
            session["auth"] = True
            session["user"] = user
            return redirect("/", code=302)
        else:
            flash("Неверные логин или пароль")
            return redirect("/log", code=302)


@app.route("/log/obrCH", methods = ["POST"])
def loginOBRCH():
    if request.method == "POST":
        link = serchLink(session.get('short_id'))
        if link[1] == link_types[1]:
            user = authUser(request.form['login'], request.form['password'])
            if(user):
                session["auth"] = True
                session["user"] = user
                return redirect(f"/{session.get('short_id')}", code=302)
            else:
                flash("Неверные логин или пароль")
                return redirect(f"general/{session.get('short_id')}", code=302)
        if link[1] == link_types[2]:
            user = authUser(request.form['login'], request.form['password'])
            if(user):
                session["auth"] = True
                session["user"] = user
                user_id =serchUser(user)
                if(user_id[0] == link[2]):
                    return redirect(f"/{session.get('short_id')}", code=302)
                else:
                    flash("Вы не являетесь хозяином приватной ссылки")
                    return redirect(f"general/{session.get('short_id')}", code=302)
            else:
                flash("Неверные логин или пароль")
                return redirect(f"general/{session.get('short_id')}", code=302)
        return redirect("/", code=302)





@app.route("/reg")
def reg():

    menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"}, {"name": f"{session.get('user')}", "url": "/profile"}]
    return render_template('reg.html',menu=menu, menuauth= menuauth)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", code=302)

@app.route("/reg/obr", methods = ["POST"])
def regOBR():
    if request.method == "POST":
        if(request.form["password"] != request.form["password_confirmation"]):
            flash("Пароли не совподают")
            return redirect("/reg", code=302)
        else:
            user = addUser(request.form["login"], request.form["password"])
            if(user):
                session["auth"] = True
                session["user"] = user
                return redirect("/", code=302)
            else:
                flash("Пользователь с таким логином уже зарегистрирован")
                return redirect("/reg", code=302)

    return redirect("/reg", code=302)

@app.route("/profile")
def profile():
    if not session.get("auth"):
        return redirect("/", code=302)

    menuauth = [{"name": "Главная", "url": "/"}, {"name": "Выход", "url": "/logout"}, {"name": f"{session.get('user')}", "url": "/profile"}]

    user_id = serchUser(session.get("user"))
    userLinks =  getAllUserLinks(user_id[0])

    host_url =request.host_url


    return render_template('profile.html',linkTypes = linkTypes, menu=menu, menuauth= menuauth, userLinks= userLinks, host_url= host_url)


@app.route("/changeLinkType", methods = ["POST"])
def changeLinkType():
    if request.method == "POST":
        data = json.loads(request.data)
        type = int(data['type'])
        id = int(data['id'])
        changeLinkTypeInDB( id, type)
        return ''
    else:
        return redirect("/", code=302)

@app.route("/delLink", methods = ["POST"])
def delLink():
    if request.method == "POST":
        data = json.loads(request.data)
        id = int(data['id'])
        delLinkInDB(id)
        user_id = serchUser(session.get('user'))
        links = getAllUserLinks(user_id[0])
        return json.dumps(links)
    else:
        return redirect("/", code=302)

@app.route("/getlinkTypes", methods = ["POST"])
def getlinkTypes():
    if request.method == "POST":
        return json.dumps(linkTypes)
    else:
        return redirect("/", code=302)

@app.route("/gethostname", methods = ["POST"])
def gethostname():
    if request.method == "POST":
        host_url = request.host_url
        return json.dumps(host_url)
    else:
        return redirect("/", code=302)

@app.route("/getLinkName", methods = ["POST"])
def getLinkName():
    if request.method == "POST":
        data = json.loads(request.data)
        id = int(data['id'])
        link = serchLinkById(id)
        return json.dumps(link[0])
    else:
        return redirect("/", code=302)



@app.route("/changeLinkNickName", methods = ["POST"])
def changeLinkNickName():
    if request.method == "POST":
        print(request.form)
        castom_url = request.form["nickName"]
        id = request.form["id"]
        if (serchLinkForName(castom_url) != None):
            flash("Введите другой псевдоним", category="error")
            return redirect("/profile", code=302)

        print(changeLinknickname(id, castom_url))
        return redirect("/profile", code=302)

if __name__ == "__main__":
    app.run(debug=True)


