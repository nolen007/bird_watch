const express = require('express');
const mysql = require('mysql2');
const path = require('path');
const fs = require('fs').promises; // Using promises for cleaner async/await

const app = express();
const port = 3000;
const wavsDirectory = path.join(__dirname, 'public/wav');

// Serve static files (for the audio)
app.use(express.static('public'));
app.use(express.static(__dirname + '/public'));

// Configure database connection
const db = mysql.createConnection({
  host: '192.168.131.121',     // Replace with your database host
  user: 'root',     // Replace with your database user
  password: 'Glassess14', // Replace with your database password
  database: 'bird_watch'   // Replace with your database name
});
db.connect((err) => {
  if (err) {
    console.error('Database connection failed: ' + err.stack);
    return;
  }
  console.log('Connected to database');
});

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', async (req, res) => {
  const query = `
SELECT CommonName, BeginPath, BeginTime, EndTime, Confidence
FROM (
    SELECT 
        CommonName, 
        BeginPath, 
        BeginTime, 
        EndTime, 
        Confidence,
        ROW_NUMBER() OVER (PARTITION BY BeginPath ORDER BY Confidence DESC) as rn
    FROM bird_data
    WHERE confidence > 0.80 
      AND CommonName != 'nocall'
      AND CommonName != 'Dog'
) AS subquery
WHERE rn = 1
ORDER BY BeginPath DESC;
  `;

  try {
    const [results] = await db.promise().query(query);
    const wavFiles = await fs.readdir(wavsDirectory);
    const wavFileNames = wavFiles.filter(file => file.endsWith('.wav')).map(file => file);

    const birdsWithAudioInfo = results.map(bird => {
      const filenameFromPath = bird.BeginPath ? path.basename(bird.BeginPath) : '';
      const hasMatchingWav = wavFileNames.includes(filenameFromPath);
      const audioPathForPlay = hasMatchingWav ? `/wav/${filenameFromPath}` : null;
      return { ...bird, hasMatchingWav, audioPathForPlay };
    });

    res.render('index', { birds: birdsWithAudioInfo });

  } catch (error) {
    console.error('Error fetching data or reading WAV directory:', error);
    res.status(500).send('Error fetching data');
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
