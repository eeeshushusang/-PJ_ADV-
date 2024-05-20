from django.db import models
from decimal import Decimal, InvalidOperation


class CompositeValue:
    def __init__(self, decimal_part, char_part):
        try:
            self.decimal_part = Decimal(decimal_part).quantize(Decimal('0.00'))
            if len(str(self.decimal_part)) > 5:
                raise ValueError("Decimal part cannot exceed 5 digits in total.")
        except InvalidOperation:
            raise ValueError("Invalid decimal value.")

        self.char_part = str(char_part)
        if len(self.char_part) > 20:
            raise ValueError("Char part cannot exceed 20 characters.")

    def __str__(self):
        return f"{self.decimal_part}:{self.char_part}"

    @classmethod
    def from_db_value(cls, value):
        if value is None:
            return None
        parts = value.split(':')
        if len(parts) != 2:
            raise ValueError("Invalid storage format.")
        return cls(*parts)


class CompositeField(models.Field):
    def get_internal_type(self):
        return 'CharField'

    def db_type(self, connection):
        return 'varchar(100)'  # Adjust size as needed

    def from_db_value(self, value, expression, connection):
        return CompositeValue.from_db_value(value)

    def to_python(self, value):
        if isinstance(value, CompositeValue) or value is None:
            return value
        return CompositeValue.from_db_value(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not (0 <= value.decimal_part <= 10):
            raise ValueError("Decimal value must be between 0 and 10.")
