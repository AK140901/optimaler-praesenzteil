import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bewertungsmodell Präsenzanteil",
    page_icon="📊",
    layout="wide"
)

HELP_TEXT = "1 = trifft gar nicht zu | 5 = trifft voll zu"

criteria = {
    "k1": {"name": "Komplexität der Aufgaben", "relevance": 3.14894, "presence": 2.51064},
    "k2": {"name": "Abstimmungsbedarf zwischen Teammitgliedern", "relevance": 3.55319, "presence": 2.68085},
    "k3": {"name": "Durchführung kreativer oder kollaborativer Aufgaben", "relevance": 3.42553, "presence": 3.10638},
    "k4": {"name": "Durchführung konzentrierter Einzelarbeit", "relevance": 3.25532, "presence": 1.59574},
    "k5": {"name": "Phase des Projekts", "relevance": 3.31915, "presence": 2.95745},
    "k6": {"name": "Informeller Wissensaustausch im Team", "relevance": 3.76596, "presence": 3.44681},
    "k7": {"name": "Spontane Gespräche und Austausch zwischen Mitarbeitenden", "relevance": 3.40426, "presence": 3.25532},
    "k8": {"name": "Weitergabe von Erfahrungswissen", "relevance": 3.25532, "presence": 3.14894},
    "k9": {"name": "Einarbeitung neuer Mitarbeitender", "relevance": 4.38298, "presence": 4.25532},
    "k10": {"name": "Gemeinsames Lernen im Team", "relevance": 3.21277, "presence": 3.19149},
    "k11": {"name": "Qualität der Kommunikation im Team", "relevance": 3.57447, "presence": 2.87234},
    "k12": {"name": "Vermeidung von Missverständnissen", "relevance": 3.38298, "presence": 2.76596},
    "k13": {"name": "Schnelligkeit von Abstimmungen", "relevance": 3.08511, "presence": 2.74468},
    "k14": {"name": "Klärung komplexer Sachverhalte", "relevance": 3.02128, "presence": 3.12766},
    "k15": {"name": "Qualität von Feedbackprozessen", "relevance": 3.21277, "presence": 3.23404},
    "k16": {"name": "Teamzusammenhalt", "relevance": 4.12766, "presence": 3.74468},
    "k17": {"name": "Vertrauen innerhalb des Teams", "relevance": 3.68085, "presence": 3.53191},
    "k18": {"name": "Aufbau persönlicher Beziehungen", "relevance": 4.00000, "presence": 3.87234},
    "k19": {"name": "Teamgefühl und Zugehörigkeit", "relevance": 4.12766, "presence": 3.76596},
    "k20": {"name": "Integration neuer Mitarbeitender", "relevance": 4.46809, "presence": 4.25532},
    "k21": {"name": "Bedürfnis der Mitarbeitenden nach Flexibilität", "relevance": 3.80851, "presence": 2.48936},
    "k22": {"name": "Individuelle Präferenzen hinsichtlich des Arbeitsortes", "relevance": 3.68085, "presence": 2.40426},
    "k23": {"name": "Arbeitszufriedenheit der Mitarbeitenden", "relevance": 3.95745, "presence": 2.55319},
    "k24": {"name": "Motivation der Mitarbeitenden", "relevance": 3.80851, "presence": 2.72340},
    "k25": {"name": "Vereinbarkeit von Beruf und Privatleben", "relevance": 4.06383, "presence": 2.21277},
    "k26": {"name": "Möglichkeit, Mitarbeitende effektiv zu führen", "relevance": 3.23404, "presence": 2.91489},
    "k27": {"name": "Überblick über Arbeitsfortschritte im Team", "relevance": 2.31915, "presence": 2.29787},
    "k28": {"name": "Steuerung und Koordination der Arbeit", "relevance": 2.68085, "presence": 2.51064},
    "k29": {"name": "Unterstützung der Mitarbeitenden durch Führung", "relevance": 2.78723, "presence": 2.70213},
    "k30": {"name": "Austausch zwischen Führungskraft und Team", "relevance": 3.06383, "presence": 2.97872},
    "k31": {"name": "Produktivität der Mitarbeitenden", "relevance": 3.31915, "presence": 2.59574},
    "k32": {"name": "Effizienz der Zusammenarbeit im Team", "relevance": 3.42553, "presence": 2.80851},
    "k33": {"name": "Ablenkungen im Büro", "relevance": 3.04255, "presence": 2.57447},
    "k34": {"name": "Effizienz von Remote-Arbeit", "relevance": 3.29787, "presence": 2.10638},
    "k35": {"name": "Fokus auf Arbeitsergebnisse", "relevance": 3.27660, "presence": 2.42553},
    "k36": {"name": "Erfahrung des Teams", "relevance": 3.38298, "presence": 2.78723},
    "k37": {"name": "Eingespieltheit des Teams", "relevance": 3.51064, "presence": 2.97872},
    "k38": {"name": "Grad der Selbstorganisation", "relevance": 3.68085, "presence": 2.55319},
    "k39": {"name": "Stabilität der Teamstruktur", "relevance": 3.29787, "presence": 3.00000},
}

