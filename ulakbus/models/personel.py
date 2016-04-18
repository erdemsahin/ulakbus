# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
""" Personel Modülü

Bu modül Ulakbüs uygulaması için personel modelini ve  personel ile ilişkili modelleri içerir.

"""

from pyoko import Model, field
from .auth import Unit, User

PERSONEL_TURU = [
    (1, 'Akademik'),
    (2, 'İdari')
]


class Personel(Model):
    """Personel Modeli

    Personelin özlük ve iletişim bilgilerini içerir.

    """

    tckn = field.String("TC No", index=True)
    ad = field.String("Adı", index=True)
    soyad = field.String("Soyadı", index=True)
    cinsiyet = field.Integer("Cinsiyet", index=True, choices='cinsiyet')
    uyruk = field.String("Uyruk", index=True)
    ikamet_adresi = field.String("İkamet Adresi", index=True)
    ikamet_il = field.String("İkamet İl", index=True)
    ikamet_ilce = field.String("İkamet İlçe", index=True)
    adres_2 = field.String("Adres 2", index=True)
    adres_2_posta_kodu = field.String("Adres 2 Posta Kodu", index=True)
    oda_no = field.String("Oda Numarası", index=True)
    oda_tel_no = field.String("Oda Telefon Numarası", index=True)
    cep_telefonu = field.String("Cep Telefonu", index=True)
    e_posta = field.String("E-Posta", index=True)
    e_posta_2 = field.String("E-Posta 2", index=True)
    e_posta_3 = field.String("E-Posta 3", index=True)
    web_sitesi = field.String("Web Sitesi", index=True)
    yayinlar = field.String("Yayınlar", index=True)
    projeler = field.String("Projeler", index=True)
    kan_grubu = field.String("Kan Grubu", index=True)
    ehliyet = field.String("Ehliyet", index=True)
    verdigi_dersler = field.String("Verdiği Dersler", index=True)
    unvan = field.Integer("Ünvan", index=True, choices="akademik_unvan")
    biyografi = field.Text("Biyografi")
    notlar = field.Text("Notlar")
    engelli_durumu = field.String("Engellilik", index=True)
    engel_grubu = field.String("Engel Grubu", index=True)
    engel_derecesi = field.String("Engel Derecesi")
    engel_orani = field.Integer("Engellilik Oranı")
    personel_turu = field.Integer("Personel Türü", choices=PERSONEL_TURU, index=True)
    cuzdan_seri = field.String("Seri", index=True)
    cuzdan_seri_no = field.String("Seri No", index=True)
    baba_adi = field.String("Ana Adı", index=True)
    ana_adi = field.String("Baba Adı", index=True)
    dogum_tarihi = field.Date("Doğum Tarihi", index=True, format="%d.%m.%Y")
    dogum_yeri = field.String("Doğum Yeri", index=True)
    medeni_hali = field.Integer("Medeni Hali", index=True, choices="medeni_hali")
    kayitli_oldugu_il = field.String("İl", index=True)
    kayitli_oldugu_ilce = field.String("İlçe", index=True)
    kayitli_oldugu_mahalle_koy = field.String("Mahalle/Köy")
    kayitli_oldugu_cilt_no = field.String("Cilt No")
    kayitli_oldugu_aile_sira_no = field.String("Aile Sıra No")
    kayitli_oldugu_sira_no = field.String("Sıra No")
    kimlik_cuzdani_verildigi_yer = field.String("Cüzdanın Verildiği Yer")
    kimlik_cuzdani_verilis_nedeni = field.String("Cüzdanın Veriliş Nedeni")
    kimlik_cuzdani_kayit_no = field.String("Cüzdan Kayıt No")
    kimlik_cuzdani_verilis_tarihi = field.String("Cüzdan Kayıt Tarihi")
    birim = Unit("Birim")
    hizmet_sinifi = field.Integer("Hizmet Sınıfı", index=True, choices="hizmet_sinifi")
    user = User(one_to_one=True)

    class Meta:
        app = 'Personel'
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        list_fields = ['ad', 'soyad', 'tckn', 'durum']
        search_fields = ['ad', 'soyad', 'cep_telefonu', 'tckn']

    def durum(self):
        return self.nufus_kayitlari.durum if self.nufus_kayitlari.key else None

    durum.title = "Durum"

    # TODO: metod adi cok genel. daha anlasilir bir ad secip, refactor edelim.
    def kadro(self):
        """Kadro

        Personelin atama bilgilerinden kadrosuna erişir.

        Returns:
            Kadro örneği (instance)

        """

        atama = Atama.personel_guncel_atama(self)
        return atama.kadro

    def __unicode__(self):
        return "%s %s" % (self.ad, self.soyad)


