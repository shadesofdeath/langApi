import json
import os
import requests
from datetime import datetime, UTC
import time

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

LANGUAGES = [
    "ar-sa", "bg-bg", "cs-cz", "da-dk", "de-de", "el-gr", "en-gb", "en-us",
    "es-es", "es-mx", "et-ee", "fi-fi", "fr-ca", "fr-fr", "he-il", "hr-hr",
    "hu-hu", "it-it", "ja-jp", "ko-kr", "lt-lt", "lv-lv", "nb-no", "nl-nl",
    "pl-pl", "pt-br", "pt-pt", "ro-ro", "ru-ru", "sk-sk", "sl-si", "sr-latn-rs",
    "sv-se", "th-th", "tr-tr", "uk-ua", "zh-cn", "zh-tw"
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
    headers = {'User-Agent': 'LangAPI/1.0'}

    for version in UUP_VERSIONS:
        for lang in LANGUAGES:
            try:
                params = {
                    'id': version['id'],
                    'lang': lang,
                    'edition': 'core'
                }
                
                response = requests.get(base_url, params=params, headers=headers)
                time.sleep(1)  # API rate limiting
                
                if response.status_code != 200:
                    print(f"Error {response.status_code} for {version['version']} {lang}")
                    continue
                
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    print(f"Invalid JSON for {version['version']} {lang}")
                    continue
                
                if 'response' not in data or 'files' not in data['response']:
                    continue
                
                lang_files = filter_language_files(data['response']['files'], lang)
                
                output = {
                    'version': version['version'],
                    'arch': version['arch'],
                    'language': lang,
                    'timestamp': datetime.now(UTC).isoformat(),
                    'files': lang_files
                }
                
                os_type = 'windows11' if version['is_win11'] else 'windows10'
                save_dir = f'data/{os_type}/{version["arch"]}/{lang}'
                os.makedirs(save_dir, exist_ok=True)
                
                with open(f'{save_dir}/files.json', 'w', encoding='utf-8') as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                print(f"Error processing {version['version']} {lang}: {str(e)}")

if __name__ == "__main__":
    collect_language_files()