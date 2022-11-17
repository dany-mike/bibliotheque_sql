import streamlit as st
import datetime

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Création de compte")

with st.form("formulaire_compte"):
    today = datetime.date.today()
    st.write()

    nom = st.text_input('Nom')
    st.write('Your name is', nom)
    st.write("Date de naissance")
    d = st.date_input(
        "Date de naissance",
        datetime.date(int(str(today).split('-')[0]), int(str(today).split('-')[1]), int(str(today).split('-')[2])))

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Nom: ", nom, "Date de naissance", d)
