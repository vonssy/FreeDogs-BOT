# FreeDogs BOT
FreeDogs BOT

Register Here : [FreeDogs](https://t.me/theFreeDogs_bot/app?startapp=ref_Yum5S6tN)

## Fitur

  - Auto Get Account Information
  - Auto Tap Tap
  - Auto Complete Task
  - Multi Account

## Prasyarat

Pastikan Anda telah menginstal Python3.9 dan PIP.

## Instalasi

1. **Kloning repositori:**
   ```bash
   git clone https://github.com/vonssy/FreeDogs-BOT.git
   ```
   ```bash
   cd FreeDogs-BOT
   ```

2. **Instal Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Konfigurasi

- **query.txt:** Anda akan menemukan file `query.txt` di dalam direktori proyek. Pastikan `query.txt` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:

  ```bash
  query_id%3D
  user%3D
  ```

### How To Get FreeDogs Query

  Kamu dapat copy dan paste kode berikut di console pada DevTools untuk memperoleh query yang dibutuhkan, jangan lupa `allow pasting` dahulu jika pertama kali menggunakan console.

  ```bash
  let value = sessionStorage.getItem('telegram-apps/launch-params');
  value = value.replace(/^"|"$/g, '');

  let tgWebAppDataStart = value.indexOf('query_id%3D');

  if (tgWebAppDataStart === -1) {
  tgWebAppDataStart = value.indexOf('user%3D');
  }

  if (tgWebAppDataStart !== -1) {
  let tgWebAppData = value.substring(tgWebAppDataStart);
  let ampersandPos = tgWebAppData.indexOf('&');

  if (ampersandPos !== -1) {
      tgWebAppData = tgWebAppData.substring(0, ampersandPos);
  }

  copy(tgWebAppData)

  console.log('Sukses menyalin query');
  } else {
  console.log('Query tidak ditemukan.');
  }
  ```

## Jalankan

```bash
python bot.py #or python3 bot.py
```

## Penutup

Terima kasih telah mengunjungi repository ini, jangan lupa untuk memberikan kontribusi berupa follow dan stars.
Jika Anda memiliki pertanyaan, menemukan masalah, atau memiliki saran untuk perbaikan, jangan ragu untuk menghubungi saya atau membuka *issue* di repositori GitHub ini.

**vonssy**