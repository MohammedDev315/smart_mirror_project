from crypt import methods
import email
from operator import le
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
conn = psycopg2.connect(" dbname='postgres' host='192.168.8.181' port=5434  user='postgres' password='pass'  ")
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
                'email' : records[2],
                'user_image_url' : records[4]  #fiveth col is user image
        }
        return jsonify(retrun_json_fun('success' , message = '' , data = user_data))
    else:
        return jsonify(retrun_json_fun('failed' , message = 'check email or password' , data = 'check email or password'))
    


@app.route('/create_user' , methods=["GET" , "POST"])
def create_user():

    fullname = request.json['fullname']
    email = request.json['email']
    password = request.json['password']
    user_image_url = request.json['user_image_url']

    try:
        query = 'insert into users (fullname , email , password , user_image_url) values(%s,%s,%s,%s)'
        cur.execute(query , (fullname , email , password , user_image_url) )
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


@app.route('/get_excercise_plan', methods=['POST'  ,  'GET'])
def get_excercise_plan():
    user_id = request.json['uid']
    query = "select * from exercise_plan where uid = %s  "
    cur.execute(query , (user_id, ))
    records = cur.fetchone()
    
    if records != None:
        exercise_plan_data = {
            'planid':records[0], 'exr1':records[1],
             'done1':records[2], 'exr2':records[3], 'done2':records[4], 'exr3':records[5],
             'done3':records[6], 'exr4':records[7], 'done4':records[8], 'uid':records[9] }

        query = "select * from exercise_details where exrid=%s or exrid=%s or exrid=%s or exrid=%s "
        cur.execute(query , (exercise_plan_data['exr1'],
                            exercise_plan_data['exr2'],
                            exercise_plan_data['exr3'],
                            exercise_plan_data['exr4'] ))
        exercise_details_records = cur.fetchall()
        
        tem_exercise_details_records = [] 
        for exr in exercise_details_records:
            tem_exercise_details_records.append({
                'exrid' : exr[0],
                'name' : exr[1],
                'image' : exr[2],
                'description' : exr[3],
                'type' : exr[4]
            })
        exercise_details_records = tem_exercise_details_records

        for detail in exercise_details_records:
            if exercise_plan_data['exr1'] == detail['exrid']:
                exercise_plan_data['exr1'] = detail
            if exercise_plan_data['exr2'] == detail['exrid']:
                exercise_plan_data['exr2'] = detail    
            if exercise_plan_data['exr3'] == detail['exrid']:
                exercise_plan_data['exr3'] = detail
            if exercise_plan_data['exr4'] == detail['exrid']:
                exercise_plan_data['exr4'] = detail



        return jsonify(retrun_json_fun('success' , message = '' , data = exercise_plan_data))
    else:
        return jsonify(retrun_json_fun('failed' , message = 'Something Wrong' , data = 'Something Wrong' ))
    


@app.route('/roll_back',methods=['GET'])
def rol_back():
    curs = conn.cursor()
    curs.execute("ROLLBACK")
    conn.commit()
    return 'ROLLBACK'




if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")


# # docker run -p 5434:5432 --name post_estimation_database -e POSTGRES_PASSWORD=pass -d postgres

# docker rm flask-post-estimation-container
# docker image rm flask-post-estimation-image
# docker build --tag flask-post-estimation-image .
# docker run -d -p 5006:5000 --name flask-post-estimation-container flask-post-estimation-image


