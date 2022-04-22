import pandas as pd
import streamlit as st
import prepocessor,helper
import altair as alt
df=pd.read_csv('us_counties_covid19_daily.csv')
df_fin=prepocessor.preprocess(df)
st.sidebar.title("Covid19 US Dashboard")
st.sidebar.image('https://www.cdc.gov/media/dpk/diseases-and-conditions/coronavirus/images/outbreak-coronavirus-world-1024x506px.jpg?_=31301')
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








      
