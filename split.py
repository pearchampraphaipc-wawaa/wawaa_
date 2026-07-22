import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the curriculum section
    # We know it starts with <section class="curriculum" id="curriculum">
    # and ends before <!-- NEWS & ACTIVITIES SECTION -->
    
    start_str = '  <!-- ════════════════════════════════════════\n       CURRICULUM SECTION\n       ════════════════════════════════════════ -->\n  <section class="curriculum" id="curriculum">'
    
    end_str = '  <!-- ════════════════════════════════════════\n       NEWS & ACTIVITIES SECTION'
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find section boundaries")
        return
        
    curriculum_section = content[start_idx:end_idx]
    
    # Remove from index.html
    new_index_content = content[:start_idx] + content[end_idx:]
    
    # Also update nav link in index.html
    new_index_content = new_index_content.replace(
        '<a href="#curriculum" class="nav-link">หลักสูตร</a>',
        '<a href="curriculum.html" class="nav-link">หลักสูตร</a>'
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_index_content)
        
    # Create curriculum.html
    # We will use the same header as apply.html
    header = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมปัญญาประดิษฐ์ (AI Engineering)">
  <title>หลักสูตรการศึกษา | วิศวกรรมปัญญาประดิษฐ์</title>
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
  <!-- BACKGROUND ANIMATION -->
  <div class="bg-particles">
    <div class="orb"></div>
    <div class="orb"></div>
    <div class="orb"></div>
  </div>

  <!-- NAVBAR -->
  <nav class="navbar" id="navbar" style="background: rgba(13, 14, 21, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
    <div class="container">
      <a href="index.html" class="nav-logo">
        <div class="logo-icon"><i class="fas fa-robot"></i></div>
        <span>AI Engineering</span>
      </a>

      <ul class="nav-links" id="navLinks">
        <li><a href="index.html" class="nav-link">กลับหน้าหลัก</a></li>
      </ul>
    </div>
  </nav>

  <!-- ADD PADDING FOR NAVBAR -->
  <div style="padding-top: 100px;"></div>
"""

    footer = """
  <!-- ════════════════════════════════════════
       FOOTER
       ════════════════════════════════════════ -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid" style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        <div class="footer-col" style="margin-bottom: 30px;">
          <div class="footer-logo">
            <div class="logo-icon"><i class="fas fa-robot"></i></div>
            <span style="font-size: 1.5rem; font-family: var(--font-heading); font-weight: 700; color: #fff;">AI Engineering</span>
          </div>
          <p style="color: var(--clr-text-muted); line-height: 1.8; margin-top: 15px; max-width: 500px;">
            สร้างวิศวกรปัญญาประดิษฐ์ที่มีคุณภาพ<br>พร้อมขับเคลื่อนอนาคตด้วยเทคโนโลยี AI
          </p>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2026 หลักสูตรวิศวกรรมปัญญาประดิษฐ์และการสั่งการ มหาวิทยาลัยอุบลราชธานี. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="script.js"></script>
  <script>
    // Tab functionality for curriculum
    const yearTabs = document.querySelectorAll('.year-tab');
    const curriculumTables = document.querySelectorAll('.curriculum-tables');

    yearTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-tab');

        // Remove active class from all tabs
        yearTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Hide all curriculum tables
        curriculumTables.forEach(grid => {
          grid.style.display = 'none';
        });

        // Show target grid
        document.getElementById(target).style.display = 'flex';
      });
    });
  </script>
</body>
</html>
"""
    
    with open('curriculum.html', 'w', encoding='utf-8') as f:
        f.write(header + curriculum_section + footer)
        
    print("Successfully created curriculum.html and updated index.html")

if __name__ == '__main__':
    main()
