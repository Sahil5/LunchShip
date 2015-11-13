import datetime

from wtforms.fields import Field
from wtforms.widgets import Input


class LunchTimeField(Field):
    widget = Input(input_type='time')

    def _value(self):
        return ''

    def process_formdata(self, time_string):
        hours, minutes = time_string[0].split(':')

        meridian = None

        if len(minutes) > 2:
            minutes, meridian = minutes[:2], minutes[2:].strip()

        hours, minutes = int(hours), int(minutes)

        if meridian is None:
            now = datetime.datetime.now()
            current_hour = now.hour
            current_minute = now.minute
            if current_hour < hours or (current_hour == hours and current_minute < minutes):
                meridian = 'AM'
            else:
                meridian = 'PM'

        if meridian == 'PM':
            hours += 12

        self.data = datetime.time(hours, minutes)
