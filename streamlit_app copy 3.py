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

HELP_TEXT = "1 = trifft gar nicht zu | 5 = trifft voll zu"

# ------------------------------------------------------------
# Empirische Gewichtungen aus Phase 2
# relevance = Mittelwert Relevanz
# presence = Mittelwert Präsenzabhängigkeit
# ------------------------------------------------------------

criteria = {
    "k1": {"name": "Komplexität der Aufgaben", "relevance": 3.181818182, "presence": 2.545454545},
    "k2": {"name": "Abstimmungsbedarf zwischen Teammitgliedern", "relevance": 3.613636364, "presence": 2.727272727},
    "k3": {"name": "Durchführung kreativer oder kollaborativer Aufgaben", "relevance": 3.477272727, "presence": 3.136363636},
    "k4": {"name": "Durchführung konzentrierter Einzelarbeit", "relevance": 3.295454545, "presence": 1.613636364},
    "k5": {"name": "Phase des Projekts", "relevance": 3.409090909, "presence": 3.0},

    "k6": {"name": "Informeller Wissensaustausch im Team", "relevance": 3.818181818, "presence": 3.5},
    "k7": {"name": "Spontane Gespräche und Austausch zwischen Mitarbeitenden", "relevance": 3.386363636, "presence": 3.272727273},
    "k8": {"name": "Weitergabe von Erfahrungswissen", "relevance": 3.25, "presence": 3.113636364},
    "k9": {"name": "Einarbeitung neuer Mitarbeitender", "relevance": 4.454545455, "presence": 4.25},
    "k10": {"name": "Gemeinsames Lernen im Team", "relevance": 3.25, "presence": 3.227272727},

    "k11": {"name": "Qualität der Kommunikation im Team", "relevance": 3.590909091, "presence": 2.909090909},
    "k12": {"name": "Vermeidung von Missverständnissen", "relevance": 3.409090909, "presence": 2.795454545},
    "k13": {"name": "Schnelligkeit von Abstimmungen", "relevance": 3.090909091, "presence": 2.75},
    "k14": {"name": "Klärung komplexer Sachverhalte", "relevance": 3.045454545, "presence": 3.136363636},
    "k15": {"name": "Qualität von Feedbackprozessen", "relevance": 3.272727273, "presence": 3.25},

    "k16": {"name": "Teamzusammenhalt", "relevance": 4.159090909, "presence": 3.75},
    "k17": {"name": "Vertrauen innerhalb des Teams", "relevance": 3.704545455, "presence": 3.522727273},
    "k18": {"name": "Aufbau persönlicher Beziehungen", "relevance": 4.0, "presence": 3.909090909},
    "k19": {"name": "Teamgefühl und Zugehörigkeit", "relevance": 4.159090909, "presence": 3.795454545},
    "k20": {"name": "Integration neuer Mitarbeitender", "relevance": 4.545454545, "presence": 4.272727273},

    "k21": {"name": "Bedürfnis der Mitarbeitenden nach Flexibilität", "relevance": 3.818181818, "presence": 2.5},
    "k22": {"name": "Individuelle Präferenzen hinsichtlich des Arbeitsortes", "relevance": 3.681818182, "presence": 2.409090909},
    "k23": {"name": "Arbeitszufriedenheit der Mitarbeitenden", "relevance": 3.977272727, "presence": 2.568181818},
    "k24": {"name": "Motivation der Mitarbeitenden", "relevance": 3.818181818, "presence": 2.75},
    "k25": {"name": "Vereinbarkeit von Beruf und Privatleben", "relevance": 4.068181818, "presence": 2.204545455},

    "k26": {"name": "Möglichkeit, Mitarbeitende effektiv zu führen", "relevance": 3.272727273, "presence": 2.954545455},
    "k27": {"name": "Überblick über Arbeitsfortschritte im Team", "relevance": 2.318181818, "presence": 2.295454545},
    "k28": {"name": "Steuerung und Koordination der Arbeit", "relevance": 2.704545455, "presence": 2.522727273},
    "k29": {"name": "Unterstützung der Mitarbeitenden durch Führung", "relevance": 2.795454545, "presence": 2.727272727},
    "k30": {"name": "Austausch zwischen Führungskraft und Team", "relevance": 3.068181818, "presence": 3.0},

    "k31": {"name": "Produktivität der Mitarbeitenden", "relevance": 3.340909091, "presence": 2.613636364},
    "k32": {"name": "Effizienz der Zusammenarbeit im Team", "relevance": 3.477272727, "presence": 2.840909091},
    "k33": {"name": "Ablenkungen im Büro", "relevance": 3.068181818, "presence": 2.568181818},
    "k34": {"name": "Effizienz von Remote-Arbeit", "relevance": 3.295454545, "presence": 2.090909091},
    "k35": {"name": "Fokus auf Arbeitsergebnisse", "relevance": 3.25, "presence": 2.431818182},

    "k36": {"name": "Erfahrung des Teams", "relevance": 3.340909091, "presence": 2.818181818},
    "k37": {"name": "Eingespieltheit des Teams", "relevance": 3.5, "presence": 3.0},
    "k38": {"name": "Grad der Selbstorganisation", "relevance": 3.704545455, "presence": 2.590909091},
    "k39": {"name": "Stabilität der Teamstruktur", "relevance": 3.295454545, "presence": 3.022727273},
}

