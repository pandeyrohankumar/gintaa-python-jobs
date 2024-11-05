from check_date import CheckDate
from scheduler import Schedular

check_date_result = CheckDate.check_date()

if check_date_result:
    minute, hr = check_date_result
    Schedular.update_scheduler(minute, hr)
