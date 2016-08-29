# -*-  coding: utf-8 -*-
"""Form Modülü

Bu modül `Form` modeli ve bu modelle ilintili data modellerini içerir.

"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from operator import attrgetter

from ulakbus.lib.view_helpers import list_fields_accessor

__author__ = 'H.İbrahim Yılmaz (drlinux)'

from pyoko import Model, field, Node
from .auth import Role, Permission, User


class Form(Model):
    """Form Model sınıfı.

    Bu model, genel kullanım amaçlı olarak sisteme yüklenecek olan formların kayıt edileceği data
    modelidir.

    """
    ad = field.String("Form Adı", index=True)
    file = field.File("File", index=True,
                      random_name=True)  # form eger PDF olarak yulendiyse bu alan kullanilir.
    permissions = Permission()
    date = field.Date("Form Tarihi", index=True, format="%d.%m.%Y")

    class Meta:
        app = 'Form'
        verbose_name = "Form"
        verbose_name_plural = "Formlar"
        list_fields = ['ad', 'date']
        search_fields = ['ad', 'date']

    def __unicode__(self):
        return '%s %s' % (self.ad, self.date)


class FormData(Model):
    """FormData Model sınıfı.

    Bu model, `Form` modelinde kayıtlı olan formlara ait dataların tutulacağı data modelidir.
    Veriler data field'ı içine json serialized olarak kayıt edilmektedir.

    """
    form = Form()
    data = field.Text("Form Data", index=True)  # form datasi json serialized olarak saklanir
    user = User()
    role = Role()
    date = field.Date("Form Data Tarihi", index=True, format="%d.%m.%Y")

    class Meta:
        app = 'Form'
        verbose_name = "Form Data"
        verbose_name_plural = "Form Data"
        list_fields = ['user_full_name', 'form_adi', 'data', 'date']
        search_fields = ['data', 'date']

    form_adi = list_fields_accessor(attrgetter("form.ad"), "Form Adı")
    user_full_name = list_fields_accessor(attrgetter("user.full_name"), "Ad Soyad")

    def _form(self):
        return "%s" % self.form

    def __unicode__(self):
        return '%s %s' % (self.form, self.date)
