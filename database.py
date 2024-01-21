import streamlit as st
import sqlite3

def CreateTable():
    
    connection = sqlite3.connect('cv.db')
    cursor = connection.cursor()
   
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(500) NOT NULL,
    Email_ID VARCHAR(500) NOT NULL,
    Mobile_No VARCHAR(15) NOT NULL,
    resume_score VARCHAR(8) NOT NULL,
    User_level VARCHAR(30) NOT NULL,
    Predicted_Field VARCHAR(60) NOT NULL,
    Actual_skills VARCHAR(1200) NOT NULL,
    Timestamp VARCHAR(50) NOT NULL)''')
    
    connection.commit()
    connection.close()


def insert_data(name, email, mobile, res_score, cand_level, reco_field, skills, timestamp):
    connection = sqlite3.connect('cv.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user_data (Name,Email_ID,Mobile_No,resume_score,User_level,Predicted_Field,Actual_skills,Timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, email, mobile, str(res_score), cand_level, reco_field, skills, timestamp))
    connection.commit()
    connection.close()
