import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
from vega_datasets import data
import prepocessor,helper
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from PIL import Image


st.sidebar.image('https://www.cdc.gov/media/dpk/diseases-and-conditions/coronavirus/images/outbreak-coronavirus-world-1024x506px.jpg?_=31301')
st.sidebar.title("Covid19 Visualizations")

#---------------------------------------------------------------------------
#LULU'S CODE - USED IN BASE_DATAFRAME AND INTERACTIVE_TOTAL_CASES_BAR_CHART
@st.cache
def load_data():
    df1 = pd.read_csv('datasets/us_states_covid19_daily.csv')
    return df1

df1 = load_data()

columns_to_show = ['positive', 'negative', 'hospitalizedCurrently','hospitalizedCumulative','state']
df1.groupby(["state"])[columns_to_show].agg([np.max])
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
#BASE_DATAFRAME
if st.sidebar.checkbox('Show Base Dataframe'):
    st.write(df1)
#---------------------------------------------------------------------------


    

#---------------------------------------------------------------------------
#INTERACTIVE_TOTAL_CASES_BAR_CHART
if st.sidebar.checkbox('Total Cases Bar Chart'):    
    st.title('Total Covid-19 Cases By State in 2020')   
    sel_state = st.selectbox('Select State', df1.state)
    chart = alt.Chart(df1.reset_index()).mark_bar().encode(
        x="state:N",
        y="positive:Q",
        color=alt.condition(
            alt.datum.state == sel_state, # if state equals selected state 
            alt.value('orange'),     
            alt.value('steelblue')  
        )
    ).properties(
        width=600,
        height=400
    )
    st.write(chart)
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
# LULU_PIE_CHART (Doesn't seem to be working so commenting it out for now)

# st.write(chart)
# st.title('Cumulative Hospitalizations')
# df1=df1.sort_index(ascending=False)

# chart2 = alt.Chart(df1.head(5)).mark_arc().encode(
    # theta=alt.Theta(field="hospitalizedCumulative", type="quantitative"),
    # color=alt.Color(field="state", type="nominal"),
# )
# st.write(chart2)
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
#FELIPE_CHOROPLETH_MAPS
if st.sidebar.checkbox('Show Choropleth Map'):
    
    #function for the two choropleth maps
    def ch_map(selection):
    
        #gets states base map
        states = alt.topo_feature(data.us_10m.url, 'states')
    
        #gets total positive cases and writes map
        if (selection == 'Total Positive'):
            st.title('Total Positive Cases (2020)') 
            ch = pd.read_csv('sub_datasets/total_positive.csv')
            ch.columns = ['Index', 'State', 'Positive']
            ch_map = alt.Chart(states).mark_geoshape().encode(
                color='Positive:Q',
                tooltip=['id:O', 'Positive:Q']
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(ch, 'Index', ['Positive'])
            ).project(
                type='albersUsa'
            ).properties(
                width=600,
                height=400
            )
            st.write(ch_map)
        
        #gets total negative cases and writes map
        if (selection == 'Total Negative'):
            st.title('Total Negative Cases (2020)') 
            ch = pd.read_csv('sub_datasets/total_negative.csv')
            ch.columns = ['Index', 'State', 'Negative']
            ch_map = alt.Chart(states).mark_geoshape().encode(
                color='Negative:Q',
                tooltip=['id:O', 'Negative:Q']
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(ch, 'Index', ['Negative'])
            ).project(
                type='albersUsa'
            ).properties(
                width=600,
                height=400
            )
            st.write(ch_map)
            
    #Creates a select box and then calls the ch_map function        
    selection = st.selectbox('Select One:',
                             ('Total Positive', 'Total Negative'))
    ch_map(selection)
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
#LULU'S PICS - EXTRA VISUALIZATIONS (Linear Regression)
if st.sidebar.checkbox('More Visualizations'):  
  
    image1 = Image.open('pictures/1.png')
    image2 = Image.open('pictures/2.png')
    image3 = Image.open('pictures/3.png')
    image4 = Image.open('pictures/4.png')
    
    st.image(image1, caption="")
    st.image(image2, caption="")
    st.image(image3, caption="")
    st.image(image4, caption="")
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
#SAI_VISUALIZATIONS

df=pd.read_csv('datasets/us_counties_covid19_daily.csv')
df_fin=prepocessor.preprocess(df)
st.sidebar.title("Covid19 US Dashboard")
user_menu= st.sidebar.radio('Select a Dashboard to dispaly',
    ("countywise Dashboard","State and county Monthwise dashboard","statewise cases and deaths comparsion",
    "countywise cases and deaths comparsion in particular state")
)

