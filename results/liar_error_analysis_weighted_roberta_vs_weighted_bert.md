# LIAR Error Analysis: Weighted RoBERTa vs Weighted BERT

## Models Analyzed

- Weighted RoBERTa representative checkpoint: `roberta-base`, seed `52` (best overall single run in the 5-seed sweep)
- Weighted BERT representative checkpoint: `bert-base-uncased`, seed `72` (highest FAKE recall in the 5-seed weighted BERT sweep)
- Dataset split analyzed: LIAR `test.tsv` only
- Both models use class weights computed from the LIAR train split only and load `best_state_dict` before test evaluation

## Test Metrics Used for Analysis

- Weighted RoBERTa seed 52: test accuracy `0.6606`, macro-F1 `0.6496`, REAL recall `0.7437`, FAKE recall `0.5533`
- Weighted BERT seed 72: test accuracy `0.6472`, macro-F1 `0.6439`, REAL recall `0.6597`, FAKE recall `0.6311`

## Pattern Summary

- Weighted RoBERTa false positives: label_boundary_ambiguity: 135, ambiguous_wording: 73, context_dependent: 71, numeric_claim: 47, negation: 36, short_statement: 25, other: 8
- Weighted RoBERTa false negatives: numeric_claim: 114, label_boundary_ambiguity: 106, context_dependent: 94, ambiguous_wording: 88, negation: 25, other: 20, short_statement: 9
- Weighted BERT false positives: label_boundary_ambiguity: 188, ambiguous_wording: 117, context_dependent: 96, numeric_claim: 79, negation: 32, short_statement: 29, other: 7
- Weighted BERT false negatives: numeric_claim: 100, label_boundary_ambiguity: 87, context_dependent: 76, ambiguous_wording: 52, negation: 26, other: 15, short_statement: 8
- BERT correct / RoBERTa wrong: label_boundary_ambiguity: 56, ambiguous_wording: 54, context_dependent: 46, numeric_claim: 37, negation: 17, other: 10, short_statement: 5
- RoBERTa correct / BERT wrong: label_boundary_ambiguity: 90, ambiguous_wording: 62, numeric_claim: 55, context_dependent: 53, negation: 14, short_statement: 8, other: 4

## Why FAKE Recall Is Still Difficult

- Many binary FAKE examples come from the LIAR labels `barely-true` and `false`, while many REAL examples come from `half-true` and `mostly-true`; the boundary is semantically narrow, so models often predict REAL when a claim sounds partly plausible.
- Numeric and policy claims are hard because they require external fact verification; surface text alone often looks fluent and factual even when the gold label is FAKE.
- Context-dependent claims remain difficult because the project input is only `statement`; missing speaker, venue, timing, and background evidence makes short political claims especially ambiguous.

## Why Weighted BERT Helps FAKE Recall

- The weighted loss increases the penalty for missing FAKE-class examples, so weighted BERT moves its decision boundary toward predicting FAKE more often.
- In the selected comparison, weighted BERT catches more FAKE examples than weighted RoBERTa on statements that contain weakly supported accusations, hedged claims, or borderline `barely-true` examples.
- This shows up directly in FAKE recall: weighted BERT seed 72 reaches `0.6311` vs weighted RoBERTa seed 52 at `0.5533`.

## Why Weighted RoBERTa Performs Better Overall But Not Best On FAKE Recall

- Weighted RoBERTa is stronger overall because it makes fewer broad calibration errors on REAL examples, especially on short and context-light statements where weighted BERT can over-predict FAKE.
- That improves overall accuracy and macro-F1, but it also means RoBERTa keeps a slightly more conservative FAKE decision boundary than weighted BERT.
- In practice, weighted RoBERTa wins on overall balance, while weighted BERT still has an advantage on catching more FAKE items.

## Weighted RoBERTa False Positives