# ------------------------------------------------------------
# Leitfragen
# direction:
# presence = hoher Wert erhöht Präsenzbedarf
# remote = hoher Wert reduziert Präsenzbedarf
# ------------------------------------------------------------

questions = {
    "q1": {
        "dimension": "Aufgaben und Tätigkeiten",
        "text": "Wie stark ist Ihr Team im Arbeitsalltag auf gemeinsame Abstimmung und koordinierte Zusammenarbeit angewiesen?",
        "direction": "presence",
        "criteria": ["k1", "k2"],
    },
    "q2": {
        "dimension": "Aufgaben und Tätigkeiten",
        "text": "Wie häufig erfordert die Arbeit Ihres Teams kreative oder kollaborative Problemlösungen?",
        "direction": "presence",
        "criteria": ["k3"],
    },
    "q3": {
        "dimension": "Aufgaben und Tätigkeiten",
        "text": "Wie stark basiert die Arbeit Ihres Teams auf konzentrierter und individuell ausführbarer Einzelarbeit?",
        "direction": "remote",
        "criteria": ["k4"],
    },
    "q4": {
        "dimension": "Aufgaben und Tätigkeiten",
        "text": "Wie häufig befindet sich Ihr Team in Projektphasen mit erhöhtem Abstimmungs- und Koordinationsbedarf?",
        "direction": "presence",
        "criteria": ["k5"],
    },

    "q5": {
        "dimension": "Wissensaustausch und Lernen",
        "text": "Wie wichtig ist spontaner und informeller Wissensaustausch für die tägliche Zusammenarbeit Ihres Teams?",
        "direction": "presence",
        "criteria": ["k6", "k7"],
    },
    "q6": {
        "dimension": "Wissensaustausch und Lernen",
        "text": "Wie stark basiert die Arbeit Ihres Teams auf Erfahrungswissen und gemeinsamem Lernen?",
        "direction": "presence",
        "criteria": ["k8", "k10"],
    },
    "q7": {
        "dimension": "Wissensaustausch und Lernen",
        "text": "Wie häufig werden neue Mitarbeitende in Ihr Team integriert oder eingearbeitet?",
        "direction": "presence",
        "criteria": ["k9"],
    },

    "q8": {
        "dimension": "Kommunikation und Abstimmung",
        "text": "Wie wichtig sind direkte und schnelle Abstimmungen für die Arbeitsfähigkeit Ihres Teams?",
        "direction": "presence",
        "criteria": ["k11", "k13"],
    },
    "q9": {
        "dimension": "Kommunikation und Abstimmung",
        "text": "Wie häufig müssen in Ihrem Team komplexe Sachverhalte gemeinsam geklärt werden?",
        "direction": "presence",
        "criteria": ["k14"],
    },
    "q10": {
        "dimension": "Kommunikation und Abstimmung",
        "text": "Wie wichtig ist die Vermeidung von Missverständnissen und Kommunikationsfehlern in Ihrem Arbeitsalltag?",
        "direction": "presence",
        "criteria": ["k12"],
    },
    "q11": {
        "dimension": "Kommunikation und Abstimmung",
        "text": "Wie relevant sind persönliche und situationsbezogene Feedbackprozesse in Ihrem Team?",
        "direction": "presence",
        "criteria": ["k15"],
    },

    "q12": {
        "dimension": "Teamdynamik und soziale Einbindung",
        "text": "Wie wichtig sind persönlicher Kontakt und soziale Interaktion für den Zusammenhalt Ihres Teams?",
        "direction": "presence",
        "criteria": ["k16", "k19"],
    },
    "q13": {
        "dimension": "Teamdynamik und soziale Einbindung",
        "text": "Wie stark basiert die Zusammenarbeit Ihres Teams auf gegenseitigem Vertrauen und persönlichen Beziehungen?",
        "direction": "presence",
        "criteria": ["k17", "k18"],
    },
    "q14": {
        "dimension": "Teamdynamik und soziale Einbindung",
        "text": "Wie wichtig ist die soziale Integration neuer Mitarbeitender für die Stabilität Ihres Teams?",
        "direction": "presence",
        "criteria": ["k20"],
    },

    "q15": {
        "dimension": "Mitarbeitendenbezogene Faktoren",
        "text": "Wie hoch ist das Bedürfnis Ihrer Mitarbeitenden nach räumlicher Flexibilität und individueller Arbeitsgestaltung?",
        "direction": "remote",
        "criteria": ["k21", "k22"],
    },
    "q16": {
        "dimension": "Mitarbeitendenbezogene Faktoren",
        "text": "Welche Bedeutung haben hybride Arbeitsmöglichkeiten für Zufriedenheit und Motivation Ihrer Mitarbeitenden?",
        "direction": "remote",
        "criteria": ["k23", "k24", "k25"],
    },

    "q17": {
        "dimension": "Führung",
        "text": "Wie stark basiert Ihre Führungsarbeit auf persönlichem Austausch und unmittelbarer Interaktion mit dem Team?",
        "direction": "presence",
        "criteria": ["k29", "k30"],
    },
    "q18": {
        "dimension": "Führung",
        "text": "Wie wichtig ist direkte Präsenz für die Steuerung und Koordination Ihres Teams?",
        "direction": "presence",
        "criteria": ["k26", "k27", "k28"],
    },

    "q19": {
        "dimension": "Effizienz und Produktivität",
        "text": "Wie stark profitiert die Produktivität Ihres Teams von ruhigen und störungsarmen Arbeitsbedingungen?",
        "direction": "remote",
        "criteria": ["k31", "k33"],
    },
    "q20": {
        "dimension": "Effizienz und Produktivität",
        "text": "Wie effizient funktioniert die Zusammenarbeit Ihres Teams im Remote-Kontext?",
        "direction": "remote",
        "criteria": ["k32", "k34"],
    },
    "q21": {
        "dimension": "Effizienz und Produktivität",
        "text": "Wie stark erfolgt die Leistungsbewertung in Ihrem Team primär ergebnisorientiert?",
        "direction": "remote",
        "criteria": ["k35"],
    },

    "q22": {
        "dimension": "Teamstruktur und Reifegrad",
        "text": "Wie eingespielt und erfahren ist Ihr Team in der Zusammenarbeit?",
        "direction": "remote",
        "criteria": ["k36", "k37"],
    },
    "q23": {
        "dimension": "Teamstruktur und Reifegrad",
        "text": "Wie selbstorganisiert und strukturell stabil arbeitet Ihr Team?",
        "direction": "remote",
        "criteria": ["k38", "k39"],
    },
}

