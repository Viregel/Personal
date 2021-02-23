#Covid Model

import pandas as pd
import datetime as dt

data_range = 150
vaccination_rate = 0.005 # Underestimate of the current rate; closer to 0.007
unvaccinated_pop = 0.73 # Rough vaccination rate as of today
R_base = 6 # Base spread of new variant (likely a gross overestimate; roughly 4.5 in reality)
mitigation_factor = 0.18 # Current mitigation factor (rough)
reopening_dates = [dt.date(2021, 3, 8), dt.date(2021, 3, 29), dt.date(2021, 4, 12), dt.date(2021, 5, 17), dt.date(2021, 6, 21)]
R_mitigation = [0.2, 0.3, 0.5, 0.8, 1.0] # Levels of mitigation at associated dates
vaccine_mitigation = 0.26 # Actually 1 - mitigation of the vaccine
initial_cases = 8000 # Rough cases as of today
cases_over_time = []
start_date = dt.date.today()
time_range = pd.date_range(start_date, periods=data_range).tolist()

cases_over_time.append(initial_cases)

for i in range (0, data_range-1):
    for d in reopening_dates:
        if d <= time_range[i]:
            mitigation_factor = R_mitigation[reopening_dates.index(d)]
    last_case = len(cases_over_time) - 1
    unvaccinated_pop -= vaccination_rate
    if(unvaccinated_pop < 0):
        unvaccinated_pop = 0
    new_cases = (cases_over_time[last_case])*(mitigation_factor*(R_base)*(unvaccinated_pop + (vaccine_mitigation*(1-unvaccinated_pop))))
    if new_cases <= 100: # Trends towards zero new cases once cases are arbitrarily low
        new_cases = new_cases * 0.5
    cases_over_time.append(round(new_cases))
    
df1 = pd.DataFrame({'Covid Cases': cases_over_time}, index=time_range)

lines = df1.plot.line(title="Lockdown Model")