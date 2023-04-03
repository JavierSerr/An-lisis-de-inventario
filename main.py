#Python3.9.16
#Run the app by typing into the terminal prompt 'streamlit run main.py'

#Download the packagery
#make sure you have all of the requirements updated

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import random as rnd
import datetime as dt

#Declare random seed
rnd.seed(5)

#Read database for today 
inventory=pd.read_excel(
    io= 'Data_9-02-23.xlsx',
    engine= 'openpyxl',
    sheet_name= 'Inventory',
    skiprows= 2,
    usecols= 'A:G',
    nrows= 29,
    dtype={'SKU': str}
)
proyection=pd.read_excel(
    io= 'Data_9-02-23.xlsx',
    engine= 'openpyxl',
    sheet_name= 'Proyections',
    skiprows= 2,
    usecols= 'A:G',
    nrows= 29,
    dtype={'SKU': str}
)
restock=pd.read_excel(
    io= 'Data_9-02-23.xlsx',
    engine= 'openpyxl',
    sheet_name= 'Restock',
    skiprows= 2,
    usecols= 'A:G',
    nrows= 29,
    dtype={'SKU': str}
)

#Configure dashboard
st.set_page_config(page_title= 'Dahsboard',
                    page_icon= ':briefcase:',
                    layout= 'wide')

#Configure sidebar
st.sidebar.header('Filter')

#Category filter
category = st.sidebar.multiselect(
    'Select the category: ',
    options= inventory['Category'].unique(),
    default= 'Drinks'
)
df_selection = inventory.query(
    "Category == @category"
)
proy_selection = proyection.query(
    "Category == @category"
)
res_selection = restock.query(
    "Category == @category"
)
#Subcategory filter
sub_category = st.sidebar.multiselect(
    'Select the sub-category: ',
    options= df_selection['Subcategory'].unique(),
)
df_selection = df_selection.query(
    "Subcategory == @sub_category"
)
proy_selection = proy_selection.query(
    "Subcategory == @sub_category"
)
res_selection = res_selection.query(
    "Subcategory == @sub_category"
)
#Product filter
product = st.sidebar.multiselect(
    'Select the product: ',
    options= df_selection['Product'],
    default= df_selection['Product']
)
df_selection = df_selection.query(
    "Product == @product"
)
proy_selection = proy_selection.query(
    "Product == @product"
)
res_selection = res_selection.query(
    "Product == @product"
)

#Site filter
site = st.sidebar.multiselect(
    'Select a site: ',
    options= ['A','B','C'],
    default= ['A','B','C']
)
if ('A' in site)==False:
    df_selection = df_selection.drop('Units A', axis = 1)
    proy_selection = proy_selection.drop('Units A', axis = 1)
    res_selection = res_selection.drop('Units A', axis = 1)
if ('B' in site)==False:
    df_selection = df_selection.drop('Units B', axis = 1)
    proy_selection = proy_selection.drop('Units B', axis = 1)
    res_selection = res_selection.drop('Units B', axis = 1)
if ('C' in site)==False:
    df_selection = df_selection.drop('Units C', axis = 1)
    proy_selection = proy_selection.drop('Units C', axis = 1)
    res_selection = res_selection.drop('Units C', axis = 1)

#Obtain total
df_selection['Total']= df_selection.iloc[:,4:].sum(axis=1)
proy_selection['Total']= proy_selection.iloc[:,4:].sum(axis=1)
res_selection['Total']= res_selection.iloc[:,4:].sum(axis=1)

#Make up historic data
data_inv=pd.DataFrame({'Day':range(0,-60,-1)})
data_proy=pd.DataFrame({'Day':range(0,-60,-1)})
data_res=pd.DataFrame({'Day':range(0,-60,-1)})

#For every selected product make up historics
for i in range(len(df_selection)):
    #Create empty rows
    new_row_inv=np.zeros(60)
    new_row_proy=np.zeros(60)
    new_row_res=np.zeros(60)    

    #Set end value according to xlsx file
    new_row_inv[-1] = df_selection.iloc[i,-1]
    new_row_proy[-1] = proy_selection.iloc[i,-1]
    new_row_res[-1] = res_selection.iloc[i,-1]

    #declare a random weight(rate of inventory gorwth)
    weight = (rnd.random()-0.5)*2
    for k in range(0,59):
        new_row_inv[k]= np.rint(df_selection.iloc[i,-1]- 60*weight + k*weight + rnd.random()*10)
        new_row_proy[k]= np.rint(proy_selection.iloc[i,-1]- 60*weight*2/3 + 2*k*weight/3 + rnd.random()*5)
        new_row_res[k]= np.rint(res_selection.iloc[i,-1]- 60*weight/2 + k*weight/2 + rnd.random()*10-5)
    data_inv[df_selection.iloc[i,1]] = new_row_inv.tolist()
    data_proy[proy_selection.iloc[i,1]] = new_row_proy.tolist()
    data_res[res_selection.iloc[i,1]] = new_row_res.tolist()

#Design figures
fig_inventory = px.line(
    data_inv,
    x= 'Day',
    y= data_inv.columns[1:],
    title='Inventory'
)
fig_proyection = px.line(
    data_proy,
    x= 'Day',
    y= data_proy.columns[1:],
    title='14-day proyections'
)
fig_restock = px.line(
    data_res,
    x= 'Day',
    y= data_res.columns[1:],
    title='Restock history'
)


#Plot the figures in 3 columns
#left_column, middle_column, right_column = st.columns(3)
#left_column.plotly_chart(fig_inventory, use_container_width=True)
#middle_column.plotly_chart(fig_proyection, use_container_width=True)
#right_column.plotly_chart(fig_restock, use_container_width=True)


#st.dataframe(df_selection)

#Plot the charts
st.plotly_chart(fig_inventory, use_container_width=True)
st.plotly_chart(fig_proyection, use_container_width=True)
st.plotly_chart(fig_restock, use_container_width=True)


