const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const multer = require('multer');

const app = express();
app.use(cors());
app.use(express.json());

// Set up storage for uploaded images
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = path.join(__dirname, 'images');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'news-' + uniqueSuffix + path.extname(file.originalname));
  }
});
const upload = multer({ storage: storage });

const DATA_FILE = path.join(__dirname, 'data', 'news.json');

// Login endpoint
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === '410') {
    res.json({ success: true, token: 'fake-jwt-token-for-simplicity' });
  } else {
    res.status(401).json({ success: false, message: 'Invalid credentials' });
  }
});

// Middleware to check fake token
const requireAuth = (req, res, next) => {
  const token = req.headers.authorization;
  if (token === 'Bearer fake-jwt-token-for-simplicity') {
    next();
  } else {
    res.status(401).json({ success: false, message: 'Unauthorized' });
  }
};

// Get all news
app.get('/api/news', (req, res) => {
  fs.readFile(DATA_FILE, 'utf8', (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') return res.json([]);
      return res.status(500).json({ error: 'Failed to read data' });
    }
    try {
      res.json(JSON.parse(data));
    } catch(e) {
      res.json([]);
    }
  });
});

// Add new news
app.post('/api/news', requireAuth, upload.single('image'), (req, res) => {
  fs.readFile(DATA_FILE, 'utf8', (err, data) => {
    let news = [];
    if (!err) {
      try { news = JSON.parse(data); } catch(e) {}
    }
    
    const newId = news.length > 0 ? Math.max(...news.map(n => n.id)) + 1 : 1;
    const newEntry = {
      id: newId,
      title: req.body.title,
      image: req.file ? 'images/' + req.file.filename : (req.body.image || ''),
      size: req.body.size || 'small'
    };
    
    news.unshift(newEntry); // Add to beginning
    
    fs.writeFile(DATA_FILE, JSON.stringify(news, null, 2), (err) => {
      if (err) return res.status(500).json({ error: 'Failed to save data' });
      res.json({ success: true, news: newEntry });
    });
  });
});

// Delete news
app.delete('/api/news/:id', requireAuth, (req, res) => {
  const id = parseInt(req.params.id);
  fs.readFile(DATA_FILE, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Failed to read data' });
    
    let news = JSON.parse(data);
    news = news.filter(n => n.id !== id);
    
    fs.writeFile(DATA_FILE, JSON.stringify(news, null, 2), (err) => {
      if (err) return res.status(500).json({ error: 'Failed to save data' });
      res.json({ success: true });
    });
  });
});

// Edit news
app.put('/api/news/:id', requireAuth, upload.single('image'), (req, res) => {
  const id = parseInt(req.params.id);
  fs.readFile(DATA_FILE, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Failed to read data' });
    
    let news = JSON.parse(data);
    const index = news.findIndex(n => n.id === id);
    if (index === -1) return res.status(404).json({ error: 'News not found' });
    
    // Update fields
    if (req.body.title) news[index].title = req.body.title;
    if (req.body.size) news[index].size = req.body.size;
    if (req.file) {
      news[index].image = 'images/' + req.file.filename;
    }
    
    fs.writeFile(DATA_FILE, JSON.stringify(news, null, 2), (err) => {
      if (err) return res.status(500).json({ error: 'Failed to save data' });
      res.json({ success: true, news: news[index] });
    });
  });
});

// Serve static files (with clean URLs support)
app.use(express.static(__dirname, {
  extensions: ['html']
}));

const PORT = 3333;
app.listen(PORT, () => {
  console.log(`Backend Server running on http://localhost:${PORT}`);
});
