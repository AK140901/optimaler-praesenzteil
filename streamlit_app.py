import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bewertungsmodell Präsenzanteil",
    page_icon="📊",
    layout="wide"
)

HELP_TEXT = "1 = trifft gar nicht zu | 5 = trifft voll zu"

criteria = {
    "k1": {"name": "Komplexität der Aufgaben", "relevance": 3.15217, "presence": 2.52174},
    "k2": {"name": "Abstimmungsbedarf zwischen Teammitgliedern", "relevance": 3.57447, "presence": 2.70213},
    "k3": {"name": "Durchführung kreativer oder kollaborativer Aufgaben", "relevance": 3.43478, "presence": 3.10870},
    "k4": {"name": "Durchführung konzentrierter Einzelarbeit", "relevance": 3.26087, "presence": 1.60870},
    "k5": {"name": "Phase des Projekts", "relevance": 3.32609, "presence": 2.95652},

    "k6": {"name": "Informeller Wissensaustausch im Team", "relevance": 3.78261, "presence": 3.45652},
    "k7": {"name": "Spontane Gespräche und Austausch zwischen Mitarbeitenden", "relevance": 3.41304, "presence": 3.26087},
    "k8": {"name": "Weitergabe von Erfahrungswissen", "relevance": 3.26087, "presence": 3.15217},
    "k9": {"name": "Einarbeitung neuer Mitarbeitender", "relevance": 4.39130, "presence": 4.26087},
    "k10": {"name": "Gemeinsames Lernen im Team", "relevance": 3.21739, "presence": 3.19565},

    "k11": {"name": "Qualität der Kommunikation im Team", "relevance": 3.58696, "presence": 2.89130},
    "k12": {"name": "Vermeidung von Missverständnissen", "relevance": 3.39130, "presence": 2.78261},
    "k13": {"name": "Schnelligkeit von Abstimmungen", "relevance": 3.08696, "presence": 2.76087},
    "k14": {"name": "Klärung komplexer Sachverhalte", "relevance": 3.02174, "presence": 3.13043},
    "k15": {"name": "Qualität von Feedbackprozessen", "relevance": 3.21739, "presence": 3.23913},

    "k16": {"name": "Teamzusammenhalt", "relevance": 4.14894, "presence": 3.74468},
    "k17": {"name": "Vertrauen innerhalb des Teams", "relevance": 3.69565, "presence": 3.54348},
    "k18": {"name": "Aufbau persönlicher Beziehungen", "relevance": 4.00000, "presence": 3.89130},
    "k19": {"name": "Teamgefühl und Zugehörigkeit", "relevance": 4.13043, "presence": 3.78261},
    "k20": {"name": "Integration neuer Mitarbeitender", "relevance": 4.47826, "presence": 4.26087},

    "k21": {"name": "Bedürfnis der Mitarbeitenden nach Flexibilität", "relevance": 3.85106, "presence": 2.55319},
    "k22": {"name": "Individuelle Präferenzen hinsichtlich des Arbeitsortes", "relevance": 3.72917, "presence": 2.50000},
    "k23": {"name": "Arbeitszufriedenheit der Mitarbeitenden", "relevance": 3.97826, "presence": 2.56522},
    "k24": {"name": "Motivation der Mitarbeitenden", "relevance": 3.82609, "presence": 2.73913},
    "k25": {"name": "Vereinbarkeit von Beruf und Privatleben", "relevance": 4.06522, "presence": 2.21739},

    "k26": {"name": "Möglichkeit, Mitarbeitende effektiv zu führen", "relevance": 3.23913, "presence": 2.93478},
    "k27": {"name": "Überblick über Arbeitsfortschritte im Team", "relevance": 2.32609, "presence": 2.30435},
    "k28": {"name": "Steuerung und Koordination der Arbeit", "relevance": 2.69565, "presence": 2.52174},
    "k29": {"name": "Unterstützung der Mitarbeitenden durch Führung", "relevance": 2.80435, "presence": 2.71739},
    "k30": {"name": "Austausch zwischen Führungskraft und Team", "relevance": 3.06522, "presence": 2.97826},

    "k31": {"name": "Produktivität der Mitarbeitenden", "relevance": 3.34043, "presence": 2.60870},
    "k32": {"name": "Effizienz der Zusammenarbeit im Team", "relevance": 3.43478, "presence": 2.82609},
    "k33": {"name": "Ablenkungen im Büro", "relevance": 3.04348, "presence": 2.58696},
    "k34": {"name": "Effizienz von Remote-Arbeit", "relevance": 3.30435, "presence": 2.10870},
    "k35": {"name": "Fokus auf Arbeitsergebnisse", "relevance": 3.28261, "presence": 2.43478},

    "k36": {"name": "Erfahrung des Teams", "relevance": 3.39130, "presence": 2.80435},
    "k37": {"name": "Eingespieltheit des Teams", "relevance": 3.52174, "presence": 2.97826},
    "k38": {"name": "Grad der Selbstorganisation", "relevance": 3.69565, "presence": 2.56522},
    "k39": {"name": "Stabilität der Teamstruktur", "relevance": 3.30435, "presence": 3.00000},
}

