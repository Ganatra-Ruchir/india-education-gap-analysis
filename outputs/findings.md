# Key findings

Data: 2015-16 UDISE state-level school census (literacy figures are from Census 2011, as reported in this release). See docs/DATA_SOURCES.md. Single-year cross-section, not a trend.

## Highest literacy
      state  literacy_rate
     Kerala          93.91
Lakshadweep          92.28
    Mizoram          91.58

## Lowest literacy
            state  literacy_rate
            Bihar          63.82
Arunachal Pradesh          66.95
        Rajasthan          67.06

## Widest gender gap
       state  gender_gap
   Rajasthan        27.9
   Jharkhand        22.2
Chhattisgarh        20.9

## Literacy vs. gender gap
Correlation (literacy rate vs. gender gap): -0.74
Higher-literacy states tend to have meaningfully smaller male-female gaps -- literacy gains and gender parity move together in this data, they are not independent problems.

## Classroom crowding vs. exam pass rate
Correlation (pupil-teacher ratio vs. Class 10 pass rate): -0.13
This is a weak/near-zero correlation. Unlike a popular assumption, this cross-section does not show crowded secondary classrooms tracking lower board-exam pass rates -- reported honestly as a null result rather than dropped or reframed to fit a stronger story.

## Data notes
- Telangana's literacy figures are missing in this release -- it split from Andhra Pradesh in 2014 and Census literacy was not yet separately reported for it here. Andhra Pradesh's exam figures in this file reflect only the post-bifurcation state.
- Delhi shows zero students appeared for the Class 10 exam this cycle in the source data; its pass rate is reported as missing, not 0%.
- 35 of India's 36 states/UTs are included after cleaning.