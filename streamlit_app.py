import streamlit as st
from influxdb_client import InfluxDBClient
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Ladesäulen Übersicht", layout="centered")

# InfluxDB-Konfiguration
url = st.secrets["url"]
token = st.secrets["token"]
org = st.secrets["org"]
bucket = st.secrets["bucket"]

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Definition der Stationen
stations = {
    "L1": "Linke Säule #1",
    "L2": "Linke Säule #2",
    "M1": "Mittlere Säule #1",
    "M2": "Mittlere Säule #2",
    "R1": "Rechte Säule #1",
    "R2": "Rechte Säule #2"
}

# Messgrößen
measurements = ["Power", "Cur_I1", "Cur_I2", "Cur_I3", "Enrg", "Frq", "Status"]

# Auto-Refresh alle 30 Sekunden
st_autorefresh(interval=30 * 1000, key="auto-refresh")

# Funktion zur Abfrage einzelner Werte
def get_latest_value(station, measurement):
    query = f'''
    from(bucket: "{bucket}")
    |> range(start: -1h)
    |> filter(fn: (r) => r["_measurement"] == "{station}_{measurement}")
    |> last()
    '''
    try:
        tables = query_api.query(query)
        for table in tables:
            for record in table.records:
                return record.get_value()
    except Exception as e:
        print(f"Fehler bei {station}_{measurement}: {e}")
    return None

# Funktion zur Darstellung der Gauge als visuelle Fortschrittsanzeige
def render_gauge(value):
    max_value = 11  # Maximale Kapazität in kW
    percentage = (value / max_value) * 100  # Prozentualer Anteil des Wertes

    # CSS für den Fortschrittsbalken
    return f"""
    <div style="position: relative; width: 100px; height: 100px; border-radius: 50%; background: #f0f0f0; float: right; margin-left: 20px;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 18px; color: black;">
            <b>{value:.2f} kW</b>
        </div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: {percentage}%; height: 100%; border-radius: 50%; background: green;"></div>
    </div>
    """

# Funktion zur Anzeige einer Station
def display_station(station_key, station_label):
    values = {m: get_latest_value(station_key, m) for m in measurements}
    power = values.get("Power", 0)
    status = values.get("Status", "-")

    # Farbiger Status-Text bei CHRG
    if status == "CHRG":
        status_html = f'<span style="color: blue;"><b>Status:</b> {status}</span>'
    else:
        status_html = f'<span><b>Status:</b> {status}</span>'

    # Quader-Hintergrund mit Flexbox-Layout
    bg_color = "#59f06a"

    # Quader mit Messwerten und Gauge nebeneinander
    st.markdown(f"""
    <div style="background-color:{bg_color}; border-radius:12px; padding:20px; margin-bottom:30px; display: flex; align-items: center; justify-content: space-between;">
        <div style="flex-grow: 1; text-align:left; color:black;">
            <h3 style="text-align:center; color:black;">{station_label}</h3>
            <div style="margin-bottom:15px;">
                <b>Stromstärken:</b> I1: {values.get("Cur_I1", "-")} A | 
                I2: {values.get("Cur_I2", "-")} A | 
                I3: {values.get("Cur_I3", "-")} A
            </div>
            <div style="margin-bottom:15px;">
                <b>Energie:</b> {values.get("Enrg", "-")} kWh | 
                <b>Frequenz:</b> {values.get("Frq", "-")} Hz
            </div>
            <div style="margin-bottom:15px;">
                {status_html}
            </div>
            <div style="text-align:right;">
            {render_gauge(power)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Anzeige aller Stationen
for key, label in stations.items():
    display_station(key, label)
