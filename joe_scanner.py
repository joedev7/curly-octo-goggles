cat > joe_scanner.py << 'EOF'
#!/usr/bin/env python3
"""
أداة Joe's Page Scanner
تم التطوير خصيصاً لـ Joe - شركة مسواك العراق
"""

import requests
import sys
import time
import argparse
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

class JoeScanner:
    def __init__(self):
        self.banner = """
╔══════════════════════════════════════════╗
║           Joe's Page Scanner            ║
║        تم التطوير خصيصاً لـ Joe         ║
║         شركة مسواك - العراق             ║
║    حقوق الطبع محفوظة 2024 - Joe Maswak  ║
╚══════════════════════════════════════════╝
        """
        
        self.found_pages = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Joe-Scanner-Maswak/1.0',
            'X-Scanner': 'Joe Custom Tool'
        })

    def display_banner(self):
        print(self.banner)
        print(f"[+] بدء الفحص في: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("[+] الأداة جاهزة للعمل...\n")

    def check_page(self, url, path):
        """فحص صفحة معينة"""
        try:
            full_url = urljoin(url, path)
            response = self.session.get(full_url, timeout=10, allow_redirects=True)
            
            if response.status_code < 400:
                self.found_pages.append({
                    'url': full_url,
                    'status': response.status_code,
                    'size': len(response.content)
                })
                print(f"[+] تم العثور: {full_url} [{response.status_code}]")
                return True
        except Exception as e:
            pass
        return False

    def scan_website(self, url, wordlist=None):
        """بدء فحص الموقع"""
        print(f"[+] جاري فحص: {url}")
        
        # قائمة افتراضية إذا لم يتم توفير wordlist
        if not wordlist:
            wordlist = [
                '', 'index.html', 'index.php', 'home', 'admin', 'login',
                'dashboard', 'wp-admin', 'images', 'css', 'js', 'api',
                'contact', 'about', 'products', 'services', 'blog',
                'test', 'demo', 'backup', 'old', 'new', 'archive',
                'files', 'documents', 'uploads', 'downloads', 'media',
                'static', 'public', 'private', 'secret', 'hidden',
                'config', 'setup', 'install', 'update', 'upgrade'
            ]
        
        print(f"[+] عدد الكلمات المفحوصة: {len(wordlist)}")
        print("[+] بدء عملية الفحص...\n")
        
        start_time = time.time()
        
        # استخدام multi-threading لتحسين الأداء
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for path in wordlist:
                future = executor.submit(self.check_page, url, path)
                futures.append(future)
            
            # انتظار انتهاء جميع العمليات
            for future in futures:
                future.result()
        
        end_time = time.time()
        self.generate_report(url, start_time, end_time)

    def generate_report(self, url, start_time, end_time):
        """توليد تقرير بالفروع المكتشفة"""
        print("\n" + "="*60)
        print("🎯 تقرير Joe's Scanner النهائي")
        print("="*60)
        
        print(f"🔗 الموقع المستهدف: {url}")
        print(f"📊 عدد الصفحات المكتشفة: {len(self.found_pages)}")
        print(f"⏰ وقت الفحص: {end_time - start_time:.2f} ثانية")
        print(f"👤 المُشغل: Joe - Maswak Iraq")
        print("\n📄 الصفحات المكتشفة:")
        print("-" * 60)
        
        for page in self.found_pages:
            print(f"🌐 {page['url']} - الحالة: {page['status']} - الحجم: {page['size']} بايت")
        
        print("\n" + "="*60)
        print("✅ تم الانتهاء من الفحص بنجاح!")
        print("="*60)

def main():
    scanner = JoeScanner()
    scanner.display_banner()
    
    parser = argparse.ArgumentParser(description='Joe\'s Page Scanner - Maswak Iraq')
    parser.add_argument('-u', '--url', required=True, help='الموقع المستهدف')
    parser.add_argument('-w', '--wordlist', help='قائمة الكلمات (اختياري)')
    
    args = parser.parse_args()
    
    try:
        # تحميل wordlist إذا تم توفيرها
        wordlist = None
        if args.wordlist:
            with open(args.wordlist, 'r', encoding='utf-8') as f:
                wordlist = [line.strip() for line in f.readlines()]
        
        scanner.scan_website(args.url, wordlist)
        
    except KeyboardInterrupt:
        print("\n[!] تم إيقاف الفحص بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"[!] خطأ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF