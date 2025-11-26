from flask import Flask, render_template_string, request, url_for
import random
import string

app = Flask(__name__)

# Serverseitige Speicherung
data_store = {}  # code -> {"name": ..., "room": ...}

# Zimmer-Losliste
available_rooms = []  # wird beim POST gesetzt

# HTML Vorlage für Startseite
HTML_FORM = """
<!doctype html>
<title>Zimmerziehung</title>
<h2>Personen & Zimmer eintragen</h2>
<form method="post">
  <label>Personen (kommagetrennt):</label><br>
  <input type="text" name="names" required><br><br>
  <label>Zimmer (kommagetrennt, gleiche Anzahl oder mehr):</label><br>
  <input type="text" name="rooms" required><br><br>
  <button type="submit">Links generieren</button>
</form>
{% if links %}
<h3>Links für jede Person:</h3>
<ul>
{% for name, link in links.items() %}
  <li>{{ name }}: <a href="{{ link }}" target="_blank">{{ link }}</a></li>
{% endfor %}
</ul>
{% endif %}
"""

# HTML Vorlage für gezogenes Zimmer
HTML_DRAW = """
<!doctype html>
<title>Zimmer</title>
<h2>{{ name }}</h2>
<p>Dein Zimmer: {{ room }}</p>
"""

# Zufälligen Code generieren
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Zimmer wie Los ziehen
def pick_room():
    rooms_with_stock = [r for r in available_rooms if r["count"] > 0]
    if not rooms_with_stock:
        return None
    room = random.choice(rooms_with_stock)
    room["count"] -= 1
    return room["name"]

@app.route("/", methods=["GET", "POST"])
def index():
    global available_rooms
    links = {}
    if request.method == "POST":
        names = [n.strip() for n in request.form["names"].split(",") if n.strip()]
        rooms_input = [r.strip() for r in request.form["rooms"].split(",") if r.strip()]

        if len(rooms_input) < len(names):
            return "Es müssen mindestens genauso viele Zimmer wie Personen vorhanden sein!", 400

        # Zimmer vorbereiten (ein Los pro Zimmer)
        available_rooms = [{"name": r, "count": 1} for r in rooms_input]
        random.shuffle(available_rooms)  # optional

        for name in names:
            room = pick_room()
            if not room:
                links[name] = "Kein Zimmer mehr verfügbar"
                continue
            code = generate_code()
            data_store[code] = {"name": name, "room": room}
            links[name] = url_for("draw", code=code, _external=True)

    return render_template_string(HTML_FORM, links=links)

@app.route("/draw/<code>")
def draw(code):
    person = data_store.get(code)
    if not person:
        return "Ungültiger Link", 404
    return render_template_string(HTML_DRAW, name=person["name"], room=person["room"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
