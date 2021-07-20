from django.db.models.sql import OR
from emegency.models.journalModel import Journal
from emegency.models.cameraModel import Camera
from emegency.models.carsModel import Cars
from django.db.models import F
from django.db.models import Q
import math
import datetime
from django.db.transaction import commit, rollback


class JournalDb:

    @staticmethod
    def get_all_records(page_n):
        if page_n is not None:
            print(page_n)
            page_n -= 1
            try:
                all_record = Journal.objects.order_by('-opened_at').select_related('id_camera')[page_n*11:(11+(page_n*11))]
                rows = Journal.objects.count()
                print(rows)
                number_of_pages = {"number_of_pages": math.ceil(rows/11)}
                result = all_record.values('opened_at', 'id_car', 'id_camera', url_camera=F('id_camera__url_camera'),
                                           car_description=F('id_car__description'),
                                           camera_description=F('id_camera__description'))
                print(result)
                list_result = [
                    {"date": journal['opened_at'].strftime("%d-%m-%Y"),
                     "time": journal['opened_at'].strftime("%H:%M:%S"),
                     "id_camera": journal['id_camera'],
                     "camera_description": journal['camera_description'],
                     "car_description": journal['car_description'],
                     "url_camera": journal['url_camera']} for journal in result]
                print(list_result)
                return list_result, number_of_pages
            except Exception as e:
                print(e)
        else:
            return None

    @staticmethod
    def get_get():
        try:
            all_record = Journal.objects.order_by('-opened_at').select_related('id_camera', 'id_car').all()
            rows = Journal.objects.count()
            # print(rows)
            number_of_pages = {"number_of_pages": math.ceil(rows / 11)}
            result = list(all_record.values('opened_at', 'id_car', 'id_camera', url_camera=F('id_camera__url_camera'),
                                       car_description=F('id_car__description'),
                                       camera_description=F('id_camera__description')))
            return result, number_of_pages
        except Exception as e:
            print(e)

    @staticmethod
    def aa(data):
        print('2121')
        print(data)
        filters1 = {1: Q(id_car=data['list_filters'][0]),
                    2: Q(id_car=data['list_filters'][0]) | Q(id_car=data['list_filters'][1]),
                    3: Q(id_car=data['list_filters'][0]) | Q(id_car=data['list_filters'][1]) | Q(id_car=data['list_filters'][2]),
                    4: Q(id_car__gte=1)}
        a = filters1.get(len(data['list_filters']))
        print(a)

    @staticmethod
    def one_filter(data):
        return Q(id_car=data['list_filters'][0])

    @staticmethod
    def three_filter(data):
        return Q(id_car=data['list_filters'][0]) | Q(id_car=data['list_filters'][1]) | Q(
                                id_car=data['list_filters'][2])

    @staticmethod
    def two_filter(data):
        return Q(id_car=data['list_filters'][0]) | Q(id_car=data['list_filters'][1])

    @staticmethod
    def four_filter():
        return Q(id_car__gte=1)

    def multiple_filters(self, page_n, data):
        if page_n is not None:
            page_n -= 1
            try:
                print(len(data))
                filters1 = {1: self.one_filter,
                            2: self.two_filter,
                            3: self.three_filter,
                            4: self.four_filter}
                selection = filters1.get(len(data['list_filters']))(data)
                print(selection)
                filter_records = Journal.objects.filter(selection).order_by('-opened_at').select_related('id_camera', 'id_car')\
                    .values('opened_at', 'id_car', 'id_camera', url_camera=F('id_camera__url_camera'),
                                       car_description=F('id_car__description'),
                                       camera_description=F('id_camera__description'))[page_n*11:(11+(page_n*11))]
                rows = Journal.objects.filter(selection).count()
                number_of_pages = {"number_of_pages": math.ceil(rows / 11)}
                print(filter_records)
                if len(filter_records) > 0:
                    print(len(filter_records))
                    return list(filter_records), number_of_pages
                else:
                    return None
            except Exception as e:
                print(e)

    @staticmethod
    def last_record():
        last = None
        try:
            last_record = Journal.objects.order_by('-id_journal')[:1]
            last = last_record.values('opened_at', 'id_car', 'id_camera')[0]
        except Exception as e:
            print(e)
        if last is not None:
            return last
        else:
            return []

    def add_record(self, id_camera, id_car):
        if id_camera is not None:
            try:
                Journal.objects.create(id_camera=Camera.objects.get(id_camera=id_camera),
                                       id_car=Cars.objects.get(id_car=id_car), opened_at=datetime.datetime.now())
                return True
            except Exception as err:
                print(err)
                return False