questions = {
    "q1": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie stark ist Ihr Team im Arbeitsalltag auf gemeinsame Abstimmung und koordinierte Zusammenarbeit angewiesen?", "direction": "presence", "criteria": ["k1", "k2"]},
    "q2": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie häufig erfordert die Arbeit Ihres Teams kreative oder kollaborative Problemlösungen?", "direction": "presence", "criteria": ["k3"]},
    "q3": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie stark basiert die Arbeit Ihres Teams auf konzentrierter und individuell ausführbarer Einzelarbeit?", "direction": "remote", "criteria": ["k4"]},
    "q4": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie häufig befindet sich Ihr Team in Projektphasen mit erhöhtem Abstimmungs- und Koordinationsbedarf?", "direction": "presence", "criteria": ["k5"]},

    "q5": {"dimension": "Wissensaustausch und Lernen", "text": "Wie wichtig ist spontaner und informeller Wissensaustausch für die tägliche Zusammenarbeit Ihres Teams?", "direction": "presence", "criteria": ["k6", "k7"]},
    "q6": {"dimension": "Wissensaustausch und Lernen", "text": "Wie stark basiert die Arbeit Ihres Teams auf Erfahrungswissen und gemeinsamem Lernen?", "direction": "presence", "criteria": ["k8", "k10"]},
    "q7": {"dimension": "Wissensaustausch und Lernen", "text": "Wie häufig werden neue Mitarbeitende in Ihr Team integriert oder eingearbeitet?", "direction": "presence", "criteria": ["k9"]},

    "q8": {"dimension": "Teamstruktur und Reifegrad", "text": "Wie eingespielt und erfahren ist Ihr Team in der Zusammenarbeit?", "direction": "remote", "criteria": ["k36", "k37"]},
    "q9": {"dimension": "Teamstruktur und Reifegrad", "text": "Wie selbstorganisiert und strukturell stabil arbeitet Ihr Team?", "direction": "remote", "criteria": ["k38", "k39"]},

    "q10": {"dimension": "Kommunikation und Abstimmung", "text": "Wie wichtig sind direkte und schnelle Abstimmungen für die Arbeitsfähigkeit Ihres Teams?", "direction": "presence", "criteria": ["k11", "k13"]},
    "q11": {"dimension": "Kommunikation und Abstimmung", "text": "Wie häufig müssen in Ihrem Team komplexe Sachverhalte gemeinsam geklärt werden?", "direction": "presence", "criteria": ["k14"]},
    "q12": {"dimension": "Kommunikation und Abstimmung", "text": "Wie wichtig ist die Vermeidung von Missverständnissen und Kommunikationsfehlern in Ihrem Arbeitsalltag?", "direction": "presence", "criteria": ["k12"]},
    "q13": {"dimension": "Kommunikation und Abstimmung", "text": "Wie relevant sind persönliche und situationsbezogene Feedbackprozesse in Ihrem Team?", "direction": "presence", "criteria": ["k15"]},

    "q14": {"dimension": "Mitarbeitendenbezogene Faktoren", "text": "Wie hoch ist das Bedürfnis Ihrer Mitarbeitenden nach räumlicher Flexibilität und individueller Arbeitsgestaltung?", "direction": "remote", "criteria": ["k21", "k22"]},
    "q15": {"dimension": "Mitarbeitendenbezogene Faktoren", "text": "Welche Bedeutung haben hybride Arbeitsmöglichkeiten für Zufriedenheit und Motivation Ihrer Mitarbeitenden?", "direction": "remote", "criteria": ["k23", "k24", "k25"]},

    "q16": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie wichtig sind persönlicher Kontakt und soziale Interaktion für den Zusammenhalt Ihres Teams?", "direction": "presence", "criteria": ["k16", "k19"]},
    "q17": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie stark basiert die Zusammenarbeit Ihres Teams auf gegenseitigem Vertrauen und persönlichen Beziehungen?", "direction": "presence", "criteria": ["k17", "k18"]},
    "q18": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie wichtig ist die soziale Integration neuer Mitarbeitender für die Stabilität Ihres Teams?", "direction": "presence", "criteria": ["k20"]},

    "q19": {"dimension": "Effizienz und Produktivität", "text": "Wie stark profitiert die Produktivität Ihres Teams von ruhigen und störungsarmen Arbeitsbedingungen?", "direction": "remote", "criteria": ["k31", "k33"]},
    "q20": {"dimension": "Effizienz und Produktivität", "text": "Wie effizient funktioniert die Zusammenarbeit Ihres Teams im Remote-Kontext?", "direction": "remote", "criteria": ["k32", "k34"]},
    "q21": {"dimension": "Effizienz und Produktivität", "text": "Wie stark erfolgt die Leistungsbewertung in Ihrem Team primär ergebnisorientiert?", "direction": "remote", "criteria": ["k35"]},

    "q22": {"dimension": "Führung", "text": "Wie stark basiert Ihre Führungsarbeit auf persönlichem Austausch und unmittelbarer Interaktion mit dem Team?", "direction": "presence", "criteria": ["k29", "k30"]},
    "q23": {"dimension": "Führung", "text": "Wie wichtig ist direkte Präsenz für die Steuerung und Koordination Ihres Teams?", "direction": "presence", "criteria": ["k26", "k27", "k28"]},
}

