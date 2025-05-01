
import streamlit as st
import pandas as pd

# Daten laden
historische_angebote = pd.read_csv("historische_angebote.csv")
staffelpreise = pd.read_csv("staffelpreise.csv")

st.set_page_config(page_title="KI-Angebotsdemo", layout="wide")
st.title("KI-Assistenzsystem für Angebotskalkulation")

st.header("1. Kundenanfrage eingeben")

col1, col2 = st.columns(2)

with col1:
    datei = st.file_uploader("Zeichnung oder STEP-Datei hochladen", type=["pdf", "tiff", "step"])
    stueckzahl = st.number_input("Stückzahl", min_value=1, step=1, value=10)

with col2:
    bemerkung = st.text_area("Besonderheiten / Normhinweise", placeholder="z. B. Schweißnaht optisch sauber")

if st.button("Analyse starten"):
    st.header("2. Analyse der Anfrage")

    # Simuliertes Matching
    matched = historische_angebote.sort_values("Ähnlichkeitsquote (%)", ascending=False).head(3)
    st.subheader("Ähnliche historische Angebote")
    st.dataframe(matched)

    st.subheader("Erkannte Unsicherheiten")
    if bemerkung.strip():
        st.warning(f"Hinweis aus Bemerkung: '{bemerkung}' wird für die Normerkennung berücksichtigt.")
    else:
        st.info("Keine weiteren Hinweise erkannt. Möglicherweise fehlen Normangaben.")

    st.header("3. Kalkulationsvorschlag")
    vorschlag = staffelpreise[staffelpreise["Stückzahl"] == stueckzahl]

    if vorschlag.empty:
        st.info("Für diese Stückzahl liegen keine exakten Daten vor. Nächste Staffelpreise werden angezeigt:")
        vorschlag = staffelpreise

    st.subheader("Kalkulierte Zeit und Kosten")
    st.dataframe(vorschlag)

    st.subheader("Empfohlene Angebotsvorlage")
    st.markdown("Basierend auf ähnlichen Angeboten: **Fräsen, Bohren mit Norm DIN 2768-m**")

    st.subheader("Feature-Visualisierung (Demo)")
    st.bar_chart(vorschlag[["Bearbeitungszeit (h)", "Kosten (€)"]].set_index(vorschlag["Stückzahl"].astype(str)))
