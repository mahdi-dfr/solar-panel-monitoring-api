from multiprocessing import Queue, cpu_count, Process

import django.db.utils
import pandas as pd
from django.core.management import BaseCommand

from solar_monitoring_api.settings import BASE_DIR


def do_in_queue(data, q: Queue):
    from solar_monitoring_api.wsgi import get_wsgi_application
    get_wsgi_application()
    from country_division.models import Province, City, County, District, Village

    last_province = None
    last_county = None
    last_city = None
    last_rural_district = None
    last_village = None

    for item in data:
        province = last_province
        if not province:

            try:
                province = Province.objects.filter(title=item[1]).first()
                if not province:
                    province = Province(title=item[1])
                    province.code = f"{str(item[0]).replace('.0', '')}"
                    province.save()
            except django.db.utils.IntegrityError as e:
                province = Province.objects.get(code=f"{str(item[0]).replace('.0', '')}")

            last_province = province

        if isinstance(item[3], str) and item[3].strip() != '':
            item[3] = item[3].strip()
            last_city_is_same = last_city is not None and last_city.title == item[3]
            last_city = city = last_city if last_city_is_same else City.objects.filter(province=province,
                                                                                       code=item[2]).first()

            if not city:
                city = City(title=item[3])
                city.province = province
                city.code = f'{item[2]}'
                city.save()
                last_city = city

            if isinstance(item[5], str) and item[5].strip() != '':
                item[5] = item[5].strip()

                last_county_is_same = last_county is not None and last_county.title == item[5]
                last_county = county = last_county if last_county_is_same else County.objects.filter(city=city,
                                                                                                     code=item[
                                                                                                         4]).first()

                if not county:
                    county = County(title=item[5])
                    county.city = city
                    county.code = f'{item[4]}'
                    county.save()
                    last_county = county

                if isinstance(item[7], str) and item[7].strip() != '':
                    item[7] = item[7].strip()
                    last_rural_district_is_same = last_rural_district is not None and last_rural_district.title == item[
                        7]
                    last_rural_district = rural_district = last_rural_district if last_rural_district_is_same else \
                        District.objects.filter(county=county, code=item[6]).first()

                    if not rural_district:
                        rural_district = District(title=item[7])
                        rural_district.county = county
                        rural_district.code = f'{item[6]}'
                        rural_district.save()
                        last_rural_district = rural_district

                    if isinstance(item[10], str) and item[10].strip() != '':
                        item[10] = item[10].strip()
                        last_village_is_same = last_village is not None and last_village.title == item[10]
                        last_village = village = last_village if last_village_is_same else Village.objects.filter(
                            district=rural_district, code=item[8]).first()

                        if not village:
                            try:
                                village = Village(title=item[10])
                                village.district = rural_district
                                village.code = f'{item[8]}'
                                village.save()
                            except django.db.utils.IntegrityError as e:
                                village = Village(title=item[10] + " _ ")
                                village.district = rural_district
                                village.code = f'{item[8]}'
                                village.save()
                            last_village = village

    print("finished", last_province)
    q.get()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            '--filename',
                            type=str,
                            help='Country Division data file in "DATA" folder with extension like "file1.xlsx"',
                            )

    def handle(self, *args, **options):
        if options['filename']:
            excel_content = pd.read_excel(BASE_DIR / 'DATA' / options['filename'])
            excel_content = excel_content.values.tolist()

            counter = 0

            provinces_map = {}
            q = Queue(maxsize=cpu_count())
            p = []

            for item in excel_content:
                counter += 1
                if item[2] and not item[2] == '':
                    if item[1] not in provinces_map:
                        provinces_map[item[1]] = []
                    provinces_map[item[1]].append(item)

            for value in provinces_map.values():
                proc = Process(target=do_in_queue, args=(value, q))
                proc.start()
                p.append(proc)
                q.put(1, block=True)

            [proc.join() for proc in p]
            print("finished")
        else:
            print('"--filename" is required')
