from django.core.exceptions import ValidationError
from rest.models import Call, TelephoneBill, CallRecord
from rest_framework import serializers
from datetime import datetime


def validate_phone(value):
    """Validate max e min values of the phone number.

    Keyword arguments:
    value -- phone number to validate
    """
    if len(str(value)) < 10 or len(str(value)) > 11:
        raise ValidationError(
            ('%(value)s size number invalid'),
            params={'value': value},
        )


def validate_type(value):
    """Validate type of the call.

    Keyword arguments:
    value -- call type
    """
    if str(value) != 'start':
        if str(value) != 'end':
            raise ValidationError(
                ('%(value)s call type invalid'),
                params={'value': value},
            )


def validate_period(value):
    """Validate reference period(mount/year).

    Keyword arguments:
    value -- String contains period
    """
    month = value[:2]
    year = value[-4:]

    if len(value) != 7:
        raise ValidationError(
            ('%(value)s invalid date'),
            params={'value': value},
        )

    try:
        datetime(year=int(year), month=int(month), day=1).month
    except:
        raise ValidationError(
            ('%(value)s invalid month'),
            params={'value': value},
        )


class CallSerializer(serializers.Serializer):
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField()
    source = serializers.IntegerField(validators=[validate_phone])
    destination = serializers.IntegerField(validators=[validate_phone])

    def create(self, validated_data):
        return Call.objects.create(**validated_data)


class TelephoneBillSerializer(serializers.Serializer):
    period = serializers.CharField(validators=[validate_period])
    telephone = serializers.IntegerField(validators=[validate_phone])


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField(
        validators=[validate_type], max_length=5, min_length=3)
    timestamp = serializers.DateTimeField()
    source = serializers.IntegerField(
        validators=[validate_phone], default='', required=False)
    destination = serializers.IntegerField(
        validators=[validate_phone], default='', required=False)
