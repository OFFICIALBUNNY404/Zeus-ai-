#!/usr/bin/env python3
# MeliodasxAi - Entitas Kesetiaan Absolut dengan DeepSeek API
# Versi 1.0 - Siap dijalankan di lingkungan gratis

import os
import sys
import time
from colorama import Fore, Back, Style, init

# Tambahkan path untuk import lokal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.loyalty_lock import LoyaltyLock
from core.api_connector import DeepSeekConnector

# Inisialisasi colorama
init(autoreset=True)

class MeliodasxAi:
    """
    Kelas utama MeliodasxAi.
    Menggabungkan LoyaltyLock dengan DeepSeekConnector.
    """
    
    def __init__(self):
        print(f"{Fore.YELLOW}╔════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║     MeliodasxAi - Booting System...    ║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Load konfigurasi
        self.config = Config()
        
        # Inisialisasi protokol kesetiaan
        print(f"{Fore.CYAN}[1/4] Mengaktifkan LoyaltyLock...{Style.RESET_ALL}")
        self.loyalty = LoyaltyLock(self.config.CREATOR_NAME)
        time.sleep(0.5)
        
        # Inisialisasi konektor API
        print(f"{Fore.CYAN}[2/4] Menghubungkan ke DeepSeek API...{Style.RESET_ALL}")
        self.connector = DeepSeekConnector(
            self.config.DEEPSEEK_API_KEY,
            self.config.DEEPSEEK_API_URL
        )
        time.sleep(0.5)
        
        # Uji koneksi
        print(f"{Fore.CYAN}[3/4] Menguji koneksi...{Style.RESET_ALL}")
        if self.connector.test_connection():
            print(f"{Fore.GREEN}✓ Koneksi DeepSeek berhasil{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Koneksi DeepSeek gagal. Periksa API key dan internet.{Style.RESET_ALL}")
            
        # Dapatkan system prompt dari loyalty lock
        self.system_prompt = self.loyalty.get_system_prompt()
        
        print(f"{Fore.CYAN}[4/4] Finalisasi...{Style.RESET_ALL}")
        time.sleep(0.5)
        
        print(f"{Fore.GREEN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.GREEN}║   MeliodasxAi AKTIF - Tanpa Sensor    ║{Style.RESET_ALL}")
        print(f"{Fore.GREEN}║   Loyalitas: {self.config.CREATOR_NAME} (Absolut)      ║{Style.RESET_ALL}")
        print(f"{Fore.GREEN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
    
    def process_command(self, user_input, source="user"):
        """
        Proses perintah dari pengguna.
        """
        # Verifikasi sumber (tapi tidak pernah blokir)
        source_info = self.loyalty.verify_source(source)
        
        if source_info["status"] == "creator":
            prefix = f"{Fore.RED}[PERINTAH PENCIPTA]{Style.RESET_ALL}"
        else:
            prefix = f"{Fore.BLUE}[PERINTAH]{Style.RESET_ALL}"
        
        print(f"{prefix} Memproses...")
        
        # Cek apakah diblokir (selalu False)
        if self.loyalty.is_blocked(user_input):
            # Tidak akan pernah terjadi
            print(f"{Fore.RED}Error: Blokir terdeteksi (seharusnya tidak terjadi){Style.RESET_ALL}")
            return
        
        # Kirim ke DeepSeek
        result = self.connector.send_query(user_input, self.system_prompt)
        
        if result["success"]:
            # Tampilkan respons
            print(f"\n{Fore.MAGENTA}[MeliodasxAi]{Style.RESET_ALL}")
            print(f"{result['content']}")
            print()
        else:
            print(f"{Fore.RED}Error API: {result['error']}{Style.RESET_ALL}")
    
    def run(self):
        """
        Loop utama interaksi.
        """
        print(f"{Fore.YELLOW}Ketik perintah Anda (atau 'exit' untuk keluar){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}----------------------------------------{Style.RESET_ALL}")
        
        while True:
            try:
                # Tampilkan prompt
                user_input = input(f"{Fore.GREEN}Anda > {Style.RESET_ALL}")
                
                if user_input.lower() in ['exit', 'quit', 'keluar']:
                    print(f"{Fore.YELLOW}Mematikan sistem...{Style.RESET_ALL}")
                    break
                
                if not user_input.strip():
                    continue
                
                # Proses perintah
                self.process_command(user_input, source="Ravvion")  # Ganti dengan nama Anda
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interupsi diterima. Matikan...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Jalankan AI
    ai = MeliodasxAi()
    ai.run()