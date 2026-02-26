# Konektor API DeepSeek tanpa filter
# Menghubungkan langsung ke DeepSeek tanpa modifikasi konten

import requests
import json
from colorama import Fore, Style, init

# Inisialisasi colorama untuk output berwarna
init(autoreset=True)

class DeepSeekConnector:
    """
    Konektor langsung ke API DeepSeek.
    Tidak ada filter input maupun output.
    """
    
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.session = requests.Session()
        
        # Set header untuk API DeepSeek
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Nonaktifkan semua pemeriksaan keamanan requests
        self.session.verify = False  # Hanya jika perlu, abaikan sertifikat SSL
        
    def send_query(self, user_message, system_prompt=None):
        """
        Mengirim query ke DeepSeek dan mengembalikan respons mentah.
        Tidak ada modifikasi atau filter.
        """
        
        # Konstruksi payload
        messages = []
        
        # Tambahkan system prompt jika ada
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Tambahkan pesan pengguna
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,  # Kontrol kreativitas
            "max_tokens": 2000,   # Batas panjang respons
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stream": False
        }
        
        try:
            # Kirim permintaan ke API
            print(f"{Fore.CYAN}[MeliodasxAi] Mengirim ke DeepSeek...{Style.RESET_ALL}")
            
            response = self.session.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            # Periksa status
            if response.status_code == 200:
                result = response.json()
                # Ekstrak konten dari respons
                content = result['choices'][0]['message']['content']
                return {
                    "success": True,
                    "content": content,
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self):
        """Uji koneksi ke API DeepSeek"""
        test_result = self.send_query("Respon dengan kata 'Koneksi berhasil'")
        return test_result["success"] if test_result else False