import re
import os

# Configuration
SOURCE_FILE = "/Users/Celia/Downloads/yiliao/中国医疗AI大模型行业深度研究报告.md"
OUTPUT_FILE = "/Users/Celia/Downloads/yiliao/report.html"

# Enhanced CSS Styles (V19 Visual Polish)
CSS = """
:root {
    --primary: #1A365D; /* Navy Blue (Level 1) */
    --primary-bg: #EBF8FF;
    --secondary: #2C7A7B; /* Teal (Level 2 Text) */
    --secondary-bg: #E6FFFA;
    --h4-color: #276749; /* Dark Green (Level 3 Header) */
    --h4-bg: #F0FFF4; /* Light Green Bg */
    --highlight: #C05621; /* Deep Orange (Keywords in Text) */
    --dimension-label: #319795; /* Teal (Dimension Keys) */
    --text-main: #2D3748;
    --text-muted: #718096;
    --sidebar-width: 320px;
}

* { box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--text-main);
    margin: 0;
    line-height: 1.85;
    display: flex;
    background-color: #F7FAFC;
    font-size: 16px;
}

/* ---------------- Sidebar Navigation ---------------- */
.sidebar {
    width: var(--sidebar-width);
    height: 100vh;
    position: sticky;
    top: 0;
    flex-shrink: 0;
    background: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    padding: 2rem 1rem;
    overflow-y: auto;
    z-index: 100;
    box-shadow: 2px 0 15px rgba(0,0,0,0.02);
}

.nav-header { 
    margin-bottom: 2rem; 
    padding-left: 1rem; 
    border-left: 6px solid var(--primary); 
}
.nav-title { font-size: 1.3rem; font-weight: 800; color: var(--primary); }

.nav-menu { padding: 0; margin: 0; list-style: none; }
.nav-item { margin-bottom: 2px; }

.nav-link {
    display: block;
    text-decoration: none;
    color: #4A5568;
    padding: 8px 12px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 0.9rem;
    border-left: 3px solid transparent; /* Be careful not to double borders with specific level classes */
}
.nav-link:hover { background-color: #F7FAFC; /* Subtler hover for generic */ }

/* Level 1: Main Chapters */
.nav-level-1 {
    font-weight: 800;
    color: #1A365D;
    font-size: 1rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    background-color: #EBF8FF;
    padding: 10px 12px;
    border-radius: 6px;
    border-left: 5px solid #2B6CB0; /* Stronger L1 marker */
}

/* Level 2: Sub-sections */
.nav-level-2 {
    font-weight: 600;
    font-size: 0.9rem;
    color: #2D3748;
    margin-left: 1rem; /* Indent L2 block */
    padding-left: 12px;
    border-left: 2px solid #CBD5E0;
}
.nav-link.nav-level-2:hover { border-left-color: var(--secondary); background-color: #F7FAFC; }

/* Level 3: Details */
.nav-link.nav-level-3 {
    font-weight: 400;
    font-size: 0.8rem !important; /* Force smaller size */
    color: #64748B; /* Slate 500 - Distinct from L2 */
    margin-left: 0; 
    padding-left: 3.5rem; /* Large indent for L3 */
    border-left: none;
}
.nav-link.nav-level-3:hover { color: var(--h4-color); background-color: #F0FFF4; }


/* Collapsible Nav Styles */
.nav-group {
    display: none;
    padding-left: 0;
    margin: 0;
    list-style: none;
    transition: all 0.3s ease;
}

.nav-item.expanded > .nav-group {
    display: block;
}

.nav-item-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px 0;
    cursor: pointer;
    width: 100%;
}

.nav-link {
    flex: 1; /* Take up remaining space */
    text-align: left;
    display: block;
    text-decoration: none;
    color: #4A5568;
    padding: 8px 12px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 0.9rem;
    border-left: 3px solid transparent;
}

.nav-toggle {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #A0AEC0;
    font-size: 0.8rem;
    transition: transform 0.2s;
    margin-left: 4px; /* Changed from margin-right */
}

.nav-item.expanded > .nav-item-container .nav-toggle {
    transform: rotate(90deg);
}

.nav-group .nav-link {
    border-left: none !important;
}


/* ---------------- Main Content ---------------- */
.main-content {
    flex: 1;
    padding: 5rem 10%;
    max-width: 1300px;
    background: white;
    min-height: 100vh;
}

/* Title */
.report-title {
    font-size: 3rem;
    color: var(--primary);
    text-align: center;
    margin-bottom: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--primary) 0%, #2B6CB0 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* H2: Level 1 Header (Big Blue Block) */
h2 {
    font-size: 2.2rem;
    color: #FFFFFF;
    margin-top: 6rem;
    margin-bottom: 2.5rem;
    padding: 1.2rem 2rem;
    background: linear-gradient(90deg, #1A365D 0%, #2A4365 100%);
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    font-weight: 700;
}

/* H3: Level 2 Header (Teal with MATCHING Underline - User Requested) */
/* Changed underline color to match text */
h3 {
    font-size: 1.7rem;
    color: var(--secondary);
    margin-top: 4rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
    border-bottom: 3px solid var(--secondary); /* Matching Teal Border */
    padding-bottom: 0.5rem;
    display: inline-block;
}

/* H4: Level 3 Header (Green Box Style - User Requested) */
/* Changed from Purple to Green */
h4 {
    font-size: 1.3rem;
    color: var(--h4-color); /* Dark Green */
    background-color: var(--h4-bg); /* Light Green Bg */
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    padding: 12px 18px;
    border-left: 6px solid var(--h4-color); /* Green Border */
    border-radius: 4px 8px 8px 4px;
    font-weight: 700;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}

/* H5: Level 4 Header (Sub-item Title) */
h5 {
    font-size: 1.15rem;
    color: #2B6CB0; /* Blue-ish */
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    font-weight: 700;
    padding-left: 10px;
    border-left: 4px solid #BEE3F8;
}

p { margin-bottom: 1.5rem; text-align: justify; color: #4A5568; }

/* ---------------- Dimensions & Keywords ---------------- */

/* Dimension Labels (Teal / Boxed) */
/* These are the "Action:", "Logic:" labels */
.dimension-item {
    margin-bottom: 1.2rem;
    background: #F8FAFC;
    padding: 1.2rem;
    border-radius: 8px;
    border-left: 4px solid var(--dimension-label); /* ROI: Sideline instead of Topline */
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}
.dimension-label {
    color: var(--dimension-label);
    font-weight: 800;
    font-size: 1.05rem;
    margin-right: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: var(--secondary-bg);
    padding: 2px 8px;
    border-radius: 4px;
}

/* KEYWORDS (In-Text Bold) - User requested DISTINCT from Title colors */
/* Using Deep Orange/Rust to separate from Teal/Green headers */
strong {
    color: var(--highlight); 
    font-weight: 700;
    padding: 0 2px;
}

/* Citations (Gray/Small) */
.citation {
    font-size: 0.9rem;
    color: #718096;
    font-style: italic;
    background-color: #F7FAFC;
    padding: 1rem;
    border-left: 4px solid #CBD5E0;
    margin: 2rem 0;
}
.mini-citation {
    font-size: 0.85em;
    color: #A0AEC0;
    font-weight: 400;
}

/* Tables */
.table-container { margin: 3rem 0; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; }
table { width: 100%; border-collapse: collapse; }
th { background-color: #EBF8FF; color: var(--primary); padding: 18px; border-bottom: 2px solid #BFDBFE; }
td { padding: 16px 18px; border-bottom: 1px solid #EDF2F7; vertical-align: middle; }
tr:hover { background-color: #F7FAFC; }

/* Images */
figure { margin: 3rem 0; text-align: center; padding: 1.5rem; border: 1px dashed #CBD5E0; border-radius: 12px; }
img { max-width: 95%; border-radius: 6px; }
figcaption { color: #718096; margin-top: 1rem; font-style: italic; }

.anchor { scroll-margin-top: 100px; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 4px; }
"""

