from emegency.models.carsModel import Cars


class CarDb:

    @staticmethod
    def get_all_records():
        try:
            all_records = list(Cars.objects.all().values())
            print(all_records)
            if len(all_records) > 0:
                return all_records
            else:
                return None
        except Exception as e:
            print(e)