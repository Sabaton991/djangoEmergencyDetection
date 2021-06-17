from django.http import HttpRequest, JsonResponse, HttpResponse
import json
from .process.journalDb import JournalDb
from .process.carDb import CarDb
from .process.barrierDb import BarrierDb
from requests import codes
from .process.cameraDb import CameraDb
import requests
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import time

from .process.timerDb import TimerDb


@require_http_methods(["GET"])
def journal_records(request: HttpRequest):
    if request.method == 'GET':
        data = json.loads(request.body)
        page_n = data["page_number"]
        print(page_n)
        jd = JournalDb()
        a = jd.get_all_records(page_n)
        return JsonResponse(a, safe=False)


@require_http_methods(["GET"])
def last_record(request: HttpRequest):
    if request.method == 'GET':
        jd = JournalDb()
        a = jd.last_record()
        return JsonResponse(a, safe=False, status=codes.OK)


@require_http_methods(["GET"])
def car_list(request: HttpRequest):
    if request.method == 'GET':
        response = CarDb.get_all_records()
        print(type(response))
        if response is not None:
            print('aaaaa')
            return JsonResponse(response, safe=False, status=codes.OK)
        else:
            return JsonResponse({"No data": "No cars"}, status=codes.BAD)


@require_http_methods(["GET"])
def get_all_cameras(request: HttpRequest):
    if request.method == 'GET':
        cm = CameraDb()
        data = request.body
        print(len(data))
        if len(data) == 0:
            cameras = cm.get_all_camera(page_n=None)
            print(len(cameras))
            if cameras is not None:
                return JsonResponse(cameras, safe=False, status=codes.OK)
            else:
                return JsonResponse({"No data": "No cameras"}, status=codes.BAD)
        else:
            json_data = json.loads(data.decode())
            page_n = json_data["page_number"]
            cameras = cm.get_all_camera(page_n)
            print(len(cameras))
            if cameras is not None:
                return JsonResponse(cameras, safe=False, status=codes.OK)
            else:
                return JsonResponse({"No data": "No cameras"}, status=codes.BAD)


@require_http_methods(["GET"])
def option_get(request: HttpRequest):
    if request.method == 'GET':
        cm = CameraDb()
        data = request.body.decode()
        print(data)
        json_data = json.loads(data)
        page_n = json_data["page_number"]
        records = cm.get_all_records(page_n)
        if records is not None:
            return JsonResponse(records, safe=False, status=codes.OK)
        else:
            return JsonResponse({"No data": "No page number"}, status=codes.BAD)


@require_http_methods(["GET"])
def open_barrier(request):
    if request.method == 'GET':
        data = request.body.decode()
        json_data = json.loads(data)
        password = json_data["password"]
        jd = JournalDb()
        cm = CameraDb()
        print(json_data)
        open_url = cm.get_barrier_from_id_camera(json_data["id_camera"])
        if open_url is not None:
            response = requests.get(open_url, json={"password": password})
            if response.status_code == 200:
                if jd.add_record(json_data["id_camera"], json_data["id_car"]):
                    return JsonResponse({"Data": "Created"}, safe=False, status=codes.CREATED)
                else:
                    return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)
            else:
                return JsonResponse({"No data": "Not opened, no pass supplied"}, status=codes.FORBIDDEN)
        else:
            return JsonResponse({"No data": "URL is unreachable"}, status=codes.BAD)


