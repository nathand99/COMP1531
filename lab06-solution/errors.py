from datetime import datetime

class BookingError(Exception):

    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Booking validation error occurred with fields: %s"%(', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


def check_booking_error(start_date, end_date, start_location, end_location):
    errors = {}

    date_format = "%Y-%m-%d"
    start = None
    end   = None

    try:
        start = datetime.strptime(start_date, date_format)
    except:
        errors['start_date'] = "Specify a valid start date"

    try:
        end = datetime.strptime(end_date, date_format)
    except:
        errors['end_date'] = "Specify a valid end date"

    if start_location == '':
        errors['start_location'] = "Specify a valid start location"

    if end_location == '':
        errors['end_location'] = "Specify a valid end location"

    if start and end:
        if (end - start).days < 0: # assume 1-day car rent possible
            errors['period'] = "Specify a valid booking period"
    
    if errors:
        raise BookingError(errors)