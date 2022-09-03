from crypt import methods
from flask import Flask
from flask_cors import CORS
from flask import Flask , jsonify , request
import psycopg2


app = Flask(__name__)
CORS(app)

# Connect to your postgres DB
# 192.168.8.188 my computer ip on network
#  port 5433 is written durange docker creation.
conn = psycopg2.connect(" dbname='postgres' host='192.168.8.188' port=5433  user='postgres' password='pass'  ")
cur = conn.cursor()

@app.route('/')
def hello_geek():
    tem_dic = {
        'name':'Mohammed' ,
        'level' : 2 
    }
    return tem_dic


@app.route('/add_post' , methods=['POST','GET'])
def add_post():
    name = request.json['name']
    query = "INSERT INTO test1 (uname) VALUES (%s)"
    cur.execute(query , (name,))
    conn.commit()
    return name




# Get Posts 
@app.route('/page2' , methods=['GET'])
def page2():
    print('page2')
    query = 'select * from test1'
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    data_list = []
    for data in records:
        data_list.append({
            'names': data[0] ,
        })
    return jsonify(data_list)
   
if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")


# # docker run -p 5433:5432 --name docker-database-v2 -e POSTGRES_PASSWORD=pass -d postgres


# docker build --tag flask1-docker .
# docker run -d -p 5005:5000 --name flask1-container flask1-docker