dimensions = {
    "Aufgaben und Tätigkeiten": ["q1", "q2", "q3", "q4"],
    "Wissensaustausch und Lernen": ["q5", "q6", "q7"],
    "Teamstruktur und Reifegrad": ["q8", "q9"],
    "Kommunikation und Abstimmung": ["q10", "q11", "q12", "q13"],
    "Mitarbeitendenbezogene Faktoren": ["q14", "q15"],
    "Teamdynamik und soziale Einbindung": ["q16", "q17", "q18"],
    "Effizienz und Produktivität": ["q19", "q20", "q21"],
    "Führung": ["q22", "q23"],
}

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

        gewichtungsanteil = (weight / total_weight) * 100
        basisbeitrag = 50 * (weight / total_weight)
        abweichungsbeitrag = (weighted_deviation / (2 * total_weight)) * 50
        scorebeitrag = basisbeitrag + abweichungsbeitrag

        question_results.append({
            "Dimension": question["dimension"],
            "Frage": question["text"],
            "Antwort": answer,
            "Richtung": "präsenzfördernd" if question["direction"] == "presence" else "remote-fördernd",
            "Gewichtungsanteil (%)": round(gewichtungsanteil, 2),
            "Abweichungsbeitrag": round(abweichungsbeitrag, 2),
            "Scorebeitrag": round(scorebeitrag, 2),
        })

    total_score = 50 + (weighted_deviation_sum / (2 * total_weight)) * 50

    question_df = pd.DataFrame(question_results)

    dimension_df = (
        question_df.groupby("Dimension")
        .agg({
            "Gewichtungsanteil (%)": "sum",
            "Abweichungsbeitrag": "sum",
            "Scorebeitrag": "sum",
        })
        .reset_index()
    )

    dimension_df["Gewichtungsanteil (%)"] = dimension_df["Gewichtungsanteil (%)"].round(2)
    dimension_df["Abweichungsbeitrag"] = dimension_df["Abweichungsbeitrag"].round(2)
    dimension_df["Scorebeitrag"] = dimension_df["Scorebeitrag"].round(2)

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

