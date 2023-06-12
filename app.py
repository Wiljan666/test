import streamlit as st

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
if 'veiligafstand' not in st.session_state:
    st.session_state.veiligafstand=2

# UI layout
st.set_page_config(layout="wide")

# Colors
venster_kleur = "darkgray"
knoppen_kleur = "steelblue"
tabview_kleur = "lightslategray"

# Functions for generating NC-code
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
        nc_code += "G28U0\n"
        nc_code += "G28W0\n"
        nc_code += "M01(KLAAR)\n"

    st.session_state.nc_code = nc_code




    st.write("Gegenereerde NC-code:")
    st.code(nc_code)

def button_opslaan():
    nc_code = st.session_state.nc_code

    # Save the NC code to a file
    with open("generated_code.txt", "w") as f:
        f.write(nc_code)

    st.write("NC-code succesvol opgeslagen.")

def wijzigenkleur():
    # Verander kleurlogica
    st.set_page_config(page_title="SSV-app", page_icon=":wrench:", layout="wide", initial_sidebar_state="auto", \
                       menu_items={"Get help": None, "Report a bug": ":bug:"})

# UI-componenten
st.title('SSV-app')

# Linkerkolom
st.sidebar.title('Instellingen')

# Input fields
st.sidebar.subheader('Invoer')
toolnummer = st.sidebar.number_input('Toolnummer:', min_value=1, step=1, key='toolnummer')
startposx = st.sidebar.number_input('Startpositie X:', value=0.0, step=0.1, key='startposx')
startposz = st.sidebar.number_input('Startpositie Z:', value=0.0, step=0.1, key='startposz')
eindposz = st.sidebar.number_input('Eindpositie Z:', value=0.0, step=0.1, key='eindposz')
veiligafstand = st.sidebar.number_input('Veiligafstand:', value=2.0, step=0.1, key='veiligafstand')
st.sidebar.subheader('Machine instellingen')
besturing = st.sidebar.selectbox('Besturing:', ['fanuc', 'siemens'], index=0, key='besturing')
decimalen = st.sidebar.selectbox('Decimalen:', ['1', '2', '3', '4'], index=0, key='decimalen')
voeding = st.sidebar.number_input('Voeding:', value=0.0, step=0.1, key='voeding')
rpmvariatie = st.sidebar.number_input('RPM-variatie:', value=0, step=1, key='rpmvariatie')
toerental = st.sidebar.number_input('Toerental:', value=0, step=1, key='toerental')
mmvariatie = st.sidebar.number_input('MM-variatie:', value=0.0, step=0.1, key='mmvariatie')

# Genereer- en Opslaanknoppen
if st.sidebar.button('Genereer', on_click=button_genereer):
    pass

if st.sidebar.button('Opslaan', on_click=button_opslaan):
    pass

# Rechterkolom
st.write('Voeg hier je code voor de rechterkolom toe.')

# Wijzig kleur knop
if st.button('Wijzig kleur'):
    wijzigenkleur()

#streamlit run D:\Wiljan Privé\test\app.py
#cd D:\Wiljan Privé\test chrome app