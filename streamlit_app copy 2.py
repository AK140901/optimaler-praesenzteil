import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Bewertungsmodell Präsenzanteil",
    page_icon="📊",
    layout="wide"
)


# ------------------------------------------------------------
# Datenbasis: 16 Fragen, empirische Gewichtung (R getrennt von P)
# w_r ist innerhalb der 2 aktiven Fragen je Cluster renormiert
# SCORE_MIN/MAX werden dynamisch aus den Daten berechnet
# invert=True: hohe Ausprägung → weniger Präsenzbedarf (6 - A)
# ------------------------------------------------------------

QUESTIONS = [
    {"cluster": "Aufgaben und Tätigkeiten",          "cluster_weight": 0.1249, "question_id": "F1",  "label": "Wie stark ist die Arbeit in Ihrem Team durch kreative oder kollaborative Aufgaben geprägt, die gemeinsames Denken und Zusammenarbeit erfordern?", "short": "Kreative/kollaborative Aufgaben",      "w_r": 0.5050, "p": 3.11627907,   "invert": False},
    {"cluster": "Aufgaben und Tätigkeiten",          "cluster_weight": 0.1249, "question_id": "F2",  "label": "In welcher Phase befinden sich die aktuellen Projekte Ihres Teams überwiegend?",                                                                    "short": "Projektphase",                   "w_r": 0.4950, "p": 3.0,           "invert": False, "help": "1 = reine Umsetzung/Routinearbeit, 5 = Projektstart/Konzeptionsphase"},
    {"cluster": "Wissensaustausch",                  "cluster_weight": 0.1333, "question_id": "F3",  "label": "Wie viele neue Mitarbeitende befinden sich aktuell in der Einarbeitungsphase oder werden in den nächsten drei Monaten ins Team integriert?",         "short": "Onboarding",                     "w_r": 0.5373, "p": 4.255813953,  "invert": False, "help": "1 = keine, 5 = mehrere gleichzeitig"},
    {"cluster": "Wissensaustausch",                  "cluster_weight": 0.1333, "question_id": "F4",  "label": "Wie stark ist informeller Wissensaustausch – also ungeplante Gespräche und spontanes Teilen von Erfahrungen – ein relevanter Bestandteil der täglichen Arbeit in Ihrem Team?", "short": "Informeller Wissensaustausch",    "w_r": 0.4627, "p": 3.488372093,  "invert": False},
    {"cluster": "Kommunikation",                     "cluster_weight": 0.1205, "question_id": "F5",  "label": "Wie komplex und vielschichtig sind die Kommunikationsinhalte in Ihrem Team typischerweise?",                                                        "short": "Qualität der Kommunikation",     "w_r": 0.5264, "p": 2.88372093,   "invert": False, "help": "z. B. viele Rückfragen, Nuancen, nonverbale Signale erforderlich"},
    {"cluster": "Kommunikation",                     "cluster_weight": 0.1205, "question_id": "F6",  "label": "Wie stark sind regelmäßige, differenzierte Feedbackgespräche zwischen Ihnen und Ihren Teammitgliedern ein zentraler Bestandteil Ihrer Führungsarbeit?", "short": "Feedbackprozesse",              "w_r": 0.4736, "p": 3.23255814,   "invert": False},
    {"cluster": "Teamdynamik",                       "cluster_weight": 0.1511, "question_id": "F7",  "label": "Wie wichtig ist es in Ihrem Team, dass neue Mitarbeitende schnell sozial integriert werden und ein Zugehörigkeitsgefühl zur Gruppe entwickeln?",     "short": "Integration neuer Mitarbeitender","w_r": 0.5212, "p": 4.279069767,  "invert": False},
    {"cluster": "Teamdynamik",                       "cluster_weight": 0.1511, "question_id": "F8",  "label": "Wie stark ist ein ausgeprägtes Teamgefühl und ein gemeinsames Wir-Bewusstsein für die Leistungsfähigkeit Ihres Teams relevant?",                    "short": "Teamgefühl und Zugehörigkeit",   "w_r": 0.4788, "p": 3.790697674,  "invert": False},
    {"cluster": "Mitarbeitendenbezogene Faktoren",   "cluster_weight": 0.1421, "question_id": "F9",  "label": "Wie stark ist die Motivation Ihrer Teammitglieder von sozialer Interaktion, gemeinsamem Arbeiten und dem direkten Austausch mit Kolleginnen und Kollegen abhängig?", "short": "Motivation",              "w_r": 0.4901, "p": 2.720930233,  "invert": False},
    {"cluster": "Mitarbeitendenbezogene Faktoren",   "cluster_weight": 0.1421, "question_id": "F10", "label": "Wie stark beeinflusst der physische Arbeitsort nach Ihrer Einschätzung die Arbeitszufriedenheit Ihrer Teammitglieder?",                              "short": "Arbeitszufriedenheit",           "w_r": 0.5099, "p": 2.581395349,  "invert": False},
    {"cluster": "Führung",                           "cluster_weight": 0.1047, "question_id": "F11", "label": "Wie stark sind Sie als Führungskraft auf direkte Beobachtung, spontane Gespräche und physische Präsenz angewiesen, um Ihr Team effektiv zu führen?", "short": "Effektive Führung",              "w_r": 0.5167, "p": 2.953488372,  "invert": False},
    {"cluster": "Führung",                           "cluster_weight": 0.1047, "question_id": "F12", "label": "Wie häufig und wie intensiv sind ungeplante, bilaterale Gespräche zwischen Ihnen und einzelnen Teammitgliedern ein Bestandteil Ihres Führungsalltags?", "short": "Austausch Führungskraft–Team", "w_r": 0.4833, "p": 2.976744186,  "invert": False},
    {"cluster": "Effizienz und Produktivität",       "cluster_weight": 0.1208, "question_id": "F13", "label": "Wie stark hängt die Effizienz der Zusammenarbeit in Ihrem Team davon ab, dass Personen gleichzeitig am selben Ort arbeiten und direkt interagieren können?", "short": "Effizienz der Zusammenarbeit","w_r": 0.5120, "p": 2.813953488,  "invert": False},
    {"cluster": "Effizienz und Produktivität",       "cluster_weight": 0.1208, "question_id": "F14", "label": "Wie sehr profitiert die Produktivität Ihrer Teammitglieder von der gemeinsamen physischen Anwesenheit im Büro?",                                     "short": "Produktivität",                  "w_r": 0.4880, "p": 2.604651163,  "invert": False, "help": "z. B. durch schnellere Abstimmungen oder gegenseitige Motivation"},
    {"cluster": "Teamstruktur",                      "cluster_weight": 0.1025, "question_id": "F15", "label": "Wie eingespielt und routiniert arbeitet Ihr Team zusammen?",                                                                                          "short": "Eingespieltheit",                "w_r": 0.5152, "p": 2.976744186,  "invert": True,  "help": "1 = Team arbeitet erst kurz zusammen / hat sich stark verändert, 5 = langjähriges, sehr eingespieltes Team"},
    {"cluster": "Teamstruktur",                      "cluster_weight": 0.1025, "question_id": "F16", "label": "Wie stabil ist die Zusammensetzung Ihres Teams?",                                                                                                     "short": "Stabilität der Teamstruktur",    "w_r": 0.4848, "p": 3.0,           "invert": True,  "help": "1 = häufige Wechsel / Restrukturierungen, 5 = konstantes Team ohne wesentliche Veränderungen"},
]

