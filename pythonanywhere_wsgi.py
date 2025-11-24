# PythonAnywhere WSGI Configuration File
# Bu dosyayı PythonAnywhere'de /var/www/kullaniciadi_pythonanywhere_com_wsgi.py olarak kullanın

import sys

# Proje klasörünü Python path'ine ekle
# ÖNEMLİ: 'meliksahgok' yerine kendi kullanıcı adınızı yazın!
path = '/home/meliksahgok/heictojpg'
if path not in sys.path:
    sys.path.insert(0, path)

# Flask uygulamasını import et
from app import app as application

# Uygulamayı çalıştır
if __name__ == "__main__":
    application.run()

