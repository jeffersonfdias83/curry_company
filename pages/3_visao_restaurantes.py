# Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go


# Bibliotecas

import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np

st.set_page_config ( page_title = 'Visão Restaurantes')#, layout = 'wide' )

#=============== Funções ===============================


def avg_std_time_on_traffic ( df1 ):
    df1_aux = (df1.loc [:, ['City', 'Road_traffic_density', 'Time_taken(min)']]
                  .groupby (['City', 'Road_traffic_density'])
                  .agg({'Time_taken(min)': ['mean', 'std']}))     

    df1_aux.columns = ['avg_time', 'std_time']
    df1_aux = df1_aux.reset_index()

    fig = px.sunburst (df1_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time',
                       color = 'std_time', 
                       color_continuous_scale = 'RdBu', 
                       color_continuous_midpoint = np.average(df1_aux['std_time']))

    #fig.update_layout (width=400, height=300)
                
    return fig


def avg_std_time_delivery ( df1, festival, op ):
    
    """
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
        Parâmetros:
            Input:
                - df: Dataframe com os dados necessários para o cálculo
                - op: Tipo de operação que precisa ser calculado
                'avg_time': Calcula o tempo médio
                'std_time': Calcula o desvio padrão do tempo
                
            Output:
                - df: Dataframe com 2 colunas e 1 linha
             
    """
                                                                
    df1_aux = (df1.loc [:, ['Festival', 'Time_taken(min)']]
                  .groupby ('Festival')
                  .agg({'Time_taken(min)': ['mean', 'std']})) 

    # Usar agg para aplicar duas funções (média e desvio padrão) ao mesmo tempo
    df1_aux.columns = ['avg_time', 'std_time']
    df1_aux = df1_aux.reset_index()
    df1_aux = np.round (df1_aux.loc[ df1_aux['Festival'] == festival, op ], 2 )

    return df1_aux


def distance ( df1 ):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1 ['Distance'] = df1.loc [:, cols].apply (lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )
                
    avg_distance = np.round (df1 ['Distance'].mean(), 2 )
                
    return avg_distance


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


# Import dataset

#dataset_path = r"D:\Documentos\repos\2_fast_track_analisando_dados_com_python\ciclo_04\train(1).csv"

file_path = "dataset/train(1).csv"

df = pd.read_csv(file_path)

# Fazendo uma cópia do DataFrame Lido

df1 = df.copy()


# Limpeza de dados

df1 = clean_code ( df )

#===============================
# Barra Lateral
#===============================

image_path = 'logo.jpeg'
image = Image.open (image_path)
st.sidebar.image( image, width=120)

st.header('Marketplace - Visão Restaurantes') 

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

#st.sidebar.markdown("""___""")
#
#traffic_options = st.sidebar.multiselect(
#    'Quais as condições de trânsito?',
#    ['Low ', 'Medium ', 'High ', 'Jam '],
#    default = ['Low ', 'Medium ', 'High ', 'Jam '])

##st.sidebar.markdown("""___""")

#weather_options = st.sidebar.multiselect(
#    'Quais as condições de climáticas?',
#    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
#    default = ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'])
#
st.sidebar.markdown("""___""")
st.sidebar.markdown('#### Powered by Jefferson Data Science')


#===============================
# Layout no streamlit
#===============================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', '_', '_'])

with tab1:
    
    with st.container():
        st.title('Overall Metrics' )
        
        col1, col2, col3, col4, col5, col6 = st.columns ( 6 )
        with col1:
            delivery_unique = len(df1.loc [:,'Delivery_person_ID'].unique())
            col1.metric ( 'Qtd Entregadores', delivery_unique )
          
        
        with col2:
            avg_distance = distance ( df1 )
            col2.metric ( 'Dist Média Entregas', avg_distance )
                        
                
        with col3:            
            df1_aux = avg_std_time_delivery ( df1, 'Yes', 'avg_time' )
            col3.metric ( 'Tempo Médio c/Festivais', df1_aux )
            
            
        with col4:
            df_aux = avg_std_time_delivery ( df1, 'Yes', 'std_time' )
            col4.metric ( 'Desvio Padrão c/Festivais', df1_aux )           
            
            
        with col5:
            df_aux = avg_std_time_delivery ( df1, 'No', 'avg_time' )
            col5.metric ( 'Tempo Médio s/Festivais', df1_aux )           
            
            
        with col6:
            df_aux = avg_std_time_delivery ( df1, 'No', 'std_time' )
            col6.metric ( 'Desvio Padrão s/Festivais', df1_aux)
                                 
            
    with st.container():
        st.markdown("""___""")
        col1, col2 = st.columns ( 2 )
        
        with col1:
        
            st.title( 'Distribuição do Tempo')
            # Usar agg para aplicar duas funções (média e desvio padrão) ao mesmo tempo
            df1_aux = df1.loc [:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})     
            df1_aux.columns = ['avg_time', 'std_time']
            df1_aux = df1_aux.reset_index()
        
            fig = go.Figure()
            fig.add_trace ( go.Bar( name='Control', x=df1_aux['City'], y=df1_aux ['avg_time'], error_y=dict(type='data', array=df1_aux['std_time'])))
            fig.update_layout(barmode = 'group')
            
            #fig.update_layout(width=400, height=300)                      
            st.plotly_chart( fig )  
                        
            
        with col2:
            df1_aux = (df1.loc [:, ['City', 'Type_of_order', 'Time_taken(min)']]
                              .groupby (['City', 'Type_of_order'])
                              .agg({'Time_taken(min)': ['mean', 'std']}))
                
            df1_aux.columns = ['avg_time', 'std_time']
            df1_aux = df1_aux.reset_index()
            
            fig.update_layout(width=200, height=150)
            st.dataframe (df1_aux)
            
            
    with st.container():
        st.markdown("""___""")
        st.title( 'Tempo Médio de Entrega por Cidade' )
        
        col1, col2 = st.columns ( 2 )
        with col1:
            
            
            #Usar agg para aplicar duas funções (média e desvio padrão) ao mesmo tempo
            df1_aux = (df1.loc [:, ['City', 'Road_traffic_density', 'Time_taken(min)']]
                          .groupby (['City', 'Road_traffic_density'])
                          .agg({'Time_taken(min)': ['mean', 'std']}))     
            
            df1_aux.columns = ['avg_time', 'std_time']
            df1_aux = df1_aux.reset_index()
            
            fig = px.sunburst (df1_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time',
                               color = 'std_time', 
                               color_continuous_scale = 'RdBu', 
                               color_continuous_midpoint = np.average(df1_aux['std_time']))
            
            #fig.update_layout(width=400, height=300)
            st.plotly_chart (fig)
            
                                        
        with col2:
            
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1 ['Distance'] = df1.loc [:, cols].apply (lambda x: 
                                                    haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

            avg_distance = df1.loc [:, ['City','Distance']].groupby ('City').mean().reset_index()
            fig = go.Figure ( data =[ go.Pie ( labels = avg_distance ['City'], values = avg_distance ['Distance'], pull =[0, 0.1, 0])])
            
           #fig.update_layout(width=400, height=300)
            st.plotly_chart ( fig )  
            
            
            