def generate_interpretation(total_score, result, dimension_df):
    score = round(total_score, 1)

    INTERPRETATION_THRESHOLD = 1.0

    positive_dimensions = dimension_df[dimension_df["Abweichungsbeitrag"] > INTERPRETATION_THRESHOLD].sort_values(
        by="Abweichungsbeitrag",
        ascending=False
    )

    negative_dimensions = dimension_df[dimension_df["Abweichungsbeitrag"] < -INTERPRETATION_THRESHOLD].sort_values(
        by="Abweichungsbeitrag",
        ascending=True
    )

    strongest_positive = positive_dimensions.head(2)["Dimension"].tolist()
    strongest_negative = negative_dimensions.head(2)["Dimension"].tolist()

    dimension_texts_positive = {
        "Aufgaben und Tätigkeiten": "Die arbeitsbezogenen Anforderungen sprechen in diesem Fall eher für persönliche Abstimmung und koordinierte Zusammenarbeit.",
        "Wissensaustausch und Lernen": "Der Wissensaustausch wirkt präsenzfördernd, da informelles Lernen und Erfahrungswissen nach den empirischen Ergebnissen stärker von persönlicher Interaktion profitieren.",
        "Kommunikation und Abstimmung": "Die Kommunikationsanforderungen deuten darauf hin, dass direkte Abstimmungen und die Klärung komplexer Sachverhalte eine relevante Rolle spielen.",
        "Teamdynamik und soziale Einbindung": "Die Teamdynamik stellt einen zentralen Präsenztreiber dar, da soziale Einbindung, Vertrauen und Zugehörigkeit in der Befragung besonders stark mit Präsenz verbunden wurden.",
        "Mitarbeitendenbezogene Faktoren": "Die mitarbeitendenbezogenen Faktoren erhöhen in diesem Fall den Präsenzbedarf, was auf eine stärkere Bedeutung gemeinsamer Arbeitsgestaltung hinweisen kann.",
        "Führung": "Die Führungsdimension spricht eher für Präsenz, wenn persönlicher Austausch und unmittelbare Interaktion für die Führungsarbeit wichtig sind.",
        "Effizienz und Produktivität": "Die produktivitätsbezogenen Faktoren wirken in diesem Fall präsenzfördernd, wenn Zusammenarbeit oder Produktivität stärker von gemeinsamen Arbeitsbedingungen profitieren.",
        "Teamstruktur und Reifegrad": "Die Teamstruktur spricht eher für Präsenz, wenn Erfahrung, Eingespieltheit oder Selbstorganisation noch nicht ausreichend ausgeprägt sind."
    }

    dimension_texts_negative = {
        "Aufgaben und Tätigkeiten": "Die Aufgabenstruktur wirkt präsenzreduzierend, wenn ein hoher Anteil konzentrierter Einzelarbeit vorliegt.",
        "Wissensaustausch und Lernen": "Der Wissensaustausch wirkt in diesem Fall weniger präsenzabhängig, wenn Lernen und Erfahrungsweitergabe auch digital gut funktionieren.",
        "Kommunikation und Abstimmung": "Die Kommunikation scheint auch ohne hohe Präsenzanteile gut abbildbar zu sein, sofern Abstimmungen und Klärungen digital ausreichend funktionieren.",
        "Teamdynamik und soziale Einbindung": "Die Teamdynamik reduziert den Präsenzbedarf, wenn Vertrauen, Beziehungen und Zugehörigkeit bereits stabil ausgeprägt sind.",
        "Mitarbeitendenbezogene Faktoren": "Die mitarbeitendenbezogenen Faktoren sprechen eher für mehr Flexibilität, da individuelle Arbeitsortpräferenzen, Zufriedenheit und Vereinbarkeit von Beruf und Privatleben empirisch eine hohe Relevanz, aber geringere Präsenzabhängigkeit aufweisen.",
        "Führung": "Die Führungsdimension wirkt präsenzreduzierend, wenn Steuerung, Unterstützung und Austausch auch ohne regelmäßige physische Anwesenheit wirksam umgesetzt werden können.",
        "Effizienz und Produktivität": "Die Dimension Effizienz und Produktivität spricht eher für Remote-Arbeit, wenn ruhige Arbeitsbedingungen, Ergebnisorientierung und effiziente Remote-Zusammenarbeit stark ausgeprägt sind.",
        "Teamstruktur und Reifegrad": "Ein hoher Reifegrad des Teams reduziert den Präsenzbedarf, da eingespielte, erfahrene und selbstorganisierte Teams weniger stark auf physische Anwesenheit angewiesen sind."
    }

    interpretation = []

    interpretation.append(
        f"Der berechnete Präsenz-Score beträgt {score} von 100 Punkten und wird dem Arbeitsmodell "
        f"„{result['model']}“ zugeordnet. Dies entspricht einem empfohlenen Präsenzanteil von {result['days']}."
    )

    if total_score > 55:
        interpretation.append(
            "Das Ergebnis liegt oberhalb des neutralen Mittelpunktes von 50 Punkten und spricht damit tendenziell für einen höheren Präsenzanteil. "
            "Die Empfehlung sollte jedoch nicht als starre Vorgabe verstanden werden, sondern als empirisch fundierte Orientierung für die konkrete Team- und Arbeitssituation."
        )
    elif total_score < 45:
        interpretation.append(
            "Das Ergebnis liegt unterhalb des neutralen Mittelpunktes von 50 Punkten und deutet damit auf eine stärkere Eignung für remote-orientierte oder flexible hybride Arbeitsformen hin. "
            "Der Präsenzanteil sollte in diesem Fall eher gezielt für bestimmte Anlässe eingesetzt werden."
        )
    else:
        interpretation.append(
            "Das Ergebnis liegt nahe am neutralen Mittelpunkt von 50 Punkten. Dies deutet darauf hin, dass sich präsenzfördernde und remote-fördernde Faktoren weitgehend ausgleichen. "
            "Für die praktische Umsetzung erscheint daher ein flexibles hybrides Modell besonders naheliegend."
        )

    if strongest_positive:
        pos_sentences = [dimension_texts_positive[d] for d in strongest_positive if d in dimension_texts_positive]
        interpretation.append("Präsenzfördernd wirken vor allem die Dimensionen " + ", ".join(strongest_positive) + ". " + " ".join(pos_sentences))

    if strongest_negative:
        neg_sentences = [dimension_texts_negative[d] for d in strongest_negative if d in dimension_texts_negative]
        interpretation.append("Präsenzreduzierend wirken insbesondere die Dimensionen " + ", ".join(strongest_negative) + ". " + " ".join(neg_sentences))

    interpretation.append(
        "Die Interpretation berücksichtigt dabei die empirischen Ergebnisse der Befragung: Besonders soziale Integration, Teamdynamik, informeller Wissensaustausch und Onboarding wurden stärker mit physischer Präsenz verbunden. "
        "Dagegen wurden Flexibilität, konzentrierte Einzelarbeit, Selbstorganisation und Ergebnisorientierung eher als Faktoren eingeordnet, die remote-fähige Arbeitsformen begünstigen."
    )

    return "\n\n".join(interpretation)        

