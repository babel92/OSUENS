from django.shortcuts import render
from django.core import serializers
from django.utils import timezone
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Entry
from django.views.decorators.csrf import csrf_exempt
import sys
sys.path.append('..')
from mailhandler import addrToMarkerScript

# Create your views here.
def get(request):
    data=[model_to_dict(e) for e in Entry.objects.all()]
    for e in data:
        e['emergency_type']=Entry.ET_DICT[e['emergency_type']]

    #res=serializers.serialize("json",data)
    return JsonResponse(data,safe=False)

@csrf_exempt
def add(request):
    if request.method == 'POST':
        ret={}
        address=request.POST.get('address','')
        emergency_type=request.POST.get('emergency_type','CR')
        image_url=request.POST.get('image_url','')
        marker_script=request.POST.get('marker_script','')
        optional_info=request.POST.get('optional_info','')
        original_email=request.POST.get('original_email','')
        suspect_name=request.POST.get('suspect_name','')
        suspect_traits=request.POST.get('suspect_traits','')
        time=request.POST.get('time','')
        n = Entry(submit_time=timezone.now(),
        address=address,
        emergency_type=emergency_type,
        image_url=image_url,
        marker_script=marker_script,
        optional_info=optional_info,
        original_email=original_email,
        suspect_name=suspect_name,
        suspect_traits=suspect_traits,
        time=time)
        n.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('Only supports POST method')

def geo(request):
    return HttpResponse(addrToMarkerScript(request.GET['addr']))
