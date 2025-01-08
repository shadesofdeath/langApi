import json
import os
import requests
from datetime import datetime, UTC
import time
import random

# Filtreleme için FOD keywordleri
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
    'amd64_Microsoft-Windows-LanguageFeatures-Basic-.*-Package_.*\.cab',
    'amd64_Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package_.*\.cab',
    'amd64_Microsoft-Windows-LanguageFeatures-OCR-.*-Package_.*\.cab',
    'amd64_Microsoft-Windows-LanguageFeatures-TextToSpeech-.*-Package_.*\.cab',
    'amd64_Microsoft-OneCore-DeveloperMode-Desktop-Package_.*\.cab',
    'amd64_Microsoft-Windows-LanguageFeatures-Speech-.*-Package_.*\.cab',
    'Microsoft-AzureStack-HCI-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-OneCore-StorageManagement-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-OneCore-StorageManagement-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-ActiveDirectory-DS-LDS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-ActiveDirectory-DS-LDS-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-BitLocker-Recovery-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-CertificateServices-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Composition-Test-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Composition-Test-FOD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-DHCP-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-DHCP-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-DNS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-DNS-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-EMS-SAC-Desktop-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-FailoverCluster-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-FailoverCluster-Management-Tools-FOD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-FileServices-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-FileServices-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-GroupPolicy-Management-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-GroupPolicy-Management-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-InternetExplorer-Optional-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-IPAM-Client-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-IPAM-Client-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-IRDA-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-IRDA-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-LanguageFeatures-Basic-.*-Package-amd64_.*\.cab',
    'Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package-amd64\.cab',
    'Microsoft-Windows-LanguageFeatures-Handwriting-.*-Package-amd64_.*\.cab',
    'Microsoft-Windows-LanguageFeatures-OCR-.*-Package-amd64_.*\.cab',
    'Microsoft-Windows-LanguageFeatures-TextToSpeech-.*-Package-amd64_.*\.cab',
    'Microsoft-Windows-Media-Features-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Media-Features-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-MSPaint-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-MSPaint-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-NetworkController-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-NetworkLoadBalancing-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Notepad-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Notepad-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-Notepad-System-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Notepad-System-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-PowerShell-ISE-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-PowerShell-ISE-FOD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-Printing-PMCPPC-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Printing-WFS-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-RasCMAK-Client-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-RasCMAK-Client-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-RasRip-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-RemoteAccess-Management-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-RemoteAccess-Management-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-RemoteDesktop-Services-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-Server-AppCompat-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-ServerManager-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-ServerManager-Tools-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-SnippingTool-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-SNMP-Client-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-SNMP-Client-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-StepsRecorder-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-StepsRecorder-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-StorageManagement-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-StorageManagement-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-StorageMigrationService-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-StorageReplica-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-StorageReplica-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-SystemInsights-Management-Tools-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-TPM-Diagnostics-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-TPM-Diagnostics-FOD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-VolumeActivation-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-WirelessDisplay-FOD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-WMI-SNMP-Provider-Client-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-WMI-SNMP-Provider-Client-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-WordPad-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-WordPad-FoD-Package-wow64-.*-.*_.*\.cab',
    'Microsoft-Windows-WSUS-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-OneCore-DeveloperMode-Desktop-Package-amd64_.*\.cab',
    'Microsoft-Windows-Shielded-VM-Tools-FoD-Package-amd64-.*-.*_.*\.cab',
    'Microsoft-Windows-LanguageFeatures-Speech-.*-Package-amd64_.*\.cab'
]
def is_server_fod(filename, lang):
    lang = lang.rstrip('-')
    for keyword in SERVER_FOD_KEYWORDS:
        if keyword in filename and filename.endswith(f'{lang}.cab'):
            return True
    return False

def filter_language_files(files, lang):
    filtered_files = {}
    for filename, file_data in files.items():
        # Temel dosya türü kontrolü
        if not ((filename.endswith(('.esd', '.cab')) and lang in filename) or
                filename.endswith('LanguageExperiencePack_.appx')):
            continue

        # ESD dosya filtreleme
        if any(x in filename for x in [
            'core_', 'professional_', 'coren_', 'professionaln_',
            'PPIPro_', 'ServerDatacenter_', 'ServerStandard_',
            'ServerTurbine_'
        ]):
            continue

        # CAB dosya filtreleme
        if any(re.match(pattern, filename) for pattern in CAB_FILTER_PATTERNS):
            continue

        filtered_files[filename] = file_data
    return filtered_files

def collect_language_files():
    base_url = "https://api.uupdump.net/get.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'tr-TR,tr;q=0.9'
    }

    for version in UUP_VERSIONS:
        try:
            time.sleep(random.uniform(10, 15))
            
            params = {
                'id': version['id'],
                'lang': 'tr-tr',
                'edition': 'core'
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} for {version['version']}")
                continue

            data = response.json()
            if 'response' not in data or 'files' not in data['response']:
                continue

            lang_files = filter_language_files(data['response']['files'], 'tr-tr')
            
            if not lang_files:  # Eğer filtreleme sonrası dosya kalmadıysa
                continue

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