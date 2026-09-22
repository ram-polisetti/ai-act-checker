"""Curated knowledge base derived from the official EU AI Act text.

Source: Regulation (EU) 2024/1689 of the European Parliament and of the
Council, EUR-Lex EN TXT, OJ L 2024/1689
(https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689),
retrieved 2026-09-22. Descriptions below are short paraphrases of the
operative provisions; the citation attached to each rule points at the
exact article/paragraph so any determination can be checked against the
source text.

This file is data, not legal advice. The checker is a triage aid: it maps
a described system onto the Act's categories. It is not a substitute for
legal review, and edge cases (especially Article 6(3) derogations and
Article 5 exceptions) always need a lawyer.
"""

ACT_CITATION = "Regulation (EU) 2024/1689 (OJ L 2024/1689)"
ACT_SOURCE_URL = (
    "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689"
)
KNOWLEDGE_DATE = "2026-09-22"

# ---------------------------------------------------------------------------
# Article 5 — Prohibited AI practices (unacceptable risk)
# ---------------------------------------------------------------------------
# Each rule: id, article citation, short title, description, and the input
# flags (keys of the system-description schema) that trigger it. All flags
# that must hold are listed under "all_of"; any-of groups under "any_of".
PROHIBITIONS = [
    {
        "id": "P-a",
        "article": "Article 5(1)(a)",
        "title": "Subliminal, manipulative or deceptive techniques",
        "description": (
            "AI systems deploying subliminal techniques beyond a person's "
            "consciousness, or purposefully manipulative or deceptive "
            "techniques, with the objective or effect of materially "
            "distorting behaviour and causing significant harm."
        ),
        "all_of": ["manipulative_techniques"],
    },
    {
        "id": "P-b",
        "article": "Article 5(1)(b)",
        "title": "Exploitation of vulnerabilities",
        "description": (
            "AI systems exploiting vulnerabilities of a natural person or "
            "group due to age, disability, or a specific social or economic "
            "situation, with the objective or effect of materially "
            "distorting behaviour and causing significant harm."
        ),
        "all_of": ["exploits_vulnerability"],
    },
    {
        "id": "P-c",
        "article": "Article 5(1)(c)",
        "title": "Social scoring",
        "description": (
            "AI systems for the evaluation or classification of natural "
            "persons or groups over time based on social behaviour or "
            "known, inferred or predicted personal characteristics, where "
            "the score leads to detrimental treatment in unrelated "
            "contexts, or to disproportionate treatment."
        ),
        "all_of": ["social_scoring"],
    },
    {
        "id": "P-d",
        "article": "Article 5(1)(d)",
        "title": "Predictive policing / criminal risk assessment",
        "description": (
            "AI systems making risk assessments of natural persons to "
            "assess or predict the risk of committing a criminal offence, "
            "based solely on profiling or personality traits and "
            "characteristics."
        ),
        "all_of": ["crime_risk_assessment"],
    },
    {
        "id": "P-e",
        "article": "Article 5(1)(e)",
        "title": "Untargeted facial scraping",
        "description": (
            "AI systems creating or expanding facial recognition databases "
            "through the untargeted scraping of facial images from the "
            "internet or CCTV footage."
        ),
        "all_of": ["untargeted_facial_scraping"],
    },
    {
        "id": "P-f",
        "article": "Article 5(1)(f)",
        "title": "Emotion inference at work or in education",
        "description": (
            "AI systems inferring emotions of a natural person in the "
            "areas of workplace and education institutions (except where "
            "permitted by law for medical or safety reasons)."
        ),
        "all_of": ["emotion_inference"],
        "any_of": ["workplace", "education"],
    },
    {
        "id": "P-g",
        "article": "Article 5(1)(g)",
        "title": "Biometric categorisation by sensitive attributes",
        "description": (
            "Biometric categorisation systems that categorise natural "
            "persons based on biometric data to deduce or infer race, "
            "political opinions, trade union membership, religious or "
            "philosophical beliefs, sex life or sexual orientation."
        ),
        "all_of": ["biometric_categorisation_sensitive"],
    },
    {
        "id": "P-h",
        "article": "Article 5(1)(h)",
        "title": "Real-time remote biometric identification in public",
        "description": (
            "Use of 'real-time' remote biometric identification systems in "
            "publicly accessible spaces for law enforcement purposes, "
            "unless strictly necessary for one of the narrow exceptions "
            "(e.g. searching for certain crime victims, preventing a "
            "genuine terrorist threat, identifying suspects of serious "
            "listed offences) and authorised in advance."
        ),
        "all_of": [
            "real_time_remote_biometric_id",
            "public_space",
            "law_enforcement",
        ],
    },
]

