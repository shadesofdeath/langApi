const axios = require('axios');
const { UUP_TABLE } = require('./config');
const { filterWindowsFiles } = require('./utils');
const fs = require('fs').promises;
const path = require('path');

async function fetchUUPData(updateId, language) {
  const version = UUP_TABLE.find(v => v.updateId === updateId);
  if (!version) {
    throw new Error(`UpdateID '${updateId}' not found`);
  }

  const apiUrl = version.isWin11 
    ? `https://api.uupdump.net/get.php?id=${updateId}&lang=${language}`
    : `https://api.uupdump.net/get.php?id=${updateId}&lang=${language}`;

  const response = await axios.get(apiUrl);
  return response.data;
}

async function fetchAllData() {
  const results = {};

  for (const version of UUP_TABLE) {
    try {
      // Fetch data for en-us as base language
      const data = await fetchUUPData(version.updateId, 'en-us');
      
      if (data.error) {
        console.error(`Error fetching ${version.version}: ${data.error}`);
        continue;
      }

      const filteredFiles = Object.entries(data.response.files)
        .filter(([name, info]) => filterWindowsFiles({ name, ...info }, 'en-us', true))
        .reduce((acc, [name, info]) => {
          acc[name] = {
            url: info.url,
            size: info.size,
            arch: version.arch
          };
          return acc;
        }, {});

      results[version.version] = {
        updateId: version.updateId,
        arch: version.arch,
        isWin11: version.isWin11,
        files: filteredFiles
      };
    } catch (error) {
      console.error(`Error processing ${version.version}:`, error.message);
    }
  }

  // Save results to data file
  const dataPath = path.join(__dirname, '..', 'data');
  await fs.mkdir(dataPath, { recursive: true });
  await fs.writeFile(
    path.join(dataPath, 'windows-versions.json'),
    JSON.stringify(results, null, 2)
  );

  return results;
}

// Run if called directly
if (require.main === module) {
  fetchAllData().catch(console.error);
}

module.exports = { fetchAllData };