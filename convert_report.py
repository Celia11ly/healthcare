import re
import os

# Configuration
SOURCE_FILE = "/Users/Celia/Downloads/yiliao/中国医疗AI大模型行业深度研究报告.md"
OUTPUT_FILE = "/Users/Celia/Downloads/yiliao/report.html"

# Enhanced CSS Styles
CSS = """
:root {
    --primary: #0F4C81; /* Classic Blue - Professional & Medical */
    --primary-translucent: rgba(15, 76, 129, 0.05);
    --secondary: #2C3E50;
    --accent: #E7F1FF;
    --text-primary: #1A202C;
    --text-secondary: #4A5568;
    --bg-page: #F7FAFC;
    --bg-surface: #FFFFFF;
    --sidebar-width: 320px;
    --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.05);
    --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.04);
}

* { box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: var(--bg-page);
    color: var(--text-primary);
    margin: 0;
    line-height: 1.8;
    display: flex;
    -webkit-font-smoothing: antialiased;
}

/* Sidebar Navigation */
.sidebar {
    width: var(--sidebar-width);
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    background: var(--bg-surface);
    border-right: 1px solid rgba(0,0,0,0.06);
    padding: 2.5rem 1.5rem;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 2px 0 12px rgba(0,0,0,0.02);
}

.nav-header {
    margin-bottom: 2.5rem;
    padding-left: 0.8rem;
    border-left: 4px solid var(--primary);
}

.nav-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.nav-subtitle {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

.nav-menu { list-style: none; padding: 0; margin: 0; }
.nav-item { margin-bottom: 0.4rem; }

.nav-link {
    display: block;
    text-decoration: none;
    color: var(--text-secondary);
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-size: 0.92rem;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.nav-link:hover {
    background-color: var(--primary-translucent);
    color: var(--primary);
}

/* Specific Navigation Levels */
.nav-level-1 { display: none; } /* Skip document title in nav */

.nav-level-2 {
    font-weight: 700;
    color: var(--secondary);
    margin-top: 1.2rem;
    font-size: 0.95rem;
}

.nav-level-3 {
    margin-left: 1.2rem;
    font-size: 0.88rem;
    color: #555;
    padding-left: 1rem;
    border-left: 1px solid #eee;
}

.nav-level-3:hover {
    border-left: 2px solid var(--primary);
    padding-left: calc(1rem - 1px);
}

/* Main Content Area */
.main-content {
    margin-left: var(--sidebar-width);
    flex: 1;
    padding: 5rem 8%;
    max-width: 1400px;
    background: var(--bg-page);
}

/* Typography & Content Styling */
.report-title {
    font-size: 2.8rem;
    color: var(--primary);
    font-weight: 800;
    margin-bottom: 3rem;
    text-align: center;
    letter-spacing: -0.5px;
    border-bottom: 3px solid var(--primary);
    padding-bottom: 1.5rem;
}

h1 { display: none; } /* Markdown H1 is usually title, we style separately or handle logic */
/* If H1 is inside content (not title), style it: */
.content-h1 { font-size: 2.4rem; color: var(--primary); margin-bottom: 1.5rem; }

h2 { 
    font-size: 1.8rem; 
    color: var(--secondary); 
    margin-top: 4rem; 
    margin-bottom: 1.8rem; 
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #e2e8f0;
    position: relative;
    font-weight: 700;
}
h2::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 60px;
    height: 4px;
    background: var(--primary);
    border-radius: 2px;
}

h3 { 
    font-size: 1.4rem; 
    color: #2D3748; 
    margin-top: 2.5rem; 
    margin-bottom: 1.2rem; 
    font-weight: 600;
    display: flex;
    align-items: center;
}
h3::before {
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: var(--primary);
    border-radius: 50%;
    margin-right: 12px;
}

p { 
    margin-bottom: 1.5rem; 
    text-align: justify; 
    color: #4A5568;
    font-size: 1.05rem;
}

/* Tables */
.table-container {
    overflow-x: auto;
    margin: 2.5rem 0;
    border-radius: 12px;
    box-shadow: var(--shadow-card);
    background: white;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
    white-space: nowrap;
}

th { 
    background-color: var(--primary); 
    color: white; 
    padding: 1.2rem 1.5rem; 
    text-align: left; 
    font-weight: 600;
}

td { 
    padding: 1rem 1.5rem; 
    border-bottom: 1px solid #EDF2F7; 
    color: #4A5568;
}

tr:last-child td { border-bottom: none; }
tr:nth-child(even) { background-color: #F8FAFC; }
tr:hover { background-color: #F1F9FF; transition: background 0.2s; }

/* Links */
a { 
    color: var(--primary); 
    text-decoration: none; 
    border-bottom: 1px solid rgba(15, 76, 129, 0.3);
    transition: all 0.2s;
}
a:hover { 
    border-bottom-color: var(--primary); 
    background-color: rgba(15, 76, 129, 0.05);
}

/* Blockquotes */
blockquote {
    background-color: white;
    border-left: 5px solid var(--primary);
    padding: 1.5rem 2rem;
    margin: 2rem 0;
    color: #555;
    font-style: italic;
    box-shadow: var(--shadow-card);
    border-radius: 0 8px 8px 0;
}

/* Smooth Scrolling Anchor Offset */
.anchor {
    scroll-margin-top: 40px;
    height: 1px;
    width: 1px;
}

/* Images */
figure {
    margin: 2rem 0;
    text-align: center;
}
img {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: var(--shadow-card);
}
figcaption {
    margin-top: 0.8rem;
    color: #718096;
    font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 1024px) {
    .sidebar { width: 260px; }
    .main-content { margin-left: 260px; padding: 3rem 4%; }
}

@media (max-width: 768px) {
    .sidebar { display: none; } /* Would need mobile menu for full responsive, keeping simple for report */
    .main-content { margin-left: 0; padding: 2rem; }
}
"""

