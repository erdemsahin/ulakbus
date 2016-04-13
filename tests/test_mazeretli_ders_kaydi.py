# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

__author__ = 'H.İbrahim Yılmaz (drlinux)'

import time
from ulakbus.models import OgrenciProgram, Ogrenci, User
from zengine.lib.test_utils import BaseTestCase


class TestCase(BaseTestCase):
    """Bu sınıf ``BaseTestCase`` extend edilerek hazırlanmıştır.

    """

    def test_mazeretli_ders_kaydi(self):
        """Mazeretli Ders Kaydı wf test methodu.

        Mazeretli Ders Kaydı iş akışının ilk adımında öğrenci programı seçilir.

        Seçilen öğrenciye ait veritabanından dönen öğrenci programı sayısı ile
        sunucudan dönen öğrenci program sayısının eşitliği karşılaştırılıp test edilir.

        İş akışının ikinci adımında fakülte yönetim kurulu karar nosu girilir.

        İş akışının üçüncü aşamasında Öğrenci Programında ogrenci_ders_kayit_status field'ı
        mazeretli olarak güncellenir.

        Yollanan kayıtların `OgrenciProgram` modeline kayıt edilip edilmediği ve oğrenciye ait
        ogrenci_ders_kayit_status field'ın mazeretli olarak güncellenip güncellenmediğine
        bakılır.

        """

        # veritabanından test_user seçilir
        usr = User.objects.get(username='test_user')
        time.sleep(1)

        ogrenci_id = "T8PMMytvrHwhlRnQpBq8B5eB7Ut"
        program_id = "ZOQpL23OsEUWqUuslPD8CFNp74j"
        # mazeretli_ders_kaydi wF çalıştırılır
        self.prepare_client('/mazeretli_ders_kaydi', user=usr)
        resp = self.client.post(id=ogrenci_id, model="OgrenciProgram", param="ogrenci_id",
                                wf="mazeretli_ders_kaydi")

        # Öğrenciye ait programlar db'den seçilir.
        op = OgrenciProgram.objects.filter(ogrenci_id='T8PMMytvrHwhlRnQpBq8B5eB7Ut')
        ogrenci = Ogrenci.objects.get(ogrenci_id)

        # Veritabanından öğrenciye ait  çekilen program sayısı ile sunucudan dönen program sayısının
        # eşitliği karşılaştırılıp test edilir.

        assert len(resp.json['forms']['form'][1]['titleMap']) == len(op)

        # ogrencinin kayıtlı olduğu program yollanır
        program = {'program': program_id, 'sec': 1}
        resp = self.client.post(model="OgrenciProgram", wf="mazeretli_ders_kaydi", form=program)

        # fakülte yönetim kurulu karar no yollanır
        karar_no = {"sec": 1, "karar_no": "123456"}
        resp = self.client.post(model="OgrenciProgram", wf="mazeretli_ders_kaydi", form=karar_no)

        time.sleep(3)
        # Öğrencinin programdaki Ders Kayıt Durumu "Mazeretli" Olarak Güncellenmiş mi?

        md_kayit = OgrenciProgram.objects.filter(ogrenci_id='T8PMMytvrHwhlRnQpBq8B5eB7Ut')
        assert len(md_kayit) > 0

        assert md_kayit[0].ogrenci_ders_kayit_status == 1
