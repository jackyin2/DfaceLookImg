from datetime import datetime
from app import db


class Alert_Jack(db.Model):
    __tablename__="alert_jack"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_id = db.Column(db.String(100))
    yesornot = db.Column(db.Integer)
    deploy_id = db.Column(db.String(100))
    source_id = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


if __name__ == "__main__":
    # db.metadata.clear()

    db.create_all()