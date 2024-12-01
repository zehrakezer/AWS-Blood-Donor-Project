# Kan Aranıyor! 🚑

**Hayat kurtarmak bazen sadece bir tık ötede olabilir!**

Her gün binlerce insan acil kan ihtiyacıyla karşı karşıya kalıyor. Ancak doğru bağışçıya ulaşmak, çoğu zaman bir yarışa dönüşüyor. **Kan Aranıyor!** bu sorunu çözmek için geliştirilmiş bir platformdur.

## 📜 Projenin Amacı

Bu proje, kan bağışçısını ihtiyaç sahipleriyle bir araya getirerek hayat kurtarmayı hedefler. İletişim eksikliğini ortadan kaldırarak, bağış sürecini hızlı, güvenilir ve kolay hale getirir.

## 🚀 Projenin İşleyişi

1. **İlan Oluştur:** Kan ihtiyacı olan kişi platformda bir ilan açar.
2. **Bağışçıları Bilgilendir:** Sistem, aynı semtteki ve uygun kan grubundaki bağışçılara e-posta gönderir.
3. **Bağış Yap:** Bağışçı, ilanı inceleyerek “Bağışçı Ol” butonuna tıklar.
4. **Sonuçlandırma:** İlan başarılı bir bağış ile kapanır veya belirli bir süre sonunda ilan sahibi bilgilendirilerek süreç sonlandırılır.

## 🛠️ Kullanılan Teknolojiler ve Altyapı

### Backend & Frontend
- **Backend:** FastAPI ile geliştirildi.
- **Frontend:** Kullanıcı dostu bir arayüz.

### AWS Servisleri
- **EC2 Instances:** Sunucu barındırma.
- **RDS Database:** Veritabanı yönetimi.
- **Amazon SES:** E-posta gönderimi.
- **Amazon EventBridge:** Otomatik tetikleyici.
- **AWS Lambda:** İşlevsel mikro hizmetler.
- **Amazon S3 Buckets:** Dosya depolama.

### Lambda Fonksiyonları
1. **savemailadress:** Yeni üyenin e-posta adresini sisteme kaydeder.
2. **sendmail:** Kan bağışı için eşleşen bağışçılara e-posta gönderir.
3. **basarisizarama:** Maksimum arama sayısına ulaşıldığında ilan sahibini bilgilendirir.
4. **newuserpublication:** Yeni ilanları tetikleyerek uygun eşleşmeleri bulur.

## 💡 Gelecek Planları
- **Mobil Uygulama:** İlan sahipleri ve bağışçılar için mobil entegrasyon.
- **Gelişmiş Filtreleme:** Konum, kan grubu ve tarih gibi kriterlere göre ilan sıralama.
- **İstatistik ve Raporlama:** Toplam bağış sayısı, başarılı ilanlar gibi verilerin raporlanması.
- **Yerel Sağlık Kurumlarıyla Entegrasyon:** İlanların doğruluğunu artırmak.

## 👩‍💻 Katkıda Bulunanlar
- **Ömer Kutsal** - [LinkedIn](https://www.linkedin.com/in/ook15072016/)
- **Zehra Kezer** - [LinkedIn](https://www.linkedin.com/in/zehrakezer/)
- **Cevahir Özgür** - [LinkedIn](https://www.linkedin.com/in/cevahirozgur/)
- **Mesut Yürekdinç** - [LinkedIn](https://www.linkedin.com/in/mesutyurekdinc/)

## 🌐 Canlı Demo
Projenin canlı demo ( Time: 41:20 https://youtu.be/KHCmUi_z5R0?t=2487 ) inceleyebilirsiniz.

---

**Kan Aranıyor!** ile bir hayat kurtarmaya ne dersiniz? 💞