# Weighted RoBERTa Statement vs Context Comparison

- Date: 2026-04-11 22:22
- Model: `roberta-base` with weighted training loss
- Seed: `52`
- Controlled change: input text only
- Variant A: `statement` only
- Variant B: `statement + " [CTX] " + context`

## Overall Comparison

| variant | best_epoch | valid_accuracy | valid_macro_f1 | test_accuracy | test_macro_f1 | real_recall | fake_recall | context_dep_accuracy | context_dep_macro_f1 | context_dep_errors | training_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| statement_only | 3 | 0.6604 | 0.6573 | 0.6606 | 0.6496 | 0.7437 | 0.5533 | 0.6802 | 0.6596 | 165 | 7.8899 |
| statement_plus_context | 3 | 0.6565 | 0.6523 | 0.6535 | 0.6402 | 0.7507 | 0.5280 | 0.6550 | 0.6276 | 178 | 7.9311 |

## Interpretation

- Adding context increased context-dependent errors in this controlled comparison.
- Context-dependent subset size: `516`
- Statement-only context-dependent accuracy: `0.6802`
- Statement+context context-dependent accuracy: `0.6550`
- Statement-only context-dependent macro-F1: `0.6596`
- Statement+context context-dependent macro-F1: `0.6276`
- Statement-only context-dependent errors: `165`
- Statement+context context-dependent errors: `178`

## Direct Comparison vs Current Weighted RoBERTa Baseline

- Current weighted RoBERTa baseline (seed 52, statement only reference): Accuracy `0.6606`, Macro-F1 `0.6496`, REAL recall `0.7437`, FAKE recall `0.5533`
- Statement-only rerun: Accuracy `0.6606`, Macro-F1 `0.6496`, REAL recall `0.7437`, FAKE recall `0.5533`
- Statement+context: Accuracy `0.6535`, Macro-F1 `0.6402`, REAL recall `0.7507`, FAKE recall `0.5280`

## Context-Dependent Cases Improved By Adding Context

| statement | context | gold_label | statement_only_label | statement_only_prob_fake | statement_plus_context_label | statement_plus_context_prob_fake |
| --- | --- | --- | --- | --- | --- | --- |
| Wisconsin is on pace to double the number of layoffs this year. | a news conference | FAKE | REAL | 0.4674 | FAKE | 0.8409 |
| Four members of the Rhode Island General Assembly went to vote in 2010 and were told they had already voted. | a TV debate | FAKE | REAL | 0.3716 | FAKE | 0.7123 |
| In six years, (U.S. Rep. Gary) Peters introduced zero bills that became law. | a campaign ad | FAKE | REAL | 0.4474 | FAKE | 0.6456 |
| Barack Obama "rejects everyone white, including his mother and his grandparents." | his book <i>The Obama Nation</i>.  | FAKE | REAL | 0.4933 | FAKE | 0.5956 |
| Its entirely possible that the Democratic nominee, [Hillary Clinton], earned more money giving a single speech on Wall Street than I made the six years that I was there back in the 1980s In fact, its quite likely. | an interview with Chris Stigall on Talk Radio 1210 WPHT | FAKE | REAL | 0.4058 | FAKE | 0.5954 |
| Says he never wanted to raise the debt ceiling. | a flier | FAKE | REAL | 0.3332 | FAKE | 0.5587 |
| For every dollar (in the stimulus package) that is spent to help small businesses, $4 is being spent to help upkeep the grass on the lawns of Washington. | an interview on the Fox News Channel. | FAKE | REAL | 0.4743 | FAKE | 0.5477 |
| In early voting in Miami-Dade County, there is a trickle of two or three people a day at a very high cost to keep those public libraries and polls open. | a Senate Rules Committee meeting | FAKE | REAL | 0.4796 | FAKE | 0.5279 |
| Any state tax law has to start in the House and the renewal of the state hospital bed tax this year started in the Senate, which is unconstitutional. | a public meeting | FAKE | REAL | 0.4939 | FAKE | 0.5027 |
| The sex-offender registry has been around for a long time, and the research thats out there says that it has no positive impact on the public safety. | a newspaper interview | REAL | FAKE | 0.5117 | REAL | 0.4805 |

## Context-Dependent Cases Hurt By Adding Context

| statement | context | gold_label | statement_only_label | statement_only_prob_fake | statement_plus_context_label | statement_plus_context_prob_fake |
| --- | --- | --- | --- | --- | --- | --- |
| Says, when this governor came to office, he had (an) 11 billion dollar - I call it mismanagement deficit. | a panel discussion for "On The Record with Michael Aron" | REAL | REAL | 0.4458 | FAKE | 0.7380 |
| The U.S. energy policy is to "borrow money from China to buy oil from countries that don't like us." | Denver | REAL | REAL | 0.4497 | FAKE | 0.7183 |
| On his support for sharply limiting collective bargaining by public employees. | various votes and public statements | REAL | REAL | 0.4299 | FAKE | 0.6975 |
| To this day, (the Cuban government) is a regime that provides safe harbor to terrorists and fugitives. | a news conference | REAL | REAL | 0.4853 | FAKE | 0.6343 |
| Says she brought together business, labor and hospitals to give 94,000 Oregon children health care. | in a campaign ad | REAL | REAL | 0.4816 | FAKE | 0.5983 |
| First, he was in favor of my plan, now he's attacking it. | nan | REAL | REAL | 0.3681 | FAKE | 0.5915 |
| Women have come through the recession worse off than men the numbers bear that out. We went from a 7 percent unemployment rate for women when he (President Barack Obama) was elected to an 8.1 percent now. | an interview on My9TV.com's "New Jersey Now" program | REAL | REAL | 0.3888 | FAKE | 0.5614 |
| President Obama and Nancy Pelosi said Obamacare would save money because they factored in 10 years worth of tax revenue and only six and half years worth of expenses. | a television interview | REAL | REAL | 0.4895 | FAKE | 0.5537 |
| Vern Buchanan. His old business was caught illegally funneling over $60,000 in campaign donations to Buchanan to influence his election. | in a radio ad | REAL | REAL | 0.3345 | FAKE | 0.5439 |
| Says critics who say he cut Medicaid are wrong; his budget added $1.2 billion to the program | a television interview | REAL | REAL | 0.4112 | FAKE | 0.5391 |