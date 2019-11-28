from mongoengine import *
connect(host='mongodb+srv://KeelungEatServer:YW4EY3uAqMi1AcNl@cluster0-upq73.gcp.mongodb.net/KEELUNG_EAT?retryWrites=true&w=majority')
from . import order_model
from . import user_model