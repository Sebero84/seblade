import streamlit as st

# Dummy-Daten
stations = {
    "L1": "Linke Säule #1",
    "L2": "Linke Säule #2",
    "M1": "Mittlere Säule #1",
    "M2": "Mittlere Säule #2",
    "R1": "Rechte Säule #1",
    "R2": "Rechte Säule #2"
}

measurements = {
    "Power": 3.5,  # Dummy Power in kW
    "Cur_I1": 15.0,  # Dummy Stromstärke 1 in A
    "Cur_I2": 15.5,  # Dummy Stromstärke 2 in A
    "Cur_I3": 16.0,  # Dummy Stromstärke 3 in A
    "Enrg": 3103.95,  # Dummy Energie in kWh
    "Frq": 50.0,  # Dummy Frequenz in Hz
    "Status": "AVAL"  # Dummy Status
}

# Funktion zur Anzeige der Stationen
def display_station(station_key, station_label, values):
    # Power Dummy-Wert
    power = values.get("Power", 0)
    status = values.get("Status", "-")

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
        </div>

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
            {power:.2f} kW
        </div>
    </div>
    """, unsafe_allow_html=True)

# Anzeige der Stationen mit Dummy-Daten
for key, label in stations.items():
    display_station(key, label, measurements)
    
