# -*- coding: utf-8 -*-
# Yapay zeka çağrıları - AI kodu sadece bu dosyada olacak
import requests
from config import Config

class AIServiceError(Exception):
    """Yapay zeka servisine özel hata sınıfı"""
    pass

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.model = 'openai/gpt-oss-20b'
    
    def _sistem_talimati(self):
        """Config'den yapay zekanın kişiliğini getir"""
        return Config.BUSINESS_CONTEXT
    
    def yanit_uret(self, mesaj, gecmis=[]):
        """Kullanıcı mesajını Groq'a gönder, yanıt al"""
        
        # API anahtarı yoksa demo modu
        if not self.api_key:
            return "Demo modu: API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin."
        
        try:
            # Mesaj dizisini oluştur: önce sistem, sonra geçmiş, sonra yeni mesaj
            messages = [
                {'role': 'system', 'content': self._sistem_talimati()}
            ]
            
            # Geçmiş mesajları ekle
            for gecmis_mesaj in gecmis:
                messages.append(gecmis_mesaj)
            
            # Yeni kullanıcı mesajını ekle
            messages.append({'role': 'user', 'content': mesaj})
            
            # Groq API'sine istek at
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': messages,
                    'max_tokens': 500
                },
                timeout=30
            )
            
            # Yanıtı al ve döndür
            data = response.json()
            print("Groq yanıtı:", data)
            return data['choices'][0]['message']['content']
        
        except Exception as e:
            raise AIServiceError(f'Yapay zeka hatası: {e}')

# Dosya sonunda tek bir örnek oluştur
ai_service = AIService()