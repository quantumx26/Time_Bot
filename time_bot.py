from flask import Flask, render_template_string, request, url_for

app = Flask(__name__)

# Serverseitige Speicherung
data_store = {}  # code -> {"group": ..., "room": ...}

# HTML Vorlage für Startseite
HTML_FORM = """
<!doctype html>
<title>Zimmerziehung</title>
<h2>Personen & Zimmer eintragen</h2>
<form method="post">
  <button type="submit">Links generieren</button>
</form>
{% if links %}
<h3>Links für jede Gruppe:</h3>
<ul>
{% for group, link in links.items() %}
  <li>{{ group }}: <a href="{{ link }}" target="_blank">{{ link }}</a></li>
{% endfor %}
</ul>
{% endif %}
"""

# HTML Vorlage für gezogenes Zimmer mit Animation
HTML_DRAW = """
<!doctype html>
<html>
<head>
<title>Zimmer</title>
<style>
  body { font-family: Arial; text-align: center; padding: 50px; }
  .spinner {
    margin: 50px auto;
    width: 60px;
    height: 60px;
    border: 6px solid #f3f3f3;
    border-top: 6px solid #3498db;
    border-radius: 50%;
    animation: spin 2s linear infinite;
  }
  @keyframes spin { 100% { transform: rotate(360deg); } }
  #room { display: none; font-size: 24px; margin-top: 20px; }
</style>
</head>
<body>
<h2>{{ group }}</h2>
<div class="spinner" id="spinner"></div>
<div id="room">Dein Zimmer: {{ room }}</div>

<script>
  setTimeout(function() {
    document.getElementById("spinner").style.display = "none";
    document.getElementById("room").style.display = "block";
  }, 2000);
</script>
</body>
</html>
"""

import random, string

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Feste Zuordnung
groups = [
    "Fabio & Luana", "Laura & Emir", "Giorgia & Lennox",
    "Lucia & Ussama & Savio", "Yvonne & Orazio", "Loredana & Daniel",
    "Tanja & Domenico", "Luca & Luigi", "Marco & Davide"
]

rooms = [
    "Zimmer 7 / Haus 2 - Doppelbett",
    "Zimmer 4 / Haus 2 - Doppelbett",
    "Zimmer 6 / Haus 2 - Schlafcouch",
    "Zimmer 3 / Haus 2 - Doppelbett",
    "Zimmer 2 / Haus 1 - Doppelbett",
    "Zimmer 6 / Haus 2 - Doppelbett",
    "Zimmer 5 / Haus 2 - Doppelbett",
    "Zimmer 1 / Haus 1 - Doppelbett",
    "Zimmer 1 / Haus 1 - Schlafcouch"
]

@app.route("/", methods=["GET", "POST"])
def index():
    links = {}
    if request.method == "POST":
        for group, room in zip(groups, rooms):
            code = generate_code()
            data_store[code] = {"group": group, "room": room}
            links[group] = url_for("draw", code=code, _external=True)
    return render_template_string(HTML_FORM, links=links)

@app.route("/draw/<code>")
def draw(code):
    person = data_store.get(code)
    if not person:
        return "Ungültiger Link", 404
    return render_template_string(HTML_DRAW, group=person["group"], room=person["room"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
