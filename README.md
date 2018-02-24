# backend-challenge
Match customer pickup requests with non-profit recipients

Setup instructions:
<br />1) `pip install -r requirements.txt`
<br />2) `source copia-env/bin/activate`

Usage:
<br />`python matchmaker.py --pickups [Pickups.csv] --recipients [Recipients.csv] --matches [Matches.csv]`
<br />`python test_matchmaker.py --pickups [test_pickups.csv] --recipients [test_recipients.csv] --matches [test_matches.csv]`

My solution, matchmaker.py, parses the csv files specified by the parameters and then matches all the eligible recipients for each pickup. Each row of the reulting matches csv is formatted as follows:
<br />1) `date, pickup name, [recipient name, recipient distace]...`

For example, the output row corresponding to the pickup for Tommy Thompson on 2016-11-01 is:
<br />1) `2016-11-01, Tommy Thompson, David Austin, 4.18`

Meaning that...