dimensions = {
    "Aufgaben und Tätigkeiten": ["q1", "q2", "q3", "q4"],
    "Wissensaustausch und Lernen": ["q5", "q6", "q7"],
    "Kommunikation und Abstimmung": ["q8", "q9", "q10", "q11"],
    "Teamdynamik und soziale Einbindung": ["q12", "q13", "q14"],
    "Mitarbeitendenbezogene Faktoren": ["q15", "q16"],
    "Führung": ["q17", "q18"],
    "Effizienz und Produktivität": ["q19", "q20", "q21"],
    "Teamstruktur und Reifegrad": ["q22", "q23"],
}

# ------------------------------------------------------------
# Funktionen
# ------------------------------------------------------------

def criterion_weight(key):
    return criteria[key]["relevance"] * criteria[key]["presence"]


def question_weight(question):
    weights = [criterion_weight(key) for key in question["criteria"]]
    return sum(weights) / len(weights)


def signed_deviation(answer, direction):
    deviation = answer - 3

    if direction == "remote":
        deviation = deviation * -1

    return deviation


def calculate_scores(answers):
    question_results = []

    total_weight = sum(question_weight(question) for question in questions.values())
    weighted_deviation_sum = 0

    for key, question in questions.items():
        weight = question_weight(question)
        answer = answers[key]

        deviation = signed_deviation(answer, question["direction"])
        weighted_deviation = deviation * weight
        weighted_deviation_sum += weighted_deviation

        normierter_antwortwert = 50 + (deviation / 2) * 50
        beitrag_zum_gesamtscore = (weighted_deviation / (2 * total_weight)) * 100

        question_results.append({
            "Dimension": question["dimension"],
            "Frage": question["text"],
            "Antwort": answer,
            "Richtung": "präsenzfördernd" if question["direction"] == "presence" else "remote-fördernd",
            "Gewicht": round(weight, 2),
            "Normierter Antwortwert": round(normierter_antwortwert, 1),
            "Beitrag zum Gesamtscore": round(beitrag_zum_gesamtscore, 2),
        })

    total_score = 50 + (weighted_deviation_sum / (2 * total_weight)) * 100

    question_df = pd.DataFrame(question_results)

    dimension_df = (
        question_df.groupby("Dimension")
        .agg({
            "Beitrag zum Gesamtscore": "sum",
            "Gewicht": "sum",
        })
        .reset_index()
    )

    dimension_df["Beitrag zum Gesamtscore"] = dimension_df["Beitrag zum Gesamtscore"].round(2)

    return total_score, question_df, dimension_df