| statement | original_6way_label | gold_label | model | pattern_tags | predicted_label | predicted_confidence | prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sherrod Brown and his special interest allies in Washington are plotting to spend over $13 million to defeat Josh Mandel. | half-true | REAL | weighted_roberta | numeric_claim, context_dependent, label_boundary_ambiguity | FAKE | 0.9358 | 0.9358 |
| Muslim nations did not call out the people who celebrated the 9/11 attacks. | half-true | REAL | weighted_roberta | numeric_claim, negation, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.9241 | 0.9241 |
| Jennifer Carrolls an outsider. | half-true | REAL | weighted_roberta | short_statement, label_boundary_ambiguity | FAKE | 0.8864 | 0.8864 |
| I wake up every morning in a house (the White House) that was built by slaves. | true | REAL | weighted_roberta | context_dependent | FAKE | 0.9271 | 0.9271 |
| Says his views on reparations for slavery are the same as Barack Obamas and Hillary Clintons. | mostly-true | REAL | weighted_roberta | context_dependent, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.9217 | 0.9217 |
| Says a YouTube video shows Thomas DiMassimo, the man who rushed Trump at an Ohio rally, dragging the American flag on the ground like it was a piece of garbage. | true | REAL | weighted_roberta | context_dependent, ambiguous_wording | FAKE | 0.9261 | 0.9261 |
| The words subhuman mongrel, which Ted Nugent called President Barack Obama, were used by the Nazis to justify the genocide of the Jewish community. | true | REAL | weighted_roberta | other | FAKE | 0.9173 | 0.9173 |
| Republicans are attempting to remove Barack Obama from Georgias Presidential Ballot in 2012. | half-true | REAL | weighted_roberta | numeric_claim, label_boundary_ambiguity | FAKE | 0.9202 | 0.9202 |
| Obamacare was the Republican plan in the early 90s. | half-true | REAL | weighted_roberta | numeric_claim, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.9184 | 0.9184 |
| Says Scott Walkers plan to replace Obamacare is a new entitlement program for every single American human being from the time they are born right up until they grow old and become eligible for Medicare. | half-true | REAL | weighted_roberta | context_dependent, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.9163 | 0.9163 |

## Weighted RoBERTa False Negatives

| statement | original_6way_label | gold_label | model | pattern_tags | predicted_label | predicted_confidence | prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Citizens Property Insurance has over $500 billion worth of risk, with less than $10 billion worth of surplus. | barely-true | FAKE | weighted_roberta | numeric_claim, label_boundary_ambiguity | REAL | 0.8946 | 0.1054 |
| Over the past year ... our 16 counties have hemorrhaged more than 6,000 jobs with no apparent end in sight. | false | FAKE | weighted_roberta | numeric_claim, negation | REAL | 0.8395 | 0.1605 |
| Some of the wealthiest Americans are African-American now. | false | FAKE | weighted_roberta | short_statement | REAL | 0.8336 | 0.1664 |
| In 2004, "20 percent of U.S. households were getting about 75 percent of their income from the federal government. ... Another 20 percent were receiving almost 40 percent." | barely-true | FAKE | weighted_roberta | numeric_claim, context_dependent, label_boundary_ambiguity | REAL | 0.8799 | 0.1201 |
| Chile ranks third internationally in economic freedom, while the U.S. ranks 17th. | barely-true | FAKE | weighted_roberta | numeric_claim, label_boundary_ambiguity | REAL | 0.8855 | 0.1145 |
| The United States can immediately tap a domestic energy resource of more than 1.5 trillion barrels of oil, six times more than Saudi Arabia. | barely-true | FAKE | weighted_roberta | numeric_claim, label_boundary_ambiguity, ambiguous_wording | REAL | 0.8812 | 0.1188 |
| The United States is at historic record highs of individuals being apprehended on the border from countries with terrorist ties such as Pakistan or Afghanistan or Syria. | pants-fire | FAKE | weighted_roberta | other | REAL | 0.8601 | 0.1399 |
| Of the roughly 15 percent of Americans who dont have health insurance, half of them made more than $50,000 a year. | false | FAKE | weighted_roberta | numeric_claim | REAL | 0.8818 | 0.1182 |
| Texas high school graduation rate went from 27th in the country in 2002, to second highest in the country in 2013. | barely-true | FAKE | weighted_roberta | numeric_claim, label_boundary_ambiguity | REAL | 0.8815 | 0.1185 |
| We have trade agreements with 20 countries, and we have trade surpluses with each one of those 20. | false | FAKE | weighted_roberta | numeric_claim, context_dependent | REAL | 0.8754 | 0.1246 |

## Weighted BERT False Positives

