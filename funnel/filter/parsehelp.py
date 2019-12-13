import re
from datetime import datetime

class ParseHelp:
    def to_pydate(date):
        months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, 
                      Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
        match = re.search(r'\d\d+ [a-zA-Z]{3} (19|20)\d\d (\d\d(.|$))*', date)
        if match:
            pieces = match.group().split()
            pieces.extend(pieces.pop(-1).split(':'))
            pieces[1] = months[pieces[1]]
            tmp = pieces[0]
            pieces[0] = pieces[2]
            pieces[2] = tmp
            pieces = [int(x) for x in pieces]

            return datetime(*pieces)
        else:
            pieces = date.split('Z')
            return datetime.fromisoformat(pieces[0])