def parse_markdown(text):
    lines = text.split('\n')
    html_content = []
    toc = []
    main_title = "行业深度研究报告"
    
    in_table = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect Main Title
        if i == 0 and stripped.startswith('# '):
            main_title = stripped[2:].strip()
            continue 
            
        # Headers
        if stripped.startswith('#'):
            level = len(stripped.split(' ')[0])
            content = stripped.lstrip('#').strip()
            anchor = f"s-{len(toc)}"
            toc.append({'level': level, 'title': content, 'id': anchor})
            html_content.append(f'<div id="{anchor}" class="anchor"></div>')
            html_tag = f"h{min(level + 1, 6)}"
            html_content.append(f'<{html_tag}>{content}</{html_tag}>')
            continue
            
        # Tables
        if '|' in stripped and re.match(r'\|?.*\|.*\|?', stripped):
            if not in_table:
                in_table = True
                html_content.append('<div class="table-container"><table>')
            
            # Separator
            if set(stripped.replace('|','').replace('-','').replace(':','').strip()) == set():
                continue
            
            cells = [c.strip().replace('**', '') for c in stripped.strip('|').split('|')]
            row_html = '<tr>' + ''.join([f'<td>{c}</td>' for c in cells]) + '</tr>'
            html_content.append(row_html)
            continue
        if in_table:
             in_table = False
             html_content.append('</table></div>')
             
        if stripped:
            # Images
            m_img = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
            if m_img:
                html_content.append(f'<figure><img src="{m_img.group(2)}" alt="{m_img.group(1)}"><figcaption>{m_img.group(1)}</figcaption></figure>')
                continue
            
            text = stripped
            
            # Bold Processing
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            
            # Link Processing
            text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
            
            # Special Dimension Styling (Platform/Tech/Biz)
            # Expanded list to cover Section 2, 3, 4 items (Business Logic, Pain Points, Scenarios, etc.)
            dimension_keys = r"(平台定位|技术/产品细节|技术细节|商业模式|核心产品|战略定位|特色|定位|核心技术|AI应用|产品规划|变现产品|关键动作|核心动作|商业逻辑|痛点打击|数据|价值|流量端|服务端|变现端|场景重构|定位升级|渠道变革|启示|路径|核心逻辑|引流|转化|交付|变现模式|运营关键|合作模式|概念|前沿案例|展望|核心定位|痛点解决|痛点|产品与变现|合规红线必读|挂号与问诊的落地策略|双层服务体系|变现逻辑|场景|优势)"
            
            if re.search(f'<strong>{dimension_keys}</strong>', text):
                 text = re.sub(f'<strong>({dimension_keys})</strong>', r'<span class="dimension-label">\1</span>', text)
                 if text.startswith('* ') or text.startswith('- '):
                     text = text[2:]
                 html_content.append(f'<div class="dimension-item">{text}</div>')
                 continue

            # NEW: Parenthetical Citations
            # Matches （说明：...） or (引用来源：...) or (案例来源...)
            # We want to match nested parentheses or just simple ones. Simple for now: `（\s*(引用来源|数据来源|说明|案例来源)[:：].*?）`
            # Also catch (引用来源...) without bold.
            # We use a broader pattern to capture common citation formats.
            citation_pattern = r"（\s*(引用来源|数据来源|说明|案例来源|Source).*?）"
            if re.search(citation_pattern, text):
                text = re.sub(f"({citation_pattern})", r'<span class="mini-citation">\1</span>', text)

            # Citation / Core Logic (*Italic*)
            if stripped.startswith('*') and stripped.endswith('*') and len(stripped) > 5:
                content = stripped.strip('*')
                html_content.append(f'<div class="citation">{content}</div>')
                continue

            # Check for Bullet Points (Regular)
            if text.startswith('- ') or text.startswith('* '):
                 html_content.append(f'<p style="margin-left: 1.5rem; text-indent: -1rem;">•&nbsp;&nbsp;{text[2:]}</p>')
            else:
                 html_content.append(f'<p>{text}</p>')
    
    if in_table: html_content.append('</table></div>')
    return '\n'.join(html_content), toc, main_title

