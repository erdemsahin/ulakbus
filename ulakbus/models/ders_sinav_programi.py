# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from operator import attrgetter

from pyoko import Model, field, ListNode
from ulakbus.lib.date_time_helper import GUN_DILIMI, HAFTA
from ulakbus.lib.view_helpers import list_fields_accessor
from ulakbus.models import RoomType, Okutman, Sube, Donem, Unit, Ders, Room
from ulakbus.models.ogrenci import Donem
from zengine.forms import fields
from .buildings_rooms import Room
from .auth import Unit
from .ogrenci import Okutman

UYGUNLUK_DURUMU = [
    (1, "Uygun"),
    (2, "Mümkünse Uygun Değil"),
    (3, "Kesinlikle Uygun Değil")
]
DERSLIK_DURUMU = [
    (1, 'Herkese Açık'),
    (2, 'Bölüme Ait'),
    (3, 'Herkese Kapalı')
]


class ZamanDilimleri(Model):
    class Meta:
        unique_together = [('birim', 'gun_dilimi')]
        search_fields = ['gun_dilimi']
        verbose_name_plural = "Zaman Dilimleri"
        list_fields = ['gun_dilimi', 'baslama_saat', 'baslama_dakika', 'bitis_saat', 'bitis_dakika']

    birim = Unit('Bölüm')
    gun_dilimi = field.Integer('Gün Dilimi', choices=GUN_DILIMI, index=True)

    baslama_saat = field.String("Başlama Saati", index=True)
    baslama_dakika = field.String("Başlama Dakikası", index=True)

    bitis_saat = field.String("Bitiş Saati", index=True)
    bitis_dakika = field.String("Bitiş Dakikası", index=True)

    # Ara suresi de dahil. Ornek olarak 30 girildiyse ders 9, 9.30, 10 gibi surelerde baslayabilir.
    ders_araligi = field.Integer('Ders Süresi', default=60, index=True)
    ara_suresi = field.Integer('Tenefüs Süresi', default=10, index=True)

    zaman_dilimi_suresi = field.Integer("Zaman Dilimi Süresi", index=True)

    def pre_save(self):
        self.zaman_dilimi_suresi = int(self.bitis_saat) - int(self.baslama_saat)

    def __unicode__(self):
        return '%s - %s:%s|%s:%s' % (dict(GUN_DILIMI)[int(self.gun_dilimi)], self.baslama_saat,
                                     self.baslama_dakika, self.bitis_saat, self.bitis_dakika)


class OgElemaniZamanPlani(Model):
    """
        Okutman, birim ve okutmanin ilgili birimde verecegi  haftalik ders saati bilgisi tutulur.
    """

    class Meta:
        verbose_name = 'Öğretim Elemanı Zaman Kaydı'
        verbose_name_plural = 'Öğretim Elemanı Zaman Kayıtları'
        unique_together = [('okutman', 'birim')]
        list_fields = ['okutman_adi', 'birim_adi', 'toplam_ders_saati']

    okutman = Okutman("Öğretim Elemanı")
    birim = Unit("Birim")
    toplam_ders_saati = field.Integer("Öğretim Elemanı Toplam Ders Saati", index=True)

    okutman_adi = list_fields_accessor(attrgetter("okutman"), "Okutman")
    birim_adi = list_fields_accessor(attrgetter("birim.name"), "Birim")

    def __unicode__(self):
        return '%s - %s' % (self.birim, self.okutman)


