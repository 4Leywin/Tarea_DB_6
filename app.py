import streamlit as st
# import streamlit_authenticator as stauth

from db import register_user, login_user, get_email, init_db
from hash import hash_password_bcrypt, hash_password_argon2,hash_double

class App:
    def __init__(self):
        st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')
        init_db()
        st.title("Aplicacion de autenticacion")
        self.menu()
    def menu(self):
        menu = ["Home", "Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Home":
            self.home_page()
        elif choice == "Login":
            self.login_page()
        elif choice == "Register":
            self.register_page()
        
    def login_page(self):
        st.write("Iniciar sesión")
        # form
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")
        if submit_button:
            user_db = login_user((email, password))
            if user_db:
                st.success("¡Inicio de sesión exitoso!")
                # st.write(user_db)
                # navigate to home page
            else:
                st.error("Usuario o contraseña incorrectos")                
        
    def register_page(self):
        st.write("Registro de usuario")
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Register")
        if submit_button:
            password = self.cypher_password(password,'bcrypt')
            status_register = register_user((name, email, password))
            if status_register:
                st.success("Usuario registrado correctamente")
            else:    
                st.error("Error al registrar usuario")
                            
    def cypher_password(self, password,type_method):
        if type_method == "bcrypt":
            return hash_password_bcrypt(password)
        elif type_method == "argon2":
            return hash_password_argon2(password)
        elif type_method == "double":
            return hash_double(password)
        else:
            return None
    
    def home_page(self):
        st.write("Home Page")
        st.write("Usuario autenticado")

app = App()