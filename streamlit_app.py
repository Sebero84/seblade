import streamlit as st

st.set_page_config(page_title="Ladesäulen Übersicht", layout="centered")

# Auto-Refresh alle 30 Sekunden
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=30 * 1000, key="auto-refresh")

# Dummy-Werte (statt InfluxDB)
stations = {
    "L1": "Linke Säule #1",
    "R1": "Rechte Säule #1"
}

dummy_data = {
    "Cur_I1": 3.5,
    "Cur_I2": 3.7,
    "Cur_I3": 3.6,
    "Enrg": 1234.56,
    "Frq": 50.01,
    "Power": 7.89,
    "Status": "CHRG"
}


def display_station(station_key, station_label):
    values = dummy_data  # Fake-Daten
    power = values.get("Power")
    status = values.get("Status", "-")

    power_display = f"{power:.2f} kW" if isinstance(power, (int, float)) else "–"

    if status == "CHRG":
        status_html = f'<span style="color: blue;"><b>Status:</b> {status}</span>'
    else:
        status_html = f'<span><b>Status:</b> {status}</span>'

    # HTML-Block
    html = f"""
    <div style="background-color:#59f06a; border-radius:12px; padding:20px; margin-bottom:30px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            
            <!-- Linker Bereich -->
            <div style="flex: 1; color:black;">
                <h3 style="text-align:center;">{station_label}</h3>
                <p><b>Stromstärken:</b> I1: {values.get("Cur_I1", "–")} A | 
                I2: {values.get("Cur_I2", "–")} A | 
                I3: {values.get("Cur_I3", "–")} A</p>
                <p><b>Energie:</b> {values.get("Enrg", "–")} kWh | 
                <b>Frequenz:</b> {values.get("Frq", "–")} Hz</p>
                <p>{status_html}</p>
            </div>

            <!-- Rechter Power-Kreis -->
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
                margin-left: 20px;
            ">
                {power_display}
            </div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# Dummy-Testanzeige
for key, label in stations.items():
    display_station(key, label)
