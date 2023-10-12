import sqlite3
import uuid
import hashlib
# подключение к базе данных
connect = sqlite3.connect("db.db")
cursor = connect.cursor()
# создание таблиц базы данных и связей
cursor.execute('''
CREATE TABLE IF NOT EXISTS  "users" (
	"id"	INTEGER,
	"login"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')

cursor.execute('''
 CREATE TABLE IF NOT EXISTS "links_types" (
	"id"	INTEGER,
	"type"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS "links" (
	"id"	INTEGER,
	"url"	INTEGER,
	"link"	TEXT,
	"user_id"	INTEGER,
	"link_type_id"	INTEGER,	
	"count"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
    FOREIGN KEY (user_id)  REFERENCES users (id),
    FOREIGN KEY (link_type_id)  REFERENCES links_types (id)
);
''')
connect.commit()
link_typesDB = ['Публичная','Общего доступа','Приватная']
for i in link_typesDB:
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    link_typ = cursor.execute("SELECT * FROM links_types WHERE type = ?", (i,)).fetchone()
    if link_typ == None:
        cursor.execute("INSERT INTO links_types (id, type) VAlUES (NULL, ?)", (i,))
        connect.commit()
def addUser(login, password):
    # try:
        print(password)
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        user = cursor.execute("SELECT * FROM users WHERE login = ?",(login,)).fetchone()
        if(user == None):
            salt = uuid.uuid4().hex
            key = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
            cursor.execute("INSERT INTO users (id, login, password) VAlUES (NULL, ?, ?)",(login, key))
            connect.commit()
            return login
        else:
            return False
    # except:
    #     return "Что то пошло не так"
    # finally:
    #     connect.close()

def authUser(login, password):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        user = cursor.execute("SELECT * FROM users WHERE login = ?",(login,)).fetchone()
        if(user == None):
            return False
        else:
            if check_password(user[2], password):
                return login
            else:
                return False
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def getAllLinkTypes():
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        return cursor.execute("SELECT * FROM links_types").fetchall()
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def serchLinkForName(linkName):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        temp = cursor.execute("SELECT * FROM links WHERE link = ?", (linkName,)).fetchone()
        return temp
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def createLink(url, link, user_id, link_type_id):
    try:
        print("aaaaaaaa")
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO links (id, url, link, user_id, link_type_id, count) VALUES (NULL, ?, ?, ?, ?, 0)", (url, link, user_id[0], link_type_id))
        print("aaaaaaaa")
        connect.commit()
        return True
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def changeLinknickname(id,nickname):
    try:

        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE links SET link = ? WHERE id = ?", (nickname,id))
        connect.commit()
        print("aaaaaaaa")

        return True
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def serchUser(login):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        user = cursor.execute("SELECT id FROM users WHERE login = ?", (login,)).fetchone()
        return user
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def serchLink(link):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        resLink = cursor.execute("SELECT url, links_types.type, user_id FROM links INNER JOIN links_types ON links_types.id = links.link_type_id WHERE link = ?", (link,)).fetchone()

        return resLink
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def serchLinkById(id):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        resLink = cursor.execute("SELECT link FROM links WHERE id = ?", (id,)).fetchone()

        return resLink
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def updateCountOnLink(link):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE links SET count = count+1 WHERE link = ?", (link, ))
        connect.commit()
        return True
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def getAllUserLinks(user_id):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        return cursor.execute("SELECT * FROM links WHERE user_id = ?", (user_id, )).fetchall()
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def changeLinkTypeInDB(id, type):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE links SET link_type_id = ? WHERE id = ?", (type, id))
        connect.commit()
        return True
    except:
        return "Что то пошло не так"
    finally:
        connect.close()

def delLinkInDB(id):
    try:
        connect = sqlite3.connect("db.db")
        cursor = connect.cursor()
        cursor.execute("DELETE FROM links WHERE id = ?", (id,))
        connect.commit()
        return True
    except:
        return "Что то пошло не так"
    finally:
        connect.close()