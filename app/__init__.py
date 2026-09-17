# -*- coding: utf-8 -*-
# Uygulama fabrikası - tüm parçaları bir araya getirir
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from app.database import init_db
from app.routes import sayfalar, api

def create_app(ortam='default'):
    """Uygulamayı oluştur ve yapılandır"""
    app = Flask(__name__)
    
    # Ayarları yükle
    app.config.from_object(config[ortam])
    
    # CORS'u aç - farklı adreslerden istek kabul et
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Veritabanını başlat
    init_db(app)
    
    # Blueprint'leri kaydet
    app.register_blueprint(sayfalar)
    app.register_blueprint(api, url_prefix='/api')
    
    # Sunucu canlılık kontrolü
    @app.route('/health')
    def health():
        return jsonify({'durum': 'aktif', 'marka': 'Beste Köken Studio'})
    
    return app