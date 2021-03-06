# -*-  coding: utf-8 -*-
#
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.


from ulakbus.models import OgrenciProgram, Donem, DonemDanisman, Ogrenci, Personel
from zengine.lib.test_utils import BaseTestCase
from pyoko.db.connection import log_bucket, version_bucket


class TestCase(BaseTestCase):
    """
    Bu sınıf ``BaseTestCase`` extend edilerek hazırlanmıştır.
    """

    def test_danisman_atama(self):
        """
        Danışmanı atanamayan öğrenciler öğrenci işleri tarafından atılır.
        Danışman atama iş akışının ilk adımında öğrenci programı seçilir.

        Seçilen öğrenciye ait veritabanından dönen öğrenci programı sayısı ile
        sunucudan dönen öğrenci program sayısının eşitliği karşılaştırılıp test edilir.

        İkinci adımında ise atanacak danışman seçilir.

        Veritabanından dönen danışmanların sayısı ile sunucudan dönen danışmaların sayısının
        eşitliği karşılaştırılıp test edilir.

        Üçüncü adımında ise danışman kaydedilir.

        Mesaj kutusunda danışman ataması yapılan öğrencinin ad ve soyad bilgilerinin olup
        olmadığı test edilir.

        """

        # Kullanıcıya login yaptırılır.
        log_bucket_count = len(log_bucket.get_keys())
        version_bucket_keys = version_bucket.get_keys()

        self.prepare_client('/danisman_atama', username='ogrenci_isleri_1')

        resp = self.client.post(id="RnKyAoVDT9Hc89KEZecz0kSRXRF",
                                model="OgrenciProgram",
                                param="ogrenci_id",
                                wf="danisman_atama",
                                filters={'ogrenci_id': {'values': ["KhFizqvCaZGtTloAZoPH1Uy98Pw"],
                                                        'type': "check"}})

        # Öğrenciye ait programlar db'den seçilir.
        op = OgrenciProgram.objects.filter(ogrenci_id='RnKyAoVDT9Hc89KEZecz0kSRXRF')

        # Veritabanından öğrenciye ait  çekilen program sayısı ile sunucudan dönen program sayısının
        # eşitliği karşılaştırılıp test edilir.
        assert len(resp.json['forms']['form'][2]['titleMap']) == len(op)

        # Öğrenci programı seçilir.
        resp = self.client.post(model='OgrenciProgram',
                                form={'program': "UEGET7qn9CDj9VEj4n0nbQ7m89d", 'sec': 1})

        guncel_donem = Donem.guncel_donem()
        # Öğrencinin kayıtlı olduğu öğrenci programlarından biri seçilir.
        program = op[0]
        # Döneme ve birime kayıtlı olan danışmanların listesini tutar.
        donem_danisman = DonemDanisman.objects.filter(donem=guncel_donem,
                                                      bolum=program.program.birim)

        # Veritabanından dönen dönem danışmanların sayısı ile sunucudan dönen dönem  danışmanlarının
        # sayısının eşitliğini karşılaştırıp test eder.
        assert len(donem_danisman) == len(resp.json['forms']['form'][2]['titleMap'])

        # Danışman seçilir.
        resp = self.client.post(model='OgrenciProgram',
                                form={'donem_danisman': 'Js2goP48yA183oMDAN8uM5GOExM', 'sec': 1})

        # save() işlemi meta paremetresi olmadan çalıştırıldığı için aktivite kaydının tutulmaması
        # ve aynı kalması beklenir.
        assert len(log_bucket.get_keys()) == log_bucket_count
        # Yeni versiyon kayıt keyleri alınır.
        yeni_versiyon_keyleri = list(set(version_bucket.get_keys()) - set(version_bucket_keys))
        # ogrenci_program modeline ait olan versiyon keyi alınır.
        op_versiyon_key = list(
            filter(lambda x: version_bucket.get(x).data['model'] == 'ogrenci_program',
                   yeni_versiyon_keyleri))[0]
        # Seçilen danışmanın personel keyi bulunur.
        danisman_key = DonemDanisman.objects.get('Js2goP48yA183oMDAN8uM5GOExM').okutman.personel.key
        # Versiyon loglarındaki danışman id si ile seçilen danısmanın id sinin uyuştuğu kontrol edilir.
        assert version_bucket.get(op_versiyon_key).data['data']['danisman_id'] == danisman_key

        ogrenci = Ogrenci.objects.get('RnKyAoVDT9Hc89KEZecz0kSRXRF')
        assert ogrenci.ad + ' ' + ogrenci.soyad in resp.json['msgbox']['msg']
