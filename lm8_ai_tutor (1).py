import streamlit as st
import json
import urllib.request
import urllib.error

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
.box-orange { background:#1c0a00;border-left:4px solid #fb923c;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#fed7aa; }
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
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# API KEY  — reads from Streamlit secrets or sidebar input
# ═══════════════════════════════════════════════════════════════

def get_api_key():
    """Get API key from secrets or session state (user-entered)."""
    # 1. Try Streamlit secrets (for deployed apps)
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    # 2. Try session state (user entered in sidebar)
    return st.session_state.get("api_key", "")


# ── Sidebar: API key entry ─────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Key")
    st.markdown("Enter your Anthropic API key to enable AI grading.")
    key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.get("api_key", ""),
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed"
    )
    if key_input:
        st.session_state["api_key"] = key_input
        st.success("✅ Key saved")
    
    api_key = get_api_key()
    if api_key:
        st.markdown(f"<span style='color:#4ade80;font-size:0.82rem'>🤖 AI grading active</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#fbbf24;font-size:0.82rem'>⚠️ No key — using fallback grading</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Navigation")
    tidx_sidebar = st.session_state.get("task_idx", 0)
    st.markdown(f"**Task:** {tidx_sidebar + 1} / 8")
    g = st.session_state.get("grades", {})
    correct_n = sum(1 for v in g.values() if v == "correct")
    partial_n = sum(1 for v in g.values() if v == "partial")
    st.markdown(f"**Score so far:** {correct_n} correct, {partial_n} partial")
    st.markdown("---")
    st.caption("📚 HI 820 — LM8: Classification Models + High Utilizer Prediction")


# ═══════════════════════════════════════════════════════════════
# TASK DEFINITIONS
# type: concept | code_py | code_sql | mixed
# ═══════════════════════════════════════════════════════════════