| statement | original_6way_label | gold_label | model | pattern_tags | predicted_label | predicted_confidence | prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sherrod Brown and his special interest allies in Washington are plotting to spend over $13 million to defeat Josh Mandel. | half-true | REAL | weighted_bert | numeric_claim, context_dependent, label_boundary_ambiguity | FAKE | 0.8617 | 0.8617 |
| Says a Ted Cruz ad has got me bull-dozing down a house.I never bulldozed it down. Its false advertising. | half-true | REAL | weighted_bert | negation, context_dependent, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8455 | 0.8455 |
| Jennifer Carrolls an outsider. | half-true | REAL | weighted_bert | short_statement, label_boundary_ambiguity | FAKE | 0.8876 | 0.8876 |
| Suzanne Bonamici supports a plan that will cut choice for Medicare Advantage seniors. | half-true | REAL | weighted_bert | context_dependent, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8707 | 0.8707 |
| Uses headlines to portray Gov. Rick Perry as beholden to special interests. | mostly-true | REAL | weighted_bert | label_boundary_ambiguity | FAKE | 0.8681 | 0.8681 |
| Says my plan is a property tax cut. | half-true | REAL | weighted_bert | short_statement, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8658 | 0.8658 |
| Sayvideo shows massive alligator strolling across Florida golf course. | true | REAL | weighted_bert | other | FAKE | 0.8393 | 0.8393 |
| Says Scott Walkers plan to replace Obamacare is a new entitlement program for every single American human being from the time they are born right up until they grow old and become eligible for Medicare. | half-true | REAL | weighted_bert | context_dependent, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8637 | 0.8637 |
| Says Mark Pryorcut Medicare to pay for Obamacare. | half-true | REAL | weighted_bert | short_statement, label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8583 | 0.8583 |
| Says the Congressional Budget Office is expecting a protracted economic malaise for at least the next decade under current policies. | half-true | REAL | weighted_bert | label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8581 | 0.8581 |

## Weighted BERT False Negatives

| statement | original_6way_label | gold_label | model | pattern_tags | predicted_label | predicted_confidence | prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Over the past year ... our 16 counties have hemorrhaged more than 6,000 jobs with no apparent end in sight. | false | FAKE | weighted_bert | numeric_claim, negation | REAL | 0.9196 | 0.0804 |
| When undocumented children are picked up at the border and told to appear later in court ... 90 percent do not then show up. | false | FAKE | weighted_bert | numeric_claim, negation | REAL | 0.8326 | 0.1674 |
| Some of the wealthiest Americans are African-American now. | false | FAKE | weighted_bert | short_statement | REAL | 0.9017 | 0.0983 |
| What I look at every month is how many more New Jerseyans are back to work. You have another 9,900 last month that are back to work and over almost 90,000 that are back to work now since I became governor. | false | FAKE | weighted_bert | numeric_claim, context_dependent | REAL | 0.8962 | 0.1038 |
| Texas high school graduation rate went from 27th in the country in 2002, to second highest in the country in 2013. | barely-true | FAKE | weighted_bert | numeric_claim, label_boundary_ambiguity | REAL | 0.9168 | 0.0832 |
| Says If you compare the Portland Metro area to the CDCs statewide cavity rates ... the Portland Metro area would actually rank as having the 15th lowest cavity rate in the U.S. | false | FAKE | weighted_bert | numeric_claim, ambiguous_wording | REAL | 0.8606 | 0.1394 |
| And weve constantly been the lowest unemployed county in the state. | false | FAKE | weighted_bert | other | REAL | 0.9149 | 0.0851 |
| We spend in tax loopholes annually $1.1 trillion. Thats more than we spend on our defense budget in a year, on Medicare or Medicaid in a year. | barely-true | FAKE | weighted_bert | numeric_claim, label_boundary_ambiguity | REAL | 0.9125 | 0.0875 |
| Of the roughly 15 percent of Americans who dont have health insurance, half of them made more than $50,000 a year. | false | FAKE | weighted_bert | numeric_claim | REAL | 0.9089 | 0.0911 |
| Wisconsin dropped from second in the country to 41st among states where more than half the students took the ACT exam. | pants-fire | FAKE | weighted_bert | numeric_claim | REAL | 0.9037 | 0.0963 |

## Weighted BERT Correct / Weighted RoBERTa Wrong

