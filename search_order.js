const fs = require('fs');
const xml = fs.readFileSync('doc.xml', 'utf8');

// Strip XML tags to get plain text
const text = xml.replace(/<w:p[ >]/g, '\n').replace(/<[^>]+>/g, '');
const lines = text.split('\n');

const allNames = [
  'ฐิตินนท์', 'ระพีพันธ์', 'สุรเจษฐ์', 'ถนัดกิจ', 'นลิน', 'อธิพงศ์', 'สุชิน', 'สมบัติ', 
  'ฐิติวรดา', 'นันทวัฒน์', 'ธรรมรส', 'กันตภณ', 'ศุภฤกษ์', 'ธารชุดา', 'อารยา'
];

let started = false;
let order = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  if (line.includes('ประวัติและผลงานของอาจารย์ประจำหลักสูตรและอาจารย์ผู้สอน')) {
    started = true;
  }
  
  if (started) {
    if (line.includes('1. ชื่อ') || line.includes('ชื่อ - นามสกุล') || line.includes('นาย') || line.includes('นาง')) {
       for (const name of allNames) {
          if (line.includes(name) && !order.includes(name)) {
             order.push(name);
          }
       }
    }
  }
}

console.log("Found order:");
order.forEach((n, i) => console.log(`${i+1}. ${n}`));

// Check if any were missed
const missed = allNames.filter(n => !order.includes(n));
console.log("Missed:", missed);