# Dynamisch berechnete Score-Grenzen (alle A=1 bzw. alle A=5)
SCORE_MIN = 4.427
SCORE_MAX = 14.782


# ------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------

def effective_answer(answer: int, invert: bool) -> int:
    return 6 - answer if invert else answer


def contribution(answer: int, w_r: float, p: float) -> float:
    return answer * w_r * p


def map_score_to_percent(score: float) -> float:
    percent = ((score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)) * 100
    return max(0.0, min(100.0, percent))


def recommendation_from_score(score: float):
    if score <= 7.02:
        return "0–1 Präsenztag pro Woche", "Remote-first", "Ihr Team weist insgesamt eine geringe Präsenznotwendigkeit auf."
    elif score <= 9.60:
        return "1–2 Präsenztage pro Woche", "Hybrid-flexibel", "Für Ihr Team spricht vieles für ein flexibles hybrides Modell mit begrenzter Präsenz."
    elif score <= 12.19:
        return "2–3 Präsenztage pro Woche", "Hybrid-präsenzorientiert", "Mehrere Faktoren sprechen für einen spürbaren Nutzen regelmäßiger Präsenzzeiten."
    else:
        return "4–5 Präsenztage pro Woche", "Präsenz-first", "Die Ausprägung Ihres Teamkontexts spricht für einen hohen Nutzen physischer Zusammenarbeit."


def calculate_model(answers: dict):
    cluster_results = []
    total_score = 0.0

    cluster_map = {}
    for q in QUESTIONS:
        cluster_map.setdefault(q["cluster"], []).append(q)

    for cluster_name, items in cluster_map.items():
        cw = items[0]["cluster_weight"]
        cluster_inner = 0.0
        cluster_inner_min = 0.0
        cluster_inner_max = 0.0
        detail_rows = []

        for q in items:
            raw = answers[q["question_id"]]
            eff = effective_answer(raw, q["invert"])
            val = contribution(eff, q["w_r"], q["p"])
            val_min = contribution(1, q["w_r"], q["p"])
            val_max = contribution(5, q["w_r"], q["p"])

            cluster_inner += val
            cluster_inner_min += val_min
            cluster_inner_max += val_max

            detail_rows.append({
                "Frage": q["question_id"],
                "Kriterium": q["short"],
                "Antwort": raw,
                "Eff. Antwort": eff,
                "P̄": round(q["p"], 2),
                "Beitrag": round(val, 4),
            })

        weighted = cw * cluster_inner
        weighted_min = cw * cluster_inner_min
        weighted_max = cw * cluster_inner_max
        cluster_norm = 0.0
        if weighted_max > weighted_min:
            cluster_norm = ((weighted - weighted_min) / (weighted_max - weighted_min)) * 100

        total_score += weighted
        cluster_results.append({
            "Cluster": cluster_name,
            "Clustergewicht": cw,
            "Clusterbeitrag": weighted,
            "Normierter Clusterwert": cluster_norm,
            "Details": pd.DataFrame(detail_rows),
        })

    overall_percent = map_score_to_percent(total_score)
    return total_score, overall_percent, cluster_results


