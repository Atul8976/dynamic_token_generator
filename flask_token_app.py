from flask import Flask, jsonify, request

import datetime as delta
from datetime import datetime as dt
from cryptography.fernet import Fernet
import jwt
import os

app = Flask(__name__)

current_directory = os.getcwd()
internal_directory = current_directory + 'keys.key'
token_directory = current_directory+'\\token.ini'

key = None
Payload = None
Encode = None
decode = None

@app.route('/generate_key',methods=['GET'])
def generate_key():

    key = Fernet.generate_key()

    file = open(internal_directory, 'wb')
    file.write(key)
    file.close()
    return key

@app.route('/read_key',methods=['GET'])
def read_key():
    file = open(internal_directory, 'rb')
    key = file.read()
    file.close()
    return key

@app.route('/generate_token',methods=['GET'])

def Encoded():

    try:

        key = generate_key()

        Payload = {
            'exp': dt.utcnow() + delta.timedelta(seconds=60)
        }

        Encode = jwt.encode(Payload, key, algorithm='HS512')

        file = open(token_directory, 'wb')
        file.write(Encode.encode('UTF-8'))
        file.close()

        print(Encode)

        return jsonify({'token': Encode})

    except Exception as ex:
        print(ex)
        return jsonify({'token': 'Something Went Wrong Please Try Again'})


@app.route('/decode_token',methods=['POST'])

def Decoded():

    try:
        key = read_key()

        Encode = request.headers['token']

        decode = jwt.decode(Encode,key,algorithms='HS512')

        # print(decode)
        return jsonify({'token': decode})

    except jwt.exceptions.ExpiredSignatureError:

        return jsonify({'msg': 'Token Expired'})

    except Exception as ex:
        print(ex)
        return jsonify({'token': 'Something Went Wrong Please Try Again'})


if __name__ == '__main__':
    app.run(host='localhost', port=8083, debug=True)
