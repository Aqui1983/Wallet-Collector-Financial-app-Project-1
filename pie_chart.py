# Pie Chart section 
# I will be using streamlit and Plost to build this Pie Chart.

# Imports
import http.client
import requests
import streamlit as st
import json
import plost

Annual_Salary = st.sidebar.text_input("Please enter your annual Salary")

records = pd.readcsv('database.csv')