| statement | original_6way_label | gold_label | pattern_tags | bert_pred | bert_confidence | bert_prob_fake | roberta_pred | roberta_confidence | roberta_prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I wrote to Secretary Paulson, I wrote to Federal Reserve Chairman Bernanke [in March 2007], and told them this is something we have to deal with, and nobody did anything about it. | half-true | REAL | numeric_claim, negation, context_dependent, label_boundary_ambiguity | REAL | 0.5020 | 0.4980 | FAKE | 0.8745 | 0.8745 |
| There has never been a panther attack in the history of Florida. | mostly-true | REAL | negation, context_dependent, label_boundary_ambiguity | REAL | 0.6715 | 0.3285 | FAKE | 0.8308 | 0.8308 |
| John McCain has changed position on invading Iraq. | barely-true | FAKE | short_statement, label_boundary_ambiguity | FAKE | 0.7793 | 0.7793 | REAL | 0.7624 | 0.2376 |
| If you look at most of the polls, this is a margin-of-error race on Fourth of July between Mitt Romney and the president. | true | REAL | context_dependent | REAL | 0.5889 | 0.4111 | FAKE | 0.8241 | 0.8241 |
| The Affordable Care Act basically puts a penalty or a tax on employers for every new job they create. | half-true | REAL | context_dependent, label_boundary_ambiguity | REAL | 0.5190 | 0.4810 | FAKE | 0.8156 | 0.8156 |
| All private healthcare plans must conform to government rules to participate in a Healthcare Exchange. | true | REAL | ambiguous_wording | REAL | 0.7201 | 0.2799 | FAKE | 0.8173 | 0.8173 |
| General Motors is the largest corporation in the world again. | false | FAKE | other | FAKE | 0.5319 | 0.5319 | REAL | 0.7902 | 0.2098 |
| China has total control, just about, of North Korea. | barely-true | FAKE | label_boundary_ambiguity | FAKE | 0.5576 | 0.5576 | REAL | 0.8069 | 0.1931 |
| In the 2000 Florida election, at least 1,100 eligible voters were wrongly dropped from voting rolls in an attempt to purge a list of felons. Many of those who were dropped showed up to vote and were told they could not. | true | REAL | numeric_claim, negation, context_dependent, ambiguous_wording | REAL | 0.5331 | 0.4669 | FAKE | 0.8054 | 0.8054 |
| Says Donald Trump and Mike Pence want to gamble with your retirement benefits in the stock market. | barely-true | FAKE | label_boundary_ambiguity, ambiguous_wording | FAKE | 0.7165 | 0.7165 | REAL | 0.8006 | 0.1994 |

## Weighted RoBERTa Correct / Weighted BERT Wrong

| statement | original_6way_label | gold_label | pattern_tags | bert_pred | bert_confidence | bert_prob_fake | roberta_pred | roberta_confidence | roberta_prob_fake |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| If Trump had just put his fathers money in a mutual fund ... hed have $8 billion. | false | FAKE | numeric_claim, context_dependent | REAL | 0.8209 | 0.1791 | FAKE | 0.6686 | 0.6686 |
| Two months ago, Donald Trump said that ISIS was not our fight. | mostly-true | REAL | negation, context_dependent, label_boundary_ambiguity | FAKE | 0.7090 | 0.7090 | REAL | 0.7441 | 0.2559 |
| The (Russian) ruble is already going down. | mostly-true | REAL | short_statement, label_boundary_ambiguity | FAKE | 0.7611 | 0.7611 | REAL | 0.7236 | 0.2764 |
| To this day, (the Cuban government) is a regime that provides safe harbor to terrorists and fugitives. | mostly-true | REAL | context_dependent, label_boundary_ambiguity | FAKE | 0.8162 | 0.8162 | REAL | 0.5147 | 0.4853 |
| Says states mandated tests come from an English company. | mostly-true | REAL | label_boundary_ambiguity, ambiguous_wording | FAKE | 0.8081 | 0.8081 | REAL | 0.6594 | 0.3406 |
| Says Daniel Webster wants to make divorce illegal, even for abused wives. | half-true | REAL | label_boundary_ambiguity, ambiguous_wording | FAKE | 0.7581 | 0.7581 | REAL | 0.5111 | 0.4889 |
| Wind power is the most undependable form of renewable energy. | false | FAKE | other | REAL | 0.5829 | 0.4171 | FAKE | 0.6637 | 0.6637 |
| During Obamas first five years as president, black unemployment increased 42 percent. During Reagans presidency, black unemployment dropped 20 percent. | pants-fire | FAKE | numeric_claim | REAL | 0.8167 | 0.1833 | FAKE | 0.5210 | 0.5210 |
| Barack Obama has provided guns to Mexican drug cartels. | half-true | REAL | label_boundary_ambiguity | FAKE | 0.7969 | 0.7969 | REAL | 0.6449 | 0.3551 |
| Vern Buchanan. His old business was caught illegally funneling over $60,000 in campaign donations to Buchanan to influence his election. | mostly-true | REAL | numeric_claim, context_dependent, label_boundary_ambiguity | FAKE | 0.7561 | 0.7561 | REAL | 0.6655 | 0.3345 |
