import streamlit as st
import re

st.set_page_config(page_title="LM8 Tutor Agent", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #212121; color: #ececec; }
header[data-testid="stHeader"] { background: transparent; }
.chat-wrap { max-width: 860px; margin: 0 auto; padding: 0 1rem 160px 1rem; }
.msg-ai   { display:flex; justify-content:flex-start;  margin:12px 0; gap:10px; align-items:flex-start; }
.msg-user { display:flex; justify-content:flex-end;    margin:12px 0; gap:10px; align-items:flex-start; }
.msg-ai .bubble {
    background:#2a2a2a; color:#ececec; padding:14px 18px;
    border-radius:18px 18px 18px 4px; max-width:92%;
    font-size:0.93rem; line-height:1.85; border:1px solid #3a3a3a; white-space:pre-wrap;
}
.msg-user .bubble {
    background:#2f2f2f; color:#ececec; padding:12px 16px;
    border-radius:18px 18px 4px 18px; max-width:80%;
    font-size:0.93rem; line-height:1.6; white-space:pre-wrap;
}
.msg-ai   .av { width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#ab68ff,#7c3aed);display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;margin-top:2px; }
.msg-user .av { width:34px;height:34px;border-radius:50%;background:#19c37d;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:white;flex-shrink:0;margin-top:2px; }
.box-green  { background:#052e16;border-left:4px solid #4ade80;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#bbf7d0; }
.box-yellow { background:#1c1600;border-left:4px solid #fbbf24;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#fef08a; }
.box-red    { background:#1f0a0a;border-left:4px solid #f87171;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#fca5a5; }
.box-blue   { background:#0f1f2e;border-left:4px solid #38bdf8;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#bae6fd; }
.box-purple { background:#1a1a2e;border-left:4px solid #818cf8;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#c7d2fe; }
.code-sql { background:#111;border-radius:8px;padding:10px 14px;margin:6px 0;font-family:'Courier New',monospace;font-size:0.83rem;color:#fde68a;display:block;border-left:3px solid #f59e0b;white-space:pre;overflow-x:auto; }
.code-py  { background:#111;border-radius:8px;padding:10px 14px;margin:6px 0;font-family:'Courier New',monospace;font-size:0.83rem;color:#a7f3d0;display:block;border-left:3px solid #34d399;white-space:pre;overflow-x:auto; }
.tag-sql  { background:#f59e0b22;color:#fde68a;border:1px solid #f59e0b;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-py   { background:#34d39922;color:#a7f3d0;border:1px solid #34d399;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.progress-bar-wrap { position:fixed;top:0;left:0;right:0;height:3px;z-index:9999;background:#333; }
.progress-bar-fill { height:100%;background:linear-gradient(90deg,#7c3aed,#19c37d);transition:width 0.5s; }
.top-bar { position:sticky;top:0;background:#212121;border-bottom:1px solid #333;padding:10px 0 8px;margin-bottom:6px;z-index:100; }
.top-bar h2 { text-align:center;font-size:0.9rem;font-weight:500;color:#aaa;margin:0; }
.stButton > button { background:#2a2a2a!important;color:#ececec!important;border:1px solid #444!important;border-radius:20px!important;font-size:0.82rem!important;padding:5px 14px!important;transition:all 0.15s!important; }
.stButton > button:hover { background:#3a3a3a!important;border-color:#7c3aed!important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TASKS — LM8 Assignment, All 4 Questions
# Each task → sub_steps:
#   ask        : what the tutor asks the student
#   nudges     : Socratic hints (questions/pointers, never the answer)
#   check_kw   : keywords indicating a correct/partial response
#   code_errors: specific code mistakes → targeted feedback question
# ═══════════════════════════════════════════════════════════════════════════════

TASKS = [

  # ── Q1 Part A: Understanding the data ──────────────────────────────────────
  {
    "id":"q1a", "qnum":"Q1", "title":"Q1-A — The XOR Dataset",
    "icon":"📊",
    "intro":"""Let's start with <strong>Question 1</strong>.

<div class='box-purple'>
You are given this 4-row dataset:
<span class='code-py'>x, y, class
0, 1, 1
1, 0, 1
1, 1, 0
0, 0, 0</span>
You must run: Logistic Regression, Naïve Bayes, and Bayesian Network on it — then explain what you observe.
</div>

Before writing any code — look at the data carefully.""",
    "sub_steps":[
      {
        "ask":"What pattern do you notice in this dataset? What is the relationship between x, y, and class? Can a straight line separate class=0 from class=1?",
        "nudges":[
          "Plot the four points mentally: (0,1), (1,0), (1,1), (0,0). Which class does each belong to? Is there a diagonal or boundary that separates them?",
          "Notice that class=1 when x≠y and class=0 when x=y. Does that remind you of a logical operation? What is XOR?",
          "XOR (exclusive OR): output is 1 only when inputs differ. This is famously NOT linearly separable — no single straight line can divide the two classes. Why does that matter for Logistic Regression?"
        ],
        "check_kw":["xor","linear","separate","pattern","straight","line","not","boundary","class"],
        "code_errors":{},
      },
      {
        "ask":"Now write the Python code to load this dataset and run all three models: Logistic Regression, Naïve Bayes, and Bayesian Network (use BernoulliNB or GaussianNB for Naïve Bayes). Use training data to test — no train/test split needed here.",
        "nudges":[
          "Start by creating the dataframe manually: pd.DataFrame({'x':[0,1,1,0], 'y':[1,0,1,0], 'class':[1,1,0,0]}). Then set X and y.",
          "For Logistic Regression: LogisticRegression(). For Naïve Bayes: GaussianNB(). For Bayesian Network in sklearn, use BayesianGaussianMixture or just note that sklearn doesn't have a true BN — use the WEKA result or explain conceptually.",
          "Fit each model on X_train=X, y_train=y (same data). Then predict and print accuracy_score(y, model.predict(X))."
        ],
        "check_kw":["logisticregression","gaussiannb","fit","predict","accuracy","dataframe","x","y","class","import"],
        "code_errors":{
          "no_data":("DataFrame","You need to create the dataset first. Have you built the DataFrame with the 4 rows of x, y, class?"),
          "no_fit":("fit","Have you called .fit(X, y) on each model before predicting?"),
          "train_test_split":("train_test_split","With only 4 rows, a train/test split isn't meaningful here. Train and test on the same data — the goal is to see if the model can even learn this pattern."),
        },
      },
    ]
  },

  # ── Q1 Part B: Analyze results ─────────────────────────────────────────────
  {
    "id":"q1b", "qnum":"Q1", "title":"Q1-B — Analyze Model Results",
    "icon":"🔍",
    "intro":"""From the assignment results:
<div class='box-purple'>
• <strong>Logistic Regression (first run)</strong>: 50% accuracy — completely failed
• <strong>Logistic Regression (after tuning)</strong>: 100% accuracy
• <strong>Naïve Bayes</strong>: 50% accuracy — failed
• <strong>Bayesian Network</strong>: 100% accuracy
</div>
Now let's analyze WHY each model succeeded or failed.""",
    "sub_steps":[
      {
        "ask":"Logistic Regression initially got 50% accuracy (no better than random). Why would it fail on this XOR dataset? What is the fundamental limitation of Logistic Regression on this type of data?",
        "nudges":[
          "Logistic Regression creates a linear decision boundary (a straight line in 2D). What did you find earlier about whether XOR data is linearly separable?",
          "If no straight line can separate the classes, what will Logistic Regression do? It will try to find the best line — but the best possible line on XOR data still misclassifies 2 out of 4 points. That's 50%.",
          "Think about it geometrically: class=1 at (0,1) and (1,0), class=0 at (1,1) and (0,0). Any line that separates the 1s will accidentally include one of the 0s. This is the XOR problem."
        ],
        "check_kw":["linear","separable","boundary","xor","straight","line","geometric","fail","limitation"],
        "code_errors":{},
      },
      {
        "ask":"Naïve Bayes also failed (50%). Why? What assumption does Naïve Bayes make that breaks down for this data?",
        "nudges":[
          "The key word is NAÏVE. What does Naïve Bayes assume about the relationship between features x and y?",
          "Naïve Bayes assumes features are CONDITIONALLY INDEPENDENT given the class. Is x independent of y in the XOR pattern?",
          "In XOR, x and y interact — you need to know BOTH to determine the class. Naïve Bayes treats them as independent, so it misses the interaction entirely. That's why it fails."
        ],
        "check_kw":["independent","assumption","naive","conditional","interaction","feature","depend"],
        "code_errors":{},
      },
      {
        "ask":"The Bayesian Network achieved 100% accuracy. Why does it succeed where Naïve Bayes fails? And Logistic Regression was also tuned to get 100% — what parameter change would allow that?",
        "nudges":[
          "Unlike Naïve Bayes, a Bayesian NETWORK can model dependencies between variables. It explicitly learns the structure of how variables relate. So it can capture the x-y interaction.",
          "For Logistic Regression to learn XOR, it needs non-linear features. What if you added an interaction term x*y as a new feature? Then the data becomes linearly separable in 3D.",
          "In sklearn: X['xy'] = X['x'] * X['y'] creates an interaction term. With features [x, y, x*y], Logistic Regression CAN find a separating boundary. Try it!"
        ],
        "check_kw":["interaction","dependency","network","structure","nonlinear","feature","term","xy","multiply","polynomial"],
        "code_errors":{
          "no_interaction":("xy","For Logistic Regression to learn XOR, you need an interaction term. Try adding x*y as a new feature column. Does that help?"),
          "no_polynomial":("PolynomialFeatures","Another option: use sklearn's PolynomialFeatures(degree=2) to automatically create interaction terms. Have you tried that?"),
        },
      },
    ]
  },

  # ── Q2: Ensemble learning ──────────────────────────────────────────────────
  {
    "id":"q2a", "qnum":"Q2", "title":"Q2 — Combining Classification Models",
    "icon":"🤝",
    "intro":"""<strong>Question 2: How can multiple classification models be combined?</strong>

<div class='box-purple'>
This question asks you to explain ensemble learning — combining multiple models to get better predictions than any single model.
Three main methods: <strong>Bagging</strong>, <strong>Boosting</strong>, <strong>Stacking</strong>
</div>""",
    "sub_steps":[
      {
        "ask":"Explain in your own words: why would combining multiple models give better predictions than a single model? What is the core intuition behind ensemble learning?",
        "nudges":[
          "Think about a jury of 12 people vs. one judge making a decision alone. Why might the group be more reliable?",
          "Different models make different kinds of errors — one might overfit, another might underfit, a third might be biased toward certain features. If their errors don't all happen at the same time, what happens when you average them out?",
          "The key insight: models trained with different parameters or on different data subsets generalize in different ways. When you combine them, individual errors cancel out. This is called variance reduction."
        ],
        "check_kw":["combine","average","vote","error","variance","generalize","different","ensemble","reduce","cancel"],
        "code_errors":{},
      },
      {
        "ask":"Now explain the THREE main ensemble methods: Bagging, Boosting, and Stacking. For each one — describe how it works and give an example algorithm.",
        "nudges":[
          "BAGGING: Think about sampling with replacement (bootstrap). You create multiple versions of your training data and train a model on each. Then you average predictions. What famous algorithm does this? Hint: it grows many trees...",
          "BOOSTING: Instead of independent models, boosting builds models SEQUENTIALLY. Each new model focuses on the mistakes of the previous one. What does AdaBoost or Gradient Boosting do?",
          "STACKING: You train base models (level 0), then feed their predictions as inputs to a meta-model (level 1) that learns how to combine them. The meta-model learns which base models to trust more."
        ],
        "check_kw":["bagging","boosting","stacking","random forest","adaboost","gradient","bootstrap","sequential","meta","base","voting"],
        "code_errors":{},
      },
    ]
  },

  # ── Q3: Unit of analysis ───────────────────────────────────────────────────
  {
    "id":"q3a", "qnum":"Q3", "title":"Q3 — Unit of Analysis in testClaims",
    "icon":"🔬",
    "intro":"""<strong>Question 3: What is the unit of analysis? What does one record in the preprocessed data represent?</strong>

<div class='box-purple'>
The raw data has multiple tables:
• <strong>claims_10k</strong> — one row per claim per patient
• <strong>diagnoses</strong> — one row per diagnosis per claim
• <strong>drugcount</strong> — one row per month per patient
• <strong>procedures</strong> — one row per procedure per claim

After preprocessing, all of this collapses into a single analytic dataset.
</div>""",
    "sub_steps":[
      {
        "ask":"After all the SQL preprocessing (cohort → ELIX features → drug features → procedure features → join), what does ONE ROW in the final highUtilizer_Y3_final table represent? And why is that the right unit of analysis for this prediction problem?",
        "nudges":[
          "Look at the final table columns: patient_id, countClaims, highUtilizer, ELIX1-29, drug_early, drug_mid, drug_late, high_drug_use, proc_G12-G17. What is the primary key?",
          "Each row has ONE patient_id. So all the claims, diagnoses, drugs, and procedures have been aggregated UP to the patient level. What does that tell you about the unit?",
          "The prediction problem is: 'will THIS PATIENT be a high utilizer in Y3?' So the unit of analysis must be the patient — not the claim, not the diagnosis, not the month."
        ],
        "check_kw":["patient","unit","row","aggregate","one","level","predict","record","represents"],
        "code_errors":{},
      },
      {
        "ask":"The SQL pipeline uses GROUP BY patient_id in several steps. Why is that critical? What would happen if you forgot the GROUP BY when creating the ELIX features?",
        "nudges":[
          "Without GROUP BY, the MAX(CASE WHEN...) pivot would produce one row per CLAIM per patient instead of one row per PATIENT. How many rows would that be?",
          "If you then joined that multi-row result with the outcome table (which has one row per patient), what type of join problem would you get? Think: would rows multiply?",
          "GROUP BY patient_id collapses all claims for a patient into a single row, aggregating the ELIX flags with MAX(). MAX of {0,0,1,0} = 1, meaning the patient ever had that diagnosis."
        ],
        "check_kw":["group by","patient_id","collapse","aggregate","max","one row","multiply","per patient","claim"],
        "code_errors":{
          "no_group":("group","The GROUP BY patient_id is what collapses multiple claims per patient into one row. Without it, what would the output look like?"),
          "no_max":("max","Why do we use MAX() in the CASE WHEN expressions? What are the possible values of CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END per claim?"),
        },
      },
    ]
  },

  # ── Q4 Part A: Cohort + ELIX SQL ───────────────────────────────────────────
  {
    "id":"q4a", "qnum":"Q4", "title":"Q4-A — Build the Cohort (SQL Step 1)",
    "icon":"🗄️",
    "intro":"""<strong>Question 4: Construct data using 2 years to predict Year 3 high utilization.</strong>
Include: diagnoses (ELIX), drugs, procedures.

<div class='box-purple'>
The full pipeline has these layers:
🥉 <strong>Bronze</strong> — raw extraction from source tables
🥈 <strong>Silver</strong> — cleaning, filtering, feature engineering
🥇 <strong>Gold</strong>  — final ML-ready joined dataset

<strong>Step 1 (Silver): Create the cohort — patients present in BOTH Y1 and Y2</strong>
</div>""",
    "sub_steps":[
      {
        "ask":"Why do we need patients to appear in BOTH Y1 AND Y2? Why not just use all patients who appear in Y1 OR Y2?",
        "nudges":[
          "Think about what features we're building: we're using Y1 AND Y2 data together. If a patient only appears in Y1 but not Y2, their Y2 feature values would all be missing or zero. Is that valid?",
          "Also: we're predicting Y3 outcomes. To have a valid label, a patient needs to appear in Y3 as well. Patients who drop out between Y1 and Y2 are unlikely to have Y3 data.",
          "The HAVING min(year) != max(year) clause checks that a patient's minimum year ≠ maximum year — meaning they appear in at least 2 different years. That ensures longitudinal presence."
        ],
        "check_kw":["both","present","longitudinal","missing","Y1","Y2","having","min","max","drop","valid"],
        "code_errors":{},
      },
      {
        "ask":"Write the SQL to create the cohort #pat_Y1Y2 — patients who appear in both Y1 and Y2.\n<span class='tag-sql'>SQL</span> Use SELECT INTO with GROUP BY and HAVING.",
        "nudges":[
          "Start with: SELECT patient_id INTO #pat_Y1Y2 FROM claims_10k WHERE year IN ('Y1','Y2') GROUP BY patient_id ...",
          "The HAVING clause needs to check that the patient appears in BOTH years. You can use HAVING COUNT(DISTINCT year) = 2, or HAVING min(year) != max(year). Which do you prefer?",
          "Don't forget DROP TABLE IF EXISTS #pat_Y1Y2 before your SELECT INTO — otherwise it will error if the temp table already exists."
        ],
        "check_kw":["group by","having","patient_id","Y1","Y2","into","drop","where","year","distinct"],
        "code_errors":{
          "no_having":("having","You're grouping by patient_id — but how do you filter to only patients present in BOTH years? That's what the HAVING clause does."),
          "no_drop":("drop","Add DROP TABLE IF EXISTS #pat_Y1Y2 before your SELECT INTO to avoid errors on re-run."),
          "wrong_having":("count","Your HAVING clause might not correctly enforce presence in BOTH years. Try HAVING COUNT(DISTINCT year) = 2 or HAVING min(year) != max(year)."),
        },
      },
    ]
  },

  # ── Q4 Part B: ELIX features SQL ───────────────────────────────────────────
  {
    "id":"q4b", "qnum":"Q4", "title":"Q4-B — Elixhauser Features (SQL Step 2)",
    "icon":"🧬",
    "intro":"""<strong>Step 2 (Silver): Build ELIX1–ELIX29 binary features from Y1+Y2 diagnoses.</strong>

<div class='box-purple'>
The diagnoses table has one row per diagnosis per claim.
We need ONE row per patient with 29 binary columns (0/1 per ELIX category).
This is a long → wide transformation using SQL PIVOT via MAX(CASE WHEN...).
</div>""",
    "sub_steps":[
      {
        "ask":"Explain why we use MAX(CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END) for the pivot — specifically, why MAX and not SUM or COUNT?",
        "nudges":[
          "The CASE WHEN expression produces a value for each row. What are the only possible values: 0 or 1. If a patient had ELIX1 in 3 claims, what does SUM give? What does MAX give?",
          "We want a BINARY flag: did the patient EVER have this diagnosis? MAX(0,0,1,0) = 1. SUM(0,0,1,0) = 1 too — but SUM could give values > 1 if the patient had it multiple times. MAX always gives 0 or 1.",
          "So MAX is the correct choice for binary indicator variables: 1 if the patient ever had the diagnosis, 0 if never — regardless of how many times."
        ],
        "check_kw":["max","binary","ever","0","1","sum","count","flag","indicator","multiple"],
        "code_errors":{},
      },
      {
        "ask":"Now write the SQL for Step 2 — create #Elix_Y1Y2 with all 29 ELIX binary columns.\n<span class='tag-sql'>SQL</span> Join diagnoses to claims_10k, filter to Y1+Y2, pivot with MAX(CASE WHEN).",
        "nudges":[
          "Your FROM clause needs both tables: diagnoses d JOIN claims_10k c ON d.claim_id = c.claim_id. Then filter: AND c.year IN ('Y1','Y2').",
          "For each ELIX column: MAX(CASE WHEN [diagnosis] = 'ELIX1' THEN 1 ELSE 0 END) AS ELIX1. You need this pattern for ELIX1 through ELIX29.",
          "Don't forget: GROUP BY patient_id at the end — this collapses all claim-level rows into one row per patient."
        ],
        "check_kw":["join","claim_id","year","group by","patient_id","max","case when","elix","diagnosis","Y1","Y2"],
        "code_errors":{
          "no_join":("claim_id","The diagnoses table links to claims via claim_id. Make sure your JOIN uses ON d.claim_id = c.claim_id."),
          "no_year_filter":("Y1","You need to filter to Y1 and Y2 data only: AND c.year IN ('Y1','Y2')."),
          "no_group":("group by","Without GROUP BY patient_id, you'll get one row per diagnosis per claim instead of one row per patient."),
          "missing_elix":("ELIX","Each ELIX category needs its own MAX(CASE WHEN [diagnosis]='ELIXn' THEN 1 ELSE 0 END) expression."),
        },
      },
    ]
  },

  # ── Q4 Part C: Outcome (Y3 label) ─────────────────────────────────────────
  {
    "id":"q4c", "qnum":"Q4", "title":"Q4-C — Build the Outcome Variable (SQL Step 3)",
    "icon":"🏷️",
    "intro":"""<strong>Step 3 (Silver): Create the dependent variable — high utilizer label from Y3 claims.</strong>

<div class='box-purple'>
A patient is a <strong>high utilizer</strong> if they have <strong>100 or more claims in Y3</strong>.
(Note: this assignment uses 100 as threshold, not 50 like LM10)

For each patient, count their Y3 claims and create a binary label: 1 if ≥100, else 0.
</div>""",
    "sub_steps":[
      {
        "ask":"Why do we use Y3 (the THIRD year) as the outcome, and Y1+Y2 as features? What would go wrong if we used Y3 data in our features?",
        "nudges":[
          "Think about when this model would be used in practice. If it's currently the end of Y2, what data do we have available? What data do we NOT have yet?",
          "If we included Y3 diagnoses or Y3 drug use as features, we'd be using future information to predict the future. What is this problem called?",
          "Data leakage: using information that wouldn't be available at prediction time. The model would look great in testing but fail completely when deployed."
        ],
        "check_kw":["future","leakage","Y3","available","predict","deploy","outcome","label","target"],
        "code_errors":{},
      },
      {
        "ask":"Write the SQL for Step 3 — create #claims_count_Y3 with countClaims and highUtilizer (1 if ≥100 claims, else 0).\n<span class='tag-sql'>SQL</span>",
        "nudges":[
          "Filter claims_10k to WHERE year = 'Y3'. Then GROUP BY patient_id and use COUNT(*) as countClaims.",
          "The binary label uses CASE WHEN COUNT(*) >= 100 THEN 1 ELSE 0 END AS highUtilizer. Where in a GROUP BY query can you use an aggregate function in a CASE WHEN?",
          "You can either wrap it in a subquery or use the column alias. In SQL Server: CASE WHEN count(*) >= 100 THEN 1 ELSE 0 END works directly in the SELECT alongside COUNT(*)."
        ],
        "check_kw":["count","100","case when","Y3","group by","patient_id","highutilizer","year","where"],
        "code_errors":{
          "wrong_threshold":("100","In this assignment (LM8), the threshold is 100 claims in Y3, not 50. Check your CASE WHEN condition."),
          "no_filter":("Y3","Make sure you filter to WHERE year = 'Y3' — you only want Y3 claims for the outcome."),
          "no_group":("group by","You need GROUP BY patient_id to count claims per patient."),
        },
      },
    ]
  },

  # ── Q4 Part D: Drug features ───────────────────────────────────────────────
  {
    "id":"q4d", "qnum":"Q4", "title":"Q4-D — Drug Features (Silver Layer)",
    "icon":"💊",
    "intro":"""<strong>Drug Feature Engineering — Y1+Y2 drug data from the drugcount table.</strong>

<div class='box-purple'>
The drugcount table has monthly drug counts per patient.
The SQL pipeline:
1. Filter to Y1+Y2 drug data
2. Convert months to time brackets: <strong>early</strong> (0–3), <strong>mid</strong> (4–7), <strong>late</strong> (8+)
3. Create binary features: drug_early, drug_mid, drug_late, high_drug_use
</div>""",
    "sub_steps":[
      {
        "ask":"Why do we convert months into three brackets (early/mid/late) instead of keeping the raw month number? What is the purpose of this temporal bucketing?",
        "nudges":[
          "Raw month numbers (1, 2, 3... 24) are too granular for a model. There's no meaningful difference between month 4 and month 5, but there IS a difference between early-year and late-year patterns.",
          "Bucketing reduces noise and creates interpretable features. A patient who takes drugs in the 'late' period of Y1-Y2 may have a different risk profile than one who only used drugs 'early'.",
          "This is a form of feature engineering — transforming raw time data into clinically meaningful categories that a model can use more effectively."
        ],
        "check_kw":["bucket","bracket","temporal","period","granular","noise","interpret","clinical","early","mid","late","reduce"],
        "code_errors":{},
      },
      {
        "ask":"The SQL uses: cast(left(convert(varchar(8), months, 108), 2) as int) to extract the month number from a datetime column. Explain what each function does step by step. Then write the full drug feature code.",
        "nudges":[
          "CONVERT(varchar(8), months, 108) converts a datetime to time string format HH:MM:SS (style 108). What do the first 2 characters of 'HH:MM:SS' represent?",
          "LEFT(..., 2) extracts the first 2 characters — the hour portion. CAST(... AS INT) converts it to a number. So the month value is stored in the 'hours' field of a time column — that's the data encoding.",
          "For the binary features: MAX(CASE WHEN period='early' AND CAST(REPLACE(drug_count,'+','') AS INT) > 0 THEN 1 ELSE 0 END). Why do we need REPLACE(drug_count,'+','')? What might drug_count look like?"
        ],
        "check_kw":["convert","varchar","108","left","cast","int","early","mid","late","replace","drug_count","period","binary","max"],
        "code_errors":{
          "no_replace":("replace","The drug_count column may contain values like '5+' (meaning 5 or more). REPLACE(drug_count,'+','') strips the '+' before casting to int. Have you handled this?"),
          "no_cast":("cast","After extracting the month string with LEFT(), you need CAST(... AS INT) to compare it numerically with BETWEEN 0 AND 3."),
          "no_group":("group by","The final drug feature table needs GROUP BY patient_id to aggregate to patient level."),
        },
      },
    ]
  },

  # ── Q4 Part E: Procedure features ─────────────────────────────────────────
  {
    "id":"q4e", "qnum":"Q4", "title":"Q4-E — Procedure Features (Silver Layer)",
    "icon":"🔧",
    "intro":"""<strong>Procedure Feature Engineering — HCPCS procedure groups from Y1+Y2.</strong>

<div class='box-purple'>
The procedures table has HCPCS codes grouped into categories (hcpcs_grp).
We create binary features for procedure groups G-12, G-13, G-14, G-16, G-17.
This follows the same MAX(CASE WHEN...) pivot pattern as the ELIX features.
</div>""",
    "sub_steps":[
      {
        "ask":"The procedures table joins to claims_10k via claim_id (not directly via patient_id). Why is that? What does that two-step join tell us about the data structure?",
        "nudges":[
          "A procedure happens during a specific claim visit. The procedures table records WHAT was done (the procedure code). The claims table records WHO had the visit (patient_id) and WHEN (year).",
          "By joining procedures → claims → patient, we can get patient_id and year from claims while getting procedure details from procedures. This is a normalized database design.",
          "Why not store patient_id directly in procedures? Because procedures belong to claims, not directly to patients. A patient can have the same procedure in multiple claims."
        ],
        "check_kw":["join","claim_id","patient_id","normalized","structure","link","claim","procedure","two"],
        "code_errors":{},
      },
      {
        "ask":"Write the SQL for procedure feature engineering:\n1. Extract Y1+Y2 procedure groups into #proc_Y1Y2\n2. Pivot to one row per patient with binary columns for G-12, G-13, G-14, G-16, G-17\n<span class='tag-sql'>SQL</span>",
        "nudges":[
          "Step 1: SELECT c.patient_id, p.hcpcs_grp INTO #proc_Y1Y2 FROM procedures p JOIN claims_10k c ON p.claim_id = c.claim_id WHERE c.year IN ('Y1','Y2')",
          "Step 2: Same MAX(CASE WHEN hcpcs_grp = 'G-12' THEN 1 ELSE 0 END) pattern as ELIX. GROUP BY patient_id at the end.",
          "Notice: unlike ELIX which uses LEFT JOIN later, proc uses the same pattern. Each group G-12 through G-17 becomes its own binary column."
        ],
        "check_kw":["claim_id","join","hcpcs_grp","patient_id","max","case when","G-12","G-13","group by","Y1","Y2","binary"],
        "code_errors":{
          "no_join":("claim_id","Procedures don't have patient_id — you need to join to claims_10k ON p.claim_id = c.claim_id to get patient_id."),
          "no_year_filter":("Y1","Filter to WHERE c.year IN ('Y1','Y2') — you only want features from the observation years."),
          "wrong_groups":("G-12","Make sure you include all 5 procedure groups: G-12, G-13, G-14, G-16, G-17."),
        },
      },
    ]
  },

  # ── Q4 Part F: Gold layer join + Python ML ─────────────────────────────────
  {
    "id":"q4f", "qnum":"Q4", "title":"Q4-F — Gold Layer Join + Python Models",
    "icon":"🥇",
    "intro":"""<strong>Final steps: Join everything into the Gold layer, then run ML models in Python.</strong>

<div class='box-purple'>
Gold layer pipeline:
1. JOIN #pat_Y1Y2 + #Elix_Y1Y2 → #patY1Y2_Elix
2. JOIN + #claims_count_Y3 → #highUtilizer_Y3
3. LEFT JOIN + #drugBinarized_Y1Y2 → #highUtilizer_Y3_withDrugs
4. LEFT JOIN + #procBinarized_Y1Y2 → #highUtilizer_Y3_full
5. Clean NULLs with ISNULL(..., 0) → #highUtilizer_Y3_final
6. Persist to dbo.highUtilizer_Y3_final

Then: Python ML — Logistic Regression, Decision Tree, Random Forest
</div>""",
    "sub_steps":[
      {
        "ask":"Steps 1-2 use INNER JOIN but steps 3-4 (drugs and procedures) use LEFT JOIN. Why the difference? What would happen if you used INNER JOIN for the drug and procedure joins?",
        "nudges":[
          "INNER JOIN keeps only patients who appear in BOTH tables. If a patient in your main dataset has no drug records (perhaps they weren't prescribed any drugs), they would be DROPPED by an INNER JOIN with the drug table.",
          "LEFT JOIN keeps ALL patients from the left table, even if they have no match in the right table. For those patients, the drug/procedure columns will be NULL.",
          "That's why Step 5 uses ISNULL(drug_early, 0) — to convert those NULLs to 0, meaning 'this patient had no drug use in that period'. INNER JOIN would lose those patients entirely."
        ],
        "check_kw":["left join","inner join","null","missing","drop","isnull","0","keep","all","patient","drug","procedure"],
        "code_errors":{},
      },
      {
        "ask":"Now write the Python code to:\n1. Load the final CSV\n2. Prepare X and y (drop patient_id, countClaims, highUtilizer from X)\n3. Split (stratified, 80/20)\n4. Scale for Logistic Regression\n5. Train all 3 models\n6. Compare Accuracy and AUC\n<span class='tag-py'>Python</span>",
        "nudges":[
          "Load: df = pd.read_csv('highUtilizer_Y3_final.csv'). Set y = df['highUtilizer'], X = df.drop(columns=['highUtilizer','patient_id','countClaims']).",
          "Split: train_test_split(X, y, test_size=0.2, random_state=42, stratify=y). The stratify=y keeps the class ratio balanced in both splits — why is that important for imbalanced data?",
          "Scale ONLY for Logistic Regression: scaler.fit_transform(X_train) for train, scaler.transform(X_test) for test. Why must you NOT use fit_transform on the test set?"
        ],
        "check_kw":["read_csv","drop","highutilizer","patient_id","train_test_split","stratify","standardscaler","fit_transform","transform","logisticregression","decisiontree","randomforest","accuracy","roc_auc"],
        "code_errors":{
          "fit_transform_test":("fit_transform","You should only use scaler.fit_transform() on the TRAINING set. For the test set, use scaler.transform() only — otherwise you're leaking test distribution info into scaling."),
          "no_stratify":("stratify","With imbalanced classes, add stratify=y to train_test_split. This ensures both train and test sets have the same proportion of high utilizers."),
          "countclaims_in_x":("countClaims","countClaims must be dropped from X — it's a direct proxy for the label (highUtilizer is derived from it). Keeping it would be data leakage."),
          "accuracy_only":("roc_auc","The notebook also reports AUC, not just accuracy. For imbalanced data, AUC is more informative. Make sure you use roc_auc_score(y_test, model.predict_proba(X_test)[:,1])."),
        },
      },
      {
        "ask":"The notebook results show:\n• Logistic Regression: Accuracy=89.5%, AUC=0.826\n• Decision Tree: Accuracy=90.2%, AUC=0.816\n• Random Forest: Accuracy=89.4%, AUC=0.791\n\nWhich model would you choose and why? Also — does using 2 years of data (Y1+Y2) perform better than 1 year (Y2 only)?",
        "nudges":[
          "Decision Tree has the highest accuracy but lowest AUC among the three. Logistic Regression has the highest AUC. For an imbalanced classification problem, which metric matters more?",
          "AUC measures how well the model RANKS high utilizers above low utilizers across all thresholds. Accuracy can be misleadingly high if the model just predicts the majority class. Which model is most trustworthy?",
          "For Y1+Y2 vs Y2 only: the assignment reports Y2-only Logistic Regression got Accuracy=90.7%, AUC=0.812. Y1+Y2 got Accuracy=89.5%, AUC=0.826. What does a higher AUC but lower accuracy mean?"
        ],
        "check_kw":["auc","accuracy","imbalance","logistic","decision","random","choose","better","Y2","Y1","threshold","rank","prefer"],
        "code_errors":{},
      },
    ]
  },
]

# ═══════════════════════════════════════════════════════════════════════════════
# EVALUATOR — never gives answers, only corrects and guides
# ═══════════════════════════════════════════════════════════════════════════════
def evaluate(task, sub_idx, answer, attempt):
    sub = task["sub_steps"][sub_idx]
    low = answer.lower()
    is_code = any(c in answer for c in ["(","SELECT","FROM","WHERE","GROUP","def ","import ","df[","=","->"])

    hits = sum(1 for kw in sub["check_kw"] if kw.lower() in low)
    total = len(sub["check_kw"])

    errors = []
    if is_code and "code_errors" in sub:
        for key,(pattern, msg) in sub["code_errors"].items():
            if pattern.lower() not in low:
                errors.append(msg)

    if hits >= max(3, int(total*0.45)) and len(errors) == 0:
        quality = "correct"
    elif hits >= 2 or (is_code and len(errors) <= 1):
        quality = "partial"
    else:
        quality = "rethink"

    nudge_idx = min(attempt, len(sub["nudges"])-1)

    if quality == "correct":
        fb = """<div class='box-green'>✅ <strong>Great answer!</strong> You've demonstrated a solid understanding of this concept.</div>\n\nType <strong>next</strong> to continue 👉"""

    elif quality == "partial":
        fb = f"""<div class='box-yellow'>⚠️ <strong>You're on the right track!</strong> Your answer captures part of the idea — let's go deeper.</div>

Think about this 👇
<div class='box-blue'>{sub["nudges"][nudge_idx]}</div>
"""
        if errors:
            fb += "\nAlso, check these specific issues in your code:\n"
            for i, e in enumerate(errors[:2]):
                fb += f"\n🔍 <strong>Issue {i+1}:</strong> {e}"
        fb += "\n\nRevise your answer or type <strong>hint</strong> for another nudge."

    else:
        fb = f"""<div class='box-red'>❌ <strong>Not quite yet.</strong> Let's think through this step by step.</div>

Here's a question to guide you 👇
<div class='box-blue'>{sub["nudges"][0]}</div>

Take your time — think it through and try again. Type <strong>hint</strong> if you need more guidance."""

    return quality, fb


def give_hint(task, sub_idx, hint_count):
    sub = task["sub_steps"][sub_idx]
    idx = min(hint_count, len(sub["nudges"])-1)
    return f"""💡 <strong>Hint {idx+1}:</strong>
<div class='box-blue'>{sub["nudges"][idx]}</div>

Now give it another try — I'm guiding you, not giving you the answer 🧭"""


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
def init():
    defs = {
        "messages":[],"task_idx":0,"sub_idx":0,
        "stage":"welcome","lang":"Python",
        "hint_count":0,"attempt":0,
        "grades":{},"initialized":False,"awaiting_next":False,
    }
    for k,v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

def ai(t):  st.session_state.messages.append({"role":"ai",   "content":t})
def usr(t): st.session_state.messages.append({"role":"user", "content":t})

WELCOME = """🏥 <strong>Welcome to the LM8 Assignment Tutor!</strong>

I'm your AI guide for <em>HI 820 — LM8: Classification Models + High Utilizer Prediction</em>.

<div class='box-purple'>
<strong>📋 This assignment has 4 questions:</strong>
• <strong>Q1</strong> — Run Logistic Regression, Naïve Bayes, Bayesian Network on XOR data. Analyze results.
• <strong>Q2</strong> — How can multiple classification models be combined?
• <strong>Q3</strong> — What is the unit of analysis in the testClaims problem?
• <strong>Q4</strong> — Construct the full dataset (Y1+Y2 → predict Y3) with ELIX, drug, and procedure features. Run 3 ML models.
</div>

<strong>How I work:</strong>
🔹 I guide you through each question with concept checks and coding tasks
🔹 I evaluate your answers and <strong>point out specific errors in your code</strong>
🔹 I NEVER give you the answer directly — I ask questions and give nudges
🔹 Type <strong>hint</strong> anytime, or <strong>switch to SQL / switch to Python</strong> to change language

<strong>Which language do you prefer for the coding tasks?</strong>
<span class='tag-sql'>SQL</span> or <span class='tag-py'>Python</span>"""

if not st.session_state.initialized:
    ai(WELCOME)
    st.session_state.initialized = True


def present_current():
    t  = TASKS[st.session_state.task_idx]
    si = st.session_state.sub_idx
    sub = t["sub_steps"][si]
    lang_tag = "<span class='tag-sql'>SQL</span>" if st.session_state.lang=="SQL" else "<span class='tag-py'>Python</span>"

    if si == 0:
        return f"""{t['icon']} <strong>{t['title']}</strong>  {lang_tag}

{t['intro']}

<strong>❓ Let's start:</strong>
{sub['ask']}"""
    else:
        return f"""<strong>❓ Next part — {t['title']}:</strong>  {lang_tag}

{sub['ask']}"""


NEXT_W = {"next","continue","ready","go","yes","ok","sure","move on","proceed","got it","understood","done"}

def handle(raw):
    txt = raw.strip()
    if not txt: return
    usr(txt)
    low = txt.lower()

    if "restart" in low:
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

    if "switch to sql" in low:
        st.session_state.lang = "SQL"
        ai("✅ Switched to <span class='tag-sql'>SQL</span> mode!")
        return
    if "switch to python" in low:
        st.session_state.lang = "Python"
        ai("✅ Switched to <span class='tag-py'>Python</span> mode!")
        return

    if st.session_state.stage == "welcome":
        st.session_state.lang = "SQL" if "sql" in low else "Python"
        st.session_state.stage = "task"
        tag = "<span class='tag-sql'>SQL</span>" if st.session_state.lang=="SQL" else "<span class='tag-py'>Python</span>"
        ai(f"{tag} mode activated! Let's begin.\n\n{present_current()}")
        return

    if st.session_state.stage == "done":
        ai("You've completed the full LM8 assignment! 🎉 Type <strong>restart</strong> to go again.")
        return

    t  = TASKS[st.session_state.task_idx]
    si = st.session_state.sub_idx

    # Hint
    if any(w in low for w in ["hint","help","stuck","confused","don't know","idk","no idea"]):
        hc = st.session_state.hint_count
        ai(give_hint(t, si, hc))
        st.session_state.hint_count = hc + 1
        return

    # Next navigation
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        st.session_state.awaiting_next = False
        st.session_state.hint_count = 0
        st.session_state.attempt = 0

        if si + 1 < len(t["sub_steps"]):
            st.session_state.sub_idx = si + 1
            ai(present_current())
        else:
            nxt = st.session_state.task_idx + 1
            st.session_state.sub_idx = 0
            st.session_state.task_idx = nxt
            if nxt >= len(TASKS):
                st.session_state.stage = "done"
                g = st.session_state.grades
                correct_n = sum(1 for v in g.values() if v=="correct")
                partial_n = sum(1 for v in g.values() if v=="partial")
                score = int(((correct_n + 0.5*partial_n)/len(TASKS))*100)
                icons = {"correct":"✅","partial":"⚠️","rethink":"🔄","":"⬜"}
                rows = "\n".join([f"{icons.get(g.get(t2['id'],''),'⬜')}  {t2['icon']} {t2['title']}" for t2 in TASKS])
                ai(f"""🎓 <strong>LM8 Assignment Complete! Your Scorecard:</strong>

{rows}

<div class='box-green'>
<strong>Score: {correct_n}/{len(TASKS)} fully correct — {score}%</strong>
{'🌟 Outstanding work on the full LM8 pipeline!' if score>=85 else
 '🎉 Great effort! Review the ⚠️ tasks to strengthen your understanding.' if score>=55 else
 '💪 Keep practising! Re-read each step and try again.'}
</div>

<strong>Key Concepts Recap:</strong>
📊 Q1 — XOR is not linearly separable → Logistic Regression needs interaction terms
🤝 Q2 — Ensemble methods: Bagging, Boosting, Stacking
🔬 Q3 — Unit of analysis = patient (aggregated from claims/diagnoses/drugs/procedures)
🥇 Q4 — Bronze→Silver→Gold pipeline: ELIX + Drug + Procedure features, 3 ML models

Type <strong>restart</strong> to try again! 🔄""")
            else:
                ai(present_current())
        return

    # Evaluate
    quality, fb = evaluate(t, si, txt, st.session_state.attempt)
    prev = st.session_state.grades.get(t["id"],"")
    if quality=="correct" or (quality=="partial" and prev!="correct"):
        st.session_state.grades[t["id"]] = quality
    st.session_state.attempt += 1

    total_sub = len(t["sub_steps"])
    if quality == "correct":
        st.session_state.awaiting_next = True
        suffix = f"\n\nType <strong>next</strong> for {'the next part of '+t['title'] if si+1<total_sub else 'the next question'} 👉"
        ai(fb.replace("Type <strong>next</strong> to continue 👉", "") + suffix)
    else:
        ai(fb)


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════════════════════
tidx  = st.session_state.task_idx
total = len(TASKS)
pct   = int((tidx/total)*100) if st.session_state.stage=="task" and tidx<total else (100 if st.session_state.stage=="done" else 0)

st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

label = (f"{TASKS[tidx]['icon']} {TASKS[tidx]['title']}" if st.session_state.stage=="task" and tidx<total
         else ("✅ Complete" if st.session_state.stage=="done" else "Choose your language"))
lang_tag = "<span class='tag-sql'>SQL</span>" if st.session_state.lang=="SQL" else "<span class='tag-py'>Python</span>"
st.markdown(f'<div class="top-bar"><h2>🏥 LM8 Tutor Agent &nbsp;·&nbsp; {label} &nbsp;·&nbsp; {lang_tag}</h2></div>', unsafe_allow_html=True)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    if role=="ai":
        st.markdown(f'<div class="msg-ai"><div class="av">🎓</div><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-user"><div class="bubble">{msg["content"]}</div><div class="av">You</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

s = st.session_state.stage
cols = st.columns([1,1,1,1,4])
if s == "welcome":
    with cols[0]:
        if st.button("🐍 Python"): handle("python"); st.rerun()
    with cols[1]:
        if st.button("🗄️ SQL"):    handle("sql");    st.rerun()
elif s == "task":
    with cols[0]:
        if st.button("💡 Hint"):        handle("hint");             st.rerun()
    with cols[1]:
        if st.button("▶️ Next"):        handle("next");             st.rerun()
    with cols[2]:
        if st.button("🐍 Python"):      handle("switch to python"); st.rerun()
    with cols[3]:
        if st.button("🗄️ SQL"):        handle("switch to sql");    st.rerun()
elif s == "done":
    with cols[0]:
        if st.button("🔄 Restart"):     handle("restart");          st.rerun()

inp = st.chat_input("Type your answer or code… (type 'hint' if stuck)")
if inp:
    handle(inp)
    st.rerun()
