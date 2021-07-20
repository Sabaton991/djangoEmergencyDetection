from emegency.models.cameraModel import Camera
from emegency.models.barrierModel import Barrier
from django.db.models import F
import math
from django.db.transaction import commit, rollback


class CameraDb:

    @staticmethod
    def get_all_camera(page_n):
        if page_n is None:
            cameras = list(Camera.objects.all().order_by('id_camera').values('id_camera', 'url_camera',
                                                                             camera_description=F('description')))
            print(cameras)
            if len(cameras) > 0:
                return cameras
            else:
                return None
        else:
            page_n -= 1
            cameras = list(Camera.objects.order_by('id_camera').values('id_camera', 'url_camera',
                                                                       camera_description=F('description'))[page_n*11:(11+(page_n*11))])
            print(cameras)
            rows = Camera.objects.count()
            print(rows)
            number_of_pages = {"number_of_pages": math.ceil(rows/11)}
            if len(cameras) > 0:
                return cameras, number_of_pages
            else:
                return None

    @staticmethod
    def get_all_records(page_n):
        if page_n is not None:
            print(page_n)
            page_n -= 1
            try:
                all_record = list(Camera.objects.order_by('id_camera').select_related('id_barrier')
                                 .values('id_camera', 'url_camera', 'id_barrier', url_barrier=F('id_barrier__url_barrier'),
                                         camera_description=F('description'),
                                         barrier_description=F('id_barrier__name'))[page_n*10:(10+(page_n*10))])
                rows = Camera.objects.filter(id_barrier__isnull=False).count()
                number_of_pages = {"number_of_pages": math.ceil(rows/10)}
                if len(all_record) > 0:
                    return all_record, number_of_pages
                else:
                    return None
            except Exception as e:
                print(e)
                return False
        else:
            return None

    @staticmethod
    def get_barrier_from_id_camera(id_camera):
        barrier = Camera.objects.filter(id_camera=id_camera).select_related('id_barrier').values(url_barrier=F('id_barrier__url_barrier'))[0]
        print(barrier)
        return barrier["url_barrier"]

    def add_camera(self, url_camera, description, id_barrier):
        if url_camera is not None:
            try:
                Camera.objects.create(url_camera=url_camera, id_barrier=Barrier.objects.get(id_barrier=id_barrier),
                                      description=description)
                return True
            except Exception as err:
                print(err)
                return False

    def get_camera_counts_for_one_barrier(self, id_barrier):
        camera_count = Camera.objects.filter(id_barrier__id_barrier=id_barrier).select_related('id_barrier').count()
        print(camera_count)
        return camera_count

    def del_camera(self, id_camera):
        if id_camera is not None:
            try:
                Camera.objects.filter(id_camera=id_camera).delete()
                return True
            except Exception as err:
                rollback()
                print(err)
                return False

    def update_camera(self, id_camera, fetched_data):
        if id_camera and fetched_data is not None:
            try:
                Camera.objects.filter(id_camera=id_camera).update(**fetched_data)
                return True
            except Exception as err:
                print(err)
                return False