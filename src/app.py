from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import json
from mpd import MPDClient

app = Flask(__name__)

# ---- CONFIG ----
API_URL = "https://de1.api.radio-browser.info/json/stations/bytag/jazz"
ITEMS_PER_PAGE = 30

MPD_HOST = "localhost"
MPD_PORT = 6600

FAV_FILE = 'favorites.json'

def set_mpd_stream(url):
    """Connect to MPD and switch streams."""
    client = MPDClient()
    client.timeout = 2
    client.idletimeout = None
    
    client.setvol(100)

    client.connect(MPD_HOST, MPD_PORT)
    client.stop()
    client.clear()
    client.add(url)
    client.play()
    client.close()
    client.disconnect()


def load_favorites():
    try:
        with open(FAV_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_favorites(faves):
    with open(FAV_FILE, 'w') as f:
        json.dump(faves, f, indent=2)

@app.route("/")
def index():
    # pagination
    page = int(request.args.get("page", 1))

    # fetch list from API
    resp = requests.get(API_URL, timeout=5)
    stations = resp.json()

    total = len(stations)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    page_items = stations[start:end]

    return render_template(
        "index.html",
        stations=page_items,
        page=page,
        total_pages=(total // ITEMS_PER_PAGE) + 1,
    )


@app.route("/play/<station_id>")
def play_station(station_id):
    # fetch the station data from API
    resp = requests.get(API_URL, timeout=5)
    stations = resp.json()

    # find the station by its UUID
    station = next((s for s in stations if s["stationuuid"] == station_id), None)
    if station:
        stream = station["url_resolved"]
        set_mpd_stream(stream)

    return redirect(url_for("index"))

@app.route("/favorite/<uuid>", methods=["POST"])
def favorite_station(uuid):
    # find station in current API fetch
    stations = requests.get(API_URL).json()
    station = next((s for s in stations if s['stationuuid']==uuid), None)
    if not station: return '',404

    faves = load_favorites()
    if any(s['stationuuid']==uuid for s in faves):
        faves = [s for s in faves if s['stationuuid']!=uuid]
    else:
        faves.append(station)
    save_favorites(faves)
    return '', 200

@app.route("/favorites")
def favorites_list():
    return jsonify(load_favorites())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
