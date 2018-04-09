from app import app, db
from app.models import SensorEntry
from app import graph

@app.route('/')
@app.route('/index')
def index():
    return "Hello, world!"

@app.route('/dump')
def dump():
    entries = SensorEntry.query.all()
    showgraph = graph.graph(entries)
    # response = str([str(entry) + "<br \>" for entry in entries])
    return showgraph