TASKS = [
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
Run Logistic Regression, Naïve Bayes, and Bayesian Network on it — then explain what you observe.
</div>

<span class='tag-concept'>💬 Conceptual — no code needed</span>""",
    "question":"What pattern do you notice in this dataset? What is the relationship between x, y, and class? Can a straight line separate class=0 from class=1? Explain in plain English.",
    "answer_guidance":"The pattern is XOR (exclusive OR): class=1 when x≠y, class=0 when x=y. No straight line can separate class 0 from class 1 — the data is NOT linearly separable. This is the famous XOR problem.",
    "hint":"Plot the four points mentally: (0,1)→class 1, (1,0)→class 1, (1,1)→class 0, (0,0)→class 0. Try drawing a straight line to separate the 1s from the 0s on a 2D grid. Is it possible?",
  },
  {
    "id":"q1b", "qnum":"Q1", "title":"Q1-B — Why Models Succeed or Fail",
    "icon":"🔍", "type":"concept",
    "intro":"""<div class='box-purple'>
From the assignment results:
• <strong>Logistic Regression (first run)</strong>: 50% accuracy — failed
• <strong>Logistic Regression (tuned)</strong>: 100% accuracy
• <strong>Naïve Bayes</strong>: 50% accuracy — failed
• <strong>Bayesian Network</strong>: 100% accuracy
</div>
<span class='tag-concept'>💬 Conceptual — no code needed</span>""",
    "question":"Explain: (1) WHY did Logistic Regression initially fail? (2) WHY did Naïve Bayes fail? (3) WHY did the Bayesian Network succeed? (4) What change allowed Logistic Regression to reach 100% accuracy?",
    "answer_guidance":"LR failed because XOR is not linearly separable — LR only creates linear boundaries. Naïve Bayes failed because it assumes features are conditionally independent, but x and y interact in XOR. Bayesian Network succeeded because it models dependencies between variables. LR was fixed by adding an interaction term x*y — making the data linearly separable in 3D.",
    "hint":"For LR: what kind of boundary does it draw? For Naïve Bayes: the word NAÏVE refers to an assumption about features — what assumption, and why does XOR violate it? For the fix: what new feature could you add to x and y that captures their relationship?",
  },
  {
    "id":"q1c", "qnum":"Q1", "title":"Q1-C — Code: 3 Models on XOR",
    "icon":"💻", "type":"code_py",
    "intro":"""<div class='box-purple'>
Implement the three models in Python on the XOR dataset.
x=[0,1,1,0], y=[1,0,1,0], class=[1,1,0,0]
Train and test on the same 4 rows (too small to split).
</div>
<span class='tag-py'>🐍 Python code required</span>""",
    "question":"Write Python code to: (1) Create the XOR dataset, (2) Run Logistic Regression, (3) Run Gaussian Naïve Bayes, (4) Print accuracy for each. Then add an interaction term x*y to LR and show it reaches 100% accuracy.",
    "answer_guidance":"Create DataFrame with x,y,class. X=df[['x','y']], y=df['class']. Train LR and GaussianNB with .fit(X,y), predict with .predict(X), print accuracy_score. For the fix: X2=X.copy(); X2['xy']=X2['x']*X2['y']; train new LR on X2. Key: same data for train and test (only 4 rows). Must add x*y interaction term.",
    "hint":"from sklearn.linear_model import LogisticRegression; from sklearn.naive_bayes import GaussianNB; from sklearn.metrics import accuracy_score. Create df, set X=df[['x','y']], y=df['class']. For interaction: X2['xy'] = X2['x'] * X2['y'] creates a column that is 1 only when both x=1 and y=1.",
  },
  {
    "id":"q2", "qnum":"Q2", "title":"Q2 — Combining Classification Models",
    "icon":"🤝", "type":"concept",
    "intro":"""<strong>Question 2: How can multiple classification models be combined?</strong>
<div class='box-purple'>Describe ensemble learning and its three main methods.</div>
<span class='tag-concept'>💬 Conceptual — no code needed</span>""",
    "question":"(1) Why does combining multiple models give better predictions than any single model? (2) Describe Bagging, Boosting, and Stacking — how does each work and give a real algorithm example for each.",
    "answer_guidance":"Core: different models make different errors; combining cancels mistakes. Bagging: bootstrap samples + parallel models + average/vote (example: Random Forest). Boosting: sequential models, each focusing on previous mistakes (example: AdaBoost, XGBoost). Stacking: base models (level 0) + meta-model (level 1) learns to combine them.",
    "hint":"Think of a jury of 12 vs. one judge. For Bagging: parallel, random samples, independent models. For Boosting: sequential, learns from mistakes, weighted errors. For Stacking: a higher-level model that takes other models' outputs as its inputs.",
  },
  {
    "id":"q3", "qnum":"Q3", "title":"Q3 — Unit of Analysis",
    "icon":"🔬", "type":"concept",
    "intro":"""<strong>Question 3: Unit of analysis in the testClaims problem</strong>
<div class='box-purple'>Raw tables: claims_10k (one row per claim), diagnoses (one row per diagnosis), drugcount (monthly), procedures (one per procedure). All aggregated into highUtilizer_Y3_final.</div>
<span class='tag-concept'>💬 Conceptual — no code needed</span>""",
    "question":"(1) What is the unit of analysis? What does ONE ROW represent in the final table? (2) Why is GROUP BY patient_id critical? What would happen without it?",
    "answer_guidance":"Unit of analysis = PATIENT. Each row = one patient with aggregated Y1+Y2 features and Y3 label. GROUP BY collapses many rows per patient into one. Without GROUP BY: one row per claim per patient → joining with outcome causes row explosion → wrong dataset. MAX(CASE WHEN) creates binary flag: did patient EVER have this diagnosis.",
    "hint":"Look at the final table columns — what is the primary key? Each row is about WHO? If GROUP BY was missing from the ELIX step, and a patient had 200 claims in Y1+Y2, how many rows would they contribute to the ELIX table?",
  },
  {
    "id":"q4a", "qnum":"Q4", "title":"Q4-A — SQL: Cohort + ELIX Features",
    "icon":"🗄️", "type":"code_sql",
    "intro":"""<strong>Question 4: Build full dataset (Y1+Y2 → predict Y3)</strong>
<div class='box-purple'>Step 1: Cohort — patients in BOTH Y1 and Y2. Step 2: ELIX features — binary flags ELIX1-29.</div>
<span class='tag-sql'>🗄️ SQL code required</span>""",
    "question":"Write SQL for:\n(1) #pat_Y1Y2 — patients present in BOTH Y1 and Y2 from claims_10k\n(2) #Elix_Y1Y2 — binary ELIX1-ELIX29 columns, one row per patient, from Y1+Y2 diagnoses",
    "answer_guidance":"Step 1: SELECT patient_id INTO #pat_Y1Y2 FROM claims_10k WHERE year IN ('Y1','Y2') GROUP BY patient_id HAVING COUNT(DISTINCT year)=2. Step 2: SELECT patient_id, MAX(CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END) AS ELIX1, ... INTO #Elix_Y1Y2 FROM diagnoses d JOIN claims_10k c ON d.claim_id=c.claim_id AND c.year IN ('Y1','Y2') GROUP BY patient_id. Key: HAVING for both years; JOIN via claim_id; MAX(CASE WHEN) for binary pivot.",
    "hint":"Step 1: GROUP BY patient_id + HAVING COUNT(DISTINCT year)=2 to ensure both years. Step 2: diagnoses joins to claims via claim_id (not patient_id). MAX(CASE WHEN diagnosis='ELIX1' THEN 1 ELSE 0 END) — why MAX not SUM? Because we want binary (ever had it = 1), not a count.",
  },
  {
    "id":"q4b", "qnum":"Q4", "title":"Q4-B — SQL: Outcome + Gold Join",
    "icon":"🥇", "type":"code_sql",
    "intro":"""<div class='box-purple'>Step 3: Y3 outcome (highUtilizer: ≥100 claims = 1). Steps 4-6: drug/procedure features + Gold layer join.</div>
<span class='tag-sql'>🗄️ SQL code required</span>""",
    "question":"Write SQL for:\n(1) #claims_count_Y3 — count Y3 claims per patient, binary highUtilizer label (≥100 = 1)\n(2) The Gold layer join — explain why INNER JOIN for core tables and LEFT JOIN for drug/procedure tables",
    "answer_guidance":"Step 3: SELECT patient_id, COUNT(*) AS countClaims, CASE WHEN COUNT(*)>=100 THEN 1 ELSE 0 END AS highUtilizer INTO #claims_count_Y3 FROM claims_10k WHERE year='Y3' GROUP BY patient_id. Gold join: INNER JOIN for cohort+ELIX+outcome (every patient needs both features and label). LEFT JOIN for drug/procedure (not all patients have records — missing = 0, not excluded). ISNULL(...,0) cleans NULLs.",
    "hint":"For Step 3: WHERE year='Y3', GROUP BY patient_id, CASE WHEN COUNT(*)>=100 THEN 1 ELSE 0 END. For join: INNER JOIN means a patient with no match is DROPPED. LEFT JOIN means a patient with no drug records gets NULLs (then ISNULL to 0). Which is appropriate for drug/procedure data?",
  },
  {
    "id":"q4c", "qnum":"Q4", "title":"Q4-C — Python: 3 ML Models + Analysis",
    "icon":"🤖", "type":"mixed",
    "intro":"""<div class='box-purple'>Results: LR: Acc=89.5%, AUC=0.826 | DT: Acc=90.2%, AUC=0.816 | RF: Acc=89.4%, AUC=0.791. Y2-only LR: Acc=90.7%, AUC=0.812</div>
<span class='tag-py'>🐍 Python</span> + <span class='tag-concept'>💬 Explanation</span>""",
    "question":"(1) Write Python to load the CSV, prepare X/y (drop correct columns), stratified 80/20 split, scale for LR, train all 3 models, print Accuracy and AUC.\n(2) Which model to choose and why?\n(3) Does Y1+Y2 outperform Y2-only? Explain the AUC vs accuracy trade-off.",
    "answer_guidance":"Code: drop highUtilizer, patient_id, AND countClaims from X (countClaims is a proxy for the label — data leakage!). stratify=y in split. scaler.fit_transform on train, scaler.transform on test only. predict_proba[:,1] for AUC. Model choice: LR has highest AUC (0.826) — AUC is primary metric for imbalanced data. Y1+Y2: lower accuracy (89.5% vs 90.7%) but higher AUC (0.826 vs 0.812) — two years of history improves discrimination even if raw accuracy drops slightly.",
    "hint":"Key mistakes to avoid: (1) drop countClaims from X — it directly predicts highUtilizer (leakage!), (2) scaler.transform() on test set, NOT fit_transform(), (3) roc_auc_score needs predict_proba(X_test)[:,1] not predict(X_test), (4) stratify=y keeps class balance in both splits.",
  },
]

# ═══════════════════════════════════════════════════════════════
# AI GRADER
# ═══════════════════════════════════════════════════════════════

def call_claude(task, student_answer, hint_used, api_key):
    """Call Claude API to grade the student's answer."""

    type_note = {
        "concept":  "CONCEPTUAL question — student answers in plain English, no code expected.",
        "code_py":  "PYTHON CODE question — evaluate code logic and correctness.",
        "code_sql": "SQL CODE question — evaluate SQL logic and use of correct clauses.",
        "mixed":    "Requires BOTH Python code AND written explanation — evaluate both.",
    }.get(task["type"], "")

    system = f"""You are a health informatics professor grading student answers.
{type_note}

Rules:
- NEVER reveal the correct answer or copy the answer guidance
- DO say specifically what the student got right
- DO say specifically what is missing or wrong
- DO ask ONE focused Socratic question to guide improvement
- Grade: "correct" = all key concepts present, "partial" = some right but incomplete, "incorrect" = wrong or too vague

Return ONLY valid JSON, no markdown:
{{"grade":"correct|partial|incorrect","feedback":"2-3 sentences on what is right and what is missing","nudge":"one focused guiding question"}}"""

    user = f"""Task: {task['title']}
Question: {task['question']}
Correct answer guidance (do NOT reveal): {task['answer_guidance']}
Student answer: {student_answer}
Hint already given: {hint_used}"""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    raw = data["content"][0]["text"].strip()
    # Strip any markdown fences
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip().lstrip("json").strip()
            try:
                r = json.loads(part)
                return r["grade"], r["feedback"], r["nudge"]
            except Exception:
                continue
    r = json.loads(raw)
    return r["grade"], r["feedback"], r["nudge"]


def smart_fallback(task, answer):
    """Keyword-based fallback when API is unavailable."""
    low   = answer.lower()
    words = answer.split()
    wc    = len(words)

    # Task-specific keyword checks
    kw_map = {
        "q1a": (["xor","exclusive","linear","separate","class","pattern"], 3),
        "q1b": (["linear","independent","naive","interact","boundary","network","depend"], 3),
        "q1c": (["logisticregression","gaussiannb","accuracy_score","fit","predict","xy","interaction"], 3),
        "q2":  (["bagging","boosting","stacking","random forest","adaboost","error","ensemble"], 3),
        "q3":  (["patient","group by","row","aggregate","label","unit","one row"], 3),
        "q4a": (["having","count","distinct","case when","max","join","claim_id","group by"], 3),
        "q4b": (["inner join","left join","count","where year","null","isnull","outcome"], 3),
        "q4c": (["countclaims","stratify","scaler","transform","auc","roc_auc","predict_proba"], 3),
    }

    kws, threshold = kw_map.get(task["id"], ([], 2))
    hits = sum(1 for k in kws if k in low)

    if wc < 10:
        return ("incorrect",
                "Your answer is too brief — please explain your reasoning in more detail.",
                "What is the core concept this question is testing?")
    if hits >= threshold and wc >= 25:
        return ("correct",
                "You've covered the key ideas well.",
                "")
    if hits >= 2 or wc >= 40:
        return ("partial",
                f"You have some of the right ideas ({hits}/{len(kws)} key concepts found). Let's go deeper.",
                f"What is missing from: {', '.join(kws[:3])}?")
    return ("incorrect",
            "Your answer is missing the core concepts for this question.",
            f"Think about: {kws[0] if kws else 'the main idea here'}.")


def grade(task, answer, hint_used):
    """Grade with Claude API, fall back gracefully."""
    api_key = get_api_key()
    if api_key and api_key.startswith("sk-"):
        try:
            return call_claude(task, answer, hint_used, api_key)
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if "401" in str(e.code):
                return ("incorrect",
                        "⚠️ API key is invalid or expired.",
                        "Please check your Anthropic API key in the sidebar.")
            # Other HTTP errors — fall through to fallback
        except Exception:
            pass
    # No key or API error → smart fallback
    return smart_fallback(task, answer)


def render_feedback(grade_val, feedback, nudge, title):
    badge = "<span class='ai-badge'>🤖 AI</span>"
    api_key = get_api_key()
    if not (api_key and api_key.startswith("sk-")):
        badge = "<span class='ai-badge'>⚡ Auto</span>"

    if grade_val == "correct":
        extra = f"\n\n<div class='box-blue'>💡 {nudge}</div>" if nudge else ""
        return f"""<div class='box-green'>
✅ {badge} <strong>Great work on {title}!</strong>

{feedback}{extra}
</div>

Type <strong>next</strong> to continue 👉"""

    elif grade_val == "partial":
        return f"""<div class='box-yellow'>
⚠️ {badge} <strong>You're on the right track!</strong>

{feedback}
</div>

<div class='box-blue'>
💭 <strong>Think about this:</strong> {nudge}
</div>

Revise your answer or type <strong>hint</strong> for a step-by-step nudge."""

    else:
        return f"""<div class='box-red'>
❌ {badge} <strong>Not quite yet — let's rethink this.</strong>

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
        "messages": [], "task_idx": 0, "stage": "welcome",
        "hint_count": 0, "hint_used": False,
        "grades": {}, "initialized": False,
        "awaiting_next": False, "pending_answer": None,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

def ai(t):  st.session_state.messages.append({"role": "ai",   "content": t})
def usr(t): st.session_state.messages.append({"role": "user", "content": t})

WELCOME = """🏥 <strong>Welcome to the LM8 AI Tutor!</strong>

I'm your AI-powered guide for <em>HI 820 — LM8: Classification Models + High Utilizer Prediction</em>.

<div class='box-purple'>
<strong>📋 8 Tasks across 4 Questions:</strong>
• <strong>Q1</strong> — XOR data: identify pattern, explain model failures, write Python code
• <strong>Q2</strong> — Ensemble methods: Bagging, Boosting, Stacking
• <strong>Q3</strong> — Unit of analysis in testClaims
• <strong>Q4</strong> — Build the full pipeline in SQL + run 3 ML models in Python
</div>

<div class='box-green'>
✨ <strong>AI Grading:</strong> Your answers are evaluated by Claude AI — reads actual meaning, not just keywords.
Add your <strong>Anthropic API key in the sidebar</strong> to activate full AI grading.
<span class='tag-concept'>💬 Conceptual</span> tasks = plain English only, no code needed!
</div>

🔹 I NEVER give direct answers — Socratic guidance only
🔹 Type <strong>hint</strong> anytime · Type <strong>next</strong> after a correct answer

Ready? Click <strong>Start</strong> or type anything 👇"""

if not st.session_state.initialized:
    ai(WELCOME)
    st.session_state.initialized = True


def present_task(idx):
    t = TASKS[idx]
    type_tag = {
        "concept":  "<span class='tag-concept'>💬 No code needed</span>",
        "code_py":  "<span class='tag-py'>🐍 Python code</span>",
        "code_sql": "<span class='tag-sql'>🗄️ SQL code</span>",
        "mixed":    "<span class='tag-py'>🐍 Python</span> + <span class='tag-concept'>💬 Explanation</span>",
    }.get(t["type"], "")
    return (f"{t['icon']} <strong>Task {idx+1}/{len(TASKS)} — {t['title']}</strong>  "
            f"<span class='tag-q'>{t['qnum']}</span> {type_tag}\n\n"
            f"{t['intro']}\n\n"
            f"<strong>❓ Question:</strong>\n{t['question']}")


NEXT_W = {"next","continue","ready","go","yes","ok","sure","move on",
          "proceed","got it","understood","done","start","begin"}


def process_next():
    """Advance to next task or show final scorecard."""
    st.session_state.awaiting_next = False
    st.session_state.hint_count    = 0
    st.session_state.hint_used     = False
    next_idx = st.session_state.task_idx + 1
    st.session_state.task_idx = next_idx

    if next_idx >= len(TASKS):
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
        ai(f"""🎓 <strong>LM8 Assignment Complete! Scorecard:</strong>

{rows}

<div class='box-green'>
<strong>Score: {correct_n}/{len(TASKS)} fully correct — {score}%</strong>
{'🌟 Outstanding!' if score >= 85 else '🎉 Great work! Review ⚠️/❌ tasks.' if score >= 55 else '💪 Keep going! Re-read each section.'}
</div>

<strong>Key Takeaways:</strong>
📊 <strong>Q1</strong> — XOR not linearly separable. Add x*y interaction to fix LR. Naïve Bayes fails (independence assumption). Bayesian Network models dependencies.
🤝 <strong>Q2</strong> — Bagging (Random Forest, ↓ variance) · Boosting (XGBoost, ↓ bias) · Stacking (meta-model combines outputs)
🔬 <strong>Q3</strong> — Unit = PATIENT. GROUP BY collapses many rows per patient. MAX(CASE WHEN) = binary flag.
🥇 <strong>Q4</strong> — HAVING COUNT(DISTINCT year)=2 for cohort · LEFT JOIN for drug/proc · AUC > Accuracy for imbalanced data · Drop countClaims from X!

Type <strong>restart</strong> to try again 🔄""")
    else:
        ai(present_task(next_idx))


def handle(raw):
    txt = raw.strip()
    if not txt: return
    low = txt.lower()

    if "restart" in low:
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    if st.session_state.stage == "welcome":
        usr(txt)
        st.session_state.stage = "task"
        ai(f"Let's begin! 🚀\n\n{present_task(0)}")
        return

    if st.session_state.stage == "done":
        usr(txt)
        ai("Assignment complete! Type <strong>restart</strong> to go again. 🔄")
        return

    # Hint
    if any(w in low for w in ["hint","help","stuck","confused","don't know","idk"]):
        usr(txt)
        tidx = st.session_state.task_idx
        t = TASKS[tidx]
        st.session_state.hint_used = True
        hc = st.session_state.hint_count
        ai(f"""💡 <strong>Hint {hc+1} for {t['title']}:</strong>
<div class='box-blue'>{t['hint']}</div>
Give it another try — I'm pointing the way, not giving the answer 🧭""")
        st.session_state.hint_count = hc + 1
        return

    # Next navigation
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        usr(txt)
        process_next()
        return

    # Queue for AI grading
    usr(txt)
    st.session_state.pending_answer = txt
    ai("🤖 <em style='color:#7c3aed'>Grading your answer...</em>")


def grade_pending():
    """Process pending answer through AI grader."""
    txt = st.session_state.pending_answer
    if not txt:
        return

    tidx = st.session_state.task_idx
    t    = TASKS[tidx]

    # Remove spinner message
    msgs = st.session_state.messages
    if msgs and "Grading your answer" in msgs[-1]["content"]:
        msgs.pop()

    grade_val, feedback, nudge = grade(t, txt, st.session_state.hint_used)

    # Store best grade
    prev = st.session_state.grades.get(t["id"], "")
    if grade_val == "correct" or (grade_val == "partial" and prev != "correct"):
        st.session_state.grades[t["id"]] = grade_val

    fb = render_feedback(grade_val, feedback, nudge, t["title"])

    if grade_val == "correct":
        st.session_state.awaiting_next = True
        remaining = len(TASKS) - tidx - 1
        nav = f"task {tidx+2}" if remaining > 0 else "your final scorecard"
        fb = fb.replace("Type <strong>next</strong> to continue 👉",
                        f"Type <strong>next</strong> for {nav} 👉")

    ai(fb)
    st.session_state.pending_answer = None


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════

if st.session_state.get("pending_answer"):
    grade_pending()

tidx  = st.session_state.task_idx
total = len(TASKS)
pct   = (int((tidx / total) * 100) if st.session_state.stage == "task" and tidx < total
         else (100 if st.session_state.stage == "done" else 0))

st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div>',
            unsafe_allow_html=True)

