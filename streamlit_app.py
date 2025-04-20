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

stations = {
    "L1": "Linke Säule #1",
    "L2": "Linke Säule #2",
    "M1": "Mittlere Säule #1",
    "M2": "Mittlere Säule #2",
    "R1": "Rechte Säule #1",
    "R2": "Rechte Säule #2"
}

measurements = ["Power", "Cur_I1", "Cur_I2", "Cur_I3", "Enrg", "Frq", "Status"]

st_autorefresh(interval=30 * 1000, key="auto-refresh")

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

def display_station(station_key, station_label):
    values = {m: get_latest_value(station_key, m) for m in measurements}
    power = values.get("Power", 0)
    status = values.get("Status", "-")

    if status == "CHRG":
        status_html = f'<span style="color: blue;"><b>Status:</b> {status}</span>'
    else:
        status_html = f'<span><b>Status:</b> {status}</span>'

    bg_color = "#59f06a"

    # Start HTML-Block (Text-Teil links)
    st.markdown(f"""
    <div style="background-color:{bg_color}; border-radius:12px; padding:20px; margin-bottom:30px; display: flex; justify-content: space-between; align-items: center;">
        <div style="flex: 1; color:black;">
            <h3 style="text-align:center;">{station_label}</h3>
            <p><b>Stromstärken:</b> I1: {values.get("Cur_I1", "-")} A | 
            I2: {values.get("Cur_I2", "-")} A | 
            I3: {values.get("Cur_I3", "-")} A</p>
            <p><b>Energie:</b> {values.get("Enrg", "-")} kWh | 
            <b>Frequenz:</b> {values.get("Frq", "-")} Hz</p>
            <p>{status_html}</p>
        </div>
    """, unsafe_allow_html=True)

    # Power-Kreis (rechts, als separater Markdown)
    st.markdown(f"""
        <div style="
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: white;
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #ccc;
        ">
            {power:.2f} kW
        </div>
    </div> <!-- Hier wird der äußere Flex-Container sauber geschlossen -->
    """, unsafe_allow_html=True)

# Anzeige aller Stationen
for key, label in stations.items():
    display_station(key, label)