st.title("📊 Bewertungsmodell zur Bestimmung des optimalen Präsenzanteils")

st.markdown("""
### Hintergrund und Ziel des Bewertungsmodells

Dieses Bewertungsmodell wurde im Rahmen einer wissenschaftlichen Masterarbeit entwickelt. Ziel ist es, Führungskräfte bei der Bestimmung eines geeigneten Verhältnisses von Präsenz- und Remote-Arbeit in hybriden Arbeitsmodellen zu unterstützen.

Die Grundlage bilden qualitative Interviews mit Führungskräften aus der IT-Branche. Aus diesen Interviews wurden zentrale Einflussfaktoren auf den Präsenzanteil abgeleitet. Anschließend wurden diese Faktoren im Rahmen einer quantitativen Erhebung bewertet und empirisch gewichtet.

Auf Basis dieser Ergebnisse wurde ein Entscheidungsmodell entwickelt, das die individuelle Situation eines Teams berücksichtigt und daraus eine Empfehlung für den Präsenzanteil ableitet.

Die Ergebnisse dieses Bewertungsmodells basieren somit auf einer systematischen wissenschaftlichen Analyse und sind vollständig in der zugrunde liegenden Masterarbeit dokumentiert.

### Nutzung

Bitte bewerten Sie im nächsten Schritt, inwieweit die folgenden Aussagen auf Ihr Team bzw. Ihre Arbeitssituation zutreffen.
""")

