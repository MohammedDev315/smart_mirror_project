from crypt import methods
import email
from pickletools import read_uint1
from flask import Flask
from flask_cors import CORS
from flask import Flask , jsonify , request
import psycopg2


app = Flask(__name__)
CORS(app)

# Connect to your postgres DB
# 192.168.8.188 my computer ip on network
#  port 5433 is written durange docker creation.
# dbname='postgres' is the name of database which created dureing contaner creation not a container name
conn = psycopg2.connect(" dbname='postgres' host='192.168.8.188' port=5434  user='postgres' password='pass'  ")
cur = conn.cursor()


def retrun_json_fun(status , message , data):
    return_json = {
        'request' : {
            'status' : status,
            'message' : message
        },
        'data' : data
    }
    return return_json



@app.route('/')
def hello_geek():
    tem_dic = {
        'name':'Mohammed' ,
        'level' : 2 
    }
    return tem_dic



@app.route('/show_users' , methods=['GET'])
def show_users():
    query = 'select * from users'
    cur.execute(query)
    records = cur.fetchall()
    users_list =[]
    for user in records:
        users_list.append({
            'uid' : user[0],
            'fullname' : user[1],
            'email' : user[2]
        })
    
    return jsonify(retrun_json_fun('success' , message = '' , data = users_list))


@app.route('/user_log_in' , methods=['GET'  , 'POST'])
def user_log_in():
    email = request.json['email']
    passwrod = request.json['password']

    query = "select * from users where email = %s and password = %s "
    cur.execute(query , (email , passwrod))
    records = cur.fetchone()
    print(records)
    if records != None:
        print('AAA')
        user_data = {
                'uid' : records[0],
                'fullname' : records[1],
                'email' : records[2]
        }
        return jsonify(retrun_json_fun('success' , message = '' , data = user_data))
    else:
        return jsonify(retrun_json_fun('failed' , message = 'email or password is not correct' , data = 'email or password is not correct'))
    


@app.route('/create_user' , methods=["GET" , "POST"])
def create_user():

    fullname = request.json['fullname']
    email = request.json['email']
    password = request.json['password']

    try:
        query = 'insert into users (fullname , email , password) values(%s,%s,%s)'
        cur.execute(query , (fullname , email , password) )
        conn.commit()
        return jsonify(retrun_json_fun('success' , message = 'your account has been created successfully, please login' , data = 'your account has been created successfully, please login'))
    except psycopg2.Error as e:
        error = e.pgcode
        if int(error) == 23505:
            curs = conn.cursor()
            curs.execute("ROLLBACK")
            conn.commit()
            return jsonify(retrun_json_fun('failed' , message = 'email already exists' , data = 'email already exists'))
        else:
            curs = conn.cursor()
            curs.execute("ROLLBACK")
            conn.commit()
            return jsonify(retrun_json_fun('failed' , message = 'error eamil001' , data = 'error eamil001'))


        


@app.route('/roll_back',methods=['GET'])
def rol_back():
    curs = conn.cursor()
    curs.execute("ROLLBACK")
    conn.commit()
    return 'ROLLBACK'




if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")


# # docker run -p 5434:5432 --name post_estimation_database -e POSTGRES_PASSWORD=pass -d postgres


# docker build --tag flask-post-estimation-image .
# docker run -d -p 5006:5000 --name flask-post-estimation-container flask-post-estimation-image