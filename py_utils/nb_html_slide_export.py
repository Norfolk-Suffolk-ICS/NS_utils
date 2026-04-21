import nbformat
from nbconvert import HTMLExporter
import os
import base64

__all__ = ["convert_notebook_to_slides_html", "write_notebook_to_html_slide"]

######################################      STYLES & JS SCRIPTS     ###################################################
def _get_slide_styles():
    """Returns the custom CSS styles for the Slide presentation"""
    return """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif;
            background: #f5f5f5;
            color: #333;
            overflow: hidden;
            }
        
        .slide-container { width: 100vw; height: 100vh; position: relative; overflow: hidden; }
        .slide { 
            width: 100%; 
            height: 100%; 
            position: absolute; 
            top: 5px; 
            left: 5px;
            padding: 60px 80px; 
            background: white; 
            display: none; 
            overflow-y: auto; 
            box-shadow: 0 10px 20px rgba(0,0,0,0.2); 
        }
        .slide.active { display: block; }
        .slide.title-slide { 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .slide.first-image-slide {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0;
            background: white;
        }
        .slide.first-image-slide img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        
        /* Logo - TOP RIGHT */
        .slide-logo {
            position: absolute;
            top: 20px;
            right: 40px;
            max-width: 250px;
            max-height: 150px;
            z-index: 100;
        }
        
        .slide h1 { font-size: 5.5em !important; margin-bottom: 0.5em; font-weight: 800 !important; color: #064169; }
        .slide h2 { font-size: 3.5em !important; margin-bottom: 0.5em; color: #064169; border-bottom: 3px solid #064169; padding-bottom: 0.2em; }
        .slide h3 { font-size: 2.5em !important; margin-top: 1em; margin-bottom: 0.5em; color: #064169; }
        .slide p { font-size: 1.5em !important; line-height: 1.5; margin-bottom: 0.5em; }
        .slide ul, .slide ol { font-size: 1.5em !important; margin-left: 2em; margin-bottom: 0.5em; line-height: 1.5; display: inline-block; text-align: left; }
        a {color: #0000EE !important;}

        /* Media - exclude logo from general img styling */
        .slide img:not(.slide-logo) { max-height: 500px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .slide pre { background: #f8f9fa; border-left: 4px solid #064169; padding: 20px; margin: 20px auto; overflow-x: auto; border-radius: 6px; font-size: 0.95em; max-width: 90%; text-align: left; }
        .slide code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        
        /* Tables */
        .slide table { width: 90%; border-collapse: collapse; margin: 20px auto; font-size: 1em; }
        .slide table th { background: #064169; color: white; padding: 12px; text-align: left; font-weight: 600 !important; }
        .slide table td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; }
        .slide table tr:nth-child(even) { background: #f8f9fa; }
        
        /* Output areas */
        .output_area, .output_subarea { margin: 20px auto; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .plotly-graph-div, .vega-embed { margin: 20px auto !important; display: block; }
        
        /* Navigation */
        .toc-list { list-style: none; margin-left: 0; font-size: 1.4em; }
        .toc-list li { padding: 15px 20px; margin: 10px 0; background: #f0f0f0; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; }
        .toc-list li:hover { background: #e0e0e0; transform: translateX(10px); }
        .slide-controls { position: fixed; bottom: 30px; right: 30px; display: flex; align-items: center; gap: 10px; background: rgba(0,0,0,0.7); padding: 10px 15px; border-radius: 50px; z-index: 1000; }
        .nav-btn { background: #064169; color: white; border: none; padding: 8px 15px; border-radius: 25px; cursor: pointer; font-size: 1em; transition: all 0.3s ease; font-weight: 600; }
        .nav-btn:hover { background: #053050; transform: scale(1.05); }
        .nav-btn:disabled { background: #ccc; cursor: not-allowed; transform: scale(1); }
        .slide-counter { color: white; font-size: 1.1em; font-weight: 600; }
    </style>
    """

