import pandas as pd 
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import missingno
import altair as alt
# Title
st.write(" # Analyzing Malaysia's COVID dataset") 
st.write('raw data available on [this github repo](https://github.com/owid/covid-19-data/tree/master/public/data)')
# Reading data
data=pd.read_csv('owid-covid-data.csv')
data['date']=pd.to_datetime(data['date'])
data.set_index('date',inplace=True)
data['new tests (per 100,000)']=data['new_tests_per_thousand']*100
data['new deaths (per 100 million)']=data['new_deaths_per_million']*100
data['positive rate (per 100,000)']=data['positive_rate']*1000
data['reproductive rate (times 100)']=data['reproduction_rate']*100
data['new cases (per million)']= data['new_cases_per_million']
data['new deaths (per million)']=data['new_deaths_per_million']
data1=data.copy()

# South east asia data
sea_countries= ['Brunei','Cambodia','Malaysia','Indonesia','Laos','Myanmar','Philippines','Singapore','Thailand','Vietnam']
southeastasia_data=data1.loc[data1['location'].isin(sea_countries)]
southeastasia_data=southeastasia_data.drop(columns=['iso_code', 'continent'])
st.write('South East Asia Data Preview')
if st.checkbox("Show South East Asia Data"):
 st.dataframe(southeastasia_data)

# Selecting country: tests, deaths, cases trends 
country = st.selectbox("New Cases per million by Country: " ,sea_countries)

interval1=alt.selection_interval(encodings=['x'])
base_tests=alt.Chart(southeastasia_data.loc[southeastasia_data['location']==country].reset_index()).mark_line().transform_fold(fold=['new cases (per million)','new tests (per 100,000)', 'reproductive rate (times 100)'], as_=['variable','value']).encode(alt.X('date:T',title='Date'), alt.Y('value:Q',title='Tests and Cases Metrics'), color='variable:N')
chart_tests=base_tests.properties(width=800, height=50, selection=interval1)
view_tests=base_tests.properties(width=800,height=300).encode(x=alt.X('date:T',scale=alt.Scale(domain=interval1.ref())))
st.altair_chart(chart_tests&view_tests)

interval2=alt.selection_interval(encodings=['x'])
base_death=alt.Chart(southeastasia_data.loc[southeastasia_data['location']==country].reset_index()).mark_line().transform_fold(fold=['new cases (per million)','new deaths (per 100 million)'], as_=['variable', 'value']).encode(alt.X('date:T',title='Date'),alt.Y('value:Q',title='Cases and Deaths Metrics'),color='variable:N')
chart_death=base_death.properties(width=800,height=50,selection=interval2)
view_death=base_death.properties(width=800,height=300).encode(alt.X('date:T',scale=alt.Scale(domain=interval2.ref())))
st.altair_chart(chart_death&view_death)

interval3=alt.selection_interval(encodings=['x'])
base=alt.Chart(southeastasia_data.loc[southeastasia_data['location']==country].reset_index()).mark_line().transform_fold(fold=['stringency_index','new cases (per million)'], as_=['variable','value']).encode(alt.X('date:T',title='Date'),alt.Y('value:Q',title='Stringency Index and New Cases Per Million'),color='variable:N')
chart_stringency=base.properties(width=800,height=50,selection=interval3)
view_stringency=base.properties(width=800, height=300).encode(x=alt.X('date:T',scale=alt.Scale(domain=interval3.ref())))
st.altair_chart(chart_stringency&view_stringency)


# Selecting multiple countries
st.write('Choose and compare metrics between different countries')
countries = st.multiselect("Countries: ", sea_countries)
metrics= st.multiselect('Metrics: ', southeastasia_data.columns)
a=alt.Chart(southeastasia_data.loc[southeastasia_data['location'].isin(countries)].reset_index()).mark_line().transform_fold(fold=metrics, as_=['variable', 'value']).encode(alt.X('date:T'),alt.Y('value:Q',title='Metric'), color='variable:N').properties(height=300,width=500)
st.altair_chart(a)










malaysia_data=southeastasia_data.loc[southeastasia_data['location']=='Malaysia']
st.write("Malaysia's Cases Per Million Trend")
st.line_chart(malaysia_data['new_cases_per_million'])


st.write(''' # Stringency index 
1. School opening 
2. Cross state travel restrictions 
3. Restaurant dine in 
4. Mall closure 
5. Non-essential economic sector closure
6. Strict travekl restiction)''')