
import streamlit as st
import math

st.set_page_config(page_title="Kaiser Predictor PRO", page_icon="⚽")
st.title("⚽ Kaiser Predictor PRO")
st.caption("Estimateur de probabilités — aucun score n'est garanti.")

st.subheader("1. Informations du match")
mode = st.selectbox("Type de match", ["Football réel", "FIFA virtuel 4 minutes", "FIFA virtuel 6 minutes"])
domicile = st.text_input("Équipe / joueur 1", "Paris")
exterieur = st.text_input("Équipe / joueur 2", "Barcelona")

st.subheader("2. Statistiques estimées")
c1, c2 = st.columns(2)
with c1:
    buts_dom = st.number_input("Buts moyens marqués par l'équipe 1", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
    encaisses_dom = st.number_input("Buts moyens encaissés par l'équipe 1", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
with c2:
    buts_ext = st.number_input("Buts moyens marqués par l'équipe 2", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
    encaisses_ext = st.number_input("Buts moyens encaissés par l'équipe 2", min_value=0.0, max_value=10.0, value=1.3, step=0.1)

def poisson(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

if st.button("Analyser le match"):
    if not domicile.strip() or not exterieur.strip():
        st.error("Entre les deux noms d'équipe ou de joueur.")
    else:
        lam1 = (buts_dom + encaisses_ext) / 2
        lam2 = (buts_ext + encaisses_dom) / 2
        scores = []
        victoire1 = nul = victoire2 = 0.0
        for i in range(8):
            for j in range(8):
                p = poisson(i, lam1) * poisson(j, lam2)
                scores.append((p, i, j))
                if i > j:
                    victoire1 += p
                elif i == j:
                    nul += p
                else:
                    victoire2 += p
        st.subheader("3. Probabilités 1N2")
        st.write(f"**1 — {domicile} gagne :** {victoire1:.1%}")
        st.write(f"**N — Match nul :** {nul:.1%}")
        st.write(f"**2 — {exterieur} gagne :** {victoire2:.1%}")
        st.subheader("4. Cinq scores exacts estimés")
        for p, i, j in sorted(scores, reverse=True)[:5]:
            st.write(f"{domicile} {i} – {j} {exterieur} : {p:.1%}")
        st.info("Ces calculs sont des estimations mathématiques basées sur les moyennes saisies, pas des données vérifiées de 1xBet. Les matchs virtuels peuvent être très imprévisibles.")
