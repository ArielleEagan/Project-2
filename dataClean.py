#Import dependencies
import pandas as pd
import requests

#API pull for latest salary info from www.levels.fyi
salaryData = requests.get('https://www.levels.fyi/js/salaryData.json').json()
salary_df = pd.DataFrame(salaryData)

#dropping columns that are not relevant to project
salary_df = salary_df.drop(['cityid', 'dmaid','rowNumber','otherdetails','tag', 'basesalary', 'stockgrantvalue', 'bonus', 'gender'], axis=1)

#converting to float to allow for summary stats
salary_df["totalyearlycompensation"] = pd.to_numeric(salary_df["totalyearlycompensation"])
salary_df["yearsofexperience"] = pd.to_numeric(salary_df["yearsofexperience"])
salary_df["yearsatcompany"] = pd.to_numeric(salary_df["yearsatcompany"])

#coverting timestamp from object to datetime
salary_df['timestamp'] =  pd.to_datetime(salary_df['timestamp'], infer_datetime_format=True)

# Create separate cols for city, state and country
def split_location(location):
    items = location.split(', ')
    city = items[0]
    state = items[1]
    
    if len(items)==2:
        country = 'US'
    elif len(items)==3:
        country = items[2].strip()
    elif len(items)==4:
        country = ', '.join([i.strip() for i in items[2:]])
    else:
        country = None
        print(location)
        
    return [city, state, country]

salary_df['loc_items'] = salary_df.location.apply(lambda x: split_location(x))
salary_df['city'] = salary_df.loc_items.apply(lambda x: x[0])
salary_df['state'] = salary_df.loc_items.apply(lambda x: x[1])
salary_df['country'] = salary_df.loc_items.apply(lambda x: x[2])

# dropping location column  
salary_df = salary_df.drop(['location','loc_items'], axis=1)

#isolating US data for further exploration
us_df = salary_df[salary_df.country=='US'].copy()

#isolating us data to data scientist titles
us_df = us_df[us_df.title=='Data Scientist'].copy()

#apple dataframe
#creating us/datascience/IL at apple dataframe
def apple_clean(us_df):
    apple_df = us_df[us_df.company=='Apple'].copy()

    #correcting level variance with 95% confidence
    corrections = {'IC4': 'ICT4', 'ict5': 'ICT5', 'L3': 'ICT3', 'L4': 'ICT4'}
    apple_df.replace(corrections, inplace=True)

    #dropping single value for e3 and E4 as the salary/stockgrantvalue/bonus are out of allignment with the other levels
    #removed M1 and M2 both software engineer managers
    apple_df = apple_df.drop(index=apple_df[apple_df['level'] == 'e3'].index)
    apple_df = apple_df.drop(index=apple_df[apple_df['level'] == 'E4'].index)
    #removed ICT6 due to high base salary and high stock value as it indictates upper manangement
    apple_df = apple_df.drop(index=apple_df[apple_df['level'] == 'ICT6'].index)
    #removing values outside of 95% confidence
    apple_df = apple_df.drop(index=apple_df[apple_df['level'] == '3'].index)
    apple_df = apple_df.drop(index=apple_df[apple_df['level'] == '4'].index)

    #placing each level in our categories based on similiar: basesalary/yearsofexperience/yearsatcompany/stockgrantvalue/bonus
    apple_df.loc[apple_df.level == "ICT3", "Category"] = "Entry"
    apple_df.loc[apple_df.level == "ICT4", "Category"] = "Mid"
    apple_df.loc[apple_df.level == "ICT5", "Category"] = "Senior"
    return apple_df

#amazon
def amazon_clean(us_df):
    #creating us/datascience/IL at amazon dataframe
    amazon_df = us_df[us_df.company=='Amazon'].copy()

    #correcting level with 95% confidence
    amazon_df.replace('l6', 'L5', inplace=True)

    #removing values outside of 95% confidence
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == '4'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == '5'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'IC5'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'Intern'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'L'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'L 4'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'L1'].index)
    amazon_df = amazon_df.drop(index=amazon_df[amazon_df['level'] == 'L3'].index)

    #placing each level in our categories based on similiar: basesalary/yearsofexperience/yearsatcompany/stockgrantvalue/bonus
    amazon_df.loc[amazon_df.level == "L4", "Category"] = "Entry"
    amazon_df.loc[amazon_df.level == "L5", "Category"] = "Mid"
    amazon_df.loc[amazon_df.level == "L6", "Category"] = "Senior"
    return amazon_df