if user_menu =='countywise Dashboard':
    st.sidebar.title('Filtering Options')
    cols=df_fin['state'].dropna().unique().tolist()
    cols.sort()
    selected_state=st.sidebar.selectbox('select a state',cols)
    df_2=helper.countywise_cases_deaths(df_fin,selected_state)
    print(df_2)
    st.title("Countywise Covid cases in " +" "+ selected_state+" "+"for year 2020")
    map3= alt.Chart(df_2).mark_bar().encode(
        x ='county:O',
        y =alt.Y('cases:Q',title='Total  No of cases'),
        tooltip=['county:O',alt.Tooltip('cases:Q', title=" Total No of cases")]
    ).properties(
    width=1000,
    height=400).interactive()
    st.altair_chart(map3)

    st.title("Countywise Covid deaths in " +" "+ selected_state+" "+"for year 2020")
    map4= alt.Chart(df_2).mark_bar().encode(
        x ='county:O',
        y =alt.Y('deaths:Q',title='Total  No of deaths'),
        tooltip=['county:O',alt.Tooltip('deaths:Q', title=" Total No of deaths")]
    ).properties(
    width=1000,
    height=400).interactive()
    st.altair_chart(map4)


if user_menu == 'State and county Monthwise dashboard':
    st.sidebar.title('Filtering Options')
    cols=df_fin['state'].dropna().unique().tolist()
    cols.sort()
    # cols_OA=['Overall']
    # cols_OA.extend(cols)
    selected_state=st.sidebar.selectbox('select a state',cols)

    df_c=df_fin[df_fin['state']==selected_state]
    cols_county=df_c['county'].dropna().unique().tolist()
    cols_county.sort()
    # cols_county_OA=['Overall']
    # cols_county_OA.extend(cols_county)
    selected_county=st.sidebar.selectbox('select a county',cols_county)

    df_1=helper.covidcases_state_countywise(df_fin,selected_state,selected_county)
    #print(df_1)

    st.title("Monthswise Covid cases in " +" "+ selected_state+" "+ "for county"+"  "+selected_county)
    map1= alt.Chart(df_1).mark_bar().encode(
        x ='month:O',
        y =alt.Y('cases:Q',title='Total  No of Cases'),
        tooltip=['month:Q',alt.Tooltip('cases:Q', title=" Total No of cases")]
    ).properties(
    width=700,
    height=400).interactive()
    st.altair_chart(map1)

    st.title("Monthswise Covid deaths in " +" "+ selected_state+" "+ "for county"+"  "+selected_county)
    map2= alt.Chart(df_1).mark_bar().encode(
        x ='month:O',
        y =alt.Y('deaths:Q',title='Total  No of deaths'),
        tooltip=['month:Q',alt.Tooltip('deaths:Q', title=" Total No of deaths")]
    ).properties(
    width=700,
    height=400).interactive()
    st.altair_chart(map2)


if user_menu=='statewise cases and deaths comparsion':
    st.sidebar.title('Filtering Options')
    cols=df_fin['state'].dropna().unique().tolist()      
    selected_state=st.sidebar.multiselect('select one or more state(s):',cols,default=['North Carolina'])
    cases_total=helper.get_cases_total(df_fin,selected_state)
    #print(cases_total)
    map5= alt.Chart(cases_total).mark_line().encode(
            x ='month:O',
            y =alt.Y('cases:Q',title='Total Cases'),
            color='state:N',
            tooltip=['month:Q',alt.Tooltip('cases:Q', title=" Total cases")]
            ).properties(
            width=700,
            height=400,title="Total Cases").interactive()
    st.altair_chart(map5)

    map6= alt.Chart(cases_total).mark_line().encode(
            x ='month:O',
            y =alt.Y('deaths:Q',title='Total deaths'),
            color='state:N',
            tooltip=['month:Q',alt.Tooltip('deaths:Q', title=" Total deaths")]
            ).properties(
            width=700,
            height=400,title="Total deaths").interactive()
    st.altair_chart(map6)

if user_menu=='countywise cases and deaths comparsion in particular state':
    st.sidebar.title('Filtering Options')
    cols=df_fin['state'].dropna().unique().tolist()
    cols.sort()
    selected_state=st.sidebar.selectbox('select a state',cols)

    df_c=df_fin[df_fin['state']==selected_state]
    cols_county=df_c['county'].dropna().unique().tolist()
    cols_county.sort()
    selected_county=st.sidebar.multiselect('select one or more county(s):',cols_county,default=cols_county[0])
    county_cases_total=helper.get_countycases_comparsion(df_fin,selected_state,selected_county)
    #print(county_cases_total)

    map7= alt.Chart(county_cases_total).mark_line().encode(
            x ='month:O',
            y =alt.Y('cases:Q',title='Total Cases'),
            color='county:N',
            tooltip=['month:Q',alt.Tooltip('cases:Q', title=" Total cases")]
            ).properties(
            width=700,
            height=400,title="Total Cases").interactive()
    st.altair_chart(map7)

    map8= alt.Chart(county_cases_total).mark_line().encode(
            x ='month:O',
            y =alt.Y('deaths:Q',title='Total deaths'),
            color='county:N',
            tooltip=['month:Q',alt.Tooltip('deaths:Q', title=" Total deaths")]
            ).properties(
            width=700,
            height=400,title="Total deaths").interactive()
    st.altair_chart(map8)
    #---------------------------------------------------------------------------