class AdresBilgileri(Model):
    """Adres Bilgileri Modeli

    Personele ait adres bilgilerini içeren modeldir.

    Personelin birden fazla adresi olabilir.

    """

    ad = field.String("Adres Adı", index=True)
    adres = field.String("Adres", index=True)
    ilce = field.String("İlçe", index=True)
    il = field.String("İl", index=True)
    personel = Personel()

    class Meta:
        verbose_name = "Adres Bilgisi"
        verbose_name_plural = "Adres Bilgileri"

    def __unicode__(self):
        return "%s %s" % (self.ad, self.il)


class KurumIciGorevlendirmeBilgileri(Model):
    """Kurum İçi Görevlendirme Bilgileri Modeli

    Personelin, kurum içi görevlendirme bilgilerine ait modeldir.

    Görevlendirme bir birim ile ilişkili olmalıdır.

    """

    gorev_tipi = field.String("Görev Tipi", index=True, choices="gorev_tipi")
    kurum_ici_gorev_baslama_tarihi = field.Date("Başlama Tarihi", index=True, format="%d.%m.%Y")
    kurum_ici_gorev_bitis_tarihi = field.Date("Bitiş Tarihi", index=True, format="%d.%m.%Y")
    birim = Unit()
    aciklama = field.String("Açıklama")
    resmi_yazi_sayi = field.String("Resmi Yazı Sayı")
    resmi_yazi_tarih = field.Date("Resmi Yazı Tarihi", index=True, format="%d.%m.%Y")
    personel = Personel()

    class Meta:
        """``form_grouping`` kullanıcı arayüzeyinde formun temel yerleşim planını belirler.

        Layout grid (toplam 12 sütun) içerisindeki değerdir.

        Her bir ``layout`` içinde birden fazla form grubu yer alabilir: ``groups``

        Her bir grup, grup başlığı ``group_title``, form öğeleri ``items`` ve bu grubun
        açılır kapanır olup olmadığını belirten boolen bir değerden ``collapse`` oluşur.

        """

        verbose_name = "Kurum İçi Görevlendirme"
        verbose_name_plural = "Kurum İçi Görevlendirmeler"
        form_grouping = [
            {
                "layout": "4",
                "groups": [
                    {
                        "group_title": "Gorev",
                        "items": ["gorev_tipi", "kurum_ici_gorev_baslama_tarihi", "kurum_ici_gorev_bitis_tarihi",
                                  "birim", "aciklama"],
                        "collapse": False
                    }
                ]

            },
            {
                "layout": "2",
                "groups": [
                    {
                        "group_title": "Resmi Yazi",
                        "items": ["resmi_yazi_sayi", "resmi_yazi_tarih"],
                        "collapse": False
                    }
                ]

            },
        ]

    def __unicode__(self):
        return "%s %s" % (self.gorev_tipi, self.aciklama)


