const express = require('express');
const cors = require('cors');
const compression = require('compression');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(compression());

// Cache data in memory
let cachedData = null;
let lastCacheUpdate = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

async function loadData() {
  const now = Date.now();
  if (cachedData && (now - lastCacheUpdate) < CACHE_DURATION) {
    return cachedData;
  }
  
  const data = await fs.readFile(
    path.join(__dirname, '../data/windows-versions.json'),
    'utf-8'
  );
  cachedData = JSON.parse(data);
  lastCacheUpdate = now;
  return cachedData;
}

app.get('/api/windows-versions', async (req, res) => {
  try {
    const data = await loadData();
    
    // Apply filters if provided
    const { version, arch, language } = req.query;
    let filteredData = { ...data };
    
    if (version || arch || language) {
      filteredData.versions = data.versions.filter(v => 
        (!version || v.version === version) &&
        (!arch || v.arch === arch) &&
        (!language || v.languageCode === language)
      );
    }
    
    res.json(filteredData);
  } catch (error) {
    console.error('Error serving data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});