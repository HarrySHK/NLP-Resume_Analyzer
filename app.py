###### Importing Required Modules ######

import streamlit as st
from streamlit_option_menu import option_menu

###### Importing Required User-Defined Modules ######

from user import NormalUser
from admin import AdminUser
from selection_tool import Selection_Tool
from about import About


###### Main function run() ######
def main():
    st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon='jojo.png')
    
    selected=option_menu(
        menu_title="WSH Resume Analyzer",
        options = ["Resume","Selection-Tool", "About", "Admin"],
        icons=["file-earmark-break","person-bounding-box","person-workspace","gear"],
        menu_icon="emoji-laughing",
        default_index=0,
        orientation="horizontal",)
    
    st.title("AI Resume Analyser")
   
    ###### Code for client side (USER) ######

    if selected == 'Resume':
        NormalUser()
        html_code = '<p style="display:inline;">Total Resume Scanned till now: </p> <a href="https://www.hitwebcounter.com" target="_blank"><img src="https://hitwebcounter.com/counter/counter.php?page=8423204&style=0006&nbdigits=5&type=page&initCount=0" title="Free Counter" Alt="web counter" border="0" /></a>'
        st.markdown(html_code, unsafe_allow_html=True)
        
    elif selected=='Selection-Tool':
        Selection_Tool()

    ###### Code for About Page  ######
        
    elif selected == 'About':
        About()

    ###### Code for Admin Side ######
        
    else:
        AdminUser()

    
        
###### Main Function ######
        
if __name__ == "__main__":
    main()
