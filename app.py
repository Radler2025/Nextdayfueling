import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(page_title="Next Day Fueling", page_icon="🚴", layout="centered")

st.title("🚴 Next Day Fueling — Starter App")
st.caption("Minimal funktionsfähige Version für Streamlit Cloud.")

# --- Session state init
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(
        columns=[
            "Datum", "Woche", "Tag",
            "Gewicht_kg", "Recovery_Score", "RPE",
            "Schritte", "Schlaf_h",
            "Brust_cm", "Huefte_cm", "Bauch_cm", "Re_Oberschenkel_cm",
            "GU_kcal", "Training_kcal_PLAN", "Training_kcal_IST",
            "KCAL_gesamt_PLAN", "KCAL_gesamt_IST",
            "Defizit_kcal_Plan", "Defizit_TOTAL",
            "Ernaehrung_GESAMT_inkl_Binge_kcal", "Binge_kcal",
            "Carbs_g", "Fett_g", "Protein_g", "Fluessigkeit_L"
        ]
    )

st.subheader("📥 Tageswerte eingeben")

with st.form("eingabe"):
    col1, col2 = st.columns(2)
    with col1:
        datum = st.date_input("Datum", value=dt.date.today())
        gewicht = st.number_input("Gewicht (kg)", min_value=0.0, step=0.1, value=80.0)
        recovery = st.number_input("Recovery Score (0–100)", min_value=0, max_value=100, step=1, value=70)
        rpe = st.number_input("RPE (1–10)", min_value=1, max_value=10, step=1, value=5)
        schritte = st.number_input("Schritte", min_value=0, step=100, value=8000)
        schlaf = st.number_input("Schlaf (h)", min_value=0.0, step=0.25, value=7.0)
        gu = st.number_input("GU (Grundumsatz) kcal", min_value=0, step=50, value=1900)
    with col2:
        brust = st.number_input("Brust (cm)", min_value=0.0, step=0.5, value=0.0)
        huefte = st.number_input("Hüfte (cm)", min_value=0.0, step=0.5, value=0.0)
        bauch = st.number_input("Bauch (cm)", min_value=0.0, step=0.5, value=0.0)
        robs = st.number_input("Re. Oberschenkel (cm)", min_value=0.0, step=0.5, value=0.0)
        train_plan = st.number_input("Training kcal PLAN", min_value=0, step=50, value=0)
        train_ist = st.number_input("Training kcal IST", min_value=0, step=50, value=0)
        kc_plan = st.number_input("KCAL gesamt PLAN (inkl. Training)", min_value=0, step=50, value=0)
        kc_ist = st.number_input("KCAL gesamt IST (inkl. Training)", min_value=0, step=50, value=0)
        defizit_plan = st.number_input("Defizit kcal (Plan)", min_value=0, step=50, value=500)
        binge = st.number_input("KCAL davon Binge", min_value=0, step=50, value=0)
        carbs = st.number_input("Carbs (g)", min_value=0, step=5, value=0)
        fett = st.number_input("Fett (g)", min_value=0, step=1, value=0)
        protein = st.number_input("Protein (g)", min_value=0, step=1, value=0)
        fluess = st.number_input("Flüssigkeit (L)", min_value=0.0, step=0.1, value=2.0)

    # auto Felder
    woche = int(datum.strftime("%V"))
    tagname = datum.strftime("%A")

    # Defizit TOTAL (vereinfachte Formel): (GU + Training_IST) - KCAL_gesamt_IST
    # Hinweis: Der Nutzer möchte Alltag (niedriger AF) + Trainingskalorien separat addieren.
    # Hier verwenden wir GU + Training_kcal_IST als Verbrauchsseite.
    defizit_total = (gu + train_ist) - kc_ist

    ernaehrung_total = kc_ist  # bereits "KCAL gesamt IST"
    submit = st.form_submit_button("➕ Datensatz speichern")

if submit:
    new_row = {
        "Datum": datum.isoformat(),
        "Woche": woche,
        "Tag": tagname,
        "Gewicht_kg": gewicht,
        "Recovery_Score": recovery,
        "RPE": rpe,
        "Schritte": schritte,
        "Schlaf_h": schlaf,
        "Brust_cm": brust,
        "Huefte_cm": huefte,
        "Bauch_cm": bauch,
        "Re_Oberschenkel_cm": robs,
        "GU_kcal": gu,
        "Training_kcal_PLAN": train_plan,
        "Training_kcal_IST": train_ist,
        "KCAL_gesamt_PLAN": kc_plan,
        "KCAL_gesamt_IST": kc_ist,
        "Defizit_kcal_Plan": defizit_plan,
        "Defizit_TOTAL": defizit_total,
        "Ernaehrung_GESAMT_inkl_Binge_kcal": ernaehrung_total,
        "Binge_kcal": binge,
        "Carbs_g": carbs,
        "Fett_g": fett,
        "Protein_g": protein,
        "Fluessigkeit_L": fluess,
    }
    st.session_state.log = pd.concat([st.session_state.log, pd.DataFrame([new_row])], ignore_index=True)
    st.success("Gespeichert!")

st.divider()
st.subheader("📊 Verlauf (lokal in der Session)")
if st.session_state.log.empty:
    st.info("Noch keine Einträge. Oben Werte ausfüllen und speichern.")
else:
    st.dataframe(st.session_state.log, use_container_width=True)

    # CSV Download
    csv = st.session_state.log.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ CSV herunterladen", csv, file_name="nextdayfueling_log.csv", mime="text/csv")

st.caption("Hinweis: Diese Starter-App speichert Daten nur in der laufenden Session. Für dauerhaftes Speichern können wir Google Sheets, Supabase oder eine CSV im GitHub-Repo anbinden.")