def show_result(total_score: float, overall_percent: float, cluster_results: list):
    recommendation, label, explanation = recommendation_from_score(total_score)

    st.markdown("---")
    st.header("📊 Ergebnis des Bewertungsmodells")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.success(f"**Empfohlener Präsenzanteil: {recommendation}**")
        st.write(f"Einordnung: **{label}**")
        st.write(explanation)
        st.progress(int(round(overall_percent)))
        st.caption(f"Modellscore: {total_score:.2f} (Skala: {SCORE_MIN}–{SCORE_MAX}) | normiert: {overall_percent:.1f} / 100")

    with col2:
        st.markdown("**Score-Bereiche**")
        st.markdown("""
| Score | Empfehlung |
|---|---|
| 4,43 – 7,02 | Remote-first (≤ 1 Tag) |
| 7,02 – 9,60 | Hybrid-flexibel (1–2 Tage) |
| 9,60 – 12,19 | Hybrid-präsenzorientiert (2–3 Tage) |
| 12,19 – 14,78 | Präsenz-first (4–5 Tage) |
""")

    st.subheader("Stärkste Treiber der Empfehlung")
    cluster_df = pd.DataFrame([
        {"Cluster": c["Cluster"], "Normierter Clusterwert": round(c["Normierter Clusterwert"], 1), "Clusterbeitrag": round(c["Clusterbeitrag"], 3)}
        for c in cluster_results
    ]).sort_values(by="Normierter Clusterwert", ascending=False)

    for _, row in cluster_df.head(3).iterrows():
        st.write(f"- **{row['Cluster']}** ({row['Normierter Clusterwert']:.1f} / 100 Punkte)")

    st.subheader("Clusterübersicht")
    st.dataframe(cluster_df, use_container_width=True, hide_index=True)

    st.subheader("Detailansicht je Cluster")
    for cluster in cluster_results:
        with st.expander(f"🔷 {cluster['Cluster']}"):
            st.dataframe(cluster["Details"], use_container_width=True, hide_index=True)

    st.info(
        "Hinweis: Die Empfehlung stellt eine strukturierte Orientierung dar. "
        "Sie ersetzt keine individuelle Managemententscheidung, sondern unterstützt diese "
        "auf Basis empirisch gewichteter Kriterien aus der zugrunde liegenden Untersuchung."
    )


# ------------------------------------------------------------
# Startseite
# ------------------------------------------------------------

st.title("📊 Bewertungsmodell zur Bestimmung des optimalen Präsenzanteils")

st.markdown("""
### Hintergrund und Ziel des Bewertungsmodells

Dieses Bewertungsmodell wurde im Rahmen einer wissenschaftlichen Masterarbeit entwickelt.
Ziel ist es, Führungskräfte bei der Bestimmung eines geeigneten Verhältnisses von Präsenz-
und Remote-Arbeit in hybriden Arbeitsmodellen zu unterstützen.

Die Grundlage bilden qualitative Interviews mit Führungskräften aus der IT-Branche sowie
eine anschließende quantitative Erhebung zur Gewichtung der identifizierten Einflussfaktoren.
Das Modell berechnet auf Basis von **16 empirisch gewichteten Fragen** einen Gesamtscore,
der einer konkreten Präsenzempfehlung zugeordnet wird.
""")

st.info("Bewertungsskala: 1 = trifft gar nicht zu / sehr gering  |  5 = trifft voll zu / sehr stark")

if "started" not in st.session_state:
    st.session_state["started"] = False

if st.button("➡️ Bewertungsmodell starten"):
    st.session_state["started"] = True

if st.session_state["started"]:
    answers = {}
    current_cluster = None

    for q in QUESTIONS:
        if q["cluster"] != current_cluster:
            current_cluster = q["cluster"]
            st.markdown(f"---\n## {current_cluster}")

        help_text = q.get("help", "1 = trifft gar nicht zu  |  5 = trifft voll zu")
        answers[q["question_id"]] = st.slider(
            f"**{q['question_id']}** – {q['label']}",
            min_value=1,
            max_value=5,
            value=3,
            key=q["question_id"],
            help=help_text,
        )

    st.markdown("---")
    if st.button("📊 Ergebnis berechnen"):
        total_score, overall_percent, cluster_results = calculate_model(answers)
        show_result(total_score, overall_percent, cluster_results)