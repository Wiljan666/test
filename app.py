import streamlit as st

user_credentials = [ ("admin", "admin"),("heinie", "heinie"),("a","a"),("",""),("Jelmer", "jelmer")]


def button_genereer():
    toolnummer = st.session_state.toolnummer
    gereedschap = str(toolnummer)
    startposx = float(st.session_state.startposx)
    startposz = float(st.session_state.startposz)
    eindposz = float(st.session_state.eindposz)
    mmvariatie = float(st.session_state.mmvariatie)
    veiligafstand = float(st.session_state.veiligafstand)
    besturing = st.session_state.besturing
    decimalen = st.session_state.decimalen
    rpmvariatie = int(st.session_state.rpmvariatie)
    toerental = int(st.session_state.toerental)
    voeding = float(st.session_state.voeding)
    huidigetoerental = toerental

    huidigez = startposz
    if mmvariatie >= eindposz:
        spindelkant = 'G54'
    else:
        spindelkant = 'G55'

    if besturing == 'fanuc':
        spindelcommando = 'S'
        if toolnummer <= 10:
            gereedschap = '0' + str(toolnummer) + '0' + str(toolnummer)
        elif toolnummer >= 10:
            gereedschap = str(toolnummer) + str(toolnummer)
    elif besturing == 'siemens':
        spindelcommando = 'S1='
        gereedschap = str(toolnummer) + 'D1'

    nc_code = "(SSV)\n"
    nc_code += f"{spindelkant}G40G90G49\n"
    nc_code += f"T{gereedschap}\n"

    if mmvariatie >= eindposz:
        nc_code += f"G0Z{startposz + veiligafstand:.{decimalen}f}\n"
    else:
        nc_code += f"G0Z{startposz - veiligafstand:.{decimalen}f}\n"
    nc_code += f"X{startposx + veiligafstand:.{decimalen}f}\n"
    nc_code += f"G01X{startposx:.{decimalen}f}F{voeding}\n"
    nc_code += f"Z{huidigez:.{decimalen}f}\n"
    nc_code += "M01(STARTPOSITIE CONTROLEREN)\n\n"
    nc_code += f"G97{spindelcommando}{huidigetoerental}M03\n"
    huidigez -= mmvariatie

    while huidigez >= eindposz:
        if huidigetoerental >= toerental:
            huidigetoerental -= rpmvariatie
            nc_code += f"Z{huidigez:.{decimalen}f} {spindelcommando}{huidigetoerental}\n"
            huidigez -= mmvariatie
        else:
            huidigetoerental += rpmvariatie
            nc_code += f"Z{huidigez:.{decimalen}f} {spindelcommando}{huidigetoerental}\n"
            huidigez -= mmvariatie

    if huidigez + mmvariatie < eindposz:
        while huidigez <= eindposz:
            if huidigetoerental >= toerental:
                huidigetoerental -= rpmvariatie
                nc_code += f"G01Z{huidigez:.{decimalen}f} {spindelcommando}{huidigetoerental}\n"
                huidigez += mmvariatie
            else:
                huidigetoerental += rpmvariatie
                nc_code += f"G01Z{huidigez:.{decimalen}f} {spindelcommando}{huidigetoerental}\n"
                huidigez += mmvariatie
    else:
        nc_code += f"Z{eindposz:.{decimalen}f}\n"
        nc_code += f"X{startposx + veiligafstand:.{decimalen}f}\n"
        if mmvariatie >= eindposz:
            nc_code += f"G0Z{startposz + veiligafstand:.{decimalen}f}\n"
        else:
            nc_code += f"G0Z{startposz - veiligafstand:.{decimalen}f}\n"
        nc_code += "M05\n"
    if besturing == 'fanuc':
        nc_code += "G28U0\n"
        nc_code += "G28W0\n"
    elif besturing == 'siemens':
        nc_code += "G0 G90 G53X(DOOR GEBRUIKER OP TE GEVEN VEILIGE WAARDE)\n"
        nc_code += "G0 G90 G53Z(DOOR GEBRUIKER OP TE GEVEN VEILIGE WAARDE)\n"
        
        nc_code += "M01(KLAAR)\n"

    st.session_state.nc_code = nc_code




    st.write("Gegenereerde NC-code:")
    st.code(nc_code)


