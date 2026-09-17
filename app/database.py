# -*- coding: utf-8 -*-
# Veritabanı işlemleri - SQL sadece bu dosyada olacak
import sqlite3
from config import Config

def get_db():
    """Veritabanına bağlan, sütun adıyla erişim sağla"""
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """Leads tablosunu oluştur (yoksa)"""
    with app.app_context():
        conn = get_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

def lead_ekle(isim, telefon, mesaj=''):
    """Yeni ziyaretçi kaydı ekle"""
    try:
        conn = get_db()
        # Güvenlik: ? ile SQL injection önlenir
        conn.execute(
            'INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)',
            (isim, telefon, mesaj)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f'Veritabanı hatası: {e}')
        return False

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye getir"""
    try:
        conn = get_db()
        leadler = conn.execute(
            'SELECT * FROM leads ORDER BY tarih DESC'
        ).fetchall()
        conn.close()
        # Her satırı sözlüğe çevir
        return [dict(lead) for lead in leadler]
    except Exception as e:
        print(f'Veritabanı hatası: {e}')
        return []