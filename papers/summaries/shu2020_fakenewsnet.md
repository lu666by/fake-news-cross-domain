# Shu et al. (2020) — *FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media*

## 1) Citation
- Kai Shu, Deepak Mahudeswaran, Suhang Wang, Dongwon Lee, Huan Liu. *FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media.* Big Data, 2020. (arXiv:1809.01286)

## 2) One-sentence takeaway
FakeNewsNet is a multi-dimensional fake-news data repository built from PolitiFact and GossipCop fact-checks, providing not only news text but also social-context information (user profiles, posts, replies, network structure) and spatiotemporal information, addressing the limitation that earlier fake-news datasets were either content-only or social-context-only.

## 3) What they propose (simple)
- **A data repository, not a model.** The contribution is the dataset itself, plus its collection pipeline (FakeNewsTracker).
- **Two sub-datasets**, both with binary fake/real labels:
  - **PolitiFact** — political fact-checking news.
  - **GossipCop** — celebrity / entertainment fact-checking.
- **Three feature dimensions for each news piece:**
  1. **News content** — linguistic (article text, headline) and visual (images).
  2. **Social context** — Twitter users posting the news, their replies, likes, retweets, and follower/followee network.
  3. **Spatiotemporal information** — user profile locations, geo-tagged tweets, and timestamps of news pieces and user responses.
- Ground-truth labels come from professional fact-checkers (PolitiFact journalists; GossipCop scoring < 5 = fake; E! Online used as a real-news source for entertainment).

## 4) What they tested
- **Exploratory data analysis** rather than a single benchmark:
  - Word-cloud topic analysis of fake vs real news for both PolitiFact and GossipCop.
  - Distribution of publishers (concentration of fake-news publishers).
  - User account creation date distribution (statistically different between fake-news posters and real-news posters, p < 0.05).
  - Bot-score analysis using Botometer — bots are more likely to post fake news.
- They also report baseline fake-news-detection results on the dataset, although the main contribution is the data repository, not a new model.

## 5) Evidence (beginner level, one example)
- **PolitiFact:** 432 fake + 624 real news articles; ~165K tweets posting these articles; ~95K users involved.
- **GossipCop:** 5,323 fake + 16,817 real news articles; ~520K tweets posting these articles; ~265K users involved.
- The dataset is the **first public fake-news repository** to include news content, social context, and spatiotemporal information together, as shown in their comparison table against BuzzFeedNews, LIAR, BS Detector, CREDBANK, BuzzFace, and FacebookHoax.
- Bot-related signal: a Botometer analysis on 10K random users shows the proportion of bots is higher among fake-news posters than real-news posters.

## 6) Cost / practicality (important for MSc)
- The dataset is publicly available as a GitHub repository (`KaiDMML/FakeNewsNet`), but **only the news content and metadata are directly downloadable**.
- The full social-context data (tweets, user profiles, replies) must be re-collected via the Twitter API by running their crawler. This requires Twitter API access and significant time, and many original tweets/users may now be deleted or suspended.
- For an MSc project, the **practical usable subset is the news-content half** (article text + binary label). Re-collecting the full social-context data is out of scope.
- This makes FakeNewsNet useful as a **second domain** (entertainment via GossipCop, or political articles via PolitiFact) for cross-dataset evaluation against LIAR, even without the social-context features.

## 7) How I will use it in my project (direct mapping)
- FakeNewsNet is one of the candidate **second datasets** for the cross-dataset stage of my project.
- **PolitiFact subset** is the natural pairing with LIAR — both are PolitiFact-based, both are political, but FakeNewsNet uses full articles while LIAR uses short statements. This makes the train-on-LIAR / test-on-FakeNewsNet-PolitiFact direction (and vice versa) a meaningful cross-format generalisation test.
- **GossipCop subset** would represent a clear domain shift (politics → celebrity gossip), useful for a stronger cross-domain test.
- For the literature review, this paper is cited in the **datasets** section to show that the LIAR dataset is one option in a wider landscape, and that more comprehensive multi-modal fake-news datasets exist.

## 8) Risks / notes (simple)
- The dataset is **noisy** by construction — labels come from fact-checking websites whose criteria differ from each other and may change over time.
- **Class balance is uneven**: GossipCop is heavily real-skewed (16,817 real vs 5,323 fake), and PolitiFact is mildly real-skewed (624 vs 432).
- The paper itself does not present a strong fake-news detection model — citing it as a **dataset paper**, not as a method paper, is the correct framing.
- Re-collecting the full repository today is harder than at publication time because of Twitter / X API restrictions, so any thesis use should explicitly state which subset (and which year's snapshot) was used.

## 9) LLM Prompt(s) Used
You are helping me read an academic paper for my MSc thesis.

Task:
1) First, write an overall summary of the paper in 150–250 words (plain English).
2) Then, produce structured notes with sections 1–8 exactly as below.

Sections (1–8):
1) Citation (as given)
2) One-sentence takeaway
3) What they propose (simple)
4) What they tested (datasets/tasks)
5) Key evidence (beginner-level, 2–4 bullets)
6) Cost / practicality for an MSc
7) How I can use this in my project (cross-dataset fake news detection)
8) Risks / notes

Constraints:
- Use ONLY the text I paste below. Do not add outside facts.
- If something is missing, write "Not mentioned".
- Use short bullet points for sections 3–8.
- If you make an inference, clearly label it as "Inference".
- Keep wording simple and clear.
