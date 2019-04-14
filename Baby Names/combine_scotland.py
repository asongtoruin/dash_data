from glob import glob
import re

import pandas as pd

male_by_year = []
female_by_year = []

for f in glob(r'Scotland\*.csv'):
    year_code = int(re.findall(r'\d+', f)[-1])
    if year_code < 100:
        year_code += 2000
    print(year_code)
    male_by_year.append(
        pd.read_csv(f, skiprows=7, encoding='latin-1', usecols=range(1, 3),
                    names=['Name', 'Assigned'])
          .assign(Year=year_code)
          .dropna(how='any', axis=0)
    )
    female_by_year.append(
        pd.read_csv(f, skiprows=7, encoding='latin-1', usecols=range(5, 7),
                    names=['Name', 'Assigned'])
          .assign(Year=year_code)
          .dropna(how='any', axis=0)
    )

all_names = pd.concat(male_by_year).merge(
    pd.concat(female_by_year), on=['Name', 'Year'], how='outer',
    suffixes=(' Male', ' Female')
).sort_values(by='Year')

all_names['Total'] = all_names['Assigned Male'].fillna(0) + all_names['Assigned Female'].fillna(0)

all_names.to_csv('All Names Scotland.csv')

all_names = all_names.groupby('Name').filter(lambda x: x['Total'].sum() > 10)

all_names.to_csv('Filtered Names Scotland.csv', index=False)