# ---------------------------------------------------------------------------
# Annex III — High-risk AI systems (Article 6(2))
# ---------------------------------------------------------------------------
# Each area carries the Annex III point and the use-case keywords that map
# a described system onto it. "keywords" are matched against the
# space-separated "use_case_tags" in the system description.
ANNEX_III_AREAS = [
    {
        "point": "Annex III, point 1",
        "area": "Biometrics",
        "citation": "Annex III, point 1(a)-(c)",
        "description": (
            "Remote biometric identification systems (other than those "
            "prohibited by Article 5); biometric categorisation according "
            "to sensitive or protected attributes; emotion recognition "
            "systems."
        ),
        "keywords": [
            "remote_biometric_identification",
            "biometric_categorisation",
            "emotion_recognition",
        ],
    },
    {
        "point": "Annex III, point 2",
        "area": "Critical infrastructure",
        "citation": "Annex III, point 2",
        "description": (
            "AI systems intended as safety components in the management "
            "and operation of critical digital infrastructure, road "
            "traffic, or the supply of water, gas, heating or electricity."
        ),
        "keywords": [
            "critical_digital_infrastructure",
            "road_traffic",
            "water_supply",
            "gas_supply",
            "heating_supply",
            "electricity_supply",
        ],
    },
    {
        "point": "Annex III, point 3",
        "area": "Education and vocational training",
        "citation": "Annex III, point 3(a)-(d)",
        "description": (
            "Determining access or admission to education; evaluating "
            "learning outcomes; assessing the appropriate level of "
            "education; monitoring and detecting prohibited behaviour of "
            "students during tests."
        ),
        "keywords": [
            "education_admission",
            "learning_outcome_evaluation",
            "education_level_assessment",
            "exam_proctoring",
        ],
    },
    {
        "point": "Annex III, point 4",
        "area": "Employment, workers management, access to self-employment",
        "citation": "Annex III, point 4(a)-(b)",
        "description": (
            "Recruitment or selection (targeted job ads, CV screening, "
            "candidate evaluation); decisions on work-related relationships "
            "(promotion, termination), task allocation, or monitoring and "
            "evaluation of performance and behaviour."
        ),
        "keywords": [
            "recruitment",
            "cv_screening",
            "candidate_evaluation",
            "promotion_decision",
            "termination_decision",
            "task_allocation",
            "worker_monitoring",
            "performance_evaluation",
        ],
    },
    {
        "point": "Annex III, point 5",
        "area": "Essential private and public services",
        "citation": "Annex III, point 5(a)-(d)",
        "description": (
            "Eligibility for public assistance benefits; creditworthiness "
            "evaluation (except to detect financial fraud); risk assessment "
            "and pricing in life and health insurance; emergency-call "
            "evaluation and triage."
        ),
        "keywords": [
            "public_benefits_eligibility",
            "creditworthiness",
            "insurance_risk_pricing",
            "emergency_call_triage",
        ],
    },
    {
        "point": "Annex III, point 6",
        "area": "Law enforcement",
        "citation": "Annex III, point 6(a)-(g)",
        "description": (
            "Risk assessments of reoffending; polygraphs and similar tools; "
            "evaluating reliability of evidence; predicting crime based on "
            "profiling; profiling during detection/investigation of "
            "offences; crime analytics for persons."
        ),
        "keywords": [
            "recidivism_risk",
            "polygraph",
            "evidence_reliability",
            "crime_prediction",
            "criminal_profiling",
            "crime_analytics",
        ],
    },
    {
        "point": "Annex III, point 7",
        "area": "Migration, asylum and border control",
        "citation": "Annex III, point 7(a)-(d)",
        "description": (
            "Risk assessment for irregular immigration or security risk; "
            "assessing document authenticity; assisting the examination of "
            "asylum, visa or residence-permit applications."
        ),
        "keywords": [
            "immigration_risk",
            "document_authenticity",
            "asylum_application",
            "visa_application",
        ],
    },
    {
        "point": "Annex III, point 8",
        "area": "Administration of justice and democratic processes",
        "citation": "Annex III, point 8(a)-(b)",
        "description": (
            "Assisting judicial authorities in researching and interpreting "
            "facts and law; influencing the outcome of an election or "
            "referendum, or the voting behaviour of natural persons "
            "(except output labelling under Article 50)."
        ),
        "keywords": [
            "judicial_decision_support",
            "election_influence",
        ],
    },
]

