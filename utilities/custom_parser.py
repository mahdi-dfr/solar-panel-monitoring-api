from rest_framework.parsers import BaseParser, JSONParser, MultiPartParser, FormParser
from collections import defaultdict
from functools import reduce
from operator import getitem


def remove_list(data):
    newData = CustomCompatibilityDictClass()
    for i in data.keys():
        if '[]' in i:
            newData[i[:-2]] = data.getlist(i)
        else:
            newData[i] = data.get(i)
    return newData


def get_from_dict(dataDict, mapList):
    # Iterate nested dictionary
    return reduce(getitem, mapList, dataDict)


def default_to_regular(d):
    """Convert nested defaultdict to regular dict of dicts."""
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def convert_http_data_to_json(data_to_convert):
    # printing initial dictionary
    each_separate_dict = {}

    for key in data_to_convert.keys():
        a = key.find("[")
        if a > -1:
            b = key[:a]
        else:
            b = "**//" + key

        if b not in each_separate_dict:
            each_separate_dict[b] = {}

        each_separate_dict[b][key] = data_to_convert[key]

    final_dict = {}

    for key in each_separate_dict.keys():

        if key.startswith('**//'):
            final_dict[key[4:]] = each_separate_dict[key]
            continue

        tree = lambda: defaultdict(tree)
        d = tree()

        for k, v in each_separate_dict[key].items():
            *keys, final_key = [i[:-1] for i in k.split('[')]
            get_from_dict(d, keys)[final_key] = v

        final_dict[key] = default_to_regular(d)[""]

    return final_dict


class CustomCompatibilityDictClass(dict):
    """
    برای حل مشکل استفاده از تابع getlist میتوان
    از این کلاس استفاده کرد
    """

    def getlist(self, item_name: str):
        try:
            if item_name.endswith('[]'):
                return self.__getitem__(item_name[:-2])
            return self.__getitem__(item_name)
        except KeyError:
            return None


class CustomParser(BaseParser):
    """
    این کلاس برای پارس و از بین بردن براکت های
    موجود در داده های ارسالی است
    """

    def parse(self, stream, media_type=None, parser_context=None):

        data = None

        if 'application/json' in media_type:
            data = JSONParser().parse(stream, media_type, parser_context)
            data = remove_list(data)
        elif 'application/x-www-form-urlencoded' in media_type:
            data = FormParser().parse(stream, media_type, parser_context)
            data = remove_list(data)
        elif 'multipart/form-data' in media_type:
            data = MultiPartParser().parse(stream, media_type, parser_context)
            data.data = remove_list(data.data)
            data.files = remove_list(data.files)

        return data


class CustomJsonParser(CustomParser):
    """
    برای پارس داده های جیسونی استفاده میشود
    """
    media_type = 'application/json'


class CustomFormParser(CustomParser):
    """
    برای پارس داده هایی که بشکل فرم برای سرور ارسال
    میشوند و ممکن است که داده های لیستی داشته باشند
    """
    media_type = 'application/x-www-form-urlencoded'


class CustomMultiPartParser(CustomParser):
    """
    برای پارس کردن داده هایی که بشکل فرم برای سرور
    ارسال میشوند و ممکن است که داده های لیستی داشته باشند
    """
    media_type = 'multipart/form-data'
