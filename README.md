# F1 Remixed
A Python script that runs through all possible race combinations of the F1 2019-2022 seasons to find out who could have been a champions. Inspired by [this video](https://www.youtube.com/watch?v=jfa5O8sg8g0&t=359s).

The program can sort the results by total championships in all season lengths; by different season lengths; or by driver and season lengths.
For example, sort by Sergio Perez in 2020 and 1 race seasons to see that if the season consisted only of the Sahkir GP, Sergio Perez would be the 2020 champion. Or, look at the breakdown by season length for 2020 and see that any combination of 10 races would result in a Lewis Hamilton title.

Note: In the case of a tie in the standings, the program will randomly select a champion. Additionally, the tiebreaking process only factors in top 10 finishes.

For demonstration purposes, it is recommended to calculate the 2020 season as it has the fewest races and thus the shortest runtime (~30 seconds compared to ~8 minutes for 2019 and ~18 minutes for the others).

### Interesting Findings:
- The hectic 2021 season saw **10 potential winners** (up from 8 in 2020, 6 in 2022, and 5 in 2019)
- Despite not winning any races in the 2022 season, 6th place finisher Lewis Hamilton can win a championship in a **10 race** season whereas 1-time race winner and 4th place overall George Russell can only win in seasons up to **8 races**.
  * Same goes in 2019 where 1-time winner Sebastian Vettel can win a championship in a **9 race** season while 2-time winner Charles Leclerc can only win in seasons up to **8 races**.
- The 2021 season was considered by many to be the best and most competitive season in recent memory and that is backed up by the fact that runner-up Lewis Hamilton can win championships in seasons up to **20 races** (1 off the real season length of 21 races)
  * Coincidentally, in all other seasons analyzed, the actual champion always won in seasons within 8 races of the actual length.
- In 2020, 5th place and the 7th-9th places cannot win championships but the 10th-12th places can (Esteban Ocon, Lance Stroll and Pierre Gasly). This shows how championships are not just a function of how well you perform, but of how your opposition performs in comparison to you.