class KurumDisiGorevlendirmeBilgileri(Model):
    """Kurum Dışı Görevlendirme Bilgileri Modeli

    Personelin bağlı olduğu kurumun dışındaki görev bilgilerine ait modeldir.

    """

    gorev_tipi = field.Integer("Görev Tipi", index=True)
    kurum_disi_gorev_baslama_tarihi = field.Date("Başlama Tarihi", index=True, format="%d.%m.%Y")
    kurum_disi_gorev_bitis_tarihi = field.Date("Bitiş Tarihi", index=True, format="%d.%m.%Y")
    aciklama = field.Text("Açıklama", index=True)
    resmi_yazi_sayi = field.String("Resmi Yazı Sayı")
    resmi_yazi_tarih = field.Date("Resmi Yazı Tarihi", index=True, format="%d.%m.%Y")
    maas = field.Boolean("Maaş")
    yevmiye = field.Boolean("Yevmiye", default=False)
    yolluk = field.Boolean("Yolluk", default=False)
    ulke = field.Integer("Ülke", default="90", choices="ulke", index=True)
    personel = Personel()

    class Meta:
        verbose_name = "Kurum Dışı Görevlendirme"
        verbose_name_plural = "Kurum Dışı Görevlendirmeler"
        list_fields = ["ulke", "gorev_tipi", "kurum_disi_gorev_baslama_tarihi"]
        list_filters = ["ulke", "gorev_tipi", "kurum_disi_gorev_baslama_tarihi"]
        search_fields = ["aciklama", ]
        form_grouping = [
            {
                "layout": "4",
                "groups": [
                    {
                        "group_title": "Gorev",
                        "items": ["gorev_tipi", "kurum_disi_gorev_baslama_tarihi", "kurum_disi_gorev_bitis_tarihi",
                                  "ulke",
                                  "aciklama"],
                        "collapse": False
                    }
                ]

            },
            {
                "layout": "2",
                "groups": [
                    {
                        "group_title": "Resmi Yazi",
                        "items": ["resmi_yazi_sayi", "resmi_yazi_tarih"],
                        "collapse": False
                    },
                    {
                        "items": ["maas", "yevmiye", "yolluk"],
                        "collapse": False
                    }
                ]

            },
        ]

    def __unicode__(self):
        return "%s %s %s" % (self.gorev_tipi, self.aciklama, self.ulke)


class Kadro(Model):
    """Kadro Modeli

    Kurum için ayrılmış Kadro bilgilerine modeldir.

    Kadrolar 4 halde bulunabilirler: SAKLI, IZINLI, DOLU ve BOŞ

        * SAKLI: Saklı kadro, atama yapılmaya müsadesi olmayan, etkinlik onayı alınmamış
          fakat kurum için ayrılmış potansiyel kadroyu tanımlar.
        * IZINLI: Henüz atama yapılmamış, fakat etkinlik onayı alınmış kadroyu tanımlar.
        * DOLU: Bir personel tarafından işgal edilmiş bir kadroyu tanımlar. Ataması yapılmıştır.
        * BOŞ: Çeşitli sebepler ile DOLU iken boşaltılmış kadroyu tanınmlar.

    ``unvan`` ve ``unvan_kod`` karşıt alanlardır. Birisi varken diğeri mevcut olamaz.

    """

    kadro_no = field.Integer("Kadro No", required=False)
    unvan = field.Integer("Akademik Unvan", index=True, choices="akademik_unvan", required=False)
    derece = field.Integer("Derece", index=True, required=False)
    durum = field.Integer("Durum", index=True, choices="kadro_durumlari", required=False)
    birim = Unit("Birim", required=False)
    aciklama = field.String("Açıklama", index=True, required=False)
    unvan_kod = field.Integer("Unvan", index=True, choices="unvan_kod", required=False)

    class Meta:
        app = 'Personel'
        verbose_name = "Kadro"
        verbose_name_plural = "Kadrolar"
        list_fields = ['durum', 'unvan', 'aciklama']
        search_fields = ['unvan', 'derece']
        list_filters = ['durum']

    def __unicode__(self):
        return "%s %s %s" % (self.unvan, self.derece, self.durum)