def _get_slide_scripts():
    """Returns JavaScript for slide navigation."""
    return """
    <script>
        let currentSlide = 0;
        let totalSlides = 0;
        
        function initSlides() {
            const slides = document.querySelectorAll('.slide');
            totalSlides = slides.length;
            document.getElementById('total-slides').textContent = totalSlides;
            showSlide(0);
        }
        
        function showSlide(n) {
            const slides = document.querySelectorAll('.slide');
            if (n >= totalSlides) { currentSlide = totalSlides - 1; }
            else if (n < 0) { currentSlide = 0; }
            else { currentSlide = n; }
            
            slides.forEach((slide, index) => {
                slide.classList.remove('active');
                if (index === currentSlide) { slide.classList.add('active'); }
            });
            
            document.getElementById('current-slide').textContent = currentSlide + 1;
            document.querySelectorAll('.nav-btn')[0].disabled = currentSlide === 0;
            document.querySelectorAll('.nav-btn')[1].disabled = currentSlide === totalSlides - 1;
        }
        
        function nextSlide() { showSlide(currentSlide + 1); }
        function previousSlide() { showSlide(currentSlide - 1); }
        function goToSlide(slideNumber) { showSlide(slideNumber); }
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
            else if (e.key === 'ArrowLeft') { e.preventDefault(); previousSlide(); }
            else if (e.key === 'Home') { e.preventDefault(); showSlide(0); }
            else if (e.key === 'End') { e.preventDefault(); showSlide(totalSlides - 1); }
        });
        
        window.addEventListener('DOMContentLoaded', initSlides);
    </script>
    """

def _generate_slide_navigation():
    """Returns navigation controls HTML."""
    return """
    <div class="slide-controls">
        <button class="nav-btn" onclick="previousSlide()">&#10094; Previous</button>
        <span class="slide-counter"><span id="current-slide">1</span> / <span id="total-slides">0</span></span>
        <button class="nav-btn" onclick="nextSlide()">Next &#10095;</button>
    </div>
    """
############################################################################################################################

