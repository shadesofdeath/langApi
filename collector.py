import json
import os
import requests
from datetime import datetime

# UUP versiyon ve dil bilgileri
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
    # Diğer versiyonları da ekleyebilirsiniz
]

LANGUAGES = [
    "ar-sa", "bg-bg", "cs-cz", "da-dk", "de-de", "el-gr", "en-gb", "en-us",
    "es-es", "es-mx", "et-ee", "fi-fi", "fr-ca", "fr-fr", "he-il", "hr-hr",
    "hu-hu", "it-it", "ja-jp", "ko-kr", "lt-lt", "lv-lv", "nb-no", "nl-nl",
    "pl-pl", "pt-br", "pt-pt", "ro-ro", "ru-ru", "sk-sk", "sl-si", "sr-latn-rs",
    "sv-se", "th-th", "tr-tr", "uk-ua", "zh-cn", "zh-tw"
]

def filter_language_files(files, lang):
    """PowerShell'deki filtreleme mantığına benzer şekilde dil dosyalarını filtrele"""
    filtered_files = {}
    
    for filename, file_data in files.items():
        # Sadece .cab, .esd ve .appx dosyalarını al
        if not (filename.endswith(('.cab', '.esd')) and lang in filename) and \
           not filename.endswith('LanguageExperiencePack_.appx'):
            continue
            
        # Belirli ESD dosyalarını hariç tut
        if any(x in filename for x in ['core_', 'professional_', 'coren_', 
               'professionaln_', 'PPIPro_', 'ServerDatacenter_', 
               'ServerStandard_', 'ServerTurbine_']):
            continue
            
        # Server FOD dosyalarını hariç tut
        if any(x in filename for x in [
            'Microsoft-Windows-LanguageFeatures-Basic',
            'Microsoft-Windows-LanguageFeatures-OCR',
            'Microsoft-Windows-LanguageFeatures-TextToSpeech'
            # Diğer FOD keywordleri eklenebilir
        ]):
            continue
            
        filtered_files[filename] = file_data
    
    return filtered_files

def collect_language_files():
    base_url = "https://api.uupdump.net/get.php"
    
    for version in UUP_VERSIONS:
        for lang in LANGUAGES:
            try:
                # API'den veri çek
                params = {
                    'id': version['id'],
                    'lang': lang,
                    'edition': 'core'
                }
                response = requests.get(base_url, params=params)
                data = response.json()
                
                if 'response' not in data or 'files' not in data['response']:
                    continue
                
                # Dil dosyalarını filtrele
                lang_files = filter_language_files(data['response']['files'], lang)
                
                # Sonuçları kaydet
                output = {
                    'version': version['version'],
                    'arch': version['arch'],
                    'language': lang,
                    'timestamp': datetime.utcnow().isoformat(),
                    'files': lang_files
                }
                
                # Dizin yapısı oluştur
                os_type = 'windows11' if version['is_win11'] else 'windows10'
                save_dir = f'data/{os_type}/{version["arch"]}/{lang}'
                os.makedirs(save_dir, exist_ok=True)
                
                # JSON dosyasını kaydet
                with open(f'{save_dir}/files.json', 'w', encoding='utf-8') as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                print(f"Error processing {version['version']} {lang}: {str(e)}")

if __name__ == "__main__":
    collect_language_files()