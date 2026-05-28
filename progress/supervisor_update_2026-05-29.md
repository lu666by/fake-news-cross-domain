# Supervisor Update - 2026-05-29

Subject: Weekly update before our next meeting

Dear Dr. Griffith,

I wanted to send a short update before our next meeting.

This week I completed the cross-dataset stage and updated the dissertation draft. The main result is that strict direct transfer from LIAR to FakeNewsNet titles fails badly, but intermediate target-domain fine-tuning gives a much clearer recovery result.

The current interpretation is:

- The LIAR in-domain baseline is reasonable, with weighted RoBERTa giving the strongest overall local result.
- When the LIAR-trained transformer is tested directly on FakeNewsNet titles, performance drops sharply and the model becomes strongly biased toward predicting FAKE.
- A matched unweighted BERT control suggests this is mainly a dataset-shift problem, not only caused by the class-weighted loss.
- Intermediate fine-tuning on a small amount of FakeNewsNet target-domain training data substantially improves the held-out target test result. The best current setting is 20% target-domain fine-tuning, with Macro-F1 0.7447 on the held-out FakeNewsNet test split.
- I also added a small TELLER-like reasoning-atoms pilot, but I am treating it only as exploratory supporting analysis, not as a full TELLER reproduction or a main contribution.

Files worth looking at before the meeting:

- `thesis_writeup/dissertation_final.pdf`
- `results/integrated_experiment_summary/integrated_main_results_table.md`
- `progress/supervisor_meeting_talking_points_2026-05-29.md`

The main points I would like to discuss are:

1. Whether the current framing is strong enough: reproducible baselines -> strict transfer failure -> target-domain fine-tuning recovery.
2. Whether I should repeat the 10% and 20% intermediate fine-tuning settings across more seeds.
3. Whether the TELLER-like pilot should stay in the main chapter or be shortened/moved to appendix.

Best regards,
Boyu
