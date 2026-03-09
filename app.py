"""
Profil Investisseur — Streamlit
Questionnaire MiFID II : Connaissances · Risque · ESG

Thème    : fond blanc, typographie sobre, accents bleu #2563EB (style dashboard finance)
Graphique: radar chart Plotly (st.plotly_chart) sur l'écran résultats
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ── CONFIGURATION ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Profil Investisseur",
    page_icon="◆",
    layout="centered",
)

# Thème clair épuré — unique bloc CSS, zéro HTML dans le corps.
st.markdown("""
<style>
  /* Fond et typographie */
  .stApp                            { background-color: #F5F7FA; }
  section[data-testid="stSidebar"]  { display: none; }
  html, body, [class*="css"]        { font-family: 'Segoe UI', Arial, sans-serif;
                                      color: #1E293B; }
  h1                                { color: #0F172A !important; font-weight: 600 !important;
                                      letter-spacing: -0.5px; font-size: 1.9rem !important; }
  h2, h3                            { color: #1E293B !important; font-weight: 500 !important; }
  .block-container                  { max-width: 700px; padding-top: 2.5rem;
                                      background: #FFFFFF; border-radius: 12px;
                                      padding: 2.5rem 2rem 2rem; }
  hr                                { border-color: #E2E8F0 !important; }

  /* Inputs */
  input[type="text"]                { background: #F8FAFC !important;
                                      border: 1px solid #CBD5E1 !important;
                                      color: #1E293B !important;
                                      border-radius: 6px !important; }
  input[type="text"]:focus          { border-color: #2563EB !important;
                                      box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important; }

  /* Radio / multiselect */
  .stRadio label                    { color: #334155 !important; font-size: 15px; }
  .stRadio > div                    { gap: 6px; }

  /* Bouton principal */
  .stButton > button                { background: #2563EB !important;
                                      color: #FFFFFF !important;
                                      font-weight: 600 !important;
                                      border: none !important;
                                      border-radius: 6px !important;
                                      letter-spacing: 0.2px;
                                      width: 100%; }
  .stButton > button:hover          { background: #1D4ED8 !important; }

  /* Métriques */
  [data-testid="stMetric"]          { background: #F8FAFC;
                                      border: 1px solid #E2E8F0;
                                      border-radius: 8px;
                                      padding: 14px !important; }
  [data-testid="stMetricLabel"]     { color: #64748B !important;
                                      font-size: 11px !important;
                                      text-transform: uppercase;
                                      letter-spacing: 1.2px; }
  [data-testid="stMetricValue"]     { color: #0F172A !important;
                                      font-size: 18px !important;
                                      font-weight: 600 !important; }
  [data-testid="stMetricDelta"]     { color: #2563EB !important;
                                      font-size: 12px !important; }

  /* Barre de progression */
  [data-testid="stProgressBar"] > div > div { background: #2563EB !important; }

  /* Multiselect tags */
  .stMultiSelect span[data-baseweb="tag"] { background: #DBEAFE !important;
                                            color: #1D4ED8 !important; }

  /* Caption / textes secondaires */
  .stCaption, small                 { color: #94A3B8 !important; }
</style>
""", unsafe_allow_html=True)

# ── DONNÉES ───────────────────────────────────────────────────────────────────

QUESTIONS = [
    # — Connaissances —
    {"id": "Q1",  "section": "Connaissances", "multi": False,
     "label": "Qu'est-ce qu'une action ?",
     "answers": [("Un organisme de placement.", 0),
                 ("Une part de la dette d'une entreprise.", 0),
                 ("Une part du capital d'une entreprise.", 3)]},

    {"id": "Q2",  "section": "Connaissances", "multi": False,
     "label": "Diversifier son épargne, c'est…",
     "answers": [("…potentiellement diminuer les frais.", 0),
                 ("…potentiellement diminuer les risques.", 3),
                 ("…potentiellement améliorer le rendement.", 0)]},

    {"id": "Q3",  "section": "Connaissances", "multi": False,
     "label": "Combien d'opérations boursières effectuez-vous par an ?",
     "answers": [("Moins de 10.", 0), ("Entre 10 et 40.", 2), ("Plus de 40.", 3)]},

    {"id": "Q4",  "section": "Connaissances", "multi": False,
     "label": "Possédez-vous une assurance vie et / ou un Compte-titres ?",
     "answers": [("Oui", 1), ("Non", 0)]},

    {"id": "Q5",  "section": "Connaissances", "multi": False,
     "label": "Quand deux placements sont corrélés…",
     "answers": [("Ils évoluent différemment.", 0),
                 ("Ils évoluent dans le même sens.", 3),
                 ("Ils appartiennent au même groupe financier.", 0)]},

    {"id": "Q6",  "section": "Connaissances", "multi": False,
     "label": "Un placement liquide est un placement…",
     "answers": [("Consommant de l'eau (ex : datacenter).", 0),
                 ("Que je peux transférer gratuitement dans un héritage.", 0),
                 ("Avec lequel je peux récupérer l'argent à tout moment.", 3)]},

    {"id": "Q7",  "section": "Connaissances", "multi": False,
     "label": "Parmi ces placements, lequel constitue une épargne de précaution ?",
     "answers": [("Un livret A.", 3),
                 ("Un CTO avec mandat de gestion produits structurés.", 0),
                 ("Un investissement dans la pierre-papier.", 0)]},

    {"id": "Q8",  "section": "Connaissances", "multi": False,
     "label": "Le Private Equity, aussi appelé capital-investissement…",
     "answers": [("Constitue une épargne pleinement liquide.", 0),
                 ("Investit dans des actifs non cotés (entreprises, immobilier, infrastructure).", 3),
                 ("Permet d'investir strictement en local.", 0)]},

    {"id": "Q9",  "section": "Connaissances", "multi": True,
     "label": "J'ai déjà investi dans ces produits…",
     "answers": [("Actions", 1), ("Obligations", 1), ("ETF", 1),
                 ("Produits structurés", 2), ("Private Equity", 2), ("Produits dérivés", 1)]},

    # — Risque —
    {"id": "Q10", "section": "Risque", "multi": False,
     "label": "Que souhaitez-vous faire de vos investissements ?",
     "answers": [("Préserver le capital.", 1),
                 ("Générer un revenu complémentaire.", 2),
                 ("Faire croître progressivement le capital.", 3),
                 ("Maximiser la performance à long terme.", 4)]},

    {"id": "Q11", "section": "Risque", "multi": False,
     "label": "À quel horizon souhaitez-vous placer votre argent ?",
     "answers": [("Moins de 2 ans.", 1), ("2 à 5 ans.", 2),
                 ("5 à 8 ans.", 3), ("Plus de 8 ans.", 4)]},

    {"id": "Q12", "section": "Risque", "multi": False,
     "label": "Quelle partie de votre patrimoine allez-vous investir ?",
     "answers": [("Plus de 75 %.", 1), ("Entre 50 % et 75 %.", 2),
                 ("Entre 25 % et 50 %.", 3), ("Moins de 25 %.", 4)]},

    {"id": "Q13", "section": "Risque", "multi": False,
     "label": "Votre investissement vient de chuter de 15 %.",
     "answers": [("Je vends immédiatement.", 1),
                 ("J'attends que ça remonte.", 2),
                 ("Je conserve sans changer.", 3),
                 ("J'en profite pour investir davantage.", 4)]},

    {"id": "Q14", "section": "Risque", "multi": False,
     "label": "Quelle est votre capacité à immobiliser les fonds investis ?",
     "answers": [("Disponibles à tout moment.", 1),
                 ("Une partie immobilisée moins de 3 ans.", 2),
                 ("Immobilisation 3 à 8 ans.", 3),
                 ("Immobilisation plus de 8 ans.", 4)]},

    # — ESG —
    {"id": "Q15", "section": "ESG", "multi": False,
     "label": "Souhaitez-vous intégrer des critères ESG dans vos investissements ?",
     "answers": [("Non, la performance financière est prioritaire.", 0),
                 ("Oui, si cela n'impacte pas significativement la performance.", 1),
                 ("Oui, je privilégie des fonds intégrant des critères ESG.", 2),
                 ("Oui, je souhaite une stratégie majoritairement durable.", 3)]},

    {"id": "Q16", "section": "ESG", "multi": False,
     "label": "Quel niveau d'engagement souhaitez-vous en investissement durable ?",
     "answers": [("Aucune contrainte spécifique.", 0),
                 ("Exclusion des armes controversées uniquement.", 1),
                 ("Exclusions sectorielles + sélection ESG active.", 2),
                 ("Alignement avec des objectifs environnementaux mesurables.", 3)]},

    {"id": "Q17", "section": "ESG", "multi": False,
     "label": "Seriez-vous favorable à investir dans des entreprises contribuant à :",
     "answers": [("Aucune préférence particulière.", 0),
                 ("La transition énergétique.", 1),
                 ("La réduction mesurable des émissions carbone.", 2),
                 ("L'alignement avec la taxonomie européenne durable.", 3)]},

    # Q18 : exclusions sectorielles, sans score
    {"id": "Q18", "section": "ESG", "multi": True, "exclusion": True,
     "label": "Quelles industries souhaitez-vous exclure de votre portefeuille ?",
     "answers": [("Armement / armes controversées", 0), ("Tabac", 0),
                 ("Charbon thermique", 0), ("Pétrole et gaz non conventionnels", 0),
                 ("Jeux d'argent", 0), ("Pornographie", 0),
                 ("Production d'énergie fortement carbonée", 0),
                 ("Entreprises hors Pacte Mondial ONU", 0),
                 ("Combustibles fossiles", 0), ("Huile de palme non durable", 0),
                 ("OGM non encadrés", 0), ("Extraction minière controversée", 0)]},
]

SECTIONS = {
    "Connaissances": {"icon": "📘"},
    "Risque":        {"icon": "⚖️"},
    "ESG":           {"icon": "🌿"},
}

RESULTS = {
    "Connaissances": [
        (0,  9,  "Débutant",      "Vous débutez dans l'univers de l'investissement. Nous vous accompagnerons avec des solutions pédagogiques adaptées."),
        (10, 19, "Intermédiaire", "Bonne compréhension des bases. Vous êtes prêt(e) pour des stratégies plus diversifiées."),
        (20, 30, "Avancé",        "Vous maîtrisez les concepts financiers complexes et pouvez accéder à des produits sophistiqués."),
    ],
    "Risque": [
        (0,  5,  "Prudent",   "La préservation du capital est votre priorité. Vous privilégiez la sécurité sur le rendement."),
        (6,  10, "Équilibré", "Vous recherchez un équilibre entre performance et sécurité, avec une tolérance modérée à la volatilité."),
        (11, 15, "Dynamique", "Vous acceptez une volatilité importante pour viser des rendements supérieurs sur le long terme."),
        (16, 20, "Offensif",  "Vous recherchez la performance maximale et acceptez des fluctuations significatives."),
    ],
    "ESG": [
        (0, 3, "Neutre",    "La performance financière reste votre critère principal. Les aspects ESG ne sont pas une priorité à ce stade."),
        (4, 6, "Intéressé", "Vous portez un intérêt croissant aux enjeux durables, à intégrer progressivement."),
        (7, 9, "Engagé",    "Le développement durable est au cœur de votre stratégie patrimoniale."),
    ],
}

MAX_SCORES = {"Connaissances": 30, "Risque": 20, "ESG": 9}

NAV_QUESTIONS = [q for q in QUESTIONS if not q.get("exclusion")]

# ── HELPERS ───────────────────────────────────────────────────────────────────

def get_profile(section: str, score: int) -> tuple:
    for mn, mx, label, desc in RESULTS[section]:
        if mn <= score <= mx:
            return label, desc
    return "—", ""


def compute_scores() -> dict:
    scores = {s: 0 for s in SECTIONS}
    for q in NAV_QUESTIONS:
        ans = st.session_state.answers.get(q["id"])
        if not ans:
            continue
        answer_map = {label: score for label, score in q["answers"]}
        if q["multi"]:
            scores[q["section"]] += sum(answer_map.get(a, 0) for a in ans)
        else:
            scores[q["section"]] += answer_map.get(ans, 0)
    return scores


def radar_chart(scores: dict) -> go.Figure:
    """
    Radar chart Plotly — représente les 3 dimensions du profil.
    Les scores sont normalisés en pourcentage du score max de chaque section.
    """
    sections   = list(SECTIONS.keys())
    pct_scores = [round(scores[s] / MAX_SCORES[s] * 100) for s in sections]

    # Fermeture du polygone (Plotly exige de répéter le 1er point)
    categories = sections + [sections[0]]
    values     = pct_scores + [pct_scores[0]]

    fig = go.Figure()

    # Zone remplie — thème clair
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(37, 99, 235, 0.10)",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=7, color="#2563EB"),
        name="Votre profil",
        hovertemplate="%{theta} : %{r}%<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="#FFFFFF",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="%",
                tickfont=dict(size=10, color="#94A3B8"),
                gridcolor="#E2E8F0",
                linecolor="#E2E8F0",
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="#334155"),
                gridcolor="#E2E8F0",
                linecolor="#E2E8F0",
            ),
        ),
        paper_bgcolor="#F5F7FA",
        plot_bgcolor="#F5F7FA",
        showlegend=False,
        margin=dict(t=40, b=40, l=60, r=60),
        height=360,
    )
    return fig

# ── SESSION STATE ─────────────────────────────────────────────────────────────

def init():
    defaults = {
        "phase":      "welcome",
        "current_q":  0,
        "answers":    {},
        "first_name": "",
        "last_name":  "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── ÉCRAN ACCUEIL ─────────────────────────────────────────────────────────────

def render_welcome():
    st.markdown("##### ◆ PROFIL INVESTISSEUR")
    st.title("Construisons votre profil patrimonial")
    st.caption(
        "Un questionnaire en trois étapes pour définir votre stratégie d'investissement "
        "personnalisée, conforme aux exigences MiFID II."
    )
    st.divider()

    cols = st.columns(3)
    for col, (name, meta) in zip(cols, SECTIONS.items()):
        q_count = sum(1 for q in NAV_QUESTIONS if q["section"] == name)
        with col:
            st.metric(label=f"{meta['icon']}  {name}", value=f"{q_count} questions")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        fn = st.text_input("Prénom", placeholder="Ferdinand")
        st.session_state.first_name = fn
    with c2:
        ln = st.text_input("Nom", placeholder="Bardamu")
        st.session_state.last_name = ln

    st.write("")
    if st.button("Commencer le questionnaire →", disabled=not (fn and ln)):
        st.session_state.phase = "questions"
        st.session_state.current_q = 0
        st.rerun()

# ── ÉCRAN QUESTIONS ───────────────────────────────────────────────────────────

def render_questions():
    idx   = st.session_state.current_q
    q     = NAV_QUESTIONS[idx]
    total = len(NAV_QUESTIONS)
    meta  = SECTIONS[q["section"]]

    st.progress(
        (idx + 1) / total,
        text=f"{meta['icon']}  **{q['section']}**  ·  Question {idx + 1} / {total}"
    )
    st.divider()

    st.caption("Plusieurs réponses possibles" if q["multi"] else "Une seule réponse")
    st.subheader(q["label"])

    labels  = [label for label, _ in q["answers"]]
    cur_ans = st.session_state.answers.get(q["id"])

    if q["multi"]:
        default = cur_ans if isinstance(cur_ans, list) else []
        chosen  = st.multiselect("", labels, default=default, key=f"w_{q['id']}")
        st.session_state.answers[q["id"]] = chosen or None
        can_go  = True
    else:
        default_idx = labels.index(cur_ans) if cur_ans in labels else None
        chosen = st.radio("", labels, index=default_idx, key=f"w_{q['id']}")
        if chosen:
            st.session_state.answers[q["id"]] = chosen
        can_go = chosen is not None

    # Q18 — exclusions ESG, affichée sur la dernière question
    is_last = idx == total - 1
    if is_last:
        st.divider()
        q18         = next(q for q in QUESTIONS if q["id"] == "Q18")
        excl_labels = [l for l, _ in q18["answers"]]
        cur_excl    = st.session_state.answers.get("Q18") or []
        st.caption("Optionnel — Exclusions sectorielles ESG")
        st.subheader(q18["label"])
        chosen_excl = st.multiselect("", excl_labels, default=cur_excl, key="w_Q18")
        st.session_state.answers["Q18"] = chosen_excl or None

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if idx > 0 and st.button("← Précédent"):
            st.session_state.current_q -= 1
            st.rerun()
    with c2:
        label_next = "Voir mes résultats →" if is_last else "Suivant →"
        if st.button(label_next, disabled=not can_go):
            st.session_state.phase = "results" if is_last else "questions"
            if not is_last:
                st.session_state.current_q += 1
            st.rerun()

# ── ÉCRAN RÉSULTATS ───────────────────────────────────────────────────────────

def render_results():
    scores = compute_scores()
    date   = datetime.now().strftime("%d %B %Y")

    st.markdown("##### ◆ PROFIL INVESTISSEUR")
    st.title(f"{st.session_state.first_name} {st.session_state.last_name}")
    st.caption(f"Évaluation MiFID II · {date}")
    st.divider()

    # — Radar chart —
    st.plotly_chart(radar_chart(scores), use_container_width=True)
    st.divider()

    # — Métriques synthèse —
    cols = st.columns(3)
    for col, (section, _) in zip(cols, SECTIONS.items()):
        label, _ = get_profile(section, scores[section])
        with col:
            st.metric(
                label=section,
                value=label,
                delta=f"{scores[section]} / {MAX_SCORES[section]} pts",
            )

    st.divider()

    # — Détail par section —
    for section, meta in SECTIONS.items():
        label, desc = get_profile(section, scores[section])
        st.markdown(f"**{meta['icon']}  {section}** — {label}")
        st.write(desc)

        if section == "ESG":
            excl = st.session_state.answers.get("Q18") or []
            if excl:
                st.info("**Secteurs exclus :** " + " · ".join(excl))

        st.divider()

    st.caption(
        "Ce questionnaire a été réalisé conformément aux exigences de la directive MiFID II. "
        "Les résultats ne constituent pas un conseil en investissement. "
        f"Document généré le {date} · Confidentiel."
    )

    st.write("")
    if st.button("← Recommencer"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ── ROUTEUR ───────────────────────────────────────────────────────────────────

PAGES = {
    "welcome":   render_welcome,
    "questions": render_questions,
    "results":   render_results,
}

PAGES[st.session_state.phase]()
