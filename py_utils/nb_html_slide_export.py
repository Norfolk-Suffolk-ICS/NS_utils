import nbformat
from nbconvert import HTMLExporter
import re

__all__ = ["convert_notebook_to_slides_html", "write_notebook_to_html"]

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
                    break
    
    toc_lines = ['<ul class="toc-list">']
    for i, title in enumerate(slide_titles, 1):
        toc_lines.append(f'  <li onclick="goToSlide({i})">{title}</li>')
    toc_lines.append('</ul>')
    
    toc_html = '\n'.join(toc_lines)
    return toc_html, slide_titles

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
    
    # Fallback to filename if no H1 found
    import os
    return os.path.basename(notebook_path).replace('.ipynb', '').replace('_', ' ').title()

def _get_slide_styles():
    """Returns the CSS styles for slide presentation - NO BACKGROUNDS."""
    return """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; color: #333; overflow: hidden; }
        .slide-container { width: 100vw; height: 100vh; position: relative; overflow: hidden; }
        .slide { 
            width: 100%; 
            height: 100%; 
            position: absolute; 
            top: 0; 
            left: 0; 
            padding: 60px 80px; 
            background: white; 
            display: none; 
            overflow-y: auto; 
            box-shadow: 0 0 40px rgba(0,0,0,0.1); 
        }
        .slide.active { display: block; }
        .slide.title-slide { 
            background: white; 
            color: #333; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            text-align: center; 
        }
        .slide.toc-slide { 
            background: white; 
            color: #333; 
        }
        .slide.content-slide {
            text-align: center;
        }
        .slide h1 { font-size: 3.5em; margin-bottom: 0.3em; font-weight: 700; color: #064169; }
        .slide h2 { font-size: 2.5em; margin-bottom: 0.5em; color: #064169; border-bottom: 3px solid #064169; padding-bottom: 0.2em; }
        .slide h3 { font-size: 1.8em; margin-top: 1em; margin-bottom: 0.5em; color: #064169; }
        .slide p { font-size: 1.2em; line-height: 1.6; margin-bottom: 1em; }
        .slide ul, .slide ol { font-size: 1.2em; margin-left: 2em; margin-bottom: 1em; line-height: 1.8; display: inline-block; text-align: left; }
        .slide img { max-width: 90%; max-height: 500px; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .slide pre { background: #f8f9fa; border-left: 4px solid #064169; padding: 20px; margin: 20px auto; overflow-x: auto; border-radius: 6px; font-size: 0.95em; max-width: 90%; text-align: left; }
        .slide code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        .slide table { width: 90%; border-collapse: collapse; margin: 20px auto; font-size: 1em; }
        .slide table th { background: #064169; color: white; padding: 12px; text-align: left; font-weight: 600; }
        .slide table td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; }
        .slide table tr:nth-child(even) { background: #f8f9fa; }
        .toc-list { list-style: none; margin-left: 0; font-size: 1.4em; }
        .toc-list li { padding: 15px 20px; margin: 10px 0; background: #f0f0f0; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; }
        .toc-list li:hover { background: #e0e0e0; transform: translateX(10px); }
        .slide-controls { position: fixed; bottom: 30px; right: 30px; display: flex; align-items: center; gap: 20px; background: rgba(0,0,0,0.7); padding: 15px 25px; border-radius: 50px; z-index: 1000; }
        .nav-btn { background: #064169; color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-size: 1em; transition: all 0.3s ease; font-weight: 600; }
        .nav-btn:hover { background: #053050; transform: scale(1.05); }
        .nav-btn:disabled { background: #ccc; cursor: not-allowed; transform: scale(1); }
        .slide-counter { color: white; font-size: 1.1em; font-weight: 600; }
        .keyboard-hint { position: fixed; top: 20px; right: 30px; background: rgba(0,0,0,0.7); color: white; padding: 10px 15px; border-radius: 8px; font-size: 0.9em; opacity: 0.6; z-index: 999; }
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

def _split_body_into_slides(body: str):
    """Split HTML body into slides based on <h2> tags."""
    # Find all h2 positions
    h2_pattern = re.compile(r'<h2[^>]*>.*?</h2>', re.DOTALL)
    matches = list(h2_pattern.finditer(body))
    
    if not matches:
        # No h2 tags, return whole body as one slide
        return [body]
    
    slides = []
    
    # First slide: everything before first h2
    if matches[0].start() > 0:
        slides.append(body[:matches[0].start()])
    
    # Each h2 starts a new slide
    for i, match in enumerate(matches):
        start = match.start()
        # Find where this slide ends (at next h2 or end of body)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(body)
        
        slides.append(body[start:end])
    
    return slides

def convert_notebook_to_slides_html(
    notebook_path: str,
    exclude_input_cells: bool = True,
    make_table_of_contents: bool = True
) -> str:
    """Converts a Jupyter notebook to an HTML slideshow presentation."""
    import os
    
    # Creating HTML exporter instance
    html_exporter = HTMLExporter()

    if exclude_input_cells:
        html_exporter.exclude_input = True

    # Convert the notebook to HTML
    (body, resources) = html_exporter.from_filename(notebook_path)
    
    # Scripts for Plotly plots
    plotly_script_tag = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>\n'

    # Scripts for UPSET ALTAIR plots
    vega_script_tag = """
                    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>   
                    """
    
    # Get slide styles
    slide_styles = _get_slide_styles()
    
    # Extract title from H1 in notebook
    title = _extract_title_from_notebook(notebook_path)
    
    # Split body into slides
    slide_contents = _split_body_into_slides(body)
    
    # Build complete HTML
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
        '<div class="keyboard-hint">Use ← → arrows or click buttons to navigate</div>',
        '<div class="slide-container">',
        '    <div class="slide title-slide active">',
        f'        <h1>{title}</h1>',
        '        <p style="font-size: 1.3em; margin-top: 20px;">Press → to begin</p>',
        '    </div>'
    ]
    
    if make_table_of_contents:
        toc, slide_titles = _generate_table_of_contents(notebook_path)
        if slide_titles:
            html_parts.extend([
                '    <div class="slide toc-slide">',
                '        <h2>Table of Contents</h2>',
                f'        {toc}',
                '    </div>'
            ])
    
    # Add content slides
    for content in slide_contents:
        html_parts.extend([
            '    <div class="slide content-slide">',
            f'        {content}',
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