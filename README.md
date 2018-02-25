# backend-challenge
Setup instructions:
<br />1) `pip install -r requirements.txt`
<br />2) `source copia-env/bin/activate`

Usage:
<br />Main)`python matchmaker.py --pickups [Pickups.csv] --recipients [Recipients.csv] --matches [Matches.csv]`
<br />Test)`python test_matchmaker.py --pickups [test_pickups.csv] --recipients [test_recipients.csv] --matches [test_matches.csv]`

Formatting:
<br />My solution, matchmaker.py, parses the csv files specified by the parameters and then matches all the eligible recipients for each pickup. Each row of the resulting matches csv is formatted as follows:
<br /> `date,pickup name,[recipient name,recipient distace]...`

For example, the output row corresponding to the pickup for Tommy Thompson on 2016-11-01 is
<br /> `2016-11-01,Tommy Thompson,David Austin,4.18`

meaning that David Austin is Tommy's only available recipient, and he is 4.18 miles away. Pickups with no eligible recipients will appear as
<br />`2016-11-09,Lillian Splawn,None`

and multiple eligible recipients will be sorted by distance, for example
<br />`2016-11-01,Stephen Schwartz,Richard Berkey,1.45,Ricky Harris,3.49,Basil Mendez,4.71`

Notes:
<br />I had a lot of fun designing this solution and would be really excited to work on a more sophisticated version! I considered creating unique IDs for pickups and recipients and probably would for a more scalable solution, but I thought full names were good enough identifiers considering the limited size of the data. Also, I realize sorting eligible recipients by distance is simplistic, and given more time I would have liked to consider other matching criteria such as whether a recipient matched with multiple pickups on the same date.

