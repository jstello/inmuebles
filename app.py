import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# import ag
from streamlit_calendar import calendar

# Read dataframe with header on row 3, only reading columns F, G, L, M, N, and sheet `Secuencial fija`
df = pd.read_excel(r'Sorteo inmuebles Secuencial Asignados.xlsx', header=2, usecols='F:G, L:N', sheet_name='Secuencial fija')
# st.dataframe(df)
# st.stop()
# Convertir las columnas de fecha a tipo datetime
df['Llegada'] = pd.to_datetime(df['Llegada'], format='%d-%b-%Y')
df['Salida'] = pd.to_datetime(df['Salida'], format='%d-%b-%Y')

# Obtener la fecha actual
today = pd.to_datetime(datetime.now().date())


df = df[df['Llegada'] > today].copy()

df.rename(columns={
    'SantaCruz': 'SantaCruzTemp', 
    'Cartagena': 'CartagenaTemp', 
    'Miravalle': 'MiravalleTemp',
    'SantaCruz.1': 'SantaCruz',
    'Cartagena.1': 'Cartagena',
    'Miravalle.1': 'Miravalle'
}, inplace=True)
# Encontrar la fila correspondiente a la fecha actual
current_row = df[(df['Llegada'] <= today) & (df['Salida'] >= today)]

# Verificar si se encontró una fila válida 
if not current_row.empty:
    # Obtener la distribución de los inmuebles para la fecha actual
    santa_cruz = current_row['SantaCruz'].values[0]
    cartagena = current_row['Cartagena'].values[0]
    miravalle = current_row['Miravalle'].values[0]
    
    # Mostrar la distribución en Streamlit
    st.title('Distribución de Inmuebles')

    # Show assignments as KPIs
    st.markdown(f'### Fecha de hoy: {today.strftime("%d-%b-%Y")}')
    
    col1, col2, col3 = st.columns(3)
    

    with col1:
        st.metric(label="Santa Cruz", value=santa_cruz)
    
    with col2:
        st.metric(label="Cartagena", value=cartagena)
    
    with col3:
        st.metric(label="Miravalle", value=miravalle)
else:
    st.write('No se encontró una distribución válida para la fecha actual.')

with st.expander("Asignaciones por fecha..."):
    cols = st.columns(3)
    # inmueble = cols[0].selectbox('Inmueble', ['SantaCruz', 'Cartagena', 'Miravalle'])
    # tennant = cols[1].selectbox('Inquilino', ['Turritop', 'Minka', 'RC', 'AMC'])
    fecha = cols[2].date_input('Fecha', value=today)
    fecha = pd.to_datetime(fecha)
    
    df_filtered = df[(df['Llegada'] <= fecha) & (df['Salida'] >= fecha)]
    st.table(df_filtered)

# Add this new expander section
with st.expander("Cuándo me toca Santa Cruz?"):
    
    # Define a fixed color palette for the 6 tenants
    TENANT_COLORS = {
        'Chali': '#FF6B6B',  # Red
        'Turritop': '#4ECDC4',  # Teal
        'Minka': '#45B7D1',  # Blue
        'RC': '#FFA07A',  # Light Salmon
        'AMC': '#98D8C8',  # Mint
        'DC': '#F7DC6F'  # Yellow
    }
    st.write("O cualquier otro inmueble...")
    col1, col2, col3 = st.columns(3)
    inmueble = col1.selectbox('Inmueble', ['SantaCruz', 'Cartagena', 'Miravalle'])
    
    # Change the single select to a multi-select, default to selecting all
    all_inquilinos = df[inmueble].dropna().unique()
    inquilinos = col2.multiselect('Inquilinos', all_inquilinos, default=all_inquilinos)
    
    df['Año'] = df['Llegada'].dropna().dt.year.astype(int)
    
    year = col3.selectbox('Año', df['Año'].unique().astype(int), index=0)

    # Filter the dataframe based on the selected property, tenants, and year
    df_filtered = df[(df[inmueble].isin(inquilinos)) & (df['Año'] == year)]

    if not df_filtered.empty:
        st.write(f"Fechas asignadas para los inquilinos seleccionados en {inmueble} en {year}:")
        
        # Define color mapping for inmuebles
        INMUEBLE_COLORS = {
            'SantaCruz': '#FF0000',  # Red
            'Cartagena': '#00FF00',  # Green
            'Miravalle': '#0000FF'   # Blue
        }

        # Prepare calendar events
        calendar_events = []
        for _, row in df_filtered.iterrows():
            start_date = row['Llegada'].strftime('%Y-%m-%d')
            end_date = (row['Salida'] + timedelta(days=1)).strftime('%Y-%m-%d')  # Add one day to include the last day
            inquilino = row[inmueble]
            calendar_events.append({
                'title': f'{inquilino} en {inmueble}',
                'start': start_date,
                'end': end_date,
                'color': TENANT_COLORS.get(inquilino, '#808080'),  # Background color based on tenant
                'textColor': '#000000'  # Text color set to black for now
            })

        # Calendar options
        calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,dayGridWeek,dayGridDay",
            },
            "initialDate": f"{year}-01-01",
            "initialView": "dayGridMonth",
            "selectable": True,
            "editable": False,
            "displayEventTime": False,
        }

        # Display the calendar
        calendar(events=calendar_events, options=calendar_options)

    else:
        st.warning(f"No se encontraron fechas asignadas para los inquilinos seleccionados en {inmueble} en {year}.")
        st.write("El calendario aparecerá vacío porque no hay eventos para mostrar.")
        
        # Display an empty calendar for the selected year
        calendar(events=[], options=calendar_options)

with st.expander("Distribución de inmuebles"):
    
    cols = st.columns(3)
    
    # Default to selecting all tenants
    all_tenants = df['SantaCruz'].dropna().unique()
    selected_tenants = cols[0].multiselect('Inquilinos', all_tenants, default=all_tenants, key='selected_tenants')
    df_filtered = df[df['SantaCruz'].isin(selected_tenants)]
    
    # Default to selecting all years
    all_years = df_filtered['Año'].unique().astype(int)
    selected_years = cols[1].multiselect('Años', all_years, default=all_years, key='selected_years')
    df_filtered = df_filtered[df_filtered['Año'].isin(selected_years)]
    
    # Convert 'Año' column to integer
    df_filtered['Año'] = df_filtered['Año'].astype(int)
    
    # Format date columns to display in a cleaner way
    df_filtered['Llegada'] = df_filtered['Llegada'].dt.strftime('%Y-%m-%d')
    df_filtered['Salida'] = df_filtered['Salida'].dt.strftime('%Y-%m-%d')

    # Display the table with styled data
    st.table(df_filtered.style)

# Define a fixed color palette for the 6 tenants
TENANT_COLORS = {
    'Chali': '#FF6B6B',  # Red
    'Turritop': '#4ECDC4',  # Teal
    'Minka': '#45B7D1',  # Blue
    'RC': '#FFA07A',  # Light Salmon
    'AMC': '#98D8C8',  # Mint
    'DC': '#F7DC6F'  # Yellow
}