def generate():
    with open(SOURCE_FILE, 'r') as f: text = f.read()
    body, toc, title = parse_markdown(text)
    
    # Build Nested Nav
    nav_html = '<ul class="nav-menu">'
    
    if not toc:
        nav_html += '</ul>'
    else:
        last_level = 0
        
        for i, item in enumerate(toc):
            level = item['level']
            
            # Look ahead for children
            has_children = False
            if i + 1 < len(toc):
                if toc[i+1]['level'] > level:
                    has_children = True
            
            if level > last_level:
                if last_level != 0: 
                     nav_html += f'<ul class="nav-group">'
            elif level < last_level:
                step_down = last_level - level
                nav_html += ('</ul></li>' * step_down)
            else:
                if last_level != 0:
                     nav_html += '</li>'
            
            arrow = '▶ ' if has_children else ''
            # Expand Level 1 by default
            is_expanded = (level == 1)
            expand_class = "expanded" if is_expanded else ""
            
            arrow_html = f'<span class="nav-toggle">{arrow}</span>' if has_children else '<span class="nav-toggle" style="width:24px;display:inline-block"></span>'
            
            nav_html += f'''<li class="nav-item level-{level} {('has-child' if has_children else '')} {expand_class}">
                <div class="nav-item-container" onclick="toggleNav(this)">
                    <a href="#{item["id"]}" class="nav-link nav-level-{level}">{item["title"]}</a>
                    {arrow_html}
                </div>'''
            
            last_level = level
        
        if last_level > 0:
            nav_html += ('</li></ul>' * (last_level - 1)) + '</li>'

    nav_html += '</ul>'
    
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
        <div class="nav-title">行业洞察 2026</div>
    </div>
    {nav_html}
</nav>
<main class="main-content">
    <h1 class="report-title">{title}</h1>
    {body}
</main>
<script>
    function toggleNav(element) {{
        const li = element.parentElement;
        if (li.classList.contains('has-child')) {{
            li.classList.toggle('expanded');
        }}
    }}
</script>
</body>
</html>"""
    
    with open(OUTPUT_FILE, 'w') as f: f.write(html)
    print("Done.")

if __name__ == '__main__':
    generate()
