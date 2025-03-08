import streamlit as st
# import streamlit_authenticator as stauth  # Commented out auth import
# import yaml
# from yaml.loader import SafeLoader
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from streamlit_calendar import calendar
# Add authentication configuration
# with open('auth_config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# Extract credentials from config
# credentials = config['credentials']['usernames']
# names = [user['name'] for user in credentials.values()]
# usernames = list(credentials.keys())
# passwords = [user['password'] for user in credentials.values()]

# authenticator = stauth.Authenticate(
#     names=names,
#     usernames=usernames,
#     passwords=passwords,
#     cookie_name=config['cookie']['name'],
#     key=config['cookie']['key'],  # This matches the required 'key' parameter
#     cookie_expiry_days=config['cookie']['expiry_days']
# )

# Add this right after loading config
# st.write("Stored hash:", config['credentials']['usernames']['juan']['password'])
# st.write("Generated hash:", stauth.Hasher.hash('qwerqwer2'))  # Your plain password

# try:
#     # New version syntax (>=0.2.3)
#     name, authentication_status, username = authenticator.login('Login', 'main')
# except TypeError:
#     # Fallback to old version syntax (<0.2.3)
#     name, authentication_status, username = authenticator.login(location='main')

# Handle all auth states
# if authentication_status == False:
#     st.error("❌ Usuario/contraseña incorrectos")
#     st.stop()
# elif authentication_status == None:
#     st.warning("⚠️ Por favor ingrese su usuario y contraseña")
#     st.stop()

# Only show app content if authenticated
# authenticator.logout('Cerrar sesión', 'main')
# st.write(f"Bienvenido *{name}*")

# MAIN APPLICATION CONTENT (keep this uncommented)
st.title("Calendar de Inmuebles")

df = pd.read_excel(r'Sorteo inmuebles Secuencial Asignados.xlsx', header=2, usecols='F:G, L:N', sheet_name='Secuencial fija')
df['Llegada'] = pd.to_datetime(df['Llegada'], format='%d-%b-%Y')
df['Salida'] = pd.to_datetime(df['Salida'], format='%d-%b-%Y')

target_date = st.date_input("Seleccionar fecha para ver disponibilidad", date(2025, 3, 7))
today = pd.to_datetime(target_date)

start_date = today - pd.Timedelta(days=30)
df = df[df['Llegada'] >= start_date].copy()

df.rename(columns={
    'SantaCruz': 'SantaCruzTemp', 
    'Cartagena': 'CartagenaTemp', 
    'Miravalle': 'MiravalleTemp',
    'SantaCruz.1': 'SantaCruz',
    'Cartagena.1': 'Cartagena',
    'Miravalle.1': 'Miravalle'
}, inplace=True)
current_row = df[(df['Llegada'] <= today) & (df['Salida'] >= today)]

# Current dates
cols = st.columns(2)

with cols[0]:
    # Get earliest arrival date from current assignments
    start_date = current_row['Llegada'].min() if not current_row.empty else today
    st.metric(label="Desde", value=start_date.strftime('%d-%b'))

with cols[1]:
    # Get latest departure date from current assignments
    end_date = current_row['Salida'].max() if not current_row.empty else today + pd.Timedelta(days=30)
    st.metric(label="Hasta", value=end_date.strftime('%d-%b'))

cols = st.columns(3)

with cols[0]:
    st.subheader("Santa Cruz")
    if not current_row[current_row['SantaCruz'].notna()].empty:
        tenant = current_row['SantaCruz'].iloc[0]
        dates = f"{current_row['Llegada'].iloc[0].strftime('%d-%b')} a {current_row['Salida'].iloc[0].strftime('%d-%b')}"
        st.metric(label="Ocupante actual", value=tenant, delta=dates)
    else:
        st.metric(label="Disponibilidad", value="Libre", delta="Disponible ahora")

with cols[1]:
    st.subheader("Cartagena")
    if not current_row[current_row['Cartagena'].notna()].empty:
        tenant = current_row['Cartagena'].iloc[0]
        dates = f"{current_row['Llegada'].iloc[0].strftime('%d-%b')} a {current_row['Salida'].iloc[0].strftime('%d-%b')}"
        st.metric(label="Ocupante actual", value=tenant, delta=dates)
    else:
        st.metric(label="Disponibilidad", value="Libre", delta="Disponible ahora")

with cols[2]:
    st.subheader("Miravalle")
    if not current_row[current_row['Miravalle'].notna()].empty:
        tenant = current_row['Miravalle'].iloc[0]
        dates = f"{current_row['Llegada'].iloc[0].strftime('%d-%b')} a {current_row['Salida'].iloc[0].strftime('%d-%b')}"
        st.metric(label="Ocupante actual", value=tenant, delta=dates)
    else:
        st.metric(label="Disponibilidad", value="Libre", delta="Disponible ahora")

# Change the color mapping to be property-based
PROPERTY_COLORS = {
    'SantaCruz': '#FF6B6B',  # Red
    'Cartagena': '#4ECDC4',  # Teal
    'Miravalle': '#45B7D1'   # Blue
}

# Use the full dataframe
df_filtered = df

if not df_filtered.empty:
    calendar_events = []
    for _, row in df_filtered.iterrows():
        start_date = row['Llegada'].strftime('%Y-%m-%d')
        end_date = (row['Salida'] + timedelta(days=1)).strftime('%Y-%m-%d')
        # Create events for all properties
        for property in ['SantaCruz', 'Cartagena', 'Miravalle']:
            if pd.notna(row[property]):
                calendar_events.append({
                    'title': f"{property}: {row[property]}",  # Show property and tenant
                    'start': start_date,
                    'end': end_date,
                    'color': PROPERTY_COLORS.get(property, '#808080'),  # Use property color
                    'textColor': '#000000'
                })

    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek,dayGridDay",
        },
        "initialDate": f"{target_date}",
        "initialView": "dayGridMonth",
        "selectable": True,
        "editable": False,
        "displayEventTime": False,
    }

    calendar(events=calendar_events, options=calendar_options)
    st.dataframe(df_filtered)
else:
    st.warning("No se encontraron fechas asignadas.")
    calendar(events=[], options=calendar_options)
