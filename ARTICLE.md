# What India's Classrooms Tell Us: A Data Analyst's Look at the Literacy Gap

*How I used real government education data to ask a simple question — where are we falling behind, and does the story hold up when you check it?*

---

When people talk about India's progress, literacy is usually the headline number everyone reaches for. But a single national figure hides more than it reveals. The average smooths over the fact that a girl in one state and a boy in another can grow up with wildly different odds of finishing school.

So I did what a data analyst does: I stopped looking at the average and started looking at the spread — using real 2015-16 UDISE state-level school census data from India's Ministry of Education.

## The question

I wanted to answer three things, state by state:

1. **Who leads and who lags on literacy?**
2. **How wide is the gender gap** between male and female literacy — and is it its own separate problem, or does it track literacy itself?
3. **Does classroom crowding relate to exam outcomes** — something a state government could actually change?

## What the data showed

**The gap between top and bottom states is roughly 30 percentage points.** Kerala sits at 93.9% literacy; Bihar at 63.8%. That's not a rounding error.

**The gender gap clusters, and it isn't independent of overall literacy.** Rajasthan's gender gap reaches 27.9 points — the widest in the country. But the more interesting finding is the relationship between the two: states with higher overall literacy have meaningfully smaller gender gaps (correlation ≈ -0.74). Literacy gains and gender parity aren't two separate fights; in this data, they move together.

![Higher-literacy states tend to have smaller gender gaps](outputs/03_literacy_vs_gender_gap.png)

**And here's the finding I almost didn't report:** I expected classroom crowding (pupil-teacher ratio) to track exam pass rates — a popular, intuitive claim. It doesn't, at least not in this data (correlation ≈ -0.13, essentially no relationship). It would have been easy to quietly drop this chart or reframe the question until something correlated. I didn't. A null result is still a result, and reporting it honestly is the whole point of doing this analysis for real instead of for show.

![Classroom crowding vs exam pass rate](outputs/04_ptr_vs_pass_rate.png)

## Why this matters beyond the chart

The UN's Sustainable Development Goal 4 — quality education for all — isn't an abstract slogan. It's a checklist a country can be measured against. Literacy and gender parity are exactly the things that goal tracks.

Data analysis is how you turn that checklist from a poster on a wall into a to-do list with names on it. "Improve education" is a wish. "These states have the widest gender gap and it's tightly linked to their overall literacy — start there" is a plan. And "this popular assumption doesn't hold in the data" is just as useful as a plan that confirms one, because it stops someone from spending a policy budget on a lever that this data says isn't the one that's moving.

## How I built it

The whole thing is open source and runs in two commands. It's a clean pandas pipeline: load a real ~630-column government file, clean it down to what matters, derive the metrics that don't come pre-computed (pupil-teacher ratio, exam pass rate), analyze, visualize — with a pytest suite checking every derived number against an independent manual calculation.

👉 **[Link to the GitHub repo]**

## What's next

I'm looking at a newer UDISE+ release to add a second year and build an honest trend (rather than simulate one), and considering a district-level breakdown. If you work in education data or policy, or just care about this — I'd love to hear what questions *you'd* ask of it.

Because the point was never the chart. The point is being willing to report what the data actually says, even when it's a "no."

---

*I'm Ruchir Ganatra, a data analyst focused on education and social-impact data. You can find my work on [GitHub](https://github.com/Ganatra-Ruchir) and my [portfolio](https://ruchirganatra-github-io.vercel.app).*
