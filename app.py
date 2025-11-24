#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HEIC to JPG Web Converter
Web tabanlı HEIC to JPG dönüştürücü uygulaması
"""

import os
import io
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, flash
from werkzeug.utils import secure_filename
from PIL import Image
import pillow_heif

# HEIF formatını kaydet
pillow_heif.register_heif_opener()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max dosya boyutu
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Klasörleri oluştur
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'heic', 'HEIC'}


def allowed_file(filename):
    """Dosya uzantısı kontrolü"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_heic_to_jpg_bytes(heic_path, quality=95):
    """
    HEIC dosyasını JPG'ye dönüştürür ve bytes olarak döndürür
    
    Args:
        heic_path: HEIC dosyasının yolu
        quality: JPG kalitesi (1-100)
    
    Returns:
        bytes: JPG dosyasının bytes verisi
    """
    try:
        image = Image.open(heic_path)
        
        # RGB moduna dönüştür
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Bytes buffer'a kaydet
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG', quality=quality, optimize=True)
        img_io.seek(0)
        
        return img_io.getvalue()
    except Exception as e:
        raise Exception(f"Dönüştürme hatası: {str(e)}")


@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """HEIC dosyasını JPG'ye dönüştür"""
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Sadece HEIC dosyaları desteklenir'}), 400
    
    try:
        # Kalite ayarını al
        quality = int(request.form.get('quality', 95))
        if not (1 <= quality <= 100):
            quality = 95
        
        # Dosyayı geçici olarak kaydet
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(str(input_path))
        
        # Dönüştür
        jpg_bytes = convert_heic_to_jpg_bytes(input_path, quality)
        
        # Geçici dosyayı sil
        input_path.unlink()
        
        # JPG dosya adı
        jpg_filename = Path(filename).stem + '.jpg'
        
        return send_file(
            io.BytesIO(jpg_bytes),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=jpg_filename
        )
        
    except Exception as e:
        # Hata durumunda geçici dosyayı temizle
        if 'input_path' in locals() and input_path.exists():
            input_path.unlink()
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Sağlık kontrolü"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Production için gunicorn kullanılmalı
    app.run(debug=True, host='0.0.0.0', port=5000)

