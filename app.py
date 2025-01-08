# Parametre tanımlaması
param (
    [Parameter(Mandatory = $false)]
    [string]$OutputPath = 'uup_data.json'
)

# Data definitions
$script:UUP_Table = ConvertFrom-Csv @'
UpdateID,Version,Arch,IsWin11
ad27e52b-9e18-408a-9df2-8688e5273fbf,"W11 24H2",x64,true
b6049aaf-4f56-4183-8e58-32954906de64,"W11 24H2",arm64,true
30da46b4-2ff2-4682-a9ae-23b66dd98713,"W11 Server version 24H2",x64,true
fb12fdae-dd42-4d2d-b8cc-380a968e8d10,"W11 Server version 24H2",arm64,true
ebf14a71-0f6e-4958-9bf4-27c746050640,"W11 Server version 23H2",x64,true
9310ebcc-79ee-40aa-ae4a-4da849dd4684,"W10 Server version 22H2",x64,False
2ba1d737-a36b-415b-a630-85bd5146d77d,"W10 Server version 21H2",x64,false
0c36c0e6-8397-424d-b460-26cc0d044c7f,"W11 22H2 & 23H2",x64,true
a2b2e765-4612-44d8-9fb0-b11b699aaf4b,"W11 22H2 & 23H2",arm64,true
35630b7b-4509-45b6-83a1-d4c75d5aa9b6,"W11 21H2",x64,true
fba7e852-3fcc-4dad-8561-42c455cfffd7,"W11 21H2",arm64,true
e1885854-aea0-453d-9e64-bfd00535a925,"W10 22H2",x64,false
21dec2dc-8213-4021-a31c-7dd07e034dd5,"W10 22H2",x86,false
d1aaf6a7-c80b-49bb-8d79-99b6a3cfb5c1,"W10 22H2",arm64,false
3ead9b43-aa9d-4973-8195-24be0b0ce1e1,"W10 2004, 20H2, 21H1, 21H2",x64,false
70f4293c-6eaa-4db5-b059-9755ab5628d8,"W10 2004, 20H2, 21H1, 21H2",x86,false
bb720c43-af68-4dc6-a397-42f278183314,"W10 2004, 20H2, 21H1, 21H2",arm64,false
9005d4cd-fce9-466b-b98e-a67414acebd8,"W10 1809",x64,false
dcb2f7dd-8822-444b-802f-d417e19474a9,"W10 1809",x86,false
5a143235-5474-4cfa-9078-65e434d9df67,"W10 1809",arm64,false
'@

$script:RegionTable = ConvertFrom-Csv @'
Region,Language
ar-sa,Arabic
bg-bg,Bulgarian
cs-cz,Czech
da-dk,Danish
de-de,German
el-gr,Greek
en-gb,English (United Kingdom)
en-us,English (United States)
es-es,Spanish
es-mx,Spanish (Mexico)
et-ee,Estonian
fi-fi,Finnish
fr-ca,French (Canada)
fr-fr,French
he-il,Hebrew
hr-hr,Croatian
hu-hu,Hungarian
it-it,Italian
ja-jp,Japanese
ko-kr,Korean
lt-lt,Lithuanian
lv-lv,Latvian
nb-no,Norwegian
nl-nl,Dutch
pl-pl,Polish
pt-br,Portuguese (Brazil)
pt-pt,Portuguese
ro-ro,Romanian
ru-ru,Russian
sk-sk,Slovak
sl-si,Slovenian
sr-latn-rs,Serbian (Latin)
sv-se,Swedish
th-th,Thai
tr-tr,Turkish
uk-ua,Ukrainian
zh-cn,Chinese (Simplified)
zh-tw,Chinese (Traditional)
'@

# Server FOD keywords - moved to a separate array for better maintainability
$script:ServerFODKeywords = @(
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
)


function Test-IsServerFOD {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FileName,
        [Parameter(Mandatory=$true)]
        [string]$Language
    )
    
    $locale = $Language -replace '-$'
    foreach ($keyword in $script:ServerFODKeywords) {
        if ($FileName -match [regex]::Escape($keyword) + ".*$locale\.cab$") {
            return $true
        }
    }
    return $false
}

function Test-IsValidFileType {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FileName,
        [Parameter(Mandatory=$true)]
        [string]$Language
    )
    
    return ($FileName -match '\.(esd|cab)$' -and $FileName -match $Language) -or
           ($FileName -match 'LanguageExperiencePack_.*\.appx$')
}