@csrf_exempt
@require_http_methods(["POST"])
def add_all(request):
    if request.method == 'POST':
        cm = CameraDb()
        bd = BarrierDb()
        data = request.body.decode()
        json_data = json.loads(data)
        id_barrier = bd.search_barrier(json_data["url_barrier"])
        print(id_barrier)
        if id_barrier is not None:
            print('A')
            if cm.add_camera(json_data["url_camera"], json_data["description"], id_barrier):
                return JsonResponse({"Data": "Created"}, safe=False, status=codes.CREATED)
            else:
                return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)
        else:
            print('B')
            bd.add_barrier(json_data["url_barrier"])
            id_barrier = bd.search_barrier(json_data["url_barrier"])
            if cm.add_camera(json_data["url_camera"], json_data["description"], id_barrier):
                return JsonResponse({"Data": "Created"}, safe=False, status=codes.CREATED)
            else:
                return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_all(request):
    cm = CameraDb()
    bd = BarrierDb()
    data = json.loads(request.body)
    if cm.get_camera_counts_for_one_barrier(data["id_barrier"]) > 1:
        print('sdadada')
        if cm.del_camera(data["id_camera"]):
            return JsonResponse({"Data": "Deleted"}, safe=False, status=codes.OK)
        else:
            return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)
    else:
        if cm.del_camera(data["id_camera"]):
            if bd.del_barrier(data["id_barrier"]):
                return JsonResponse({"Data": "Deleted"}, safe=False, status=codes.OK)
            else:
                return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)
        else:
            return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)


@csrf_exempt
@require_http_methods(["PUT"])
def upd_all(request):
    cm = CameraDb()
    bd = BarrierDb()
    data = json.loads(request.body)
    id_camera = data.pop('id_camera')
    id_barrier = data.pop('id_barrier')
    barrier = data.pop('url_barrier')
    newBarrier = {"url_barrier": barrier}
    newCamera = {"url_camera": data["url_camera"]}
    if cm.update_camera(id_camera, data) and bd.update_barrier(id_barrier, newBarrier):
        return JsonResponse({"Data": "Updated"}, safe=False, status=codes.OK)
    else:
        return JsonResponse({"No data": "Something wrong with DB"}, status=codes.BAD)


@csrf_exempt
@require_http_methods(["POST"])
def feedback(request):
    data = json.loads(request.body)
    subject, from_to = 'EMERGENCY-CARS', 'support@reliab.tech'
    html_content = '<b>' + data["subject"] + '</b><br><br>' + data["body"]
    msg = EmailMultiAlternatives(subject, from_email=from_to, to=[from_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return JsonResponse({"Data": "Updated"}, safe=False, status=codes.OK)


def test(request):
    for i in range(10):
        start_time = time.time()
        requests.get('http://192.168.199.146:5000/api/v1/barrier/allrec')
        print(f"{(time.time() - start_time) * 1000} миллисекунд")
        print(i)
    return JsonResponse({"Data": "Updated"}, safe=False, status=codes.OK)


def create_records(request):
    for i in range(4500):
        jd = JournalDb()
        jd.add_record(id_camera=33, id_car=5)
        print(i)
    return JsonResponse({"Data": "Updated"}, safe=False, status=codes.OK)


def view_all(request):
    jd = JournalDb()
    a = jd.get_get()
    print(len(a[0]))
    return JsonResponse(a, safe=False, status=codes.OK)


def multiple_filters(request):
    jd = JournalDb()
    json_data = json.loads(request.body)
    page_n = json_data.pop('page_number')
    a = jd.multiple_filters(page_n, json_data)
    return JsonResponse(a, safe=False, status=codes.OK)


@csrf_exempt
@require_http_methods(["PUT"])
def set_timer(request):
    tm = TimerDb()
    json_data = json.loads(request.body)
    id_timer = json_data.pop('id_timer')
    if tm.upd_timer(id_timer, json_data):
        return JsonResponse({"Data": "Updated"}, safe=False, status=codes.OK)
    else:
        return JsonResponse({"Data": "Something wrong with DB"}, safe=False, status=codes.BAD)


@csrf_exempt
@require_http_methods(["GET"])
def get_timer(request):
    tm = TimerDb()
    timer = tm.get_all_records()
    if timer is not None:
        return HttpResponse(json.dumps(timer, default=str), status=codes.OK)
    else:
        return JsonResponse({"Data": "No timer set"}, status=codes.BAD)