def _extract_title_from_notebook(notebook_path: str):
    """Extract H1 title from notebook."""
    with open(notebook_path, 'r', encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for line in lines:
                if line.startswith('# ') and not line.startswith('##'):
                    return line.strip('#').strip()
    
    return os.path.basename(notebook_path).replace('.ipynb', '').replace('_', ' ').title()


def _split_notebook_into_slides(notebook_path: str, exclude_input_cells: bool = True):
    """Split notebook into slides based on ## markdown headers."""
    with open(notebook_path, 'r', encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    slides = []
    current_slide_cells = []
    current_slide_title = None
    found_first_h2 = False
    
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            
            # Find ALL ## headers in this cell
            h2_positions = []
            for i, line in enumerate(lines):
                if line.startswith('##') and not line.startswith('###'):
                    h2_positions.append(i)
            
            if h2_positions:
                # This cell has one or more ## headers
                for idx, h2_pos in enumerate(h2_positions):
                    if idx + 1 < len(h2_positions):
                        end_pos = h2_positions[idx + 1]
                    else:
                        end_pos = len(lines)
                    
                    section_lines = lines[h2_pos:end_pos]
                    section_content = '\n'.join(section_lines)
                    h2_title = section_lines[0].strip('#').strip()
                    
                    section_cell = nbformat.v4.new_markdown_cell(section_content)
                    
                    if found_first_h2:
                        if current_slide_cells:
                            slides.append((current_slide_cells, current_slide_title))
                        current_slide_cells = []
                    else:
                        if current_slide_cells:
                            slides.append((current_slide_cells, None))
                        current_slide_cells = []
                    
                    found_first_h2 = True
                    current_slide_title = h2_title
                    current_slide_cells.append(section_cell)
            else:
                current_slide_cells.append(cell)
        else:
            current_slide_cells.append(cell)
    
    if current_slide_cells:
        if found_first_h2:
            slides.append((current_slide_cells, current_slide_title))
        else:
            slides.append((current_slide_cells, None))
    
    return slides


def _generate_table_of_contents(notebook_path: str):
    """Finds all notebook headers in markdown cells and creates a table of contents."""
    with open(notebook_path, 'r', encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    slide_titles = []
    
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for line in lines:
                if line.startswith('##') and not line.startswith('###'):
                    title = line.strip('#').strip()
                    slide_titles.append(title)
    toc_lines = ['<ul class="toc-list">']
    for i, title in enumerate(slide_titles, 3):
        toc_lines.append(f'  <li onclick="goToSlide({i})">{title}</li>')
    toc_lines.append('</ul>')
    toc_html = '\n'.join(toc_lines)
    return toc_html, slide_titles


def convert_notebook_to_slides_html(notebook_path: str, author_name: str, exclude_input_cells: bool = True, make_table_of_contents: bool = True) -> str:
    """Converts a Jupyter notebook to an HTML slideshow presentation."""

    # Get package directory (where this Python file is located)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(package_dir, 'assets')
    
    # Load logo
    logo_base64 = ""
    logo_path = os.path.join(assets_dir, 'NS_IF_Logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_base64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    
    # Load first slide image
    first_slide_img = ""
    first_slide_path = os.path.join(assets_dir, 'main_slide.png')
    if os.path.exists(first_slide_path):
        with open(first_slide_path, 'rb') as f:
            first_slide_img = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    
    # Load background image
    slide_bg_img = ""
    bg_path = os.path.join(assets_dir, 'slide_bg.png')
    if os.path.exists(bg_path):
        with open(bg_path, 'rb') as f:
            slide_bg_img = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

    # Logo HTML
    logo_html = f'<a href="https://www.intelligencefunction.org" target="_blank"><img src="{logo_base64}" class="slide-logo" alt="Logo"></a>' if logo_base64 else ''

    plotly_script_tag = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>\n'
    vega_script_tag = """
                    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>   
                    """
    
    slide_styles = _get_slide_styles()
    title = _extract_title_from_notebook(notebook_path)
    slides = _split_notebook_into_slides(notebook_path, exclude_input_cells)
    
    html_exporter = HTMLExporter()
    if exclude_input_cells:
        html_exporter.exclude_input = True

    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'    <title>{title}</title>',
        f'    {plotly_script_tag}',
        f'    {vega_script_tag}',
        slide_styles,
        '</head>',
        '<body>',
        '<div class="slide-container">'
    ]

    # ALWAYS remove first element if it exists (content before first ##)
    # This prevents duplication whether notebook starts with # or ##
    if slides and len(slides) > 0:
        slides.pop(0)
    
    # SLIDE 1: First image slide
    html_parts.extend([
        '    <div class="slide first-image-slide active">',
        f'        <img src="{first_slide_img}" alt="First Slide">',
        '    </div>'
    ])
    
    # SLIDE 2: Title slide with background
    title_slide_style = f'style="background-image: url({slide_bg_img});"' if slide_bg_img else ''
    html_parts.extend([
        f'    <div class="slide title-slide" {title_slide_style}>',
        logo_html,
        f'        <h1>{title}</h1>',
        '        <p style="font-size: 1.2em; margin-top: 30px;">Website: <a href="https://www.intelligencefunction.org" target="_blank">The Intelligence Function</a></p>',
        f'        <h3>Author: {author_name}</h3>',  # ADDED COMMA
        '    </div>'
    ])
    
    # SLIDE 3: Table of contents
    if make_table_of_contents:
        toc, slide_titles = _generate_table_of_contents(notebook_path)
        if slide_titles:
            html_parts.extend([
                '    <div class="slide toc-slide">',
                '        <h2>Table of Contents</h2>',
                f'        {toc}',
                '    </div>'
            ])
    
    # SLIDES 4+: Content slides (each ## becomes a slide)
    for slide_cells, slide_title in slides:
        (body, _) = html_exporter.from_notebook_node(nbformat.v4.new_notebook(cells=slide_cells))
        html_parts.extend([
            '    <div class="slide content-slide">',
            f'        {body}',
            '    </div>'
        ])
    
    html_parts.extend([
        '</div>',
        _generate_slide_navigation(),
        _get_slide_scripts(),
        '</body>',
        '</html>'
    ])

    return '\n'.join(html_parts)


def write_notebook_to_html_slide(notebook_content: str, notebook_path: str) -> None:
    """Writes notebook HTML content to a file."""
    if '.ipynb' in notebook_path:
        output_file_path = notebook_path.replace('.ipynb', '_slides.html')
    else:
        raise ValueError(f"{notebook_path} is not a .ipynb file")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(notebook_content)
    
    return