# Unified file filtering function
function Filter-WindowsFiles {
    param (
        [Parameter(Mandatory=$true)]
        [PSObject]$File,
        [Parameter(Mandatory=$true)]
        [string]$Language,
        [Parameter(Mandatory=$false)]
        [bool]$HideServerFODs = $false
    )
    
    # First check if it's a valid file type
    if (-not (Test-IsValidFileType -FileName $File.Name -Language $Language)) {
        return $false
    }
    
    # If hiding server FODs is enabled, check if this is a server FOD
    if ($HideServerFODs -and (Test-IsServerFOD -FileName $File.Name -Language $Language)) {
        return $false
    }
    
    # Always hide specific ESD files
if ($File.Name -match 'core_.*\.esd$' -or 
    $File.Name -match 'professional_.*\.esd$' -or 
    $File.Name -match 'coren_.*\.esd$' -or 
    $File.Name -match 'professionaln_.*\.esd$' -or 
    $File.Name -match 'PPIPro_.*\.esd$' -or
    $File.Name -match 'ServerDatacenter_.*\.esd$' -or
    $File.Name -match 'ServerStandard_.*\.esd$' -or
    $File.Name -match 'ServerTurbine_.*\.esd$') {
    return $false
}

    
    # Always hide specific CAB files
    $alwaysHideCABFilesPatterns = @(
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
        'Microsoft-Windows-WSUS-Tools-FoD-Package-amd64-.*-.*_.*\.cab'
        'Microsoft-OneCore-DeveloperMode-Desktop-Package-amd64_.*\.cab',
        'Microsoft-Windows-Shielded-VM-Tools-FoD-Package-amd64-.*-.*_.*\.cab'
         'Microsoft-Windows-LanguageFeatures-Speech-.*-Package-amd64_.*\.cab'
    )
    
    foreach ($pattern in $alwaysHideCABFilesPatterns) {
        if ($File.Name -match $pattern) {
            return $false
        }
    }
    
    return $true
}


function Get-UUPFiles {
    param (
        [Parameter(Mandatory=$true)]
        [string]$UpdateID,
        [Parameter(Mandatory=$false)]
        [string]$Language = $null
    )

    $record = $script:UUP_Table | Where-Object { $_.UpdateID -eq $UpdateID }

    if ($null -eq $record) {
        throw "UpdateID '$UpdateID' not found in the UUP_Table."
    }

    if ($record.IsWin11 -eq "true") {
        $apiUrl = "https://api.uupdump.net/get.php?id=$UpdateID&lang=$Language"
    } else {
        if ($Language -eq $null) {
            throw "Language parameter is mandatory for Windows 10 updates."
        }
        $apiUrl = "https://api.uupdump.net/get.php?id=$UpdateID&$desiredEdition"
    }

    return Invoke-RestMethod -Uri $apiUrl -Method Get
}

# Main script logic
$allData = @{}

foreach ($item in $script:UUP_Table) {
    $updateID = $item.UpdateID
    $version = $item.Version
    $arch = $item.Arch
    
    Write-Host "Processing: Version=$version, Arch=$arch, UpdateID=$updateID"
    
    $allData[$updateID] = @{
    'Version' = $version;
    'Arch' = $arch;
    'Languages' = @{}
    }
    
     foreach ($langItem in $script:RegionTable) {
        $languageRegion = $langItem.Region
        $languageName = $langItem.Language
         try {
                $response = Get-UUPFiles -UpdateID $updateID -Language $languageRegion
                if ($response.error) {
                    Write-Host "  Error for language '$languageName' ($languageRegion): $($response.error)"
                }
                elseif ($response.response -and $response.response.files) {
                    $filteredFiles = @()
                    foreach ($file in $response.response.files.PSObject.Properties) {
                        if (Filter-WindowsFiles -File $file -Language $languageRegion) {
                            $filteredFiles += @{
                            'Name' = $file.Name;
                            'Size' = [Math]::Round($file.Value.size / 1MB, 2);
                            'URL' = $file.Value.url
                            }
                        }
                    }
                    if ($filteredFiles.Count -gt 0) {
                    $allData[$updateID].Languages[$languageRegion] = @{
                         'LanguageName' = $languageName
                        'Files' = $filteredFiles
                         }
                    Write-Host "  Success for language '$languageName' ($languageRegion), $($filteredFiles.Count) files found."
                    }else {
                            Write-Host "  No files found for '$languageName' ($languageRegion)."
                    }
                } else {
                   Write-Host "   API did not return files for language '$languageName' ($languageRegion)." 
                }
          }
           catch {
                Write-Host "  Error processing language '$languageName' ($languageRegion): $($_.Exception.Message)"
           }
     }
}

# Convert to JSON and save to file
$allData | ConvertTo-Json -Depth 10 | Out-File $OutputPath
Write-Host "Data saved to: $OutputPath"