class Izin(Model):
    """İzin Modeli

    Personelin ücretli izin bilgilerini içeren modeldir.

    """

    tip = field.Integer("Tip", index=True, choices="izin")
    baslangic = field.Date("Başlangıç", index=True, format="%d.%m.%Y")
    bitis = field.Date("Bitiş", index=True, format="%d.%m.%Y")
    onay = field.Date("Onay", index=True, format="%d.%m.%Y")
    adres = field.String("Geçireği Adres", index=True)
    telefon = field.String("Telefon", index=True)
    personel = Personel()
    vekil = Personel()

    class Meta:
        app = 'Personel'
        verbose_name = "İzin"
        verbose_name_plural = "İzinler"
        list_fields = ['tip', 'baslangic', 'bitis', 'onay', 'telefon']
        search_fields = ['tip', 'baslangic', 'onay']

    def __unicode__(self):
        return '%s %s' % (self.tip, self.onay)


class UcretsizIzin(Model):
    """Ücretsiz izin Modeli

    Personelin ücretsiz izin bilgilerini içeren modeldir.

    """

    tip = field.Integer("Tip", index=True, choices="ucretsiz_izin")
    baslangic_tarihi = field.Date("İzin Başlangıç Tarihi", index=True, format="%d.%m.%Y")
    bitis_tarihi = field.Date("İzin Bitiş Tarihi", index=True, format="%d.%m.%Y")
    donus_tarihi = field.Date("Dönüş Tarihi", index=True, format="%d.%m.%Y")
    donus_tip = field.Integer("Dönüş Tip", index=True)
    onay_tarihi = field.Date("Onay Tarihi", index=True, format="%d.%m.%Y")
    personel = Personel()

    class Meta:
        app = 'Personel'
        verbose_name = "Ücretsiz İzin"
        verbose_name_plural = "Ücretsiz İzinler"
        list_fields = ['tip', 'baslangic_tarihi', 'bitis_tarihi', 'donus_tarihi']
        search_fields = ['tip', 'onay_tarihi']

    def __unicode__(self):
        return '%s %s' % (self.tip, self.onay_tarihi)


class Atama(Model):
    """Atama Modeli

    Personelin atama bilgilerini içeren modeldir.

    """

    kurum_sicil_no = field.String("Kurum Sicil No", index=True)
    personel_tip = field.Integer("Personel Tipi", index=True)
    hizmet_sinif = field.Integer("Hizmet Sınıfı", index=True, choices="hizmet_sinifi")
    statu = field.Integer("Statü", index=True)
    gorev_suresi_baslama = field.Date("Görev Süresi Başlama", index=True, format="%d.%m.%Y")
    gorev_suresi_bitis = field.Date("Görev Süresi Bitiş", index=True, format="%d.%m.%Y")
    goreve_baslama_tarihi = field.Date("Göreve Başlama Tarihi", index=True, format="%d.%m.%Y")
    ibraz_tarihi = field.Date("İbraz Tarihi", index=True, format="%d.%m.%Y")
    durum = field.Integer("Durum", index=True)
    mecburi_hizmet_suresi = field.Date("Mecburi Hizmet Süresi", index=True, format="%d.%m.%Y")
    nereden = field.Integer("Nereden", index=True)
    atama_aciklama = field.String("Atama Açıklama", index=True)
    goreve_baslama_aciklama = field.String("Göreve Başlama Açıklama", index=True)
    kadro_unvan = field.Integer("Kadro Unvan", index=True)
    kadro_derece = field.Integer("Kadro Derece", index=True)
    kadro = Kadro()
    personel = Personel(one_to_one=True)

    class Meta:
        app = 'Personel'
        verbose_name = "Atama"
        verbose_name_plural = "Atamalar"
        list_fields = ['personel_tip', 'hizmet_sinif', 'gorev_suresi_baslama', 'ibraz_tarihi', 'durum']
        search_fields = ['personel_tip', 'hizmet_sinif', 'statu']

    def __unicode__(self):
        return '%s %s %s' % (self.kurum_sicil_no, self.gorev_suresi_baslama, self.ibraz_tarihi)

    @classmethod
    def personel_guncel_atama(cls, personel):
        """
        Personelin goreve_baslama_tarihi ne göre son atama kaydını döndürür.

        Returns:
            Atama örneği (instance)

        """

        return cls.objects.set_params(sort='goreve_baslama_tarihi desc').filter(personel=personel)[0]
