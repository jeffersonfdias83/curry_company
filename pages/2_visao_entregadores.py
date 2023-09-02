# Libraries

from haversine import haversine
import plotly.express as px


# Bibliotecas

import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config ( page_title = 'Visão Entregadores', layout = 'wide' )


#=============== Funções ===============================

def entregadores_mais_rapidos ( df1 ):                                                
    df2 = (df1.loc [:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby( ['City','Delivery_person_ID'] )
              .mean()
              .sort_values( ['City','Time_taken(min)'], ascending = True)
              .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian ', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index ( drop = True)
                
    return df3

def entregadores_mais_lentos ( df1 ):            
    df2 = (df1.loc [:, ['Delivery_person_ID','City','Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .mean()
              .sort_values(['City','Time_taken(min)'], ascending = False)
              .reset_index())
    
    df_aux01 = df2.loc [df2['City'] == 'Metropolitian ', :].head(10)
    df_aux02 = df2.loc [df2['City'] == 'Urban ', :].head(10)
    df_aux03 = df2.loc [df2['City'] == 'Semi-Urban ', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index ( drop = True)

    return df3


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

df = pd.read_csv("train(1)")


# Fazendo uma cópia do DataFrame Lido

df1 = df.copy()


# Limpeza de dados

df1 = clean_code ( df )

#===============================
# Barra Lateral
#===============================

image_path = 'logo.jpeg'
image = Image.open (image_path)
st.sidebar.image( image, width=180)

st.header('Marketplace - Visão Entregadores') 

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

weather_options = st.sidebar.multiselect(
    'Quais as condições de climáticas?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default = ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('#### Powered by Jefferson Data Science')

#Filtros Selecionados (Data)

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtros de Trânsito

linhas_selecionadas = df1['Road_traffic_density'].isin (traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

linhas_selecionadas = df1['Weatherconditions'].isin (weather_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

#===============================
# Layout no streamlit
#===============================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', '_', '_'])

with tab1:
    
    with st.container():
        st.header('Overall Metrics' )
        
        col1, col2, col3, col4 = st.columns ( 4, gap = 'large' )
        with col1:
            # A maior idade dos entregadores
            maior_idade = df1.loc [:, 'Delivery_person_Age'].max()
            col1.metric ( 'Maior Idade', maior_idade )

        with col2:
            # A menor idade dos entregadores
            menor_idade = df1.loc [:, 'Delivery_person_Age'].min()
            col2.metric ( 'Menor Idade', menor_idade )
            
        with col3:
            # A melhor condição de veículos
            melhor_veiculo = df1.loc [:, 'Vehicle_condition'].max()
            col3.metric ( 'Melhor Condição', melhor_veiculo )
            
        with col4:
            # A pior condição de veículos
            pior_veiculo = df1.loc [:, 'Vehicle_condition'].min()
            col4.metric ( 'Pior Condição', pior_veiculo )
    
    with st.container():
        st.markdown( """---""")
        st.header('Avaliações' )
        
        col1, col2 = st.columns ( 2 )
        with col1:
            st.markdown ( '##### Avaliação Média por Entregador' )
            df1_avg_media_entregador = ( df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index())
            
            st.dataframe ( df1_avg_media_entregador )
            
        with col2:
            st.markdown ( '##### Avaliação Média por Trânsito' )
            df1_avg_std_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                      .groupby('Road_traffic_density')
                                      .agg({'Delivery_person_Ratings':['mean', 'std']}))
            
            
            # mudança de nome das colunas
            df1_avg_std_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # reset do index
            df1_avg_std_by_traffic = df1_avg_std_by_traffic.reset_index()
            st.dataframe ( df1_avg_std_by_traffic )
                               
            
            st.markdown ( '##### Avaliação Média por Clima' )
            df1_avg_std_by_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                      .groupby('Weatherconditions')
                                      .agg({'Delivery_person_Ratings':['mean', 'std']}))
            
            # mudança de nome das colunas
            df1_avg_std_by_weather.columns = ['delivery_mean', 'delivery_std']
            # reset do index
            df1_avg_std_by_weather = df1_avg_std_by_weather.reset_index()
            st.dataframe ( df1_avg_std_by_weather )
            
         
    with st.container():
        st.markdown( """---""")
        st.header('Velocidade de Entrega' )
        
        col1, col2 = st.columns ( 2 )
        with col1:
            st.markdown ( '##### Top Entregadores Mais Rápidos' )
            df3 = entregadores_mais_rapidos ( df1 )
            st.dataframe ( df3 ) 
                                                   
        with col2:
            st.markdown ( '##### Top Entregadores Mais Lentos' )
            df3 = entregadores_mais_lentos ( df1 )
            st.dataframe ( df3 )
                
            
            
