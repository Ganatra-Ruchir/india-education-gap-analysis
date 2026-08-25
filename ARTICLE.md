# What India's Classrooms Tell Us: A Data Analyst's Look at the Literacy Gap

*How I used public education data to ask a simple question — where are we falling behind, and what can we actually do about it?*

---

When people talk about India's progress, literacy is usually the headline number everyone reaches for. But a single national figure hides more than it reveals. The average smooths over the fact that a girl in one state and a boy in another can grow up with wildly different odds of finishing school.

So I did what a data analyst does: I stopped looking at the average and started looking at the spread.

*(Note: the figures in this piece come from a synthetic sample dataset built to demonstrate the analysis pipeline. Before treating any number as fact, I'm replacing it with official Census, UDISE+, and UNESCO data — and you should too.)*

## The question

I wanted to answer three things, state by state:

1. **Who leads and who lags on literacy?**
2. **How wide is the gender gap** between male and female literacy?
3. **Is there a lever we can pull** on school dropout — something a state government could actually change?

## What the data showed

**The gap between top and bottom states is roughly 20 percentage points.** That's not a rounding error. That's the difference between a state where nearly everyone can read and one where a fifth of adults can't.

**The gender gap clusters.** A handful of states carry a male-female literacy gap above 11 points. Averages hide this completely — you only see it when you split the number in two and look at girls and boys separately.

**And here's the finding I care about most:** the pupil-teacher ratio and the secondary dropout rate move together, with a correlation around 0.89. In plain terms — the more crowded the classroom, the more kids leave school. That's not destiny; it's a policy lever. Hire teachers, shrink class sizes, and the data suggests dropout should ease.

![Crowded classrooms vs dropout](outputs/03_dropout_vs_ptr.png)

## Why this matters beyond the chart

The UN's Sustainable Development Goal 4 — quality education for all — isn't an abstract slogan. It's a checklist a country can be measured against. Literacy, gender parity, and keeping kids in school through secondary are exactly the things that goal tracks.

Data analysis is how you turn that checklist from a poster on a wall into a to-do list with names on it. "Improve education" is a wish. "These five states have the widest gender gap and the most crowded classrooms — start there" is a plan.

## How I built it

The whole thing is open source and runs in three commands. It's a clean pandas pipeline: load, clean, analyse, visualise. I deliberately kept it simple and reusable so anyone learning data analysis can fork it, drop in their own data, and get charts out the other end.

👉 **[Link to the GitHub repo]**

## What's next

I'm swapping the sample data for real Census and UDISE+ figures, adding a district-level breakdown, and building a small dashboard so you can explore it yourself. If you work in education data, policy, or just care about this — I'd love to hear what questions *you'd* ask of it.

Because the point was never the chart. The point is what we decide to do once we can finally see clearly.

---

*I'm Ruchir Ganatra, a data analyst focused on education and social-impact data. You can find my work on [GitHub](https://github.com/Ganatra-Ruchir) and my [portfolio](https://ruchirganatra-github-io.vercel.app).*