# Article 6(1): AI as safety component of products covered by Annex I
# Union harmonisation legislation (machinery, medical devices, etc.)
ANNEX_I_SAFETY_COMPONENT = {
    "article": "Article 6(1)",
    "title": "Safety component under Annex I product legislation",
    "description": (
        "The AI system is intended as a safety component of a product "
        "(or is itself such a product) covered by the Union harmonisation "
        "legislation listed in Annex I, and that product requires "
        "third-party conformity assessment."
    ),
}

# ---------------------------------------------------------------------------
# Article 50 — Transparency obligations (limited risk)
# ---------------------------------------------------------------------------
TRANSPARENCY_RULES = [
    {
        "id": "T-1",
        "article": "Article 50(1)",
        "title": "Disclosure of AI interaction",
        "description": (
            "Providers of AI systems intended to interact directly with "
            "natural persons must ensure those persons are informed they "
            "are interacting with an AI system."
        ),
        "all_of": ["interacts_with_persons"],
    },
    {
        "id": "T-2",
        "article": "Article 50(2)",
        "title": "Machine-readable marking of synthetic content",
        "description": (
            "Providers of AI systems (including GPAI systems) generating "
            "synthetic audio, image, video or text content must ensure "
            "outputs are marked in a machine-readable format and detectable "
            "as artificially generated or manipulated."
        ),
        "all_of": ["generates_synthetic_content"],
    },
    {
        "id": "T-3",
        "article": "Article 50(3)",
        "title": "Notice for emotion recognition / biometric categorisation",
        "description": (
            "Deployers of an emotion recognition or biometric "
            "categorisation system must inform exposed natural persons of "
            "the system's operation."
        ),
        "any_of": ["emotion_recognition_deployed", "biometric_categorisation_deployed"],
    },
    {
        "id": "T-4",
        "article": "Article 50(4)",
        "title": "Deepfake disclosure",
        "description": (
            "Deployers of an AI system generating or manipulating image, "
            "audio or video content constituting a deep fake must disclose "
            "that the content was artificially generated or manipulated."
        ),
        "all_of": ["deepfake"],
    },
]

# ---------------------------------------------------------------------------
# Articles 51-55 — General-purpose AI models
# ---------------------------------------------------------------------------
SYSTEMIC_RISK_FLOP_THRESHOLD = 1e25  # Article 51(2): > 10^25 FLOP

GPAI_PROVIDER_DUTIES = [
    {
        "article": "Article 53(1)(a), Annex XI",
        "duty": "Draw up and keep up-to-date technical documentation of the model.",
    },
    {
        "article": "Article 53(1)(b), Annex XII",
        "duty": (
            "Draw up, keep up-to-date and make available information and "
            "documentation to providers intending to integrate the model "
            "into their AI systems."
        ),
    },
    {
        "article": "Article 53(1)(c)",
        "duty": (
            "Put in place a policy to comply with Union copyright law, "
            "including identifying and complying with reservations of "
            "rights (opt-outs) under Directive (EU) 2019/790."
        ),
    },
    {
        "article": "Article 53(1)(d)",
        "duty": (
            "Draw up and make publicly available a sufficiently detailed "
            "summary of the content used for training."
        ),
    },
    {
        "article": "Article 53(2)",
        "duty": (
            "Note: providers of GPAI models released under a free and "
            "open-source licence are exempt from the (a) and (b) duties, "
            "unless the model presents systemic risk."
        ),
    },
]

SYSTEMIC_RISK_DUTIES = [
    {
        "article": "Article 55(1)(a)",
        "duty": (
            "Perform model evaluations per standardised protocols, "
            "including adversarial testing, to identify and mitigate "
            "systemic risks."
        ),
    },
    {
        "article": "Article 55(1)(b)",
        "duty": (
            "Assess and mitigate possible systemic risks at Union level, "
            "including their sources."
        ),
    },
    {
        "article": "Article 55(1)(c)",
        "duty": (
            "Track, document and report serious incidents and corrective "
            "measures to the AI Office and national authorities without "
            "undue delay."
        ),
    },
    {
        "article": "Article 55(1)(d)",
        "duty": (
            "Ensure an adequate level of cybersecurity protection for the "
            "model and its physical infrastructure."
        ),
    },
]

