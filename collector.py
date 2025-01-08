import json
import os
import re
import requests
from datetime import datetime, UTC
import time
import random

UUP_VERSIONS = [
    {"id": "ad27e52b-9e18-408a-9df2-8688e5273fbf", "version": "W11 24H2", "arch": "x64", "is_win11": True},
    {"id": "b6049aaf-4f56-4183-8e58-32954906de64", "version": "W11 24H2", "arch": "arm64", "is_win11": True},
    # Diğer sürümler...
]

SERVER_FOD_KEYWORDS = [
    'Microsoft-Windows-LanguageFeatures-Basic',
    'Microsoft-Windows-LanguageFeatures-OCR',
    'Microsoft-Windows-LanguageFeatures-TextToSpeech',
    'Microsoft-Windows-Client-LanguagePack',
    'Microsoft-AzureStack-HCI-Management-Tools-FOD-Package', 
    'Microsoft-OneCore-StorageManagement-FoD-Package', 
    'Microsoft-Windows-ActiveDirectory-DS-LDS-Tools-FoD-Package', 
    'Microsoft-Windows-BitLocker-Recovery-Tools-FoD-Package', 
    'Microsoft-Windows-CertificateServices-Tools-FoD-Package', 
    'Microsoft-Windows-Console-Host-Legacy-FoD-Package', 
    'Microsoft-Windows-DHCP-Tools-FoD-Package', 
    'Microsoft-Windows-DNS-Tools-FoD-Package', 
    'Microsoft-Windows-EMS-SAC-Desktop-Tools-FoD-Package', 
    'Microsoft-Windows-FailoverCluster-Management-Tools-FOD-Package', 
    'Microsoft-Windows-FileServices-Tools-FoD-Package', 
    'Microsoft-Windows-GroupPolicy-Management-Tools-FoD-Package', 
    'Microsoft-Windows-IPAM-Client-FoD-Package', 
    'Microsoft-Windows-IRDA-Package', 
    'Microsoft-Windows-NetworkController-Tools-FoD-Package', 
    'Microsoft-Windows-NetworkLoadBalancing-Tools-FoD-Package', 
    'Microsoft-Windows-RasCMAK-Client-Package', 
    'Microsoft-Windows-RasRip-Package', 
    'Microsoft-Windows-RemoteAccess-Management-Tools-FoD-Package', 
    'Microsoft-Windows-RemoteDesktop-Services-Tools-FoD-Package', 
    'Microsoft-Windows-Server-AppCompat-FoD-Package', 
    'Microsoft-Windows-ServerCoreFonts-NonCritical-Fonts-BitmapFonts-FOD-Package', 
    'Microsoft-Windows-ServerCoreFonts-NonCritical-Fonts-MinConsoleFonts-FOD-Package', 
    'Microsoft-Windows-ServerCoreFonts-NonCritical-Fonts-Support-FOD-Package', 
    'Microsoft-Windows-ServerCoreFonts-NonCritical-Fonts-TrueType-FOD-Package', 
    'Microsoft-Windows-ServerCoreFonts-NonCritical-Fonts-UAPFonts-FOD-Package', 
    'Microsoft-Windows-ServerManager-Tools-FoD-Package', 
    'Microsoft-Windows-SNMP-Client-Package', 
    'Microsoft-Windows-StorageManagement-FoD-Package', 
    'Microsoft-Windows-StorageMigrationService-Management-Tools-FOD-Package', 
    'Microsoft-Windows-StorageReplica-Tools-FoD-Package', 
    'Microsoft-Windows-SystemInsights-Management-Tools-FOD-Package', 
    'Microsoft-Windows-TPM-Diagnostics-FOD-Package', 
    'Microsoft-Windows-VolumeActivation-Tools-FoD-Package',
    'Microsoft-Windows-Shielded-VM-Tools-FoD-Package',
    'Microsoft-Windows-WMI-SNMP-Provider-Client-Package',
    'Microsoft-OneCore-DeveloperMode-Desktop-Package',
    'microsoft-windows-composition-test-fod-package',
    'microsoft-windows-ipam-client-fod-package',
    'microsoft-windows-irda-package',
    'microsoft-windows-systeminsights-management-tools-fod-package',
    'microsoft-windows-wmi-snmp-provider-client-package',
    'microsoft-windows-media-features-package',
    'Microsoft-Windows-WSUS-Tools-FoD-Package'
]

