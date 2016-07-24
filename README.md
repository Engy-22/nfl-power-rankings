# nfl-power-rankings

Statistical formula to calculate weekly NFL power rankings

Breakdown of the latest ranking formula:

* victory value (25%) - teams wins * strength of victory (relative scale of 0 to 100 by the highest upper bound value)

* pythagorean win value (25%) - points scored) / (points scored + points against) * games played (relative scale  of0 to 100 by the highest upper bound value)

* point differential value (25%) - (ppg differential plus/minus average * strength of schedule (relative scale of 0 to 100 by the highest upper bound value)

* win_percentage value (10%) - win percentage (relative scale of 0 to 100 by the highest upper bound value)

* points scored value (5%) — points scored (relative scale of 0 to 100 by the highest upper bound value i.e. league best 28 points equals 100, 21 equals 75, and 14 points equals 50 on the scale)

* points against value (5%) — points against (relative scale of 0 to 100 by the lowest lower bound value i.e. league best 14 points equals 100, 21 equals ~66, and 28 points equals 50 on the scale)

* turnover differential value (5%) - turnover_differential plus/minus (relative scale of -100 to 100 by the lowest lower bound value)

#### Run Locally

e.g. ```python src/main.py 2015 17```
