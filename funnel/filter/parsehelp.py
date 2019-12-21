import re
from datetime import datetime

class ParseHelp:
    def to_pydate(date):
        months = dict(Jan=1, January=1, Feb=2, February=2, Mar=3, March=3, Apr=4, April=4, 
                      May=5, Jun=6, June=6, Jul=7, July=7, Aug=8, August=8, Sep=9, September=9,
                      Oct=10, October=10, Nov=11, November=11, Dec=12, December=12)
        match = re.search(r'\d\d+ [a-zA-Z]+ (19|20)\d\d (\d\d(.|$))*', date)
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