def parse_markdown(text):
    lines = text.split('\n')
    html_content = []
    toc = []
    
    in_table = False
    table_buffer = []
    
    # Extract main title if present (first line #)
    main_title = "行业深度研究报告"
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Check for Main Title (H1) at start
        if i == 0 and stripped_line.startswith('# '):
            main_title = stripped_line[2:].strip()
            html_content.append(f'<div class="report-title">{main_title}</div>')
            continue

        # Headers & TOC
        if stripped_line.startswith('#'):
            level = len(stripped_line.split(' ')[0])
            content = stripped_line.lstrip('#').strip()
            
            # Generate ID
            anchor_id = f"section-{len(toc)}"
            toc.append({'level': level, 'title': content, 'id': anchor_id})
            
            # Add anchor for navigation target
            html_content.append(f'<div id="{anchor_id}" class="anchor"></div>')
            
            # H1 inside body is treated as H2 styling wise or just kept as H1 tag but styled with class
            tag_level = level
            if level == 1: tag_level = 1 # Should be rare if first line captured
            
            html_content.append(f'<h{tag_level}>{content}</h{tag_level}>')
            continue
            
        # Tables
        if '|' in stripped_line:
            # Check if it's a valid table row (simple heuristic)
            if re.match(r'\|?.*\|.*\|?', stripped_line):
                if not in_table:
                    in_table = True
                    html_content.append('<div class="table-container"><table>')
                
                # Check if separator row (---)
                if set(stripped_line.replace('|', '').replace('-', '').replace(':', '').strip()) == set():
                    continue 
                
                # Row processing
                cells = [c.strip() for c in stripped_line.strip('|').split('|')]
                tag = 'th' if len(table_buffer) == 0 else 'td'
                row_html = '<tr>' + ''.join([f'<{tag}>{cell}</{tag}>' for cell in cells]) + '</tr>'
                html_content.append(row_html)
                table_buffer.append(stripped_line)
                continue
        elif in_table:
            in_table = False
            html_content.append('</table></div>')
            table_buffer = []
        
        # Images (![alt](src))
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', stripped_line)
        if img_match:
            alt, src = img_match.groups()
            html_content.append(f'<figure><img src="{src}" alt="{alt}"><figcaption>{alt}</figcaption></figure>')
            continue

        # Standard Text Formatting
        if stripped_line:
            # Skip closing table div if empty line after table
            if in_table: 
                in_table = False
                html_content.append('</table></div>')
                table_buffer = []

            # Bold (**text**)
            line_formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped_line)
            
            # Links ([text](url))
            line_formatted = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', line_formatted)

            # Lists
            if stripped_line.startswith('- ') or stripped_line.startswith('* '):
                # Simple list handling (wrap in ul if sequential is better but p works for simple reading)
                 html_content.append(f'<p style="margin-left: 1.5rem;">• {line_formatted[2:]}</p>')
            else:
                html_content.append(f'<p>{line_formatted}</p>')
            
    return '\n'.join(html_content), toc, main_title

def generate_html():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    body_html, toc, title = parse_markdown(md_text)
    
    # Build Sidebar with Hierarchy
    nav_html = '<ul class="nav-menu">'
    for item in toc:
        if item['level'] == 1: continue # Skip main title
        
        nav_class = f"nav-level-{item['level']}"
        # Only show level 2 and 3 in nav
        if item['level'] > 3: continue 
        
        nav_html += f'<li class="nav-item"><a href="#{item["id"]}" class="nav-link {nav_class}">{item["title"]}</a></li>'
    nav_html += '</ul>'

    # Combine
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>{CSS}</style>
    </head>
    <body>
        <nav class="sidebar">
            <div class="nav-header">
                <div class="nav-title">行业洞察</div>
                <div class="nav-subtitle">2026深度研究报告</div>
            </div>
            {nav_html}
        </nav>
        <main class="main-content">
            {body_html}
        </main>
    </body>
    </html>
    """
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Successfully created {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_html()
