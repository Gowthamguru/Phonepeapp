#Import important libraries
import streamlit as st
from streamlit_option_menu import option_menu
from  explore import  exploreapp
from charts import  chartsapp

# Set the Page configuration
st.set_page_config(
    page_title="PhonePe Pulse Transactions",
    layout="wide",
    initial_sidebar_state="expanded")

# Define the Home content
def homecontent():
    st.markdown(
    "<h2 style='color: #230B43; font-family:Arial; text-align:center;'>Phonepe data visualization</h2>",
    unsafe_allow_html=True
    )
    st.markdown('''<h3> User friendly tool to explore the data</h3>''',unsafe_allow_html=True)
    st.markdown('''<h4>Domain : </h4> <p>Finance and Payment Systems</p>''',unsafe_allow_html=True)
    st.markdown('''<h4>Technologies Used : </h4> <p>Github,Python,Mysql,Streamlit,pandas,mysql-connector,sqlachemy</p>''',unsafe_allow_html=True)
    st.markdown('''<h4>Overview : </h4> <p>In the Streamlit app you can visualize the phonepe plus transactions of user,insurance and top records with the chart and geographical view</p>''',unsafe_allow_html=True)

# Sidebar menu

# Inject custom CSS for sidebar width
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 270px !important;      /* sidebar width */
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 270px !important;      /* actual content area width */
    }
    </style>
""", unsafe_allow_html=True)
# Define the Sidebar
with st.sidebar:
    selected = option_menu(None, ["Home", 'Top Charts','Explore Data'],
                           icons=['house', 'activity','kanban'], menu_icon="cast", default_index=0,
    styles = {
        "container": {"padding": "2!important", "background-color": "#230B43"},
        "icon": {"color": "orange", "font-size": "16px"},
        "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px",
                     "--hover-color": "#391C59"},
        "nav-link-selected": {"background-color": "#391C59"}, }
    )

# Define the sidebar menu select event
if selected =="Home":
    homecontent()
if selected == "Explore Data":
    exploreapp()
if selected == "Top Charts":
    chartsapp()