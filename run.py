from app import app
# from settings import Config


if __name__ == '__main__':
    # app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    app.run(debug=True, host="127.0.0.1", port=5001)
    