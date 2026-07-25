const fs = require('fs');
const lines = fs.readFileSync('curriculum.html', 'utf8').split('\n');
const line = lines[159]; // index 159 is line 160
console.log(JSON.stringify(line));
