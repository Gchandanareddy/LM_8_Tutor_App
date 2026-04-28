import streamlit as st
import json
import urllib.request

st.set_page_config(
    page_title="LM8 AI Tutor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    font-size:0.93rem; line-height:1.88; border:1px solid #3a3a3a; white-space:pre-wrap;
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
.tag-py   { background:#34d39922;color:#a7f3d0;border:1px solid #34d399;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-sql  { background:#f59e0b22;color:#fde68a;border:1px solid #f59e0b;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-concept { background:#ec489933;color:#f9a8d4;border:1px solid #ec4899;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-q    { background:#7c3aed33;color:#c4b5fd;border:1px solid #7c3aed;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.ai-badge { background:#7c3aed33;color:#c4b5fd;border:1px solid #7c3aed;border-radius:8px;padding:1px 7px;font-size:0.7rem;font-weight:600;margin-left:5px; }
.progress-bar-wrap { position:fixed;top:0;left:0;right:0;height:3px;z-index:9999;background:#333; }
.progress-bar-fill { height:100%;background:linear-gradient(90deg,#7c3aed,#19c37d);transition:width 0.5s; }
.top-bar { position:sticky;top:0;background:#212121;border-bottom:1px solid #333;padding:10px 0 8px;margin-bottom:6px;z-index:100; }
.top-bar h2 { text-align:center;font-size:0.9rem;font-weight:500;color:#aaa;margin:0; }
.stButton > button { background:#2a2a2a!important;color:#ececec!important;border:1px solid #444!important;border-radius:20px!important;font-size:0.82rem!important;padding:5px 14px!important;transition:all 0.15s!important; }
.stButton > button:hover { background:#3a3a3a!important;border-color:#7c3aed!important; }
.spinner { color:#7c3aed;font-style:italic;font-size:0.88rem; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TASK DEFINITIONS
# type: "concept" = plain English answer expected (NO code needed)
#       "code_py" = Python code expected
#       "code_sql" = SQL code expected
#       "mixed"   = code + explanation expected
# ═══════════════════════════════════════════════════════════════

TASKS = [

  # ── Q1-A: XOR pattern (CONCEPT — no code needed) ─────────────
  {
    "id":"q1a", "qnum":"Q1", "title":"Q1-A — The XOR Pattern",
    "icon":"📊", "type":"concept",
    "intro":"""<strong>Question 1: Logistic Regression + Naïve Bayes + Bayesian Network on XOR Data</strong>

<div class='box-purple'>
You are given this 4-row dataset:
<pre style='color:#a7f3d0;background:#111;padding:10px;border-radius:6px;margin:8px 0'>x, y, class
0, 1, 1
1, 0, 1
1, 1, 0
0, 0, 0</pre>
You need to run: Logistic Regression, Naïve Bayes, and Bayesian Network on it — then explain what you observe.
</div>

Before any code — look at the data carefully. <span class='tag-concept'>💬 Conceptual</span>""",
    "question":"What pattern do you notice in this dataset? What is the relationship between x, y, and class? Can a straight line separate class=0 from class=1? Explain in plain English.",
    "answer_guidance":"""The student should recognise:
- The pattern is XOR (exclusive OR): class=1 when x≠y, class=0 when x=y
- The four points form a checkerboard / diagonal pattern
- NO straight line can separate class 0 from class 1 — the data is NOT linearly separable
- This is the famous XOR problem in machine learning""",
    "hint":"Plot the four points mentally: (0,1)→class 1, (1,0)→class 1, (1,1)→class 0, (0,0)→class 0. Try drawing a straight line to separate the 1s from the 0s. Is it possible?",
  },

  # ── Q1-B: Why models fail (CONCEPT — no code needed) ─────────
  {
    "id":"q1b", "qnum":"Q1", "title":"Q1-B — Why Models Succeed or Fail",
    "icon":"🔍", "type":"concept",
    "intro":"""<div class='box-purple'>
From running the models in WEKA and Python on the XOR data:
• <strong>Logistic Regression (first run)</strong>: 50% accuracy — failed
• <strong>Logistic Regression (tuned)</strong>: 100% accuracy
• <strong>Naïve Bayes</strong>: 50% accuracy — failed  
• <strong>Bayesian Network</strong>: 100% accuracy

Use training data to test. <span class='tag-concept'>💬 Conceptual</span>
</div>""",
    "question":"Explain: (1) WHY did Logistic Regression initially fail? (2) WHY did Naïve Bayes fail? (3) WHY did the Bayesian Network succeed? (4) What parameter or feature change allowed Logistic Regression to reach 100%? Which models work and which do not work on this type of data?",
    "answer_guidance":"""Student should explain:
1. LR failed: XOR is NOT linearly separable — LR can only create linear decision boundaries. No straight line can separate the two classes in 2D.
2. Naïve Bayes failed: assumes features are conditionally INDEPENDENT given the class. In XOR, x and y interact — knowing x AND y together determines the class, but neither alone does. The naive independence assumption breaks XOR.
3. Bayesian Network succeeded: unlike Naïve Bayes, it can model dependencies between variables (non-naive structure). It explicitly learns that x and y interact.
4. LR was fixed by adding an interaction term x*y as a new feature. With [x, y, x*y] the data becomes linearly separable in 3D space.
The student should conclude: models that assume linearity (LR) or independence (Naïve Bayes) fail on XOR. Models that capture non-linear interactions (Bayesian Network, LR with interaction features) succeed.""",
    "hint":"For LR: think geometrically — what kind of boundary does LR draw? For Naïve Bayes: the word NAÏVE refers to an assumption about features. What assumption, and why does XOR violate it? For the Bayesian Network: what can it model that Naïve Bayes cannot?",
  },

  # ── Q1-C: Write code for 3 models (CODE — Python) ────────────
  {
    "id":"q1c", "qnum":"Q1", "title":"Q1-C — Code: Run 3 Models on XOR",
    "icon":"💻", "type":"code_py",
    "intro":"""<div class='box-purple'>
Now implement the three models in Python. The dataset:
x=[0,1,1,0], y=[1,0,1,0], class=[1,1,0,0]
Train and test on the same 4 rows (dataset is too small to split).
<span class='tag-py'>Python</span>
</div>""",
    "question":"Write Python code to: (1) Create the XOR dataset as a DataFrame, (2) Run Logistic Regression, (3) Run Gaussian Naïve Bayes, (4) Print accuracy for each. Then modify LR to add an interaction term x*y and show it reaches 100% accuracy.",
    "answer_guidance":"""Expected code structure:
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

df = pd.DataFrame({'x':[0,1,1,0], 'y':[1,0,1,0], 'class':[1,1,0,0]})
X = df[['x','y']]
y = df['class']

# LR — fails
lr = LogisticRegression(); lr.fit(X,y); print(accuracy_score(y, lr.predict(X)))

# Naive Bayes — fails
nb = GaussianNB(); nb.fit(X,y); print(accuracy_score(y, nb.predict(X)))

# LR with interaction term — succeeds
X2 = X.copy(); X2['xy'] = X2['x'] * X2['y']
lr2 = LogisticRegression(); lr2.fit(X2,y); print(accuracy_score(y, lr2.predict(X2)))

Key things to check: creates correct dataset, uses same data for train+test (4 rows too small to split), adds x*y interaction term.""",
    "hint":"Create the DataFrame with x, y, class columns. Train each model with .fit(X, y) and predict with .predict(X). For the interaction term: X['xy'] = X['x'] * X['y'] creates a new column that is 1 only when both x=1 and y=1.",
  },

  # ── Q2: Ensemble learning (CONCEPT — no code needed) ──────────
  {
    "id":"q2", "qnum":"Q2", "title":"Q2 — Combining Classification Models",
    "icon":"🤝", "type":"concept",
    "intro":"""<strong>Question 2: How can multiple classification models be combined?</strong>

<div class='box-purple'>
Describe ensemble learning methods and explain how combining models improves predictions.
<span class='tag-concept'>💬 Conceptual — no code needed</span>
</div>""",
    "question":"(1) Why does combining multiple models give better predictions than any single model? What is the core intuition? (2) Describe the THREE main ensemble methods: Bagging, Boosting, and Stacking — how does each work and name a real algorithm example for each.",
    "answer_guidance":"""Student should cover:
CORE INTUITION: Different models make different errors. When errors don't correlate, averaging/voting cancels individual mistakes. Models trained with different parameters generalise in different ways.

BAGGING (Bootstrap Aggregating): Create multiple training datasets by sampling with replacement (bootstrap). Train a model on each. Average predictions (regression) or majority vote (classification). Example: Random Forest (many decision trees on bootstrap samples). Reduces VARIANCE.

BOOSTING: Build models SEQUENTIALLY. Each new model focuses on the examples the previous model got wrong. Weight misclassified examples more heavily. Example: AdaBoost, Gradient Boosting, XGBoost. Reduces BIAS.

STACKING: Train multiple BASE models (level 0). Use their predictions as inputs to a META-MODEL (level 1) that learns how to best combine them. The meta-model learns which base models to trust for which inputs.""",
    "hint":"Think of a jury of 12 vs. one judge. For Bagging — think random sampling with replacement and parallel training. For Boosting — think sequential learning from mistakes. For Stacking — think of a higher-level model that learns from the outputs of other models.",
  },

  # ── Q3: Unit of analysis (CONCEPT — no code needed) ───────────
  {
    "id":"q3", "qnum":"Q3", "title":"Q3 — Unit of Analysis",
    "icon":"🔬", "type":"concept",
    "intro":"""<strong>Question 3: Unit of analysis in the testClaims problem</strong>

<div class='box-purple'>
The raw tables: claims_10k (one row per claim), diagnoses (one row per diagnosis per claim), drugcount (one row per month per patient), procedures (one row per procedure per claim).

After preprocessing, all of this is aggregated into the <strong>highUtilizer_Y3_final</strong> table.
<span class='tag-concept'>💬 Conceptual — no code needed</span>
</div>""",
    "question":"(1) What is the unit of analysis? What does ONE ROW in highUtilizer_Y3_final represent? (2) Why is GROUP BY patient_id critical in the SQL pipeline? What would happen without it?",
    "answer_guidance":"""Student should explain:
UNIT OF ANALYSIS = the PATIENT. Each row represents one patient with:
- Features from Y1+Y2: ELIX1-29 (diagnosis flags), drug_early/mid/late/high_drug_use, proc_G12-G17
- Label from Y3: highUtilizer (1 if ≥100 claims in Y3, else 0)

GROUP BY patient_id is critical because:
- The raw data has many rows per patient (one per claim, one per diagnosis, one per month)
- GROUP BY collapses all of a patient's data into a SINGLE row
- MAX(CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END) creates a binary flag: did this patient EVER have this diagnosis in Y1+Y2?
- Without GROUP BY: one row per claim → joining with outcome table causes row explosion → wrong dataset
- The prediction task is per-patient: will THIS PATIENT be a high utilizer in Y3?""",
    "hint":"Look at the final table columns: patient_id, countClaims, highUtilizer, ELIX1-29, drug features, proc features. What is the primary key? Each row is about WHO? And think: if GROUP BY was missing from the ELIX step, how many rows would one patient contribute?",
  },

  # ── Q4-A: Cohort + ELIX SQL (CODE — SQL) ─────────────────────
  {
    "id":"q4a", "qnum":"Q4", "title":"Q4-A — SQL: Cohort + ELIX Features",
    "icon":"🗄️", "type":"code_sql",
    "intro":"""<strong>Question 4: Build the full dataset (Y1+Y2 → predict Y3 high utilization)</strong>

<div class='box-purple'>
Include: diagnoses (ELIX), procedures, drug use.
<strong>Step 1</strong>: Cohort — patients present in BOTH Y1 AND Y2
<strong>Step 2</strong>: ELIX features — binary flags ELIX1-ELIX29 from diagnoses in Y1+Y2
<span class='tag-sql'>SQL (T-SQL)</span>
</div>""",
    "question":"Write the SQL for:\n(1) Step 1 — create #pat_Y1Y2: patients who appear in both Y1 and Y2 from claims_10k\n(2) Step 2 — create #Elix_Y1Y2: binary ELIX1-ELIX29 columns, one row per patient, for Y1+Y2 data",
    "answer_guidance":"""Expected SQL:

Step 1:
DROP TABLE IF EXISTS #pat_Y1Y2
SELECT patient_id
INTO #pat_Y1Y2
FROM claims_10k
WHERE year IN ('Y1','Y2')
GROUP BY patient_id
HAVING COUNT(DISTINCT year) = 2   -- or HAVING min(year) != max(year)

Step 2:
DROP TABLE IF EXISTS #Elix_Y1Y2
SELECT patient_id,
  MAX(CASE WHEN diagnosis='ELIX1'  THEN 1 ELSE 0 END) AS ELIX1,
  MAX(CASE WHEN diagnosis='ELIX2'  THEN 1 ELSE 0 END) AS ELIX2,
  ... (ELIX3 through ELIX29)
  MAX(CASE WHEN diagnosis='ELIX29' THEN 1 ELSE 0 END) AS ELIX29
INTO #Elix_Y1Y2
FROM diagnoses d
JOIN claims_10k c ON d.claim_id = c.claim_id
AND c.year IN ('Y1','Y2')
GROUP BY patient_id

Key concepts: HAVING COUNT(DISTINCT year)=2 ensures both years; MAX(CASE WHEN) for binary pivot; JOIN via claim_id (not patient_id directly); GROUP BY patient_id for one row per patient.""",
    "hint":"Step 1: GROUP BY patient_id + HAVING to ensure the patient appears in BOTH years. Step 2: diagnoses joins to claims via claim_id (not patient_id). Use MAX(CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END) — why MAX not SUM? Because we want binary (ever had it = 1), not a count.",
  },

  # ── Q4-B: Y3 outcome + Gold join SQL (CODE — SQL) ─────────────
  {
    "id":"q4b", "qnum":"Q4", "title":"Q4-B — SQL: Outcome + Gold Layer Join",
    "icon":"🥇", "type":"code_sql",
    "intro":"""<div class='box-purple'>
<strong>Step 3</strong>: Y3 outcome — highUtilizer (≥100 claims in Y3 = 1, else 0)
<strong>Step 4+5</strong>: Drug and procedure features from Y1+Y2
<strong>Step 6</strong>: Join everything (INNER for core tables, LEFT for drug/procedure)
<span class='tag-sql'>SQL (T-SQL)</span>
</div>""",
    "question":"Write the SQL for:\n(1) Step 3 — #claims_count_Y3: count Y3 claims per patient, create highUtilizer binary label (≥100 = 1)\n(2) The final Gold layer join: why do you use INNER JOIN for some tables and LEFT JOIN for drug/procedure tables?",
    "answer_guidance":"""Step 3:
DROP TABLE IF EXISTS #claims_count_Y3
SELECT patient_id,
  COUNT(*) AS countClaims,
  CASE WHEN COUNT(*) >= 100 THEN 1 ELSE 0 END AS highUtilizer
INTO #claims_count_Y3
FROM claims_10k
WHERE year = 'Y3'
GROUP BY patient_id

Gold layer join:
-- INNER JOIN cohort + ELIX (every patient must have both features and label)
SELECT e.*
INTO #patY1Y2_Elix
FROM #pat_Y1Y2 p
JOIN #Elix_Y1Y2 e ON p.patient_id = e.patient_id

SELECT p.*, c.countClaims, c.highUtilizer
INTO #highUtilizer_Y3
FROM #patY1Y2_Elix p
JOIN #claims_count_Y3 c ON p.patient_id = c.patient_id

-- LEFT JOIN drug/procedure (not all patients have drug/procedure records)
SELECT h.*, d.drug_early, d.drug_mid, d.drug_late, d.high_drug_use
INTO #highUtilizer_Y3_withDrugs
FROM #highUtilizer_Y3 h
LEFT JOIN #drugBinarized_Y1Y2 d ON h.patient_id = d.patient_id

Key: INNER JOIN for core pipeline (need both features and label). LEFT JOIN for drug/proc (patient may have zero records — that should be 0, not excluded). ISNULL(...,0) to clean NULLs.""",
    "hint":"For Step 3: WHERE year='Y3', GROUP BY patient_id, COUNT(*) for claims, CASE WHEN COUNT(*)>=100 THEN 1 ELSE 0 END. For the join: INNER JOIN means a patient with no Y3 claims is DROPPED. LEFT JOIN means a patient with no drug records gets NULLs (later cleaned to 0). Which is correct for each case?",
  },

  # ── Q4-C: Python ML (MIXED — code + explanation) ──────────────
  {
    "id":"q4c", "qnum":"Q4", "title":"Q4-C — Python: 3 ML Models + Analysis",
    "icon":"🤖", "type":"mixed",
    "intro":"""<div class='box-purple'>
From the notebook:
• Logistic Regression: Accuracy=89.5%, AUC=0.826
• Decision Tree:       Accuracy=90.2%, AUC=0.816
• Random Forest:       Accuracy=89.4%, AUC=0.791
• Y2-only LR:          Accuracy=90.7%, AUC=0.812
<span class='tag-py'>Python</span> + <span class='tag-concept'>Explanation</span>
</div>""",
    "question":"(1) Write Python code to load highUtilizer_Y3_final.csv, prepare X/y (drop correct columns), stratified 80/20 split, scale for LR, train all 3 models, print Accuracy and AUC.\n(2) Which model would you choose and why?\n(3) Does using Y1+Y2 perform better than Y2 alone? Explain the AUC vs accuracy trade-off.",
    "answer_guidance":"""Code:
df = pd.read_csv('highUtilizer_Y3_final.csv')
y = df['highUtilizer']
X = df.drop(columns=['highUtilizer','patient_id','countClaims'])  # must drop countClaims — it's a direct proxy for the label!
X = pd.get_dummies(X, drop_first=True)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train); X_test_scaled = scaler.transform(X_test)  # transform only on test!
lr = LogisticRegression(max_iter=1000); lr.fit(X_train_scaled,y_train)
tree = DecisionTreeClassifier(max_depth=5,random_state=42); tree.fit(X_train,y_train)
rf = RandomForestClassifier(n_estimators=100,random_state=42); rf.fit(X_train,y_train)
# evaluate with accuracy_score and roc_auc_score(y_test, model.predict_proba(X_test)[:,1])

Model choice: Logistic Regression — highest AUC (0.826). AUC is primary metric for imbalanced data because accuracy can be gamed by always predicting majority class.

Y1+Y2 vs Y2: Y1+Y2 has slightly lower accuracy (89.5% vs 90.7%) but higher AUC (0.826 vs 0.812). Higher AUC means better discrimination — it correctly ranks high utilizers above low utilizers more often. Two years of history improves the model's true predictive power even if raw accuracy drops slightly.""",
    "hint":"Key things to check: (1) drop countClaims from X — it's a direct proxy for highUtilizer and causes data leakage, (2) use scaler.transform() not fit_transform() on the test set, (3) use predict_proba(X_test)[:,1] for AUC (probabilities, not class labels), (4) stratify=y in train_test_split for imbalanced classes.",
  },
]

# ═══════════════════════════════════════════════════════════════
# AI GRADER — Claude API
# ═══════════════════════════════════════════════════════════════

def call_claude_grader(task, student_answer, hint_used):
    """Use Claude API to intelligently grade the student's answer."""

    qtype = task["type"]
    type_instruction = {
        "concept":  "This is a CONCEPTUAL question — no code is required. Evaluate understanding and reasoning expressed in plain English.",
        "code_py":  "This is a PYTHON CODE question. Evaluate code logic, structure, and correctness — not syntax details.",
        "code_sql": "This is a SQL CODE question. Evaluate SQL logic, structure, and use of correct clauses.",
        "mixed":    "This question requires BOTH code AND explanation. Evaluate both the code quality and the conceptual reasoning."
    }.get(qtype, "Evaluate understanding.")

    system_prompt = f"""You are a strict but supportive health informatics professor grading a student answer.

{type_instruction}

Your role:
- NEVER give the student the direct answer or copy the answer guidance
- DO identify specifically what the student got right
- DO point out specific gaps or misconceptions
- DO ask ONE focused Socratic question to guide them forward
- Be concise and encouraging
- Grade as: "correct" (understands all key concepts), "partial" (some right ideas, missing elements), or "incorrect" (wrong or missing core concepts)

Respond ONLY in this exact JSON format (no markdown, no extra text):
{{"grade": "correct|partial|incorrect", "feedback": "2-3 sentences: what they got right + what is missing", "nudge": "one focused guiding question to help them improve"}}"""

    user_prompt = f"""Task: {task['title']}

Question asked to student:
{task['question']}

What a correct answer should cover (DO NOT reveal this to the student):
{task['answer_guidance']}

Student's answer:
{student_answer}

Note: hint was {'already given' if hint_used else 'not yet given'}.

Grade this answer and respond in the required JSON format."""

    try:
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 600,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())

        raw = data["content"][0]["text"].strip()
        # Strip markdown code fences if present
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                try:
                    result = json.loads(part)
                    return result["grade"], result["feedback"], result["nudge"]
                except:
                    continue
        result = json.loads(raw)
        return result["grade"], result["feedback"], result["nudge"]

    except Exception as e:
        # Fallback: basic length + word check
        words = student_answer.split()
        if len(words) < 8:
            return "incorrect", "Your answer is too brief. Please explain your thinking more fully.", "What is the core concept this question is asking about?"
        if len(words) >= 30:
            return "partial", "You've written a thoughtful answer. Let's make sure you've covered all the key points.", "Can you be more specific about the mechanism or provide an example?"
        return "partial", "You've made a start — let's build on it.", "What else is important to mention here?"


def render_grade(grade, feedback, nudge, title):
    """Build styled feedback HTML from AI grade."""
    badge = "<span class='ai-badge'>🤖 AI Graded</span>"

    if grade == "correct":
        return f"""<div class='box-green'>
✅ {badge} <strong>Well done on {title}!</strong>

{feedback}
</div>

Type <strong>next</strong> to continue 👉"""

    elif grade == "partial":
        return f"""<div class='box-yellow'>
⚠️ {badge} <strong>Good thinking — you're on the right track!</strong>

{feedback}
</div>

<div class='box-blue'>
💭 <strong>Think about this:</strong> {nudge}
</div>

Revise your answer or type <strong>hint</strong> for a step-by-step nudge."""

    else:
        return f"""<div class='box-red'>
❌ {badge} <strong>Not quite yet — let's approach this differently.</strong>

{feedback}
</div>

<div class='box-blue'>
💭 <strong>Guiding question:</strong> {nudge}
</div>

Take your time and try again. Type <strong>hint</strong> for guidance."""


# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
def init():
    defs = {
        "messages": [],
        "task_idx": 0,
        "stage": "welcome",
        "hint_count": 0,
        "hint_used": False,
        "grades": {},
        "initialized": False,
        "awaiting_next": False,
        "pending_answer": None,   # store answer while grading
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

def ai(t):  st.session_state.messages.append({"role": "ai",   "content": t})
def usr(t): st.session_state.messages.append({"role": "user", "content": t})


# ── Welcome ───────────────────────────────────────────────────
WELCOME = """🏥 <strong>Welcome to the LM8 AI Tutor!</strong>

I'm your AI-powered guide for <em>HI 820 — LM8: Classification Models + High Utilizer Prediction</em>.

<div class='box-purple'>
<strong>📋 Assignment — 4 Questions, 8 Tasks:</strong>

<strong>Q1</strong> — XOR dataset: spot the pattern, explain why models fail/succeed, write Python code
<strong>Q2</strong> — How do ensemble methods combine models? (conceptual, no code)
<strong>Q3</strong> — What is the unit of analysis? (conceptual, no code)
<strong>Q4</strong> — Build the full testClaims pipeline in SQL + run 3 ML models in Python
</div>

<div class='box-green'>
✨ <strong>AI-Powered Grading:</strong>
Your answers are evaluated by <strong>Claude AI</strong> — not keyword matching.
I read the actual meaning of your answer and give you intelligent, specific feedback.
For <span class='tag-concept'>💬 Conceptual</span> questions: just write in plain English — no code needed!
For <span class='tag-py'>Python</span> / <span class='tag-sql'>SQL</span> questions: write the code.
</div>

🔹 I NEVER give direct answers — I guide you with Socratic questions
🔹 Type <strong>hint</strong> anytime for a step-by-step nudge
🔹 Type <strong>next</strong> to move forward after a correct answer

Ready? Click <strong>Start</strong> or type anything 👇"""

if not st.session_state.initialized:
    ai(WELCOME)
    st.session_state.initialized = True


def present_task(idx):
    t = TASKS[idx]
    type_tag = {
        "concept":  "<span class='tag-concept'>💬 Conceptual</span>",
        "code_py":  "<span class='tag-py'>🐍 Python</span>",
        "code_sql": "<span class='tag-sql'>🗄️ SQL</span>",
        "mixed":    "<span class='tag-py'>🐍 Python</span> + <span class='tag-concept'>💬 Explanation</span>",
    }.get(t["type"], "")

    return (f"{t['icon']} <strong>Task {idx+1}/{len(TASKS)} — {t['title']}</strong>  "
            f"<span class='tag-q'>{t['qnum']}</span> {type_tag}\n\n"
            f"{t['intro']}\n\n"
            f"<strong>❓ Question:</strong>\n{t['question']}")


NEXT_W = {"next","continue","ready","go","yes","ok","sure","move on","proceed",
          "got it","understood","done","next question","start","begin"}


def handle(raw):
    txt = raw.strip()
    if not txt: return
    usr(txt)
    low = txt.lower()

    # Global: restart
    if "restart" in low:
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # Welcome → begin
    if st.session_state.stage == "welcome":
        st.session_state.stage = "task"
        ai(f"Let's begin! 🚀\n\n{present_task(0)}")
        return

    # Done
    if st.session_state.stage == "done":
        ai("You've completed the full LM8 assignment! 🎉 Type <strong>restart</strong> to try again.")
        return

    tidx = st.session_state.task_idx
    t    = TASKS[tidx]

    # ── Hint ─────────────────────────────────────────────────
    if any(w in low for w in ["hint","help","stuck","confused","don't know","idk","no idea"]):
        st.session_state.hint_used = True
        hc = st.session_state.hint_count
        ai(f"""💡 <strong>Hint {hc+1} for {t['title']}:</strong>

<div class='box-blue'>{t['hint']}</div>

Now give it another try — I'm pointing the way, not giving the answer 🧭""")
        st.session_state.hint_count = hc + 1
        return

    # ── Next navigation ────────────────────────────────────
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        st.session_state.awaiting_next = False
        st.session_state.hint_count    = 0
        st.session_state.hint_used     = False

        next_idx = tidx + 1
        st.session_state.task_idx = next_idx

        if next_idx >= len(TASKS):
            # ── Final scorecard ────────────────────────────
            st.session_state.stage = "done"
            g = st.session_state.grades
            correct_n = sum(1 for v in g.values() if v == "correct")
            partial_n = sum(1 for v in g.values() if v == "partial")
            score = int(((correct_n + 0.5 * partial_n) / len(TASKS)) * 100)
            icons = {"correct":"✅","partial":"⚠️","incorrect":"❌","":"⬜"}
            rows = "\n".join(
                f"{icons.get(g.get(t2['id'],''),'⬜')}  {t2['icon']} {t2['title']}"
                for t2 in TASKS
            )
            ai(f"""🎓 <strong>LM8 Assignment Complete! Your Scorecard:</strong>

{rows}

<div class='box-green'>
<strong>Score: {correct_n}/{len(TASKS)} fully correct — {score}%</strong>
{'🌟 Outstanding work across all questions!' if score >= 85 else
 '🎉 Great effort! Review the ⚠️/❌ tasks to deepen your understanding.' if score >= 55 else
 '💪 Good start! Re-read each section and try again.'}
</div>

<strong>Key Takeaways:</strong>
📊 <strong>Q1</strong> — XOR is not linearly separable. LR needs interaction term x*y. Naïve Bayes fails due to independence assumption. Bayesian Network models variable dependencies.
🤝 <strong>Q2</strong> — Ensemble methods: Bagging (Random Forest, reduces variance), Boosting (AdaBoost/XGBoost, reduces bias), Stacking (meta-model combines base models).
🔬 <strong>Q3</strong> — Unit of analysis = PATIENT. GROUP BY patient_id collapses many rows per patient to one. MAX(CASE WHEN) creates binary flags.
🥇 <strong>Q4</strong> — HAVING COUNT(DISTINCT year)=2 for cohort; MAX(CASE WHEN) for ELIX pivot; LEFT JOIN for drug/proc (patients may have no records); AUC > Accuracy for imbalanced data.

Type <strong>restart</strong> to try again! 🔄""")
        else:
            ai(present_task(next_idx))
        return

    # ── Grade with AI ──────────────────────────────────────
    # Show spinner while grading
    ai("🤖 <span class='spinner'>Grading your answer with AI...</span>")
    st.rerun()


def grade_pending():
    """Called on next render if we have a pending answer to grade."""
    if not st.session_state.get("pending_answer"):
        return

    txt  = st.session_state.pending_answer
    tidx = st.session_state.task_idx
    t    = TASKS[tidx]

    # Remove the spinner message
    if st.session_state.messages and "Grading your answer" in st.session_state.messages[-1]["content"]:
        st.session_state.messages.pop()

    # Call AI grader
    grade, feedback, nudge = call_claude_grader(t, txt, st.session_state.hint_used)

    # Store grade
    prev = st.session_state.grades.get(t["id"], "")
    if grade == "correct" or (grade == "partial" and prev != "correct"):
        st.session_state.grades[t["id"]] = grade

    # Build feedback
    fb = render_grade(grade, feedback, nudge, t["title"])

    if grade == "correct":
        st.session_state.awaiting_next = True
        total = len(TASKS)
        nav = "the next task" if tidx + 1 < total else "your final scorecard"
        fb = fb.replace("Type <strong>next</strong> to continue 👉",
                        f"Type <strong>next</strong> for {nav} 👉")

    ai(fb)
    st.session_state.pending_answer = None


# ── Check if we need to grade ─────────────────────────────────
# We store the student's answer separately so we can show the spinner
# then process on the next render cycle

def submit_for_grading(txt):
    """Store answer and trigger grading on next render."""
    usr(txt)
    # Check for commands first
    low = txt.lower()
    if "restart" in low:
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        return
    if any(w in low for w in ["hint","help","stuck","confused","don't know","idk","no idea"]):
        st.session_state.hint_used = True
        tidx = st.session_state.task_idx
        t = TASKS[tidx]
        hc = st.session_state.hint_count
        ai(f"""💡 <strong>Hint {hc+1} for {t['title']}:</strong>

<div class='box-blue'>{t['hint']}</div>

Now give it another try — I'm pointing the way, not giving the answer 🧭""")
        st.session_state.hint_count = hc + 1
        return
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        handle(txt)
        return
    if st.session_state.stage in ("welcome", "done"):
        handle(txt)
        return

    # Queue for AI grading
    st.session_state.pending_answer = txt
    ai("🤖 <span class='spinner'>Grading your answer with AI...</span>")


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════

# Process any pending grading first
if st.session_state.get("pending_answer"):
    grade_pending()

tidx  = st.session_state.task_idx
total = len(TASKS)
pct   = (int((tidx / total) * 100)
         if st.session_state.stage == "task" and tidx < total
         else (100 if st.session_state.stage == "done" else 0))

st.markdown(
    f'<div class="progress-bar-wrap">'
    f'<div class="progress-bar-fill" style="width:{pct}%"></div>'
    f'</div>',
    unsafe_allow_html=True
)

if st.session_state.stage == "task" and tidx < total:
    label = f"{TASKS[tidx]['icon']} {TASKS[tidx]['title']}"
elif st.session_state.stage == "done":
    label = "✅ Assignment Complete"
else:
    label = "LM8 AI Tutor — Ready"

st.markdown(
    f'<div class="top-bar"><h2>🏥 LM8 AI Tutor &nbsp;·&nbsp; {label}</h2></div>',
    unsafe_allow_html=True
)

# Chat messages
st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "ai":
        st.markdown(
            f'<div class="msg-ai"><div class="av">🎓</div>'
            f'<div class="bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="msg-user"><div class="bubble">{msg["content"]}</div>'
            f'<div class="av">You</div></div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Quick buttons
s = st.session_state.stage
cols = st.columns([1, 1, 1, 4])
if s == "welcome":
    with cols[0]:
        if st.button("🚀 Start"):
            handle("start"); st.rerun()
elif s == "task":
    with cols[0]:
        if st.button("💡 Hint"):
            handle("hint"); st.rerun()
    with cols[1]:
        if st.button("▶️ Next"):
            handle("next"); st.rerun()
elif s == "done":
    with cols[0]:
        if st.button("🔄 Restart"):
            handle("restart"); st.rerun()

# Chat input — submit for AI grading
inp = st.chat_input("Type your answer… (type 'hint' if stuck, 'next' to advance)")
if inp:
    submit_for_grading(inp)
    st.rerun()
