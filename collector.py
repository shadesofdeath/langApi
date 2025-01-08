import json
import os
import requests
from datetime import datetime, UTC
import time
import random

UUP_VERSIONS = [
    {
        "id": "ad27e52b-9e18-408a-9df2-8688e5273fbf",
        "version": "W11 24H2",
        "arch": "x64",
        "is_win11": True
    },
    {
        "id": "b6049aaf-4f56-4183-8e58-32954906de64",
        "version": "W11 24H2",
        "arch": "arm64",
        "is_win11": True
    }
]

def filter_language_files(files, lang):
    filtered_files = {}
    for filename, file_data in files.items():
        if not (filename.endswith(('.cab', '.esd')) and lang in filename) and \
           not filename.endswith('LanguageExperiencePack_.appx'):
            continue
        if any(x in filename for x in ['core_', 'professional_', 'coren_', 
               'professionaln_', 'PPIPro_', 'ServerDatacenter_', 
               'ServerStandard_', 'ServerTurbine_']):
            continue
        if any(x in filename for x in [
            'Microsoft-Windows-LanguageFeatures-Basic',
            'Microsoft-Windows-LanguageFeatures-OCR',
            'Microsoft-Windows-LanguageFeatures-TextToSpeech'
        ]):
            continue
        filtered_files[filename] = file_data
    return filtered_files

def collect_language_files():
    base_url = "https://api.uupdump.net/get.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    for version in UUP_VERSIONS:
        try:
            # Random bekleme süresi (10-15 saniye arası)
            sleep_time = random.uniform(10, 15)
            time.sleep(sleep_time)
            
            params = {
                'id': version['id'],
                'lang': 'tr-tr',
                'edition': 'core'
            }
            
            response = requests.get(
                base_url, 
                params=params, 
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Error {response.status_code} for {version['version']}")
                continue
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"Invalid JSON for {version['version']}")
                continue
            
            if 'response' not in data or 'files' not in data['response']:
                continue
            
            lang_files = filter_language_files(data['response']['files'], 'tr-tr')
            
            output = {
                'version': version['version'],
                'arch': version['arch'],
                'language': 'tr-tr',
                'timestamp': datetime.now(UTC).isoformat(),
                'files': lang_files
            }
            
            os_type = 'windows11' if version['is_win11'] else 'windows10'
            save_dir = f'data/{os_type}/{version["arch"]}/tr-tr'
            os.makedirs(save_dir, exist_ok=True)
            
            with open(f'{save_dir}/files.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error processing {version['version']}: {str(e)}")

if __name__ == "__main__":
    collect_language_files()