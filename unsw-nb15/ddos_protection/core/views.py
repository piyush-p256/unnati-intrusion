import json
import joblib
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import TrafficLog
from .serializers import TrafficLogSerializer

# Load preprocessing objects + model
model          = joblib.load('core/ml_model/attack_category_model.pkl')
scaler         = joblib.load('core/ml_model/scaler.joblib')
le_proto       = joblib.load('core/ml_model/le_proto.joblib')
le_state       = joblib.load('core/ml_model/le_state.joblib')
le_attack_cat  = joblib.load('core/ml_model/le_attack_cat.joblib')

# Top-30 features used during training
FEATURES = ['dur','proto','state','spkts','dpkts','sbytes','dbytes','rate',
            'sttl','dttl','sload','dload','sloss','dloss','sinpkt','dinpkt',
            'sjit','djit','swin','stcpb','tcprtt','synack','ackdat','smean',
            'dmean','ct_srv_src','ct_state_ttl','ct_src_dport_ltm',
            'ct_dst_sport_ltm','ct_srv_dst']

@csrf_exempt
def attack_endpoint(request):
    # Only POST with JSON body
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    # Build feature vector
    fv = []
    for f in FEATURES:
        v = data.get(f, 0)
        # apply categorical encoding
        if f == 'proto':
            fv.append(le_proto.transform([v])[0])
        elif f == 'state':
            fv.append(le_state.transform([v])[0])
        else:
            fv.append(v)
    # Scale & predict
    fv_scaled = scaler.transform([fv])
    pred_idx  = model.predict(fv_scaled)[0]
    attack_ty = le_attack_cat.inverse_transform([pred_idx])[0]

    # Log it
    is_block = attack_ty != 'Normal'
    log = TrafficLog.objects.create(
        ip_address = request.META.get('REMOTE_ADDR'),
        attack_type = attack_ty,
        blocked    = is_block,
        raw_data   = data
    )

    # Block only non-normal traffic
    if is_block:
        return HttpResponseForbidden(json.dumps({'attack_type': attack_ty}), content_type='application/json')
    return JsonResponse({'attack_type': attack_ty, 'status': 'allowed'})

def dashboard(request):
    return render(request, 'core/dashboard.html')

def get_logs(request):
    logs = TrafficLog.objects.order_by('-timestamp')[:100]
    serializer = TrafficLogSerializer(logs, many=True)
    return JsonResponse(serializer.data, safe=False)

def block_log(request, log_id):
    log = TrafficLog.objects.get(pk=log_id)
    log.blocked = True
    log.save()
    return JsonResponse({'status': 'blocked'})
