from mongoengine import *
connect(host='mongodb+srv://KeelungEatServer:YW4EY3uAqMi1AcNl@cluster0-upq73.gcp.mongodb.net/KEELUNG_EAT?retryWrites=true&w=majority')
from .user_model import *
from .order_model import *
from .store_model import *