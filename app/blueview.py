from app import app
from app.Dface import dface


app.register_blueprint(dface, url_prefix="/")
