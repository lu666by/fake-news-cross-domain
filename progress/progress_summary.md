# Progress Summary (living document)

> Note (for supervisor): The up-to-date plan + progress tracker is maintained in `tracking.md` (single source of truth).  
> This file provides short narrative context only.

## Latest update: 2026-03-19 (Ireland time)

### What I have achieved

Since the last update, I continued the LIAR implementation work and revised the baseline direction after the supervisor meeting.

1. **Repository organisation and tracking**
   - `tracking.md` remains the single place that records task status and evidence links.
   - `plans/` and `progress/` files are kept short and provide only narrative context.

2. **LIAR dataset loading and inspection**
   - `notebooks/01_liar_load.ipynb` loads the LIAR `train`, `valid`, and `test` splits.
   - The notebook prints:
     - dataset shapes
     - label distribution
     - example statements
     - example contexts
     - simple text statistics

   Current LIAR split sizes:
   - Train: 10240
   - Valid: 1284
   - Test: 1267

3. **LIAR TF-IDF baseline: Version 1 completed**
   - Implemented the initial LIAR binary baseline in `notebooks/02_tfidf_baseline.ipynb`.
   - Model: **TF-IDF + Logistic Regression**
   - Version 1 result:
     - Accuracy: 0.6196
     - Macro-F1: 0.5935

4. **LIAR TF-IDF baseline: Version 2 improvement**
   - Revised the notebook to make model selection more systematic.
   - The updated version now:
     - uses the fixed binary mapping for this project
     - compares preprocessing settings
     - compares TF-IDF settings on the validation split
     - evaluates the final selected configuration on the test split

   Current binary mapping:
   - REAL (0): `true`, `mostly-true`, `half-true`
   - FAKE (1): `barely-true`, `false`, `pants-fire`

   Current Version 2 selected configuration:
   - Preprocess: `P0_minimal`
   - `ngram_range=(1,2)`
   - `min_df=1`
   - `max_df=1.0`

   Current Version 2 result:
   - Accuracy: 0.6243
   - Macro-F1: 0.5968

   Compared with Version 1, this is only a small improvement:
   - Accuracy delta: +0.0047
   - Macro-F1 delta: +0.0033

5. **Current performance pattern**
   - The main remaining weakness is still the FAKE class.
   - In the current Version 2 test result:
     - REAL recall = 0.7857
     - FAKE recall = 0.4159
   - This means the model still tends to predict REAL more easily than FAKE.

---

### Key takeaways so far

- The initial LIAR baseline has now been completed as **Version 1**, but the result is still relatively low.
- A more systematic **Version 2** baseline has also been completed, but the improvement over Version 1 is still small.
- The current experiments suggest that stronger preprocessing did not improve this LIAR binary baseline.
- The main problem is no longer basic setup, but the limited performance of the traditional baseline, especially weak recall for the FAKE class.
- This means the next step should still focus on understanding and improving the traditional baseline before moving to stronger models.

---

### Open questions / risks (only items I can clearly explain)

**Why is the LIAR baseline still relatively low?**

- What it means: even after improving the experimental structure, the baseline result is still only around 0.62 accuracy and 0.60 macro-F1.
- Why it matters: the dissertation needs a stronger and better justified baseline before later cross-dataset experiments.
- Next step: compare with the literature, test class balancing, and compare another traditional classifier such as `LinearSVC`.

**Weak recall for the FAKE class**

- What it means: many FAKE examples are still misclassified as REAL.
- Why it matters: this lowers Macro-F1 and suggests the model is biased toward the REAL class.
- Next step: test class weighting and compare alternative traditional classifiers.

**Literature comparison is still needed**

- What it means: the current project result has not yet been fully placed beside reported LIAR results from previous work.
- Why it matters: the supervisor specifically asked how the current result compares with other published results.
- Next step: add a short literature comparison section in `results/liar_baseline.md`.

---

### Next actions

The next implementation steps are:

1. keep improving the traditional LIAR baseline before moving to stronger models
2. test class balancing for Logistic Regression
3. compare Logistic Regression with another traditional classifier such as `LinearSVC`
4. add a short literature comparison for LIAR results
5. update `results/liar_baseline.md` with:
   - Version 1 result
   - Version 2 result
   - validation comparisons
   - short interpretation of the remaining error pattern

Dates and detailed task status are tracked in:

`tracking.md`