CAB_FILTER_PATTERNS = [
    r'amd64_Microsoft-Windows-LanguageFeatures-Basic-.*-Package_.*\.cab',
    r'amd64_Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package_.*\.cab',
    r'amd64_Microsoft-Windows-LanguageFeatures-OCR-.*-Package_.*\.cab',
    r'amd64_Microsoft-Windows-LanguageFeatures-TextToSpeech-.*-Package_.*\.cab',
    r'amd64_Microsoft-OneCore-DeveloperMode-Desktop-Package_.*\.cab',
    r'amd64_Microsoft-Windows-LanguageFeatures-Speech-.*-Package_.*\.cab',
    r'Microsoft-AzureStack-HCI-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-OneCore-StorageManagement-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-OneCore-StorageManagement-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-ActiveDirectory-DS-LDS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-ActiveDirectory-DS-LDS-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-BitLocker-Recovery-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-CertificateServices-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Composition-Test-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Composition-Test-FOD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-DHCP-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-DHCP-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-DNS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-DNS-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-EMS-SAC-Desktop-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-FailoverCluster-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-FailoverCluster-Management-Tools-FOD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-FileServices-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-FileServices-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-GroupPolicy-Management-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-GroupPolicy-Management-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-InternetExplorer-Optional-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-IPAM-Client-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-IPAM-Client-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-IRDA-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-IRDA-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-LanguageFeatures-Basic-.*-Package-amd64_.*\.cab',
    r'Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package-amd64\.cab',
    r'Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package-amd64_.*\.cab',
    r'Microsoft-Windows-LanguageFeatures-OCR-.*-Package-amd64_.*\.cab',
    r'Microsoft-Windows-LanguageFeatures-TextToSpeech-.*-Package-amd64_.*\.cab',
    r'Microsoft-Windows-Media-Features-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Media-Features-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-MSPaint-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-MSPaint-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-NetworkController-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-NetworkLoadBalancing-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Notepad-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Notepad-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Notepad-System-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Notepad-System-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-PowerShell-ISE-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-PowerShell-ISE-FOD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Printing-PMCPPC-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Printing-WFS-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RasCMAK-Client-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RasCMAK-Client-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RasRip-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RemoteAccess-Management-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RemoteAccess-Management-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-RemoteDesktop-Services-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-Server-AppCompat-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-ServerManager-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-ServerManager-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-SnippingTool-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-SNMP-Client-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-SNMP-Client-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StepsRecorder-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StepsRecorder-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StorageManagement-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StorageManagement-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StorageMigrationService-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StorageReplica-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-StorageReplica-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-SystemInsights-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-TPM-Diagnostics-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-TPM-Diagnostics-FOD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-VolumeActivation-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WirelessDisplay-FOD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WMI-SNMP-Provider-Client-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WMI-SNMP-Provider-Client-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WordPad-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WordPad-FoD-Package-wow64-.*-.*_.*\.cab',
    r'Microsoft-Windows-WSUS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-OneCore-DeveloperMode-Desktop-Package-amd64_.*\.cab',
    r'Microsoft-Windows-Shielded-VM-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    r'Microsoft-Windows-LanguageFeatures-Speech-.*-Package-amd64_.*\.cab'
]

EXCLUDED_FILENAMES = [
    'core_', 'professional_', 'coren_', 'professionaln_',
    'PPIPro_', 'ServerDatacenter_', 'ServerStandard_',
    'ServerTurbine_'
]

def is_server_fod(filename, lang):
    """Belirtilen dosyanın Server FOD içerip içermediğini kontrol eder."""
    lang = lang.rstrip('-')
    return any(keyword in filename and filename.endswith(f'{lang}.cab') for keyword in SERVER_FOD_KEYWORDS)

def filter_language_files(files, lang):
    """Dil dosyalarını filtreler."""
    filtered_files = {}
    for filename, file_data in files.items():
        # ESD veya CAB uzantılı dosyaları ve dil kodunu kontrol et
        if not ((filename.endswith(('.esd', '.cab')) and lang in filename) or
                filename.endswith('LanguageExperiencePack_.appx')):
            continue
            
        # Hariç tutulacak belirli dosyaları filtrele
        if any(excluded in filename for excluded in EXCLUDED_FILENAMES):
            continue

        # CAB dosyalarını belirli desenlere göre filtrele
        if any(re.match(pattern, filename) for pattern in CAB_FILTER_PATTERNS):
            continue

        filtered_files[filename] = file_data
    
    return filtered_files

def get_language_files(version_info, lang='tr-tr'):
    """Belirtilen sürüm bilgisine göre dil dosyalarını getirir."""
    base_url = "https://api.uupdump.net/get.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': f'{lang},{lang.split("-")[0]};q=0.9'
    }
    
    params = {
        'id': version_info['id'],
        'lang': lang,
        'edition': 'core'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'response' not in data or 'files' not in data['response']:
            print(f"Invalid response format for {version_info['version']}")
            return None
            
        return filter_language_files(data['response']['files'], lang)
    except Exception as e:
        print(f"Error fetching data for {version_info['version']}: {str(e)}")
        return None

def save_version_data(version_info, lang_files, lang='tr-tr'):
    """Dil dosyalarını JSON formatında kaydeder."""
    if not lang_files:
        print(f"No files to save for {version_info['version']}")
        return
        
    output = {
        'version': version_info['version'],
        'arch': version_info['arch'],
        'updateId': version_info['id'],
        'isWin11': version_info['is_win11'],
        'language': lang,
        'timestamp': datetime.now(UTC).isoformat(),
        'files': lang_files
    }
    
    os_type = 'windows11' if version_info['is_win11'] else 'windows10'
    version_dir = version_info['version'].replace(' ', '_').lower()
    save_dir = f'data/{os_type}/{version_dir}/{version_info["arch"]}/{lang}'
    
    os.makedirs(save_dir, exist_ok=True)
    
    with open(f'{save_dir}/files.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {version_info['version']} ({version_info['arch']})")

def collect_language_files():
    """Dil dosyalarını toplar ve kaydeder."""
    print("Starting language files collection...")
    
    for version in UUP_VERSIONS:
        try:
            print(f"\nProcessing {version['version']} ({version['arch']})...")
            time.sleep(random.uniform(5, 10))  # Rate limiting
            
            lang_files = get_language_files(version)
            if lang_files:
                save_version_data(version, lang_files)
            
        except Exception as e:
            print(f"Error processing {version['version']}: {str(e)}")
            continue

if __name__ == "__main__":
    collect_language_files()
