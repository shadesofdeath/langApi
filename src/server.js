const express = require('express');
const NodeCache = require('node-cache');
const path = require('path');
const fs = require('fs').promises;

const app = express();
const cache = new NodeCache({ stdTTL: 7200 }); // 2 hour cache

// Middleware to parse JSON
app.use(express.json());

// Get all Windows versions
app.get('/api/versions', async (req, res) => {
  try {
    const cachedData = cache.get('versions');
    if (cachedData) {
      return res.json(cachedData);
    }

    const dataPath = path.join(__dirname, '..', 'data', 'windows-versions.json');
    const data = JSON.parse(await fs.readFile(dataPath, 'utf8'));
    
    cache.set('versions', data);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get specific version
app.get('/api/versions/:version', async (req, res) => {
  try {
    const { version } = req.params;
    const { arch } = req.query;

    const cachedData = cache.get('versions');
    let data;
    
    if (cachedData) {
      data = cachedData;
    } else {
      const dataPath = path.join(__dirname, '..', 'data', 'windows-versions.json');
      data = JSON.parse(await fs.readFile(dataPath, 'utf8'));
      cache.set('versions', data);
    }

    const versionData = data[version];
    if (!versionData) {
      return res.status(404).json({ error: 'Version not found' });
    }

    if (arch && versionData.arch !== arch) {
      return res.status(404).json({ error: 'Architecture not found for this version' });
    }

    res.json(versionData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});