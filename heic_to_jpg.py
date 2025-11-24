#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HEIC to JPG Image Converter
HEIC formatındaki fotoğrafları JPG formatına dönüştürür.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

# HEIF formatını kaydet
pillow_heif.register_heif_opener()


def convert_heic_to_jpg(input_path: str, output_path: str = None, quality: int = 95) -> bool:
    """
    HEIC dosyasını JPG formatına dönüştürür.
    
    Args:
        input_path: Giriş HEIC dosyasının yolu
        output_path: Çıkış JPG dosyasının yolu (None ise otomatik oluşturulur)
        quality: JPG kalitesi (1-100, varsayılan: 95)
    
    Returns:
        bool: Başarılı ise True, hata varsa False
    """
    try:
        input_file = Path(input_path)
        
        # Giriş dosyasının varlığını kontrol et
        if not input_file.exists():
            print(f"[HATA] Dosya bulunamadi: {input_path}")
            return False
        
        # Çıkış dosyası yolu belirlenmemişse otomatik oluştur
        if output_path is None:
            output_file = input_file.with_suffix('.jpg')
        else:
            output_file = Path(output_path)
        
        # HEIC dosyasını aç
        print(f"[ISLENIYOR] {input_file.name}")
        image = Image.open(input_file)
        
        # RGB moduna dönüştür (HEIC bazen RGBA olabilir)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Şeffaflık varsa beyaz arka plan ekle
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # JPG olarak kaydet
        image.save(output_file, 'JPEG', quality=quality, optimize=True)
        print(f"[BASARILI] {output_file.name} olusturuldu")
        return True
        
    except Exception as e:
        print(f"[HATA] {str(e)}")
        return False


def convert_directory(input_dir: str, output_dir: str = None, quality: int = 95, recursive: bool = False):
    """
    Bir dizindeki tüm HEIC dosyalarını JPG'ye dönüştürür.
    
    Args:
        input_dir: Giriş dizini
        output_dir: Çıkış dizini (None ise giriş diziniyle aynı)
        quality: JPG kalitesi (1-100)
        recursive: Alt dizinleri de tarayıp dönüştür
    """
    input_path = Path(input_dir)
    
    if not input_path.exists() or not input_path.is_dir():
        print(f"[HATA] Gecersiz dizin: {input_dir}")
        return
    
    # Çıkış dizini belirlenmemişse giriş dizinini kullan
    if output_dir is None:
        output_path = input_path
    else:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # HEIC dosyalarını bul
    if recursive:
        heic_files = list(input_path.rglob('*.heic')) + list(input_path.rglob('*.HEIC'))
    else:
        heic_files = list(input_path.glob('*.heic')) + list(input_path.glob('*.HEIC'))
    
    # macOS metadata dosyalarını filtrele (._ ile başlayanlar)
    heic_files = [f for f in heic_files if not f.name.startswith('._')]
    
    if not heic_files:
        print(f"[UYARI] {input_dir} dizininde HEIC dosyasi bulunamadi")
        return
    
    print(f"[BULUNDU] {len(heic_files)} HEIC dosyasi\n")
    
    success_count = 0
    for heic_file in heic_files:
        # Çıkış dosyası yolu
        if output_dir is None:
            jpg_file = heic_file.with_suffix('.jpg')
        else:
            # Alt dizin yapısını koru
            relative_path = heic_file.relative_to(input_path)
            jpg_file = output_path / relative_path.with_suffix('.jpg')
            jpg_file.parent.mkdir(parents=True, exist_ok=True)
        
        if convert_heic_to_jpg(str(heic_file), str(jpg_file), quality):
            success_count += 1
        print()  # Boş satır
    
    print(f"[OZET] {success_count}/{len(heic_files)} dosya basariyla donusturuldu")


def main():
    """Ana fonksiyon - komut satırı argümanlarını işler"""
    if len(sys.argv) < 2:
        print("""
HEIC to JPG Donusturucu

Kullanim:
  python heic_to_jpg.py <dosya_veya_dizin> [cikis_dizini] [--quality=95] [--recursive]

Ornekler:
  python heic_to_jpg.py foto.heic
  python heic_to_jpg.py foto.heic cikti.jpg
  python heic_to_jpg.py ./fotolar
  python heic_to_jpg.py ./fotolar ./jpg_fotolar --recursive
  python heic_to_jpg.py ./fotolar --quality=90

Parametreler:
  dosya_veya_dizin    : Donusturulecek HEIC dosyasi veya dizin
  cikis_dizini        : (Opsiyonel) Cikis dosyasi/dizini
  --quality=N         : JPG kalitesi (1-100, varsayilan: 95)
  --recursive         : Alt dizinleri de tarayip donustur
        """)
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = None
    quality = 95
    recursive = False
    
    # Argümanları parse et
    for arg in sys.argv[2:]:
        if arg.startswith('--quality='):
            try:
                quality = int(arg.split('=')[1])
                if not (1 <= quality <= 100):
                    print("[UYARI] Kalite 1-100 arasi olmali, varsayilan (95) kullaniliyor")
                    quality = 95
            except ValueError:
                print("[UYARI] Gecersiz kalite degeri, varsayilan (95) kullaniliyor")
        elif arg == '--recursive':
            recursive = True
        elif output_path is None:
            output_path = arg
    
    path = Path(input_path)
    
    # Dosya mı dizin mi?
    if path.is_file():
        # Tek dosya dönüştür
        convert_heic_to_jpg(input_path, output_path, quality)
    elif path.is_dir():
        # Dizin dönüştür
        convert_directory(input_path, output_path, quality, recursive)
    else:
        print(f"[HATA] Gecersiz yol: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()

