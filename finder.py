import re
import os
import datetime


class Finder:
    file_pattern = re.compile(
        r'^(\d{4})(\d{2})(\d{2})_[\s\S]*\.(jpg|jpeg|mov|mp4|dng)$')
    path = None
    greater_than = None
    greater_equal_than = None

    def __init__(self, path):
        self.path = path

    def gt(self, dt):
        self.greater_than = dt
        return self

    def ge(self, dt):
        self.greater_equal_than = dt
        return self

    def scan(self):
        files = os.listdir(self.path)

        for name in files:
            matched = self.file_pattern.match(name)
            if matched:
                year = int(matched.group(1))
                month = int(matched.group(2))
                day = int(matched.group(3))
                date = datetime.datetime(year, month, day)

                # Check for file date.
                if self.greater_than and self.greater_than >= date:
                    continue
                if self.greater_equal_than and self.greater_equal_than > date:
                    continue

                # Make directory name as yyyy-mm-dd.
                dir_name = '{:04d}-{:02d}-{:02d}'.format(year, month, day)
                yield (name, dir_name)
