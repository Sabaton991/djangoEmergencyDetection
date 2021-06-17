from emegency.models.barrierModel import Barrier
from django.db.transaction import commit, rollback


class BarrierDb:

    def add_barrier(self, url_barrier):
        if url_barrier is not None:
            try:
                Barrier.objects.create(url_barrier=url_barrier)
                commit()
                return True
            except Exception as err:
                print(err)
                rollback()
                return False

    def del_barrier(self, id_barrier):
        if id_barrier is not None:
            try:
                Barrier.objects.filter(id_barrier=id_barrier).delete()
                commit()
                return True
            except Exception as err:
                rollback()
                print(err)
                return False

    def update_barrier(self, id_barrier, fetched_data):
        if id_barrier and fetched_data is not None:
            try:
                Barrier.objects.filter(id_barrier=id_barrier).update(**fetched_data)
                commit()
                return True
            except Exception as err:
                rollback()
                print(err)
                return False

    def search_barrier(self, url_barrier):
        oneBarrier = None
        if url_barrier is not None:
            oneBarrier = Barrier.objects.values('id_barrier').filter(url_barrier=url_barrier).first()
        if oneBarrier is not None:
            return oneBarrier['id_barrier']
        else:
            return None