# ---------------------------------------------------------------------------
# High-risk conformity checklist — Chapter III, Section 2 requirements
# (Articles 9-15) plus provider/deployer duties.
# ---------------------------------------------------------------------------
HIGH_RISK_CHECKLIST = [
    {
        "article": "Article 9",
        "item": "Risk management system",
        "detail": (
            "Establish, implement, document and maintain a risk management "
            "system as a continuous iterative process throughout the "
            "high-risk AI system's lifecycle."
        ),
    },
    {
        "article": "Article 10",
        "item": "Data and data governance",
        "detail": (
            "Training, validation and testing datasets must be relevant, "
            "sufficiently representative, as error-free as possible, and "
            "have appropriate statistical properties for the intended "
            "purpose; examine datasets for biases likely to affect health, "
            "safety, fundamental rights or lead to discrimination."
        ),
    },
    {
        "article": "Article 11, Annex IV",
        "item": "Technical documentation",
        "detail": (
            "Draw up technical documentation per Annex IV before placing on "
            "the market or putting into service, and keep it up to date."
        ),
    },
    {
        "article": "Article 12",
        "item": "Record-keeping / logging",
        "detail": (
            "Design the system with automatic logging capabilities; for "
            "Annex III systems the logs must at minimum record the period "
            "of each use, the reference database used, the input data, and "
            "the persons involved in verification."
        ),
    },
    {
        "article": "Article 13",
        "item": "Transparency and instructions for use",
        "detail": (
            "Design for sufficient transparency; provide instructions for "
            "use covering capabilities, limitations, and the level of "
            "accuracy/robustness so deployers can interpret outputs."
        ),
    },
    {
        "article": "Article 14",
        "item": "Human oversight",
        "detail": (
            "Design for effective human oversight, including the ability to "
            "intervene or stop the system; for biometric identification, "
            "verification by at least two natural persons with the "
            "necessary competence, training and authority."
        ),
    },
    {
        "article": "Article 15",
        "item": "Accuracy, robustness and cybersecurity",
        "detail": (
            "Achieve appropriate levels of accuracy, robustness and "
            "cybersecurity throughout the lifecycle; be resilient to errors, "
            "faults, inconsistencies and adversarial attempts (data "
            "poisoning, model evasion, confidentiality attacks)."
        ),
    },
    {
        "article": "Article 16",
        "item": "Provider obligations",
        "detail": (
            "Ensure the system meets Section 2 requirements; operate a "
            "quality management system (Article 17); complete the "
            "conformity assessment (Article 43); draw up the EU declaration "
            "of conformity and affix the CE marking; take corrective action "
            "and inform authorities where non-conformity is found."
        ),
    },
    {
        "article": "Article 26",
        "item": "Deployer obligations",
        "detail": (
            "Use the system per the instructions; assign human oversight to "
            "persons with competence, training and authority; monitor "
            "operation and report serious incidents and malfunctions."
        ),
    },
    {
        "article": "Article 27",
        "item": "Fundamental rights impact assessment (FRIA)",
        "detail": (
            "Deployers that are bodies governed by public law, or private "
            "entities providing public services, and deployers of Annex "
            "III systems in certain areas must perform a fundamental "
            "rights impact assessment before first use."
        ),
    },
    {
        "article": "Article 43",
        "item": "Conformity assessment",
        "detail": (
            "Follow the applicable conformity assessment procedure — "
            "internal control (Annex VI) or assessment of the quality "
            "management system and technical documentation with a notified "
            "body (Annex VII)."
        ),
    },
    {
        "article": "Article 49, Annex VIII",
        "item": "EU database registration",
        "detail": (
            "Register the high-risk AI system in the EU database with the "
            "information listed in Annex VIII before placing on the market "
            "or putting into service."
        ),
    },
    {
        "article": "Article 72",
        "item": "Post-market monitoring",
        "detail": (
            "Establish a post-market monitoring system proportionate to "
            "the system's nature, collecting data on performance and "
            "serious incidents throughout its lifetime."
        ),
    },
]
