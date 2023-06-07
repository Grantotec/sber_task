from flask import Flask


app = Flask(__name__)


@app.route('/get_deposit_info', methods=['GET'])
def hello():

    return {'Status': 200, 'Value': 'OK'}


if __name__ == '__main__':
    app.run()
