# Tüm ayarları ve gizli anahtarları tek merkezde tutan dosya
import os
from dotenv import load_dotenv

# .env dosyasını oku
load_dotenv()

class Config:
    # Gizli anahtarlar .env'den okunur
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan_anahtar')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    
    # Veritabanı dosyasının yolu
    DATABASE_URL = 'bestekoken.db'
    
    # Yapay zeka sağlayıcısı
    AI_PROVIDER = 'groq'
    
    # CORS ayarı - hangi adreslerden istek kabul edilir
    CORS_ORIGINS = ['*']
    
    # Yapay zekanın kim olduğunu tanımlayan metin
    BUSINESS_CONTEXT = """Sen Beste Köken Studio'nun GIS asistanısın.
    Beste Köken Studio, yüksek lisans ve doktora öğrencilerine tez süreçlerinde
    GIS analizi, tematik haritalama ve mekânsal analiz hizmetleri sunan bir danışmanlık markasıdır.
    Ziyaretçilere hizmetler hakkında bilgi ver, sorularını yanıtla.
    Sonunda iletişim bilgisi (isim ve telefon) bırakmalarını iste.
    Türkçe konuş, samimi ve profesyonel ol."""

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Hangi ortamda olduğumuza göre config seç
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}