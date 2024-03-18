import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# import ag
# Cargar los datos desde el documento
data = '''
Inicio	Fin	SantaCruz	Cartagena	Miravalle
1-Jan-2024	11-Jan-2024	Minka	RC	AMC
12-Jan-2024	22-Jan-2024	RC	AMC	DC
23-Jan-2024	2-Feb-2024	AMC	DC	Chali
...
'''

# Read dataframe with header on row 3, only reading columns F, G, L, M, N, and sheet `Secuencial fija`
df = pd.read_excel(r'C:\Users\juan_tello\Documents\CanoSanz\Sorteo inmuebles Secuencial Asignados.xlsx', header=2, usecols='F:G, L:N', sheet_name='Secuencial fija')
# st.dataframe(df)
# st.stop()
# Convertir las columnas de fecha a tipo datetime
df['Llegada'] = pd.to_datetime(df['Llegada'], format='%d-%b-%Y')
df['Salida'] = pd.to_datetime(df['Salida'], format='%d-%b-%Y')

# Obtener la fecha actual
today = pd.to_datetime(datetime.now().date())

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

with st.expander("Busca la distribucion en una fecha:"):
    cols = st.columns(3)
    # inmueble = cols[0].selectbox('Inmueble', ['SantaCruz', 'Cartagena', 'Miravalle'])
    # tennant = cols[1].selectbox('Inquilino', ['Turritop', 'Minka', 'RC', 'AMC'])
    fecha = cols[2].date_input('Fecha', value=today)
    fecha = pd.to_datetime(fecha)
    
    df_filtered = df[(df['Llegada'] <= fecha) & (df['Salida'] >= fecha)]
    st.table(df_filtered)

with st.expander("Distribución de inmuebles	"):
    st.table(df)