def model_from_score(score):
    if score <= 25:
        return {
            "model": "Remote-first",
            "days": "≤ 1 Präsenztag pro Woche",
            "description": "Präsenz sollte gezielt und anlassbezogen eingesetzt werden."
        }
    elif score <= 50:
        return {
            "model": "Hybrid-flexibel",
            "days": "1–2 Präsenztage pro Woche",
            "description": "Remote-Arbeit kann dominieren, Präsenz sollte gezielt für Abstimmung und soziale Prozesse genutzt werden."
        }
    elif score <= 75:
        return {
            "model": "Hybrid-präsenzorientiert",
            "days": "2–3 Präsenztage pro Woche",
            "description": "Regelmäßige Präsenz ist sinnvoll, da mehrere zentrale Arbeitsprozesse von persönlicher Interaktion profitieren."
        }
    else:
        return {
            "model": "Präsenz-first",
            "days": "4–5 Präsenztage pro Woche",
            "description": "Ein hoher Präsenzanteil ist sinnvoll, da die Team- und Arbeitsstruktur stark auf persönliche Zusammenarbeit angewiesen ist."
        }

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

Bitte bewerten Sie im nächsten Schritt, inwieweit die folgenden Aussagen auf Ihr Team bzw. Ihre Arbeitssituation zutreffen.
""")

st.info("Bewertungsskala: 1 = trifft gar nicht zu | 5 = trifft voll zu")

start = st.button("➡️ Guideline starten")

if start:
    st.session_state["started"] = True

# ------------------------------------------------------------
# Fragebogen
# ------------------------------------------------------------

if st.session_state.get("started"):
    st.markdown("---")
    st.header("🧭 Kontextbasierte Leitfragen")

    answers = {}

    for dimension_name, question_keys in dimensions.items():
        expanded = dimension_name == "Aufgaben und Tätigkeiten"

        with st.expander(f"🔷 {dimension_name}", expanded=expanded):
            for key in question_keys:
                answers[key] = st.slider(
                    questions[key]["text"],
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=key,
                    help=HELP_TEXT
                )

    st.markdown("---")

    calculate = st.button("📊 Ergebnis berechnen")

    if calculate:
        total_score, question_df, dimension_df = calculate_scores(answers)
        result = model_from_score(total_score)

        st.header("📊 Ergebnis der Guideline")

        st.success(f"Empfohlenes Arbeitsmodell: **{result['model']}**")
        st.subheader(f"Empfohlener Präsenzanteil: {result['days']}")
        st.write(result["description"])

        st.progress(int(total_score))
        st.caption(f"Gesamtscore: {round(total_score, 1)} von 100 Punkten")

        st.subheader("Zentrale Treiber der Empfehlung")

        top_dimensions = dimension_df.sort_values(
            by="Beitrag zum Gesamtscore",
            ascending=False
        ).head(3)

        for _, row in top_dimensions.iterrows():
            if row["Beitrag zum Gesamtscore"] > 0:
                st.write(
                    f"- **{row['Dimension']}** "
                    f"(+{round(row['Beitrag zum Gesamtscore'], 2)} Punkte)"
                )

        st.subheader("Präsenzreduzierende Faktoren")

        reducing_dimensions = dimension_df.sort_values(
            by="Beitrag zum Gesamtscore",
            ascending=True
        ).head(3)

        for _, row in reducing_dimensions.iterrows():
            if row["Beitrag zum Gesamtscore"] < 0:
                st.write(
                    f"- **{row['Dimension']}** "
                    f"({round(row['Beitrag zum Gesamtscore'], 2)} Punkte)"
                )

        with st.expander("Details zur Berechnung anzeigen"):
            st.write("Die Tabelle zeigt die Berechnung je Leitfrage.")

            st.dataframe(
                question_df[
                    [
                        "Dimension",
                        "Frage",
                        "Antwort",
                        "Richtung",
                        "Gewicht",
                        "Normierter Antwortwert",
                        "Beitrag zum Gesamtscore",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.write("Die Tabelle zeigt die aggregierten Werte je Leitdimension.")

            st.dataframe(
                dimension_df[
                    [
                        "Dimension",
                        "Gewicht",
                        "Beitrag zum Gesamtscore",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )