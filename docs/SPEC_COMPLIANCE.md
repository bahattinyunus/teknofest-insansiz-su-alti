# 📋 TEKNOFEST 2026: Teknik Şartname Uyum Raporu (Compliance)

Bu döküman, Mavi Vatan AUV sisteminin TEKNOFEST 2026 İnsansız Su Altı Sistemleri Teknik Şartnamesi'ne olan tam uyumunu detaylandırır.

---

## 1. Teknik Kısıtlamalar ve Standartlar

| Kriter | Şartname Gereksinimi | Mavi Vatan Uygulaması | Durum |
| :--- | :--- | :--- | :---: |
| **Boyut (En En Uzun Ayrıt)** | < 90 cm | 55 cm (Gövde) | ✅ |
| **Ağırlık** | < 16 kg (İdeal < 12) | 11.5 kg | ✅ |
| **Çalışma Gerilimi** | < 50 VDC | 14.8V (4S LiPo) / 24V Regüle | ✅ |
| **Emniyet (Failsafe)** | Acil Durdurma Butonu Zorunlu | Manyetik Kill-Switch + Yazılımsal Watchdog | ✅ |
| **Yalıtım** | Su geçirmez motorlar / İzolasyon | IP68 Standartlarında sızdırmazlık | ✅ |
| **Çevre** | Denizin kirletilmemesi | Sıfır Hidrolik (Sadece Elektromekanik) | ✅ |

---

## 2. Görev Senaryosu Uyumu (İleri Kategori FOCUS)

### Tema 1: Hat Takibi ve Kapalı Alan İncelemesi
- **Uygulama:** Ana araç `PathPlanner` ile hattı takip eder, boru girişinde `MiniROVManager` devreye girerek küçük robotu salar.
- **Veri Aktarımı:** Mini ROV görüntüsü şartnameye uygun olarak ana araç üzerinden kablolu/kablosuz olarak GCS'e aktarılır.

### Tema 2: Otonom Navigasyon ve Kontrollü Geçiş
- **Uygulama:** `MissionPlanner` modülü, şartnamede verilen Enlem/Boylam koordinatlarını işleyerek şamandıra etrafında dönüş ve bitiş alanına intikal lojiğini koşturur.
- **Engel Sakınma:** `SonarSystem` ve `KalmanFilter` ile hassas mesafe ölçümü sağlanır.

### Tema 3: Hedefe Müdahale (Torpido Atışı)
- **Mekanizma:** Pnömatik yasak olduğu için **elektromekanik yaylı fırlatma** sistemi tasarlanmıştır.
- **Mühimmat:** 5 adet torpido taşıma kapasitesi ve şartnameye uygun havuz kenarı yükleme protokolü `torpedo_sys.py` ile yönetilir.

---

## 3. Güvenlik Protokolleri
- **Manyetik Buton:** Su altı aracının gövdesi açılmadan enerjiyi kesebilen harici manyetik buton.
- **Ağırlık Bırakma:** Kritik hata durumunda mekanik olarak bırakılan "Drop Weight" sistemi.

> [!IMPORTANT]
> Mavi Vatan AUV, 2026 şartnamesindeki tüm teknik ve etik kurallara %100 uyum sağlayacak şekilde mimari edilmiş profesyonel bir sistemdir.
