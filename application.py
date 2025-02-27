from flask import Flask, render_template, session, redirect, url_for,request
from flask_session import Session
from tempfile import mkdtemp
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)

# Setup OpenTelemetry Tracing
trace_provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

@app.route("/")
def start():
    return render_template("launch.html")

@app.route('/', methods=['POST','GET'])
def my_form_post():
    if request.method=="POST":
        global fplayer,splayer
        fplayer = request.form['name']
        splayer = request.form['username']
        fplayer = fplayer.upper()
        splayer = splayer.upper()
    return redirect(url_for("index"))

@app.route("/play")
def index():

    if "board" not in session:
        global board
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        board = session["board"]
        session["turn"] = "X" 
        winner = check_winner(session["board"])
        if winner is not None:
            return render_template('winner.html', winner=winner)

    return render_template("game.html", fplayer=fplayer,splayer=splayer,game=session["board"], turn=session["turn"])


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    if session["turn"] == "X":
        session["board"][row][col]="X"
        session["turn"]="Y"
    else:
        session["board"][row][col]="O"
        session["turn"]="X"

    winner = check_winner(session["board"])
    if winner is not None:
        return render_template('winner.html', winner=winner)

    return redirect(url_for("index"))

app.run()
