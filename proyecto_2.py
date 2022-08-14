
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import io 
from datetime import date
from pyexpat import features
import seaborn as sns
import matplotlib.pyplot as plt




sidebar = st.container()

data = pd.read_csv('report/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')

data['date'] = pd.to_datetime(data['date'])

data.drop(data.filter(regex='anticipated'), axis=1, inplace=True)
data.drop(data.filter(regex='suspected'), axis=1, inplace=True)
data.drop(data.filter(regex='numerator|denominator'), axis=1, inplace=True)

data.fillna(0, inplace=True)



with st.sidebar:
    choose = option_menu("Proyecto_Covid", ["Inicio", "Camas UCI", "Ocupación", "Conclusiones"],
                         icons=['house', 'building', 'reception-4', 'book'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#5e5c5c"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#121111"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


logo = Image.open(r'report/SARS-CoV-2_without_background.png')
if choose == "Inicio":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Proyecto Final COVID</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=130 )
    
    st.write("El siguiente boceto tiene en cuenta el conjunto de datos agregados  por estado para la utilización del hospital por parte de los departamentos de salud estatales/territoriales en nombre de sus centros de atención médica y (3) la Red Nacional de Seguridad de la Atención Médica (antes del 15 de julio), que corresponden a USA, con datos tomados durante la pandemia.\n\nCOVID-19 Impacto en los pacientes y capacidad hospitalaria informados por estado Timeseries https://dev.socrata.com/foundry/healthdata.gov/g62h-syeh")    
    


    
    st.subheader('Muertes por Covid-19 USA')
    df_geo = pd.DataFrame(data, columns= ['state',
                                        'deaths_covid'])
    st.write(df_geo.groupby(by='state',as_index=False).sum().sort_values(by='deaths_covid', ascending=False))
    df_geo.set_index('state', inplace = True)

    df_geo.reset_index('state', inplace = True)
    
    fig = px.choropleth(df_geo,
                    locations= df_geo['state'],
                    locationmode="USA-states",
                    scope='usa',
                    color=df_geo['deaths_covid'],
                    color_continuous_scale="hot_r",
        
                    )

    fig.update_layout(
                        title_text='Muertes por COVID-19 por estado en USA',
                        geo_scope='usa',

                    )

    profile = Image.open(r'report/newplot.png')
    st.image(profile, width=1000)

if choose == "Camas UCI":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #d6cec6;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Uso de Camas UCI por estado</p>', unsafe_allow_html=True) 


    with col2:               # To display the header text using css style
        st.image(logo, width=130 )
    st.write('Total de uso de camas UCI(Unidades de cuidados intensivos). Con las columnas utilizadas(staffed_adult_icu_bed_occupancy) y (staffed_pediatric_icu_bed_occupancy)')
    
    st.subheader('Ranking de Ocupación de camas por estado')

    porcentaje_uci = pd.DataFrame()

    uci = pd.DataFrame()

    uci['Fecha'] = data['date']
    uci['Estado'] = data['state']
    uci['Ocupación_de_camas_de_UCI_para_adultos_con_personal'] = data['staffed_adult_icu_bed_occupancy']
    uci['Ocupación_de_camas_en_la_UCI_pediátrica_con_personal'] = data['staffed_pediatric_icu_bed_occupancy']

        # Agrupacion por Estado
    estados_2 = uci.groupby('Estado').sum([['Ocupación_de_camas_de_UCI_para_adultos_con_personal'],['Ocupación_de_camas_en_la_UCI_pediátrica_con_personal']])
    estados_2['total_camas_uci'] = estados_2['Ocupación_de_camas_de_UCI_para_adultos_con_personal'] + estados_2['Ocupación_de_camas_en_la_UCI_pediátrica_con_personal']
    st.write(estados_2.groupby("Estado").sum().sort_values(by="total_camas_uci", ascending=False).head(10))

    estados_2.reset_index('Estado', inplace = True)

    fig, ax = plt.subplots()
    sns.lineplot(x='Estado', y='total_camas_uci', data=estados_2, ax=ax)
    plt.gcf().set_size_inches(15, 8)
    st.pyplot(fig)
    

    
    st.subheader('Porcentaje camas UCI por estado, en el año 2020')
    profile = Image.open('report/Total_camas2.box.jpg')
    st.image(profile, width=700 )
    

    

if choose == "Ocupación":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #d6cec6;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Estados con ocupación hospitalaria por COVID</p>', unsafe_allow_html=True) 


    with col2:               # To display the header text using css style
        st.image(logo, width=130 )
    st.write('Estados con mayor ocupación hospitalaria por COVID. Las columnas utilizadas son : (total_adult_patients_hospitalized_confirmed_covid)(staffed_icu_adult_patients_confirmed_covid)(total_pediatric_patients_hospitalized_confirmed_covid)')  
    st.subheader('Ranking de estador con mayor ocupación hospilataria')

    camas = pd.DataFrame()



    camas['Fecha'] = data['date']
    camas['Estado'] = data['state']
    camas['Camas_UCI'] = data['total_adult_patients_hospitalized_confirmed_covid']
    camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_UCI'] = data['staffed_icu_adult_patients_confirmed_covid']
    camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_hospitalización_pediátrica'] = data['total_pediatric_patients_hospitalized_confirmed_covid']

    # Pasando a INT  total_adult_patients_hospitalized_confirmed_covid
    camas['Camas_UCI'] = camas['Camas_UCI'].astype(int)

    # Pasando a INT  total_pediatric_patients_hospitalized_confirmed_covid
    camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_UCI'] = camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_UCI'].astype(int)

    # Pasando a INT  total_pediatric_patients_hospitalized_confirmed_covid
    camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_hospitalización_pediátrica'] = camas['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_hospitalización_pediátrica'].astype(int)

    # Camas por estados
    camas_estado = camas.groupby('Estado').sum([['Camas_UCI'],['hospitalización_cama_covid_utilización'],['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_UCI']])

    camas_estado['Mayor_Ocupacion'] = camas_estado['Camas_UCI'] + camas_estado['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_UCI'] + camas_estado['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_hospitalización_pediátrica'] +  camas_estado['Pacientes_informados_actualmente_hospitalizados_en_una_cama_de_hospitalización_pediátrica']

    st.write(camas_estado.sort_values(by="Mayor_Ocupacion", ascending=False).head(5))

    fig, ax = plt.subplots()
    sns.lineplot(x='Estado', y='Mayor_Ocupacion', data=camas_estado, ax=ax)
    plt.gcf().set_size_inches(15, 8)

    
    st.pyplot(fig)

    st.subheader('Ranking de Ocupación de camas hospitalaria por estado, en el primer semestre del año 2020')
    profile = Image.open('report/ranking_estados.jpg')
    st.image(profile, width=700 )


if choose == "Conclusiones":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #d6cec6;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Conclusiones</p>', unsafe_allow_html=True) 


    with col2:               # To display the header text using css style
        st.image(logo, width=130 )
    st.write('Tomando conclusiones del analisis realizado del trabajo, fue que el peor mes de la pandemia fue el 21-01 que fue el mes que mas hubo Muertes por covid. Y tambien fue donde hubo reporte de falta de personal Medico.') 
    st.subheader('Muertes por COVID')
    profile = Image.open(r'report/deaths_covid.jpg')
    st.image(profile, width=700 )

    st.subheader('Falta de personal medico')
    profile = Image.open(r'report/falta_de_personal.jpg')
    st.image(profile, width=700 )

    st.subheader('Relación entre muertes y falta de personal medico')
    profile = Image.open(r'report/relacion_muertes_falta_de_personal.jpg')
    st.image(profile, width=700 )
    

    st.write('Con respecto a los recursos hospilatarios, recomendaria una mayor inversión en temas de recursos, para futuros problemas como lo que paso con pandemia, recursos como camas, respiradores, etc.Se recomienda tambien contar con una mayor de personal capacitado, para tiempos de pandemía, que fueron bastantes escasos en comparación a como a sucedido la pandemia por COVID')   
    






    