class ZamanCetveli(Model):
    """
        Ilgili birime ait belirlenen zaman dilimleri ders program koordinatoru tarafindan
        ogretim elemanlarin saat araliklarina gore durumlarini belirleyecegi model
    """

    class Meta:
        verbose_name = 'Zaman Cetveli'
        verbose_name_plural = "Zaman Cetvelleri"
        unique_together = [('zaman_dilimi', 'ogretim_elemani_zaman_plani', 'gun')]
        search_fields = ['gun', 'durum']
        list_fields = ['_zaman_dilimi', '_ogretim_elemani_zaman_plani', 'gun', 'durum']

    birim = Unit("Birim")
    gun = field.Integer("Gün", choices=HAFTA, index=True)
    zaman_dilimi = ZamanDilimleri("Zaman Dilimi")
    durum = field.Integer("Uygunluk Durumu", choices=UYGUNLUK_DURUMU, default=1, index=True)
    ogretim_elemani_zaman_plani = OgElemaniZamanPlani("Öğretim Elemanı")

    _zaman_dilimi = list_fields_accessor(attrgetter("zaman_dilimi"), "Zaman Aralığı")
    _ogretim_elemani_zaman_plani = list_fields_accessor(attrgetter("ogretim_elemani_zaman_plani"), "Öğretim Elemanı Zaman Planı")

    def __unicode__(self):
        return '%s - %s - %s' % (self.ogretim_elemani_zaman_plani, self.zaman_dilimi,
                                 dict(UYGUNLUK_DURUMU)[int(self.durum)])


class DerslikZamanPlani(Model):
    class Meta:
        verbose_name = 'Derslik Zaman Planı'
        verbose_name_plural = "Derslik Zaman Planları"
        unique_together = [
            ('derslik', 'gun', 'baslangic_saat', 'baslangic_dakika', 'bitis_saat', 'bitis_dakika')]
        search_fields = ['gun', 'derslik_durum']
        list_fields = ['birim_adi', 'derslik_adi', 'gun', 'baslangic_saati', "bitis_saati", 'derslik_durum']

    unit = Unit()
    derslik = Room()
    gun = field.Integer("Gün", choices=HAFTA, index=True)
    baslangic_saat = field.String('Başlangıç Saati', default='08', index=True)
    baslangic_dakika = field.String('Başlangıç Dakikası', default='30', index=True)
    bitis_saat = field.String("Bitiş Saati", default='12', index=True)
    bitis_dakika = field.String("Bitiş Dakikası", default='00', index=True)
    derslik_durum = field.Integer("Durum", choices=DERSLIK_DURUMU, index=True)

    def __unicode__(self):
        return '%s %s %s:%s|%s:%s %s' % (self.derslik, dict(HAFTA)[self.gun],
                                         self.baslangic_saat, self.baslangic_dakika,
                                         self.bitis_saat, self.bitis_dakika,
                                         dict(DERSLIK_DURUMU)[int(self.derslik_durum)])

    birim_adi = list_fields_accessor(attrgetter("unit.name"), "Birim")
    derslik_adi = list_fields_accessor(attrgetter("derslik.name"), "Derslik")
    baslangic_saati = list_fields_accessor(lambda obj: "%s:%s" % (obj.baslangic_saat, obj.baslangic_dakika), "Başlangıç Saati")
    bitis_saati = list_fields_accessor(lambda obj: "%s:%s" % (obj.bitis_saat, obj.bitis_dakika), "Bitiş Saati")