if st.session_state.stage == "task" and tidx < total:
    label = f"{TASKS[tidx]['icon']} {TASKS[tidx]['title']}"
elif st.session_state.stage == "done":
    label = "✅ Complete"
else:
    label = "Ready"

st.markdown(f'<div class="top-bar"><h2>🏥 LM8 AI Tutor &nbsp;·&nbsp; {label}</h2></div>',
            unsafe_allow_html=True)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "ai":
        st.markdown(f'<div class="msg-ai"><div class="av">🎓</div><div class="bubble">{msg["content"]}</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-user"><div class="bubble">{msg["content"]}</div><div class="av">You</div></div>',
                    unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

s = st.session_state.stage
cols = st.columns([1, 1, 1, 4])
if s == "welcome":
    with cols[0]:
        if st.button("🚀 Start"):    handle("start"); st.rerun()
elif s == "task":
    with cols[0]:
        if st.button("💡 Hint"):     handle("hint");  st.rerun()
    with cols[1]:
        if st.button("▶️ Next"):     handle("next");  st.rerun()
elif s == "done":
    with cols[0]:
        if st.button("🔄 Restart"):  handle("restart"); st.rerun()

inp = st.chat_input("Type your answer… (type 'hint' if stuck, 'next' to advance)")
if inp:
    handle(inp)
    st.rerun()
