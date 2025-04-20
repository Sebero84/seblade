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
measurements = ["Power", "Cur_I1", "Cur_I2", "Cur_I3", "Enrg", "Frq", "Status", "Volt_L1", "Volt_L2", "Volt_L3"]

# Auto-Refresh alle 30 Sekunden
st_autorefresh(interval=30 * 1000, key="auto-refresh")

# Funktion zur Abfrage einzelner Werte aus der InfluxDB
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

# Funktion zur Anzeige einer Station
def display_station(station_key, station_label):
    values = {m: get_latest_value(station_key, m) for m in measurements}
    power = values.get("Power", 0)
    status = values.get("Status", "-")
    volt_l1 = values.get("Volt_L1", "-")
    volt_l2 = values.get("Volt_L2", "-")
    volt_l3 = values.get("Volt_L3", "-")

    # Farbiger Status-Text
    if status == "CHRG":
        status_html = f'<span style="color: blue;"><b>Status:</b> {status}</span>'
    else:
        status_html = f'<span><b>Status:</b> {status}</span>'

    # Quader-Hintergrund und Layout
    bg_color = "#59f06a"  # Grüner Hintergrund

    # Quader mit Messwerten und Kreis
    st.markdown(f"""
    <div style="display: flex; align-items: center; background-color:{bg_color}; border-radius:12px; padding:20px; margin-bottom:30px;">
        <div style="flex: 1; color:black;">
            <h3 style="text-align:center;">{station_label}</h3>
            <p><b>Stromstärken:</b> I1: {values.get("Cur_I1", "-")} A | 
            I2: {values.get("Cur_I2", "-")} A | 
            I3: {values.get("Cur_I3", "-")} A</p>
            <p><b>Energie:</b> {values.get("Enrg", "-")} kWh | 
            <b>Frequenz:</b> {values.get("Frq", "-")} Hz</p>
            <p><span><b>Status:</b> {status_html}</span></p>
            <p><b>Spannung:</b> L1: {volt_l1:.2f} V | 
            L2: {volt_l2:.2f} V | 
            L3: {volt_l3:.2f} V</p>
        </div>
        <div style="width: 100px; height: 100px; border-radius: 50%; background-color: white; color: black; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px; border: 2px solid #ccc; margin-left: 20px;">
            {power:.2f} kW
        </div>
    </div>
    """, unsafe_allow_html=True)

# Anzeige der Stationen mit den Werten aus InfluxDB
for key, label in stations.items():
    display_station(key, label)
