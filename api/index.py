from flask import Flask, request, Response
import edge_tts
import asyncio

app = Flask(__name__)

# Dr. Atlas için uygun ses
VOICE = "tr-TR-AhmetNeural"

async def get_audio_stream(text):
    # HATA BURADAYDI: edge-tts yerine edge_tts (alt çizgi) olmalı
    communicate = edge_tts.Communicate(text, VOICE)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

@app.route('/', methods=['GET', 'POST'])
def home():
    return "Dr. Atlas TTS API Calisiyor!"

@app.route('/tts', methods=['GET'])
def tts_endpoint():
    text = request.args.get('text')
    
    if not text:
        return "Lutfen 'text' parametresi gonderin.", 400

    try:
        # Asenkron fonksiyonu senkron Flask içinde çalıştır
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(get_audio_stream(text))
        
        # Sesi doğrudan mp3 verisi olarak döndür
        return Response(audio_bytes, mimetype="audio/mpeg")
    except Exception as e:
        # Hata olursa ekrana yazdır ki görelim
        return str(e), 500
