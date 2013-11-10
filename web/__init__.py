from flask import Flask
app = Flask(__name__)
app.secret_key = 'your mother bakes cyanide cookies in hell!'
import routes