def login(username, password):
    for user, pwd in user_credentials:
        if user.lower() == username.lower() and pwd == password.lower():
            return True
    return False

def main():
    st.set_page_config(layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_app()
    else:
        show_login()
        
        
def show_login():
    st.title("Inloggen")

    if st.session_state.logged_in:
        hide_login()
        show_app()
    else:
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type="password")

        login_button = st.button("Inloggen")

        if login_button:
            if login(username, password):
                st.session_state.logged_in = True
                hide_login()
                st.experimental_rerun()#show_app()
            else:
                st.error("Ongeldige gebruikersnaam of wachtwoord")

def hide_login():
    # Verberg het inlogscherm
    st.empty()



def show_app():
    if not st.session_state.logged_in:
        show_login()
        return
    
    # Initialize session state variables
    if 'toolnummer' not in st.session_state:
        st.session_state.toolnummer = 12
    if 'startposx' not in st.session_state:
        st.session_state.startposx = 13.8
    if 'startposz' not in st.session_state:
        st.session_state.startposz = 2
    if 'eindposz' not in st.session_state:
        st.session_state.eindposz = -99
    if 'besturing' not in st.session_state:
        st.session_state.besturing = 'fanuc'
    if 'veiligafstand' not in st.session_state:
        st.session_state.veiligafstand = 2.0
    if 'decimalen' not in st.session_state:
        st.session_state.decimalen = '3'
    if 'mmvariatie' not in st.session_state:
        st.session_state.mmvariatie= 2
    if 'rpmvariatie' not in st.session_state:
        st.session_state.rpmvariatie=150
    if 'toerental' not in st.session_state:
        st.session_state.toerental=1500
    if 'voeding' not in st.session_state:
        st.session_state.voeding=0.1
    

    # Colors
    venster_kleur = "darkgray"
    knoppen_kleur = "steelblue"
    tabview_kleur = "lightslategray"

    # Functions for generating NC-code

    # UI-componenten
    st.title('SSV-app')

    # Linkerkolom
    st.sidebar.title('Instellingen')

    # Input fields
    st.sidebar.subheader('Invoer')
    toolnummer = st.sidebar.number_input('Toolnummer:', min_value=1, step=1, key='toolnummer')
    startposx = st.sidebar.number_input('Startpositie X:', step=0.1, key='startposx')
    startposz = st.sidebar.number_input('Startpositie Z:', step=0.1, key='startposz')
    eindposz = st.sidebar.number_input('Eindpositie Z:',  step=0.1, key='eindposz')
    veiligafstand = st.sidebar.number_input('Veiligafstand:', step=0.1, key='veiligafstand')
    st.sidebar.subheader.expander('Machine instellingen')
    besturing = st.sidebar.selectbox('Besturing:', ['fanuc', 'siemens'], index=0, key='besturing')
    decimalen = st.sidebar.selectbox('Decimalen:', ['1', '2', '3', '4'], index=0, key='decimalen')
    voeding = st.sidebar.number_input('Voeding:',  step=0.1, key='voeding')
    rpmvariatie = st.sidebar.number_input('RPM-variatie:',  step=1, key='rpmvariatie')
    toerental = st.sidebar.number_input('Toerental:',  step=1, key='toerental')
    mmvariatie = st.sidebar.number_input('MM-variatie:',  step=0.1, key='mmvariatie')

    # Genereer- en Opslaanknoppen
    if st.sidebar.button('Genereer', on_click=button_genereer):
        pass

    # Rechterkolom
    st.write("""Druk links onderin op 'genereer' en de NC-code wordt hier zichtbaar.""")

    # UI-componenten en logica van de app
    # Voeg hier de rest van je app logica toe

if __name__ == '__main__':
    main()