#facebook
def fb_clean(us_df):
    #exploring us/datascience/IL at amazon
    fb_df = us_df[us_df.company=='Facebook'].copy()

    #correcting level variance with 95% confidence
    corrections = {'6': 'IC6', 'E4': 'IC4', 'E5': 'IC6', 'L3': 'IC3', 'L4': 'IC4', 'L5': 'IC5',
                    'L5 Product Growth Analyst': 'IC5', 'I4': 'IC4' }
    fb_df.replace(corrections, inplace=True)

    #removing values outside of 95% confidence
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == '5'].index)
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == 'E3'].index)
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == 'E6'].index)
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == 'L6'].index)
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == 'M1'].index)
    fb_df = fb_df.drop(index=fb_df[fb_df['level'] == 'M2'].index)    

    #placing each level in our categories based on similiar: basesalary/yearsofexperience/yearsatcompany/stockgrantvalue/bonus
    fb_df.loc[fb_df.level == "IC3", "Category"] = "Entry"
    fb_df.loc[fb_df.level == "IC4", "Category"] = "Entry"
    fb_df.loc[fb_df.level == "IC5", "Category"] = "Mid"
    fb_df.loc[fb_df.level == "IC6", "Category"] = "Senior"

    return fb_df

#google
def google_clean(us_df):
    #exploring us/datascience/IL at amazon
    google_df = us_df[us_df.company=='Google'].copy()

    #correcting level variance with 95% confidence
    google_df.replace('5', 'L5', inplace=True)

    #removing values outside of 95% confidence
    google_df = google_df.drop(index=google_df[google_df['level'] == 'Data'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'L1'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'L2'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'L6'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'L7'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'Product Manager 3'].index)
    google_df = google_df.drop(index=google_df[google_df['level'] == 'T6'].index)

    #placing each level in our categories based on similiar: basesalary/yearsofexperience/yearsatcompany/stockgrantvalue/bonus
    google_df.loc[google_df.level == "L3", "Category"] = "Entry"
    google_df.loc[google_df.level == "L4", "Category"] = "Mid"
    google_df.loc[google_df.level == "L5", "Category"] = "Senior"

    return google_df

#microsoft
def micro_clean(us_df):
    #exploring us/datascience/IL at microsoft
    micro_df = us_df[us_df.company=='Microsoft'].copy()

    #correcting level variance with 95% confidence
    corrections = {'L5': '64', 'L60': '60', 'L61': '64', 'L62': '60', 'L64': '63' }
    micro_df.replace(corrections, inplace=True)

    #removing values for unrelated titles(PEM,PPM,SDE) and high stockvaluegrant likely upper management
    micro_df = micro_df.drop(index=micro_df[micro_df['level'] == '66'].index)
    micro_df = micro_df.drop(index=micro_df[micro_df['level'] == '67'].index)
    micro_df = micro_df.drop(index=micro_df[micro_df['level'] == 'Principal EM'].index)
    micro_df = micro_df.drop(index=micro_df[micro_df['level'] == 'Principal PM'].index)
    micro_df = micro_df.drop(index=micro_df[micro_df['level'] == 'SDE II'].index)

    #placing each level in our categories based on similiar: basesalary/yearsofexperience/yearsatcompany/stockgrantvalue/bonus
    micro_df.loc[micro_df.level == "59", "Category"] = "Entry"
    micro_df.loc[micro_df.level == "60", "Category"] = "Entry"
    micro_df.loc[micro_df.level == "61", "Category"] = "Entry"
    micro_df.loc[micro_df.level == "62", "Category"] = "Mid"
    micro_df.loc[micro_df.level == "63", "Category"] = "Mid"
    micro_df.loc[micro_df.level == "64", "Category"] = "Senior"
    micro_df.loc[micro_df.level == "65", "Category"] = "Senior"

    return micro_df


apple_df = apple_clean(us_df)
amazon_df = amazon_clean(us_df)
fb_df = fb_clean(us_df)
google_df = google_clean(us_df)
micro_df = micro_clean(us_df)

cleaned_data = pd.concat([apple_df, amazon_df])

#import dependency
import pymongo
from pymongo import MongoClient
#establish connection to pymongo
conn ="mongodb://127.0.0.1:27017/"
client = MongoClient(conn)
db = client.ds_salaries
collection = db.top5
cleaned_dict = cleaned_data.to_dict("records")
collection.insert_many(cleaned_dict)