st.markdown("""
### Wissenschaftliche Grundlage

Das Bewertungsmodell basiert auf qualitativen Interviews mit IT-Führungskräften sowie einer anschließenden quantitativen Gewichtungsbefragung.

Die identifizierten Kriterien wurden hinsichtlich ihrer Relevanz und Präsenzabhängigkeit bewertet. Diese empirischen Mittelwerte bilden die Grundlage der Gewichtung im Modell.
""")

st.info("Bewertungsskala: 1 = trifft gar nicht zu | 5 = trifft voll zu")

start = st.button("➡️ Fragebogen starten")

if st.session_state.get("reset_answers"):
    for key in questions.keys():
        st.session_state[key] = 3
    st.session_state["reset_answers"] = False

if start:
    st.session_state["started"] = True

if st.session_state.get("started"):
    st.markdown("---")
    st.warning("""
    Bitte beantworten Sie die Fragen aus Sicht der strukturellen Anforderungen Ihres Teams und nicht aus Sicht einzelner persönlicher Präferenzen.
    """)
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

    col1, col2 = st.columns(2)

    with col1:
        calculate = st.button(
            "📊 Ergebnis berechnen",
            key="calculate_button",
            use_container_width=True
        )

    with col2:
        reset = st.button(
            "🔄 Antworten zurücksetzen",
            key="reset_button",
            use_container_width=True
        )

    if reset:
        st.session_state["reset_answers"] = True
        st.rerun()

    if calculate:
        total_score, question_df, dimension_df = calculate_scores(answers)
        result = model_from_score(total_score)

        st.header("📊 Ergebnis des Bewertungsmodells")

        score_rounded = round(total_score, 1)
        progress_value = max(0, min(100, total_score))

        st.markdown(
            f"""
            <div style="
                padding: 28px;
                border-radius: 18px;
                background-color: rgba(128, 128, 128, 0.08);
                border: 1px solid rgba(128, 128, 128, 0.25);
                text-align: center;
                margin-bottom: 20px;
            ">
                <div style="font-size: 18px;">
                    Ihr berechneter Präsenz-Score
                </div>
                <div style="font-size: 58px; font-weight: 700;">
                    {score_rounded}
                </div>
                <div style="font-size: 16px;">
                    von 100 Punkten
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(int(progress_value))
        st.caption(f"Score: {score_rounded} / 100 Punkte")

        st.markdown("### Einordnung des Ergebnisses")

        model_options = [
            ("Remote-first", "≤ 1 Präsenztag pro Woche", "Empfohlen bei einem Score von 0 bis 25 Punkten"),
            ("Hybrid-flexibel", "1–2 Präsenztage pro Woche", "Empfohlen bei einem Score von 26 bis 50 Punkten"),
            ("Hybrid-präsenzorientiert", "2–3 Präsenztage pro Woche", "Empfohlen bei einem Score von 51 bis 75 Punkten"),
            ("Präsenz-first", "4–5 Präsenztage pro Woche", "Empfohlen bei einem Score von 76 bis 100 Punkten"),
        ]

        st.markdown("""
        <style>
        .model-card {
            position: relative;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            background-color: rgba(128, 128, 128, 0.08);
            min-height: 150px;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            box-sizing: border-box;
        }

        .model-card-selected {
            border: 2px solid #22c55e;
            background-color: rgba(34, 197, 94, 0.12);
        }

        .model-badge {
            display: inline-block;
            margin-bottom: 8px;
            padding: 3px 10px;
            border-radius: 999px;
            background-color: rgba(34, 197, 94, 0.18);
            color: #22c55e;
            font-size: 13px;
            font-weight: 700;
        }

        .model-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.25;
        }

        .model-days {
            font-size: 15px;
            line-height: 1.35;
            opacity: 0.85;
        }

        /* Alle Info-Icons standardmäßig unsichtbar */
        .info-icon {
            position: absolute;
            top: 10px;
            right: 10px;

            width: 18px;
            height: 18px;

            border-radius: 50%;
            border: 1px solid rgba(151, 166, 195, 0.35);

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 11px;
            font-weight: 600;

            color: rgba(250, 250, 250, 0.75);
            background-color: rgba(255,255,255,0.04);

            cursor: help;
            z-index: 2;

            opacity: 0;
            transition: opacity 0.2s ease;
        }

        /* Erst sichtbar wenn man über die Box hovert */
        .model-card:hover .info-icon {
            opacity: 0.8;
        }

        .info-icon:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 32px;
            right: 0;
            width: 220px;
            padding: 10px 12px;
            border-radius: 10px;
            background-color: #262730;
            color: white;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.35;
            text-align: left;
            z-index: 9999;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        }
        .model-card {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            background-color: rgba(128, 128, 128, 0.08);
            min-height: 150px;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            box-sizing: border-box;

            margin-bottom: 12px;
        }
        .model-card.model-card-selected {
            border: 2px solid #22c55e !important;
            background-color: rgba(34, 197, 94, 0.12) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        cols = st.columns(4)

        for col, (model_name, days, tooltip) in zip(cols, model_options):
            is_selected = model_name == result["model"]

            card_class = "model-card model-card-selected" if is_selected else "model-card"
            badge_html = '<div class="model-badge">Empfohlen</div>' if is_selected else ""

            html = (
                f'<div class="{card_class}">'
                f'<div class="info-icon" data-tooltip="{tooltip}">?</div>'
                f'{badge_html}'
                f'<div class="model-title">{model_name}</div>'
                f'<div class="model-days">{days}</div>'
                f'</div>'
            )

            with col:
                st.markdown(html, unsafe_allow_html=True)

        st.markdown("### Interpretation des Ergebnisses")

        interpretation_text = generate_interpretation(total_score, result, dimension_df)

        st.markdown(interpretation_text)

        st.info("""
        Hinweis: Das Ergebnis dient als Orientierungshilfe und ersetzt keine unternehmens- oder teamspezifische Entscheidung.
        """)

        st.markdown("### Wichtigste Einflussdimensionen")

        st.markdown("""
        Die folgenden Dimensionen zeigen, welche Bereiche den Score am stärksten erhöht oder reduziert haben.
        """)
    
        st.subheader("Zentrale Treiber der Empfehlung")

        top_dimensions = dimension_df.sort_values(
            by="Abweichungsbeitrag",
            ascending=False
        ).head(3)

        found_positive = False

        RELEVANCE_THRESHOLD = 1.0

        for _, row in top_dimensions.iterrows():
            if row["Abweichungsbeitrag"] > RELEVANCE_THRESHOLD:
                found_positive = True
                st.write(
                    f"- **{row['Dimension']}** "
                    f"(+{round(row['Abweichungsbeitrag'], 2)} Punkte)"
                )

        if not found_positive:
            st.write("Es wurden keine deutlich präsenzfördernden Faktoren identifiziert.")

        st.subheader("Präsenzreduzierende Faktoren")

        reducing_dimensions = dimension_df.sort_values(
            by="Abweichungsbeitrag",
            ascending=True
        ).head(3)

        found_negative = False

        for _, row in reducing_dimensions.iterrows():
            if row["Abweichungsbeitrag"] < -RELEVANCE_THRESHOLD:
                found_negative = True
                st.write(
                    f"- **{row['Dimension']}** "
                    f"({round(row['Abweichungsbeitrag'], 2)} Punkte)"
                )

        if not found_negative:
            st.write("Es wurden keine relevanten präsenzreduzierenden Faktoren identifiziert.")

        with st.expander("Details zur Berechnung anzeigen"):
            st.markdown("""
            ### Erläuterung der Berechnungslogik

            Die Berechnung basiert auf einem gewichteten Bewertungsmodell.

            Jede Leitfrage ist mit empirisch gewichteten Kriterien verknüpft. 
            Die Gewichtung ergibt sich aus:
            - der Relevanz des Kriteriums
            - der empirisch erhobenen Präsenzabhängigkeit

            Je höher beide Werte ausfallen, desto stärker beeinflusst das jeweilige Kriterium die Gesamtempfehlung.

            Die Antworten werden anschließend relativ zu einem neutralen Mittelpunkt von 3 interpretiert:
            - Werte oberhalb von 3 verstärken die jeweilige Wirkungsrichtung
            - Werte unterhalb von 3 schwächen diese ab

            Remote-fördernde Faktoren werden dabei invers berücksichtigt.
            """)
            st.write("Die Tabelle zeigt die Berechnung je Leitfrage.")

            st.dataframe(
                question_df[
                    [
                        "Dimension",
                        "Frage",
                        "Antwort",
                        "Richtung",
                        "Gewichtungsanteil (%)",
                        "Abweichungsbeitrag",
                        "Scorebeitrag",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Summe Gewichtungsanteile: {round(question_df['Gewichtungsanteil (%)'].sum(), 1)} % | "
                f"Summe Scorebeiträge: {round(question_df['Scorebeitrag'].sum(), 1)} Punkte"
            )

            st.write("Die Tabelle zeigt die aggregierten Werte je Leitdimension.")

            st.dataframe(
                dimension_df[
                    [
                        "Dimension",
                        "Gewichtungsanteil (%)",
                        "Abweichungsbeitrag",
                        "Scorebeitrag",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Summe Gewichtungsanteile: {round(dimension_df['Gewichtungsanteil (%)'].sum(), 1)} % | "
                f"Summe Scorebeiträge: {round(dimension_df['Scorebeitrag'].sum(), 1)} Punkte"
            )
            st.markdown("""
            ### Hinweise zur Interpretation

            Das Bewertungsmodell dient als strukturierte Entscheidungshilfe und nicht als starre Vorgabe.

            Die finale Ausgestaltung hybrider Arbeitsmodelle sollte zusätzlich unternehmensspezifische Rahmenbedingungen berücksichtigen, beispielsweise:
            - organisatorische Anforderungen
            - Unternehmenskultur
            - technologische Infrastruktur
            - individuelle Teamkonstellationen
            - strategische Zielsetzungen
            """)
st.markdown("---")

st.caption("""
Hinweis: Das Bewertungsmodell wurde im Rahmen einer wissenschaftlichen Masterarbeit entwickelt und dient ausschließlich als unterstützendes Entscheidungsinstrument für hybride Arbeitsmodelle.
""")       