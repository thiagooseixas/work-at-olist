from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest.serializers import CallSerializer, TelephoneBillSerializer, CallRecordSerializer
from rest.models import Call
from datetime import datetime, timedelta, date, time


class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all().order_by('-started_at')
    serializer_class = CallSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def price_rule(start, end):
    standing_charge = 0.36
    call_charge = 0.09

    total_minutes = int((end - start).total_seconds()/60)

    if start.time() >= time(hour=6) and end.time() <= time(hour=22):
        print('Standard')
        total = float(
            str((total_minutes * call_charge) + standing_charge)[0:5])
        print(total)
    else:
        print('Reduced')
        total = float(
            str((total_minutes * call_charge) + standing_charge)[0:5])

    return total


@api_view(['POST'])
def save_call(request):
    """
    docstring here
        :param request: 
    """
    if request.method == 'POST':
        serializer = CallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_telephone_bill(request):
    """
    docstring here
        :param request: 
    """
    if request.method == 'POST':

        data = JSONParser().parse(request)
        serializer = TelephoneBillSerializer(data=data)

        if serializer.is_valid():
            if 'reference_period' in data:
                month = data['reference_period'][:2]
                year = data['reference_period'][-4:]

                call = Call.objects.filter(
                    source=data['telephone'],
                    started_at__month=month,
                    started_at__year=year).values()

            call = Call.objects.filter(source=data['telephone'])\
                .order_by('started_at')[:1].values()

            item = list(call)[0]

            call = Call.objects.filter(
                source=data['telephone'],
                started_at__month=item['started_at'].month,
                started_at__year=item['started_at'].year).values()

            price = price_rule(item['started_at'], item['ended_at'])
            hours = str(item['ended_at'].hour - item['started_at'].hour)
            minutes = str(item['ended_at'].minute - item['started_at'].minute)
            seconds = str(item['ended_at'].second - item['started_at'].second)

            result = {
                "destination": item['destination'],
                "call_start_date": item['started_at'],
                "call_start_time": item['ended_at'],
                "call_duration": hours+'h'+minutes+'m'+seconds+'s',
                "call_price": "R$ " + str(price)
            }

            return JSONResponse(result, status=201)

        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def call_record(request):
    """
    docstring here
        :param request: 
    """
    print('call start')
    data = JSONParser().parse(request)
    serializer = CallRecordSerializer(data=data, many=True)

    print('data', data)
    if serializer.is_valid():
        print('valid')
        # for data in request:
        #    print(data)

        result = {
            "destination": "teste"
        }
        return JSONResponse(result, status=201)
    else:
        print('not valid')
        return JSONResponse(serializer.errors, status=400)
