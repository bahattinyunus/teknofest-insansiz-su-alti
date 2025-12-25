# 🛠️ AUV Bakım ve Donanım Mühendisliği Rehberi

Bu döküman, Medium makalesinde vurgulanan "Mühendislik Titizliği" prensiplerine dayanarak hazırlanan periyodik bakım ve donanım standartlarını içerir.

## 1. Sızdırmazlık ve O-Ring Hassasiyeti
"Mikron düzeyindeki hassasiyet, hayatta kalmanın anahtarıdır."

- **O-Ring Kontrolü:** Her dalış öncesi contalar gözle ve elle kontrol edilmeli, en küçük bir çizilme veya kum tanesi tespit edildiğinde değiştirilmelidir.
- **Gland Fill:** CAD aşamasında belirlenen genleşme boşluğu ve sıkışma oranı (%20-30) her montajda kontrol edilmelidir.
- **Yağlama:** Molykote 111 gibi silikon bazlı yağlayıcılar, contanın yive oturmasını kolaylaştırır ve mikroskobik gözenekleri kapatır.

## 2. Korozyon Kontrolü ve Yüzey Koruması
- **Anodize Koruma:** Alüminyum gövde (6061-T6 veya 7075), MIL-A-8625 standardında Sert Eloksal (Hard Anodizing) ile kaplanmalıdır.
- **Kurbanlık Anotlar:** Magnezyum veya çinko anotlar, gövdeyi galvanik korozyondan korumak için operasyonel olarak her takvim ayında kontrol edilmelidir.
- **Tatlı Su Durulama:** Tuzlu su dalışlarından hemen sonra araç, tüm eklemleri dahil olmak üzere tatlı suyla durulanmalıdır.

## 3. Termal Yönetim ve Isı Tahliyesi
- **Soğuk Köprü:** CPU ve ESC gibi yüksek ısı üreten bileşenler, termal pedler aracılığıyla doğrudan metal kapaklara temas ettirilmelidir.
- **Isı Kuyusu:** Tüm gövdenin pasif bir radyatör olarak çalıştığından ve içeride hava cebi (air pocket) kalmadığından emin olunmalıdır.

## 4. Mekanik Checklist
- [ ] O-ring kanalları temiz mi?
- [ ] Bulkhead konnektörleri torklandı mı?
- [ ] Sızdırmazlık tüpü vakum testinden geçti mi?
- [ ] Drop Weight (Ağırlık bırakma) pimi serbest mi?