class DersEtkinligi(Model):
    class Meta:
        verbose_name = "Ders Etkinliği"
        verbose_name_plural = "Ders Etkinlikleri"
        search_fields = ['unit_yoksis_no']
        list_fields = ["okutman_adi", "ders_adi", "birim_adi", "sube_adi", "baslangic_saati", "bitis_saati"]

    solved = fields.Boolean('Ders Planı Çözüm Durumu', index=True)
    unitime_key = fields.String(index=True)  # class id
    unit_yoksis_no = fields.Integer('Bölüm Yöksis Numarası', index=True)
    room_type = RoomType('İşleneceği Oda Türü', index=True)
    okutman = Okutman("Öğretim Elemanı", index=True)
    sube = Sube('Şube', index=True)
    donem = Donem('Dönem', index=True)
    bolum = Unit('Bölüm', index=True)
    published = fields.Boolean('Ders Planı Yayınlanma Durumu', index=True)
    # Arama amaçlı
    ders = Ders('Ders', index=True)
    ek_ders = fields.Boolean(index=True)
    sure = fields.Integer("Ders Etkinliği Süresi", index=True)

    # teori = field.Integer("Ders Teori Saati", index=True)
    # uygulama = field.Integer("Ders Uygulama Saati", index=True)
    # dersin süresinin ne kadarı teori ne kadarı uygulama gibi 2+2, 4+0 gibi

    # to be calculated
    room = Room('Derslik')
    gun = fields.String("Gün", choices=HAFTA)
    baslangic_saat = fields.String("Başlangıç Saati")
    baslangic_dakika = fields.String("Başlangıç Dakikası")
    bitis_saat = fields.String("Bitiş Saati")
    bitis_dakika = fields.String("Bitiş Dakikası")

    def post_creation(self):
        """Yeni bir DersEtkinligi oluşturulduğunda arama amaçlı olan
        alanları otomatik olarak doldurur."""
        self.ders = self.sube.ders
        self.save()

    def __unicode__(self):
        return '%s - %s - %s:%s|%s:%s - %s' % (
            self.room.name, self.gun, self.baslangic_saat, self.baslangic_dakika,
            self.bitis_saat, self.bitis_dakika, self.okutman)
    okutman_adi = list_fields_accessor(attrgetter("okutman"), "Okutman")
    birim_adi = list_fields_accessor(attrgetter("bolum.name"), "Birim")
    sube_adi = list_fields_accessor(attrgetter("sube.ad"), "Şube")
    ders_adi = list_fields_accessor(attrgetter("sube.ders.ad"), "Ders")
    baslangic_saati = list_fields_accessor(lambda obj: "%s:%s" % (obj.baslangic_saat, obj.baslangic_dakika), "Başlangıç Saati")
    bitis_saati = list_fields_accessor(lambda obj: "%s:%s" % (obj.bitis_saat, obj.bitis_dakika), "Bitiş Saati")


class SinavEtkinligi(Model):
    class Meta:
        verbose_name = 'Sınav Etkinliği'
        verbose_name_plural = "Sınav Etkinlikleri"
        search_fields = ['tarih', 'ders_adi', 'sube_adi']
        list_fields = ['birim_adi', 'ders_adi', 'sube_adi', 'donem_adi', 'tarih']

    sube = Sube('Şube', index=True)
    ders = Ders('Ders', index=True)
    donem = Donem('Dönem', index=True)
    bolum = Unit('Bölüm', index=True)
    unitime_key = fields.String(index=True)
    # default False, unitime solver tarafindan True yapilir.
    solved = fields.Boolean('Sınav Planı Çözüm Durumu', index=True, default=False)

    # unitime cozumunun ardindan, is akisiyla sinav takvimi yayinlanip True yapilir.
    published = fields.Boolean('Sınav Planı Yayınlanma Durumu', index=True, default=False)

    # sistem servisiyle sinavlarin ardindan True yapilir.
    archived = fields.Boolean('Arşivlenmiş', default=False, index=True)

    tarih = fields.DateTime('Sınav Tarihi', index=True)

    class SinavYerleri(ListNode):
        room = Room('Sınav Yeri', index=True)

    @classmethod
    def sube_sinav_listesi(cls, sube, archived=False, donem=None):
        """
        Şubeye, döneme ve arşive göre sınav etkinliği listesi döndürür.

        """
        donem = donem or Donem.guncel_donem()
        return [e for e in cls.objects.filter(published=True, sube=sube,  archived=archived,
                                              donem=donem).order_by('-tarih')]

    def __unicode__(self):
        return '{} {} {}'.format(self.ders.ad, self.sube.ad, self.sinav_zamani())

    def sinav_zamani(self):
        return '{:%Y.%m.%d - %H:%M}'.format(self.tarih) if self.tarih else 'Henüz zamanlanmadi'
    donem_adi = list_fields_accessor(attrgetter("donem"), "Dönem")
    birim_adi = list_fields_accessor(attrgetter("bolum.name"), "Birim")
    sube_adi = list_fields_accessor(attrgetter("sube.ad"), "Şube")
    ders_adi = list_fields_accessor(attrgetter("sube.ders.ad"), "Ders")
