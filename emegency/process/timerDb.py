from emegency.models.timerModel import Timer


class TimerDb:

    @staticmethod
    def get_all_records():
        try:
            all_records = list(Timer.objects.all().
                               values('id_timer', 'barrier_timer', 'alert_timer'))
            print(list(all_records))
            if len(all_records) > 0:
                return all_records
            else:
                return None
        except Exception as e:
            print(e)

    @staticmethod
    def add_timer(barrier_timer, alert_timer):
        try:
            new_timer = Timer.objects.create(barrier_timer=barrier_timer, alert_timer=alert_timer)
            new_timer.save()
            return True
        except Exception as err:
            print(err)
            return False

    @staticmethod
    def del_timer(id_timer):
        try:
            Timer.objects.filter(id_timer=id_timer).delete()
            return True
        except Exception as err:
            print(err)
            return False

    @staticmethod
    def upd_timer(id_timer, fetched_data):
        try:
            Timer.objects.filter(id_timer=id_timer).update(**fetched_data)
            return True
        except Exception as err:
            print(err)
            return False