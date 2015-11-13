import datetime

from wtforms.fields import Field
from wtforms.widgets import TextInput


class LunchTimeField(Field):
    widget = TextInput()

    def _value(self):
        return ''

    def process_formdata(self, time_string):
        hours, minutes = time_string[0].split(':')
        meridian = 'AM'
        if len(minutes) > 2:
            minutes, meridian = minutes[:2], minutes[2:].strip()

        hours, minutes = int(hours), int(minutes)

        if meridian == 'PM':
            hours += 12

        self.data = datetime.time(hours, minutes)
