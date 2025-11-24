#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HEIC to JPG/WebP Web Converter
Web tabanlı HEIC to JPG/WebP dönüştürücü uygulaması
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


def convert_heic_to_format(heic_path, output_format='jpg', quality=95):
    """
    HEIC dosyasını JPG veya WebP'ye dönüştürür ve bytes olarak döndürür
    
    Args:
        heic_path: HEIC dosyasının yolu
        output_format: Çıkış formatı ('jpg' veya 'webp')
        quality: Kalite (1-100)
    
    Returns:
        tuple: (bytes, mimetype, extension)
    """
    try:
        image = Image.open(heic_path)
        
        # WebP için RGBA modunu koru, JPG için RGB'ye dönüştür
        if output_format.lower() == 'webp':
            # WebP şeffaflığı destekler, RGBA modunu koru
            if image.mode not in ('RGB', 'RGBA'):
                if image.mode == 'P':
                    image = image.convert('RGBA')
                elif image.mode in ('LA', 'L'):
                    image = image.convert('RGBA')
                else:
                    image = image.convert('RGBA')
        else:
            # JPG için RGB'ye dönüştür
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
        
        if output_format.lower() == 'webp':
            image.save(img_io, 'WEBP', quality=quality, method=6)
            mimetype = 'image/webp'
            extension = 'webp'
        else:
            image.save(img_io, 'JPEG', quality=quality, optimize=True)
            mimetype = 'image/jpeg'
            extension = 'jpg'
        
        img_io.seek(0)
        
        return img_io.getvalue(), mimetype, extension
    except Exception as e:
        raise Exception(f"Dönüştürme hatası: {str(e)}")


@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """HEIC dosyasını JPG veya WebP'ye dönüştür"""
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Sadece HEIC dosyaları desteklenir'}), 400
    
    try:
        # Format ve kalite ayarlarını al
        output_format = request.form.get('format', 'jpg').lower()
        if output_format not in ('jpg', 'webp'):
            output_format = 'jpg'
        
        quality = int(request.form.get('quality', 95))
        if not (1 <= quality <= 100):
            quality = 95
        
        # Dosyayı geçici olarak kaydet
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(str(input_path))
        
        # Dönüştür
        output_bytes, mimetype, extension = convert_heic_to_format(input_path, output_format, quality)
        
        # Geçici dosyayı sil
        input_path.unlink()
        
        # Çıkış dosya adı
        output_filename = Path(filename).stem + '.' + extension
        
        return send_file(
            io.BytesIO(output_bytes),
            mimetype=mimetype,
            as_attachment=True,
            download_name=output_filename
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

