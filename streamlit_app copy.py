import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# Grundeinstellungen
# ------------------------------------------------------------

st.set_page_config(
    page_title="Guideline Präsenzanteil",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# Datenbasis: Cluster, Items und empirische Gewichtungen
# ------------------------------------------------------------
# WICHTIG:
# relevance = Mittelwert Relevanz aus deiner Umfrage
# presence = Mittelwert Präsenzabhängigkeit aus deiner Umfrage
# Aktuell sind Beispielwerte eingetragen. Diese bitte später ersetzen.

clusters = {
    "Aufgaben und Tätigkeiten": [
        {"item": "Komplexität der Aufgaben im Team", "relevance": 4.2, "presence": 3.8},
        {"item": "Abstimmungsbedarf zwischen Teammitgliedern", "relevance": 4.4, "presence": 4.0},
        {"item": "Kreative oder kollaborative Aufgaben", "relevance": 4.5, "presence": 4.2},
        {"item": "Konzentrierte Einzelarbeit", "relevance": 3.6, "presence": 2.0},
        {"item": "Projektphase", "relevance": 4.0, "presence": 3.7},
    ],
    "Wissensaustausch": [
        {"item": "Informeller Wissensaustausch im Team", "relevance": 4.4, "presence": 4.1},
        {"item": "Spontane Gespräche zwischen Mitarbeitenden", "relevance": 4.2, "presence": 4.0},
        {"item": "Weitergabe von Erfahrungswissen", "relevance": 4.3, "presence": 3.9},
        {"item": "Einarbeitung neuer Mitarbeitender", "relevance": 4.6, "presence": 4.4},
        {"item": "Gemeinsames Lernen im Team", "relevance": 4.1, "presence": 3.6},
    ],
    "Kommunikation": [
        {"item": "Qualität der Kommunikation im Team", "relevance": 4.6, "presence": 3.7},
        {"item": "Vermeidung von Missverständnissen", "relevance": 4.4, "presence": 3.8},
        {"item": "Schnelligkeit von Abstimmungen", "relevance": 4.1, "presence": 3.4},
        {"item": "Klärung komplexer Sachverhalte", "relevance": 4.5, "presence": 4.0},
        {"item": "Qualität von Feedbackprozessen", "relevance": 4.0, "presence": 3.5},
    ],
    "Teamdynamik": [
        {"item": "Teamzusammenhalt", "relevance": 4.5, "presence": 4.0},
        {"item": "Vertrauen innerhalb des Teams", "relevance": 4.4, "presence": 3.8},
        {"item": "Aufbau persönlicher Beziehungen", "relevance": 4.1, "presence": 4.2},
        {"item": "Teamgefühl und Zugehörigkeit", "relevance": 4.3, "presence": 4.0},
        {"item": "Integration neuer Mitarbeitender", "relevance": 4.4, "presence": 4.2},
    ],
    "Mitarbeitendenbezogene Faktoren": [
        {"item": "Flexibilitätsbedürfnis der Mitarbeitenden", "relevance": 4.3, "presence": 1.8},
        {"item": "Individuelle Präferenzen hinsichtlich des Arbeitsortes", "relevance": 4.0, "presence": 1.9},
        {"item": "Arbeitszufriedenheit der Mitarbeitenden", "relevance": 4.4, "presence": 2.2},
        {"item": "Motivation der Mitarbeitenden", "relevance": 4.1, "presence": 2.3},
        {"item": "Vereinbarkeit von Beruf und Privatleben", "relevance": 4.2, "presence": 1.6},
    ],
    "Führung": [
        {"item": "Möglichkeit, Mitarbeitende effektiv zu führen", "relevance": 4.2, "presence": 3.3},
        {"item": "Überblick über Arbeitsfortschritte im Team", "relevance": 3.9, "presence": 2.8},
        {"item": "Steuerung und Koordination der Arbeit", "relevance": 4.1, "presence": 3.2},
        {"item": "Unterstützung der Mitarbeitenden durch Führung", "relevance": 4.0, "presence": 3.1},
        {"item": "Austausch zwischen Führungskraft und Team", "relevance": 4.2, "presence": 3.5},
    ],
    "Effizienz und Produktivität": [
        {"item": "Produktivität der Mitarbeitenden", "relevance": 4.5, "presence": 2.5},
        {"item": "Effizienz der Zusammenarbeit im Team", "relevance": 4.3, "presence": 3.3},
        {"item": "Ablenkungen im Büro", "relevance": 3.2, "presence": 1.8},
        {"item": "Effizienz von Remote-Arbeit", "relevance": 4.0, "presence": 1.6},
        {"item": "Fokus auf Arbeitsergebnisse", "relevance": 4.2, "presence": 1.5},
    ],
    "Teamstruktur": [
        {"item": "Erfahrung des Teams", "relevance": 3.9, "presence": 2.4},
        {"item": "Eingespieltheit des Teams", "relevance": 4.0, "presence": 2.5},
        {"item": "Grad der Selbstorganisation", "relevance": 4.1, "presence": 2.2},
        {"item": "Stabilität der Teamstruktur", "relevance": 3.8, "presence": 2.3},
    ],
}

# ------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------

def empirical_weight(item_data):
    return item_data["relevance"] * item_data["presence"]


def cluster_weight(cluster_items):
    weights = [empirical_weight(item) for item in cluster_items]
    return pd.Series(weights).median()


def calculate_result(scores, max_scores):
    total_score = sum(scores)
    max_score = sum(max_scores)

    if max_score == 0:
        return 0

    return (total_score / max_score) * 100


def recommendation_from_score(score):
    if score < 20:
        return "0–1 Präsenztag pro Woche", "überwiegend Remote-Arbeit"
    elif score < 40:
        return "1–2 Präsenztage pro Woche", "geringer Präsenzanteil"
    elif score < 60:
        return "2–3 Präsenztage pro Woche", "ausgewogenes hybrides Modell"
    elif score < 80:
        return "3–4 Präsenztage pro Woche", "erhöhter Präsenzanteil"
    else:
        return "4–5 Präsenztage pro Woche", "überwiegend Präsenzarbeit"


def show_result(norm_score, cluster_scores):
    recommendation, label = recommendation_from_score(norm_score)

    st.markdown("---")
    st.header("📊 Ergebnis der Guideline")

    st.success(f"**Empfohlener Präsenzanteil: {recommendation}**")
    st.write(f"Einordnung: **{label}**")

    st.progress(int(norm_score))
    st.caption(f"Gesamtscore: {round(norm_score, 1)} von 100 Punkten")

    st.subheader("Wichtigste Treiber der Empfehlung")

    top_clusters = (
        pd.DataFrame(cluster_scores)
        .sort_values(by="Normierter Clusterwert", ascending=False)
        .head(3)
    )

    for _, row in top_clusters.iterrows():
        st.write(f"- **{row['Cluster']}** ({round(row['Normierter Clusterwert'], 1)} Punkte)")

    st.info(
        "Hinweis: Die Empfehlung stellt eine strukturierte Orientierung dar. "
        "Sie ersetzt keine individuelle Managemententscheidung, sondern unterstützt diese "
        "auf Basis empirisch gewichteter Kriterien."
    )


# ------------------------------------------------------------
# Startseite
# ------------------------------------------------------------

st.title("📊 Guideline zur Bestimmung des optimalen Präsenzanteils")

st.markdown("""
### Hintergrund und Ziel der Guideline

Diese Guideline wurde im Rahmen einer wissenschaftlichen Masterarbeit entwickelt. Ziel ist es, Führungskräfte bei der Bestimmung eines geeigneten Verhältnisses von Präsenz- und Remote-Arbeit in hybriden Arbeitsmodellen zu unterstützen.

Die Grundlage bilden qualitative Interviews mit Führungskräften aus der IT-Branche. Aus diesen Interviews wurden zentrale Einflussfaktoren auf den Präsenzanteil abgeleitet. Anschließend wurden diese Faktoren im Rahmen einer quantitativen Erhebung bewertet und empirisch gewichtet.

Auf Basis dieser Ergebnisse wurde ein Entscheidungsmodell entwickelt, das die individuelle Situation eines Teams berücksichtigt und daraus eine Empfehlung für den Präsenzanteil ableitet.

Die Ergebnisse dieser Guideline basieren somit auf einer systematischen wissenschaftlichen Analyse und sind vollständig in der zugrunde liegenden Masterarbeit dokumentiert.

### Nutzung

Sie können zwischen zwei Varianten wählen:

**Kurze Guideline:**  
Diese Variante basiert auf den acht übergeordneten Clustern und liefert eine schnelle Orientierung.

**Ausführliche Guideline:**  
Diese Variante berücksichtigt alle Einzelkriterien innerhalb der Cluster und liefert eine differenziertere Empfehlung.
""")

mode = st.radio(
    "Welche Variante möchten Sie nutzen?",
    ["Kurze Guideline", "Ausführliche Guideline"],
    horizontal=True
)

start = st.button("➡️ Guideline starten")

if start:
    st.session_state["started"] = True

# ------------------------------------------------------------
# Kurze Guideline
# ------------------------------------------------------------

if st.session_state.get("started") and mode == "Kurze Guideline":

    st.header("⚡ Kurze Guideline")
    st.write("Bitte bewerten Sie, wie stark die folgenden Cluster auf Ihr Team zutreffen.")
    st.info("Bewertungsskala: 1 = trifft gar nicht zu | 5 = trifft voll zu")

    cluster_answers = {}
    cluster_scores = []
    scores = []
    max_scores = []

    for cluster_name, items in clusters.items():
        weight = cluster_weight(items)

        cluster_answers[cluster_name] = st.slider(
            cluster_name,
            min_value=1,
            max_value=5,
            value=3,
            help="1 = trifft gar nicht zu | 5 = trifft voll zu"
        )

        score = (cluster_answers[cluster_name] - 1) * weight
        max_score = 4 * weight

        scores.append(score)
        max_scores.append(max_score)

        cluster_scores.append({
            "Cluster": cluster_name,
            "Normierter Clusterwert": (score / max_score) * 100
        })

    calculate_short = st.button("📊 Ergebnis berechnen", key="calculate_short")

    if calculate_short:
        norm_score = calculate_result(scores, max_scores)
        show_result(norm_score, cluster_scores)

# ------------------------------------------------------------
# Ausführliche Guideline
# ------------------------------------------------------------

if st.session_state.get("started") and mode == "Ausführliche Guideline":

    st.header("🧭 Ausführliche Guideline")
    st.write("Bitte bewerten Sie die folgenden Aussagen für Ihr Team.")
    st.info("Bewertungsskala: 1 = trifft gar nicht zu | 5 = trifft voll zu")

    all_answers = {}
    all_scores = []
    all_max_scores = []
    cluster_scores = []

    for cluster_name, items in clusters.items():

        with st.expander(f"🔷 {cluster_name}", expanded=False):

            cluster_item_scores = []
            cluster_item_max_scores = []

            for idx, item_data in enumerate(items):
                key = f"{cluster_name}_{idx}"

                answer = st.slider(
                    item_data["item"],
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=key,
                    help="1 = trifft gar nicht zu | 5 = trifft voll zu"
                )

                weight = empirical_weight(item_data)
                score = (answer - 1) * weight
                max_score = 4 * weight

                all_answers[key] = answer
                all_scores.append(score)
                all_max_scores.append(max_score)

                cluster_item_scores.append(score)
                cluster_item_max_scores.append(max_score)

            cluster_norm = calculate_result(cluster_item_scores, cluster_item_max_scores)

            cluster_scores.append({
                "Cluster": cluster_name,
                "Normierter Clusterwert": cluster_norm
            })

    calculate_long = st.button("📊 Ergebnis berechnen", key="calculate_long")

    if calculate_long:
        norm_score = calculate_result(all_scores, all_max_scores)
        show_result(norm_score, cluster_scores)