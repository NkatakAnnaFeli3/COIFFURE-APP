import streamlit as st
from datetime import datetime, time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Le Salon de Anna Félix", page_icon="✂️")

# --- TITRE PRINCIPAL ---
st.title("✂️ Le Salon de Anna Félix")
st.markdown("---")

# --- INITIALISATION DES DONNÉES (Simulation de base de données) ---
if 'reservations' not in st.session_state:
    st.session_state['reservations'] = []

# --- SECTION 1 : HORAIRES D'OUVERTURE ---
st.sidebar.header("📅 Horaires d'Ouverture")
horaires = {
    "Lundi - Vendredi": "09:00 - 19:00",
    "Samedi": "09:00 - 17:00",
    "Dimanche": "Fermé"
}

for jour, heure in horaires.items():
    st.sidebar.write(f"**{jour}** : {heure}")

# Vérification du statut actuel
now = datetime.now()
current_time = now.time()
current_day = now.strftime("%A")

# Logique simplifiée pour le statut ouvert/fermé
is_open = False
if current_day != "Sunday":
    if time(9, 0) <= current_time <= time(19, 0):
        is_open = True

if is_open:
    st.success("🟢 Le salon est actuellement **OUVERT**.")
else:
    st.error("🔴 Le salon est actuellement **FERMÉ**.")

# --- SECTION 2 : RÉSERVATION ---
st.header("📅 Prendre un rendez-vous")

with st.form("form_reservation"):
    nom = st.text_input("Votre nom complet")
    service = st.selectbox("Choisissez un service", ["Coupe Femme", "Coupe Homme", "Coloration", "Brushing", "Soin Capillaire"])
    date_rdv = st.date_input("Date souhaitée", min_value=datetime.today())
    heure_rdv = st.time_input("Heure souhaitée")
    
    submit_button = st.form_submit_button("Réserver maintenant")

    if submit_button:
        if nom:
            # Enregistrement dans l'état de la session
            nouvelle_resa = {
                "id": len(st.session_state['reservations']) + 1,
                "nom": nom,
                "service": service,
                "date": date_rdv.strftime("%d/%m/%Y"),
                "heure": heure_rdv.strftime("%H:%M")
            }
            st.session_state['reservations'].append(nouvelle_resa)
            st.balloons()
            st.success(f"Merci {nom} ! Votre rendez-vous pour '{service}' est confirmé.")
        else:
            st.warning("Veuillez entrer votre nom pour réserver.")

# --- SECTION 3 : GESTION DES RÉSERVATIONS (Annulation) ---
st.markdown("---")
st.header("📋 Mes Réservations")

if not st.session_state['reservations']:
    st.info("Aucune réservation pour le moment.")
else:
    # Affichage des réservations existantes
    for i, resa in enumerate(st.session_state['reservations']):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{resa['nom']}** - {resa['service']} le {resa['date']} à {resa['heure']}")
        
        with col2:
            # Bouton d'annulation
            if st.button(f"Annuler", key=f"btn_{i}"):
                st.session_state['reservations'].pop(i)
                st.rerun() # Rafraîchit l'application pour mettre à jour la liste

# --- PIED DE PAGE ---
st.markdown("---")
st.caption("© 2024 Le Salon de Anna Félix - 123 Rue de la Coiffure, Paris")