questions = {
    "q1": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie stark ist Ihr Team im Arbeitsalltag auf gemeinsame Abstimmung und koordinierte Zusammenarbeit angewiesen?", "direction": "presence", "criteria": ["k1", "k2"]},
    "q2": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie häufig erfordert die Arbeit Ihres Teams kreative oder kollaborative Problemlösungen?", "direction": "presence", "criteria": ["k3"]},
    "q3": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie stark basiert die Arbeit Ihres Teams auf konzentrierter und individuell ausführbarer Einzelarbeit?", "direction": "remote", "criteria": ["k4"]},
    "q4": {"dimension": "Aufgaben und Tätigkeiten", "text": "Wie häufig befindet sich Ihr Team in Projektphasen mit erhöhtem Abstimmungs- und Koordinationsbedarf?", "direction": "presence", "criteria": ["k5"]},
    "q5": {"dimension": "Wissensaustausch und Lernen", "text": "Wie wichtig ist spontaner und informeller Wissensaustausch für die tägliche Zusammenarbeit Ihres Teams?", "direction": "presence", "criteria": ["k6", "k7"]},
    "q6": {"dimension": "Wissensaustausch und Lernen", "text": "Wie stark basiert die Arbeit Ihres Teams auf Erfahrungswissen und gemeinsamem Lernen?", "direction": "presence", "criteria": ["k8", "k10"]},
    "q7": {"dimension": "Wissensaustausch und Lernen", "text": "Wie häufig werden neue Mitarbeitende in Ihr Team integriert oder eingearbeitet?", "direction": "presence", "criteria": ["k9"]},
    "q8": {"dimension": "Kommunikation und Abstimmung", "text": "Wie wichtig sind direkte und schnelle Abstimmungen für die Arbeitsfähigkeit Ihres Teams?", "direction": "presence", "criteria": ["k11", "k13"]},
    "q9": {"dimension": "Kommunikation und Abstimmung", "text": "Wie häufig müssen in Ihrem Team komplexe Sachverhalte gemeinsam geklärt werden?", "direction": "presence", "criteria": ["k14"]},
    "q10": {"dimension": "Kommunikation und Abstimmung", "text": "Wie wichtig ist die Vermeidung von Missverständnissen und Kommunikationsfehlern in Ihrem Arbeitsalltag?", "direction": "presence", "criteria": ["k12"]},
    "q11": {"dimension": "Kommunikation und Abstimmung", "text": "Wie relevant sind persönliche und situationsbezogene Feedbackprozesse in Ihrem Team?", "direction": "presence", "criteria": ["k15"]},
    "q12": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie wichtig sind persönlicher Kontakt und soziale Interaktion für den Zusammenhalt Ihres Teams?", "direction": "presence", "criteria": ["k16", "k19"]},
    "q13": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie stark basiert die Zusammenarbeit Ihres Teams auf gegenseitigem Vertrauen und persönlichen Beziehungen?", "direction": "presence", "criteria": ["k17", "k18"]},
    "q14": {"dimension": "Teamdynamik und soziale Einbindung", "text": "Wie wichtig ist die soziale Integration neuer Mitarbeitender für die Stabilität Ihres Teams?", "direction": "presence", "criteria": ["k20"]},
    "q15": {"dimension": "Mitarbeitendenbezogene Faktoren", "text": "Wie hoch ist das Bedürfnis Ihrer Mitarbeitenden nach räumlicher Flexibilität und individueller Arbeitsgestaltung?", "direction": "remote", "criteria": ["k21", "k22"]},
    "q16": {"dimension": "Mitarbeitendenbezogene Faktoren", "text": "Welche Bedeutung haben hybride Arbeitsmöglichkeiten für Zufriedenheit und Motivation Ihrer Mitarbeitenden?", "direction": "remote", "criteria": ["k23", "k24", "k25"]},
    "q17": {"dimension": "Führung", "text": "Wie stark basiert Ihre Führungsarbeit auf persönlichem Austausch und unmittelbarer Interaktion mit dem Team?", "direction": "presence", "criteria": ["k29", "k30"]},
    "q18": {"dimension": "Führung", "text": "Wie wichtig ist direkte Präsenz für die Steuerung und Koordination Ihres Teams?", "direction": "presence", "criteria": ["k26", "k27", "k28"]},
    "q19": {"dimension": "Effizienz und Produktivität", "text": "Wie stark profitiert die Produktivität Ihres Teams von ruhigen und störungsarmen Arbeitsbedingungen?", "direction": "remote", "criteria": ["k31", "k33"]},
    "q20": {"dimension": "Effizienz und Produktivität", "text": "Wie effizient funktioniert die Zusammenarbeit Ihres Teams im Remote-Kontext?", "direction": "remote", "criteria": ["k32", "k34"]},
    "q21": {"dimension": "Effizienz und Produktivität", "text": "Wie stark erfolgt die Leistungsbewertung in Ihrem Team primär ergebnisorientiert?", "direction": "remote", "criteria": ["k35"]},
    "q22": {"dimension": "Teamstruktur und Reifegrad", "text": "Wie eingespielt und erfahren ist Ihr Team in der Zusammenarbeit?", "direction": "remote", "criteria": ["k36", "k37"]},
    "q23": {"dimension": "Teamstruktur und Reifegrad", "text": "Wie selbstorganisiert und strukturell stabil arbeitet Ihr Team?", "direction": "remote", "criteria": ["k38", "k39"]},
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
### Wissenschaftliche Grundlage des Bewertungsmodells

Das Bewertungsmodell basiert auf einer Kombination qualitativer und quantitativer Forschung.

In einer ersten Forschungsphase wurden leitfadengestützte Experteninterviews mit Führungskräften aus der IT-Branche durchgeführt. Ziel war die Identifikation relevanter Einflussfaktoren auf die Gestaltung hybrider Arbeitsmodelle.

In einer zweiten Phase wurden diese Kriterien im Rahmen einer standardisierten Befragung hinsichtlich ihrer:
- Relevanz für die Bestimmung des Präsenzanteils
- Abhängigkeit von physischer Präsenz

quantitativ bewertet.

Die empirisch ermittelten Mittelwerte dienen im vorliegenden Modell als Gewichtungsgrundlage. Kriterien mit höherer Relevanz und höherer Präsenzabhängigkeit beeinflussen die spätere Empfehlung somit stärker als weniger relevante Faktoren.
""")

st.info("Bewertungsskala: 1 = trifft gar nicht zu | 5 = trifft voll zu")

start = st.button("➡️ Fragebogen starten")

if start:
    st.session_state["started"] = True

if st.session_state.get("started"):
    st.markdown("---")
    st.warning("""
        Die Fragen beziehen sich nicht auf individuelle Präferenzen einzelner Mitarbeitender, 
        sondern auf die strukturellen Anforderungen des jeweiligen Teams und der Zusammenarbeit.

        Bitte beantworten Sie die Fragen möglichst aus der Perspektive der tatsächlichen Arbeitsanforderungen Ihres Teams.
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

    calculate = st.button("📊 Ergebnis berechnen")

    if calculate:
        total_score, question_df, dimension_df = calculate_scores(answers)
        result = model_from_score(total_score)

        st.header("📊 Ergebnis des Bewertungsmodells")

        st.success(f"Empfohlenes Arbeitsmodell: **{result['model']}**")
        st.subheader(f"Empfohlener Präsenzanteil: {result['days']}")
        st.write(result["description"])

        st.progress(max(0, min(100, int(total_score))))
        st.caption(f"Gesamtscore: {round(total_score, 1)} von 100 Punkten")
        st.info("""
        Der Gesamtscore stellt keine absolute Bewertung dar, sondern dient als Orientierungswert innerhalb des entwickelten Bewertungsmodells.

        Ein Wert von 50 Punkten entspricht einem theoretischen Gleichgewicht zwischen präsenzfördernden und remote-fördernden Faktoren. 
        Werte oberhalb von 50 sprechen tendenziell für einen höheren Präsenzanteil, während niedrigere Werte auf eine stärkere Eignung für ortsunabhängiges Arbeiten hinweisen.
        """)

        st.markdown("""
        ### Interpretation der Einflussfaktoren

        Die folgenden Dimensionen haben den größten Einfluss auf die berechnete Empfehlung ausgeübt.

        Dabei bedeutet:
        - positiver Beitrag = spricht eher für mehr Präsenz
        - negativer Beitrag = spricht eher für mehr Remote-Arbeit
        """)
        st.subheader("Zentrale Treiber der Empfehlung")

        top_dimensions = dimension_df.sort_values(
            by="Abweichungsbeitrag",
            ascending=False
        ).head(3)

        found_positive = False

        for _, row in top_dimensions.iterrows():
            if row["Abweichungsbeitrag"] > 0:
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
            if row["Abweichungsbeitrag"] < 0:
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