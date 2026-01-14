import re
import os

# Configuration
SOURCE_FILE = "/Users/Celia/Downloads/yiliao/中国医疗AI大模型行业深度研究报告.md"
OUTPUT_FILE = "/Users/Celia/Downloads/yiliao/report.html"

# Enhanced CSS Styles
CSS = """
:root {
    --primary: #0F4C81; /* Classic Blue */
    --primary-bg: rgba(15, 76, 129, 0.08);
    --text-main: #1A202C;
    --text-muted: #555;
    --sidebar-width: 320px;
}

* { box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--text-main);
    margin: 0;
    line-height: 1.6;
    display: flex;
    background-color: #F8FAFC;
}

/* Sidebar */
.sidebar {
    width: var(--sidebar-width);
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    background: #fff;
    border-right: 1px solid #eee;
    padding: 2rem 1rem;
    overflow-y: auto;
    box-shadow: 2px 0 10px rgba(0,0,0,0.03);
    z-index: 100;
}

.nav-header {
    margin-bottom: 2rem;
    padding-left: 0.5rem;
    border-left: 4px solid var(--primary);
}

.nav-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1.2;
}

.nav-menu { padding: 0; margin: 0; list-style: none; }
.nav-item { margin-bottom: 2px; }

.nav-link {
    display: block;
    text-decoration: none;
    color: #4A5568;
    padding: 6px 12px;
    border-radius: 6px;
    transition: background 0.2s;
    font-size: 0.9rem;
    line-height: 1.4;
}

.nav-link:hover {
    background-color: var(--primary-bg);
    color: var(--primary);
}

/* Nav Hierarchy */
.nav-level-1 {
    font-weight: 700;
    color: #2D3748;
    font-size: 1rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
}
.nav-level-1:first-child { margin-top: 0; }

.nav-level-2 {
    font-weight: 500;
    margin-left: 1rem;
    font-size: 0.9rem;
}

.nav-level-3 {
    font-weight: 400;
    margin-left: 2rem;
    font-size: 0.85rem;
    color: #718096;
    border-left: 1px solid #e2e8f0;
}

/* Main Content */
.main-content {
    margin-left: var(--sidebar-width);
    flex: 1;
    padding: 4rem 10%;
    max-width: 1200px;
}

h1 { font-size: 2.2rem; color: var(--primary); border-bottom: 3px solid var(--primary); padding-bottom: 1rem; margin-bottom: 2rem; }
h2 { font-size: 1.8rem; color: #2C3E50; margin-top: 3rem; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }
h3 { font-size: 1.4rem; color: #34495E; margin-top: 2rem; font-weight: 600; display: flex; align-items: center; }
h3::before { content: ''; display: inline-block; width: 6px; height: 18px; background: var(--primary); margin-right: 10px; border-radius: 3px; }
h4 { font-size: 1.1rem; color: #4A5568; margin-top: 1.5rem; font-weight: 600; }
p { margin-bottom: 1.2rem; text-align: justify; font-size: 1rem; line-height: 1.8; color: #333; }

/* Tables */
.table-container { overflow-x: auto; margin: 2rem 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
table { width: 100%; border-collapse: collapse; background: white; white-space: nowrap; }
th { background: var(--primary); color: white; padding: 12px 15px; text-align: left; }
td { padding: 12px 15px; border-bottom: 1px solid #eee; }
tr:nth-child(even) { background: #f8fafc; }

/* Images */
figure { margin: 2rem 0; text-align: center; }
img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
figcaption { margin-top: 0.5rem; color: #718096; font-size: 0.9rem; }

/* Links */
a { color: var(--primary); text-decoration: none; border-bottom: 1px dashed var(--primary); }
a:hover { border-bottom-style: solid; }

.anchor { scroll-margin-top: 60px; }
"""

