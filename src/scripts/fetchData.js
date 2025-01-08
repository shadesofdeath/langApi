const fetch = require('node-fetch');
const fs = require('fs').promises;
const path = require('path');

const UUP_TABLE = [
  {
    updateId: 'ad27e52b-9e18-408a-9df2-8688e5273fbf',
    version: 'W11 24H2',
    arch: 'x64',
    isWin11: true
  },
  {
    updateId: 'b6049aaf-4f56-4183-8e58-32954906de64',
    version: 'W11 24H2',
    arch: 'arm64',
    isWin11: true
  },
  {
    updateId: '0c36c0e6-8397-424d-b460-26cc0d044c7f',
    version: 'W11 22H2 & 23H2',
    arch: 'x64',
    isWin11: true
  },
  {
    updateId: 'a2b2e765-4612-44d8-9fb0-b11b699aaf4b',
    version: 'W11 22H2 & 23H2',
    arch: 'arm64',
    isWin11: true
  }
];

const LANGUAGES = [
  { code: 'tr-tr', name: 'Turkish' },
  { code: 'en-us', name: 'English (United States)' },
  { code: 'de-de', name: 'German' },
  { code: 'fr-fr', name: 'French' },
  { code: 'es-es', name: 'Spanish' }
];

async function fetchUUPData(updateId, language) {
  const apiUrl = `https://api.uupdump.net/get.php?id=${updateId}&lang=${language}`;
  const response = await fetch(apiUrl);
  return response.json();
}

function filterFiles(files, language) {
  return Object.entries(files)
    .filter(([name]) => {
      return (name.endsWith('.cab') || name.endsWith('.esd')) &&
             name.includes(language) &&
             !name.match(/(core|professional|coren|professionaln)_.*\.esd$/);
    })
    .map(([name, info]) => ({
      name,
      size: info.size,
      url: info.url
    }));
}

async function main() {
  const data = {
    lastUpdated: new Date().toISOString(),
    versions: []
  };

  for (const version of UUP_TABLE) {
    for (const lang of LANGUAGES) {
      try {
        console.log(`Fetching data for ${version.version} ${lang.code}...`);
        const uupData = await fetchUUPData(version.updateId, lang.code);
        
        if (uupData.response?.files) {
          const files = filterFiles(uupData.response.files, lang.code);
          
          if (files.length > 0) {
            data.versions.push({
              version: version.version,
              arch: version.arch,
              language: lang.name,
              languageCode: lang.code,
              files
            });
          }
        }
        
        // Rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(`Error fetching ${version.version} ${lang.code}:`, error.message);
      }
    }
  }

  // Save data
  await fs.mkdir('./data', { recursive: true });
  await fs.writeFile(
    './data/windows-versions.json',
    JSON.stringify(data, null, 2)
  );
  
  // Create index.html for GitHub Pages
  const html = `
<!DOCTYPE html>
<html>
<head>
    <title>Windows Version API</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-4">Windows Version API</h1>
        <p class="mb-4">Last updated: <span id="lastUpdated"></span></p>
        <pre id="data" class="bg-white p-4 rounded shadow overflow-auto"></pre>
    </div>
    <script>
        fetch('windows-versions.json')
            .then(response => response.json())
            .then(data => {
                document.getElementById('lastUpdated').textContent = new Date(data.lastUpdated).toLocaleString();
                document.getElementById('data').textContent = JSON.stringify(data, null, 2);
            });
    </script>
</body>
</html>`;

  await fs.writeFile('./data/index.html', html);
}

main().catch(console.error);