

from transform.base import TransformPlugin


class DateTimeTransform(TransformPlugin):
    name = "datetime"

    def apply(self, value, **kwargs):
        from datetime import datetime
        # Assuming the input value is a string representation of a date and time
        try:
            dt = datetime.fromisoformat(value)
            return dt
        except ValueError:
            raise ValueError(f"Invalid datetime format: {value}")