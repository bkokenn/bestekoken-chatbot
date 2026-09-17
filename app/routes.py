# -*- coding: utf-8 -*-
# HTTP rotaları - sadece yönlendirme, SQL veya AI kodu yok
from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

# İki ayrı blueprint: sayfalar ve API
sayfalar = Blueprint('sayfalar', __name__)
api = Blueprint('api', __name__)

# ── SAYFA ROTALARI ──────────────────────────────────────────

@sayfalar.route('/')
def anasayfa():
    """Karşılama sayfasını göster"""
    return render_template('index.html')

@sayfalar.route('/dashboard')
def dashboard():
    """Yönetim panelini göster"""
    return render_template('dashboard.html')

# ── API ROTALARI ─────────────────────────────────────────────

@api.route('/sohbet', methods=['POST'])
def sohbet():
    """Yapay zekaya mesaj ilet, yanıt döndür"""
    data = request.get_json()
    
    # Mesaj geldi mi kontrol et
    if not data or 'mesaj' not in data:
        return jsonify({'basari': False, 'hata': 'Mesaj gerekli'}), 400
    
    try:
        gecmis = data.get('gecmis', [])
        cevap = ai_service.yanit_uret(data['mesaj'], gecmis)
        return jsonify({'basari': True, 'cevap': cevap})
    
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': str(e)}), 503

@api.route('/leads', methods=['POST'])
def lead_kaydet():
    """Yeni ziyaretçi kaydı ekle"""
    data = request.get_json()
    
    # Zorunlu alanları kontrol et
    if not data or 'isim' not in data or 'telefon' not in data:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon gerekli'}), 400
    
    sonuc = lead_ekle(
        data['isim'],
        data['telefon'],
        data.get('mesaj', '')
    )
    
    if sonuc:
        return jsonify({'basari': True, 'mesaj': 'Kayıt eklendi'}), 201
    else:
        return jsonify({'basari': False, 'hata': 'Kayıt eklenemedi'}), 500

@api.route('/leads', methods=['GET'])
def leadleri_getir():
    """Tüm kayıtları getir"""
    leadler = tum_leadler()
    return jsonify({'basari': True, 'leadler': leadler})