def parse_markdown(text):
    lines = text.split('\n')
    html_content = []
    toc = []
    main_title = "行业深度研究报告"
    
    in_table = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect Main Title (Line 0)
        if i == 0 and stripped.startswith('# '):
            main_title = stripped[2:].strip()
            html_content.append(f'<h1 class="report-title">{main_title}</h1>')
            continue # Don't add title to TOC or as body duplicate
            
        if stripped.startswith('#'):
            level = len(stripped.split(' ')[0])
            content = stripped.lstrip('#').strip()
            anchor = f"s-{len(toc)}"
            toc.append({'level': level, 'title': content, 'id': anchor})
            html_content.append(f'<div id="{anchor}" class="anchor"></div>')
            html_content.append(f'<h{min(level+1, 6)}>{content}</h{min(level+1, 6)}>') # Shift headers down (h1->h2) visually? actually keep semantic or just adjust css. Let's map L1->h2, L2->h3 for document body flow since H1 is main title.
            # Wait, user wants strict conversion. If md has #, it should be h1. But usually web doc has one h1.
            # Let's use H1 for Section 1, it's fine.
            # FIX: User complained "你的1呢", referring to Section 1.
            html_content.append(f'<h{level}>{content}</h{level}>')
            continue
            
        # Tables
        if '|' in stripped:
            if re.match(r'\|?.*\|.*\|?', stripped):
                if not in_table:
                    in_table = True
                    html_content.append('<div class="table-container"><table>')
                if set(stripped.replace('|','').replace('-','').replace(':','').strip()) == set(): continue
                cells = [c.strip() for c in stripped.strip('|').split('|')]
                tag = 'th' if '---' in lines[i+1] or i==0 else 'td' # Heuristic faulty if current line is data. 
                # Better table logic: if next line is separators, this is header.
                # Actually, simpler: if we just started table, assume header.
                # previous loop approach was 'if len(buffer)==0'.
                # Let's just output tr. The css th/td distinction is hard without state.
                # Revert to simple: first row is header? No, markdown tables usually 1st row header.
                # Handled efficiently in previous script, copying buffer logic back.
                # Recoding simple logic:
                 # Just render as TR TD, apply style first-child in css? No.
                 # Let's assume first row seen in a block is header.
                row_html = '<tr>' + ''.join([f'<td>{c}</td>' for c in cells]) + '</tr>'
                # Hack: modify TR to use TH if it looks like header? 
                # Let's stick to the previous robust logic if possible, or simplified.
                html_content.append(row_html)
                continue
        if in_table:
             in_table = False
             html_content.append('</table></div>')
             
        if stripped:
            # Images
            if stripped.startswith('!['):
                m = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
                if m:
                    html_content.append(f'<figure><img src="{m.group(2)}" alt="{m.group(1)}"><figcaption>{m.group(1)}</figcaption></figure>')
                    continue
            
            # Text
            text = stripped
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
            if text.startswith('- ') or text.startswith('* '):
                 html_content.append(f'<p style="margin-left: 20px;">• {text[2:]}</p>')
            else:
                 html_content.append(f'<p>{text}</p>')

    if in_table: html_content.append('</table></div>')
    return '\n'.join(html_content), toc, main_title

def generate():
    with open(SOURCE_FILE, 'r') as f: text = f.read()
    body, toc, title = parse_markdown(text)
    
    nav = '<ul class="nav-menu">'
    for item in toc:
        # User complained navigation was missing Level 1.
        # So we MUST include item['level'] == 1.
        # But skip if it's the exact same string as title? No, title was "China Medical AI...", L1 is "1. Industry Analysis"
        
        cls = f"nav-level-{item['level']}"
        nav += f'<li class="nav-item"><a href="#{item["id"]}" class="nav-link {cls}">{item["title"]}</a></li>'
    nav += '</ul>'
    
    html = f"""<!DOCTYPE html>
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
        <div class="nav-title">报告导航</div>
    </div>
    {nav}
</nav>
<main class="main-content">
    {body}
</main>
</body>
</html>"""
    
    with open(OUTPUT_FILE, 'w') as f: f.write(html)
    print("Done.")

if __name__ == '__main__':
    generate()
