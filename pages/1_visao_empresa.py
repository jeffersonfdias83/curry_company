# Libraries

from haversine import haversine
import plotly.express as px


# Bibliotecas

import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

#st.set_page_config ( page_title = 'Visão Empresa', layout = 'wide' )

#=============== Funções ===============================

def country_maps ( df1 ):    
    df1_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .groupby( ['City', 'Road_traffic_density'])
                  .median()
                  .reset_index())

    map = folium.Map()
    for index, location_info in df1_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']], 
                        popup = location_info[['City', 'Road_traffic_density']] ).add_to( map )

    folium_static ( map, width=1024, height=600 )
        
        
def order_share_by_week ( df1 ): 
        
    df1_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df1_aux2 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                           .groupby( 'week_of_year')
                           .nunique()
                           .reset_index())

    df1_aux = pd.merge( df1_aux1, df1_aux2, how='inner' )
    df1_aux['Order_by_delivery'] = df1_aux['ID'] / df1_aux['Delivery_person_ID']
    fig = px.line( df1_aux, x='week_of_year', y='Order_by_delivery' )
            
    return fig

def order_by_week( df1 ):
        
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df1_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    fig = px.line( df1_aux, x='week_of_year', y='ID' )

    return fig

def traffic_order_city ( df1 ):               
    df1_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                  .groupby( ['City', 'Road_traffic_density'] )
                  .count()
                  .reset_index())                
    fig = px.scatter( df1_aux, x='City', y='Road_traffic_density', color='City', size='ID')
    
    return fig
                

def traffic_order_share ( df1 ):
                
    df1_aux = (df1.loc[:, [ 'ID', 'Road_traffic_density' ]]
                  .groupby ('Road_traffic_density')
                  .count()
                  .reset_index())
    
    df1_aux['entregas_perc'] = 100 * ( df1_aux['ID'] / df1_aux['ID'].sum() )
    fig = px.pie( df1_aux, values='entregas_perc', names='Road_traffic_density' )

    return fig

def order_metric ( df1 ):            
    cols = ['ID', 'Order_Date']

    # Seleção de Linhas
    df1_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

    # Desenhar o Gráfico de Linhas
    fig = px.bar( df1_aux, x='Order_Date', y='ID' )
            
    return fig


def clean_code ( df1 ):
    
    # Remover spaco da string
    for i in range( len( df ) ):
        df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
        df1.loc[i, 'Delivery_person_ID'] = df1.loc[i, 'Delivery_person_ID'].strip()
        df1.loc[i, 'Festival'] = df1.loc[i, 'Festival'].strip()


    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    linhas_vazias = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    #Excluir linhas vazias
    densidade_transito = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[densidade_transito, :]

    densidade_transito1 = df1['City'] != 'NaN '
    df1 = df1.loc[densidade_transito1, :]

    densidade_transito1 = df1['Festival'] != 'NaN '
    df1 = df1.loc[densidade_transito1, :]

    linhas_erradas = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[linhas_erradas, :]

    cidade_vazia = df1['City'] != 'NaN '
    df1 = df1.loc[cidade_vazia, :]


    # Conversao de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    # Remove as linhas da culuna multiple_deliveries que tenham o 
    # conteudo igual a 'NaN '
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # Comando para remover o texto de números
    #df = df.reset_index( drop=True )
    #for i in range( len( df ) ):
    #   df.loc[i, 'Time_taken(min)'] = re.findall( r'\d+', df.loc[i, 'Time_taken(min) '] )

    # Limpando a coluna timetaken

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split ( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    
    return df1

#============================= Início da Estrutura Lógica do Código ======================================

# Import dataset

#dataset_path = r"D:\Documentos\repos\2_fast_track_analisando_dados_com_python\ciclo_04\train(1).csv"

df = pd.read_csv("train(1)")

print ( df.head() )

# Fazendo uma cópia do DataFrame Lido
df1 = df.copy()


# Limpeza de Dados

df1 = clean_code ( df )

#===============================
# Barra Lateral
#===============================

image_path = 'logo.jpeg'
image = Image.open (image_path)
st.sidebar.image( image, width=180)

st.header('Marketplace - Visão Cliente')

st.sidebar.markdown('## Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?', 
    value=pd.datetime( 2022, 4, 13),
    min_value=pd.datetime( 2022, 2, 11),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY')

st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['Low ', 'Medium ', 'High ', 'Jam '],
    default = ['Low ', 'Medium ', 'High ', 'Jam '])

st.sidebar.markdown("""___""")
st.sidebar.markdown('#### Powered by Jefferson Data Science')


#Filtros Selecionados (Data)

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtros de Trânsito

linhas_selecionadas = df1['Road_traffic_density'].isin (traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

#===============================
# Layout no streamlit
#===============================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    
    with st.container():
        # Order Metric
        fig = order_metric ( df1 )
        st.header('Orders by Day' )
        st.plotly_chart (fig, use_container_width= True)
                            
    with st.container():
        col1, col2 = st.columns ( 2 )
    
        with col1:
            fig = traffic_order_share ( df1 )
            st.header('Traffic Order Share')
            st.plotly_chart (fig, use_container_width= True)
                           
        with col2:
            fig = traffic_order_city ( df1 )
            st.header('Traffic Order City')
            st.plotly_chart (fig, use_container_width= True)

            
with tab2:
    
    with st.container():
        fig = order_by_week ( df1 )
        st.header('Order by Week')
        st.plotly_chart (fig, use_container_width= True)
                               
    with st.container():
        fig = order_share_by_week ( df1 )
        st.header('Order Share by Week')
        st.plotly_chart (fig, use_container_width= True)
        

with tab3:
    st.markdown( "# Country Maps" )
    country_maps ( df1 )
    
    
