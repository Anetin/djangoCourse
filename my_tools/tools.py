# _*_ coding:utf-8 _*_
import decimal

__author__ = "devin"
__date__ = "2018/5/14 22:32"

import json
from django.http import HttpResponse
from datetime import date, datetime
import decimal

def getResultCode(data, status=1, msg="成功", msg_level=1):
    """返回 结果 json 要求的字典"""
    '''data 是 list
    返回参数status 默认1，#0-失败，1-成功，2-部分成功
    msg 默认 成功
    msg_level 默认为1，# 信息展示级别：1-成功，2-询问，3-警告，4-错误
    '''
    return HttpResponse(json.dumps({
        "status":status,
        "msg":msg,
        "data":data,
        "msg_level":msg_level
    }), content_type="application/json")


# ModelForms #################################################################

def my_model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.
    """
    # avoid a circular import
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        # if not f.editable:
        #     continue
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primary key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            value = f.value_from_object(instance)
            if isinstance(value, decimal.Decimal) or isinstance(value, datetime) or isinstance(value, date):
                value_str = str(value)
                data[f.name] = value_str
            else:
                data[f.name] = f.value_from_object(instance)
    return data