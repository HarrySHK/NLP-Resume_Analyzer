import streamlit as st
import pandas as pd
import base64,random
import sqlite3
import plotly.express as px


def to_1D(series):
    return pd.Series([x.replace('[', '').replace(']', '') for _list in series for x in _list.split(", ")])

def AdminUser():
    ## Admin Side
        
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'wajid' and ad_password == 'wajid123' or ad_user == 'Muhammad Haris' and ad_password == 'haris123' or ad_user == 'shayan' and ad_password == 'shiraz123':
                st.success("Welcome Admin")
                st.write('''<b>Vistors</b> <img src="https://counter4.optistats.ovh/private/freecounterstat.php?c=baukt6rkh7fz3ee4l3r9g31b29hrmq17"
                             border="0"></a> 
                         ''', unsafe_allow_html=True)
                
              
                connection = sqlite3.connect('cv.db')
                cursor = connection.cursor()
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email','Mobile_No', 'Resume Score','User Level','Predicted_Field','Actual Skills', 'Timestamp'])
                st.dataframe(df)
                st.markdown(get_csv_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                
                # Admin Side Data
                query = 'SELECT * FROM user_data;'
                plot_data = pd.read_sql(query, connection)
          
                # Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                values = plot_data.Predicted_Field.value_counts()
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(names=labels, values=values, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)
          
                # Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("📈 **Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(names=labels, values=values, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)  
        else:
             st.error("Wrong ID & Password Provided")

def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
