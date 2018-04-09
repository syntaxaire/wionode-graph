from app import db

class SensorEntry(db.Model):
    __tablename__ = 'sensor_entries'
    dt = db.Column(db.DateTime, primary_key=True)
    data = db.Column(db.Float)

    def __repr__(self):
        return f"SensorEntry object in Flask: Time: {self.dt}, sensor reading: {self.data}"
