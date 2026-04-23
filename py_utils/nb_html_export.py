import nbformat
from nbconvert import HTMLExporter
import os
import base64

__all__ = ["convert_notebook_to_html_string","write_notebook_to_html"]

######################################      STYLES & JS SCRIPTS     ###################################################
def _get_custom_styles() -> str:
    """Returns the custom CSS styles for the HTML output"""
    styles = """
    <style>
    body{
        font-family: Arial;
        margin-left: 20%;
        width: 70% !important;
    }
    #toc {
        position: fixed;
        top: 25px;
        bottom: 10px;
        left: 5px;
        width: 21%;
        background-color: #C0CED8;
        border: 2px ridge;
        overflow-y: auto;
        overflow-x: auto;
        height: fit-content;
        padding: 20px;
        border-radius: 25px;
        font-size: 14px;
        line-height: 1.3;
        padding: 5px
    }
    #toc a{
        color: #231F20;
    }
    #toc a:hover{
        color: blue;
        transform: translateX(10px);
    }
    .toc-list { list-style: none; margin-left: 0; font-size: 1.4em; }
    .toc-list li { padding: 15px 20px; margin: 10px 0; background: #f0f0f0; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; }
    .toc-list li:hover { background: #e0e0e0; transform: translateX(10px); }
    .slide-logo {
        position: fixed; 
        top: 20px;
        right: 5px;
        max-width: 280px !important;
        max-height: 150px;
        z-index: 100;
    }
    .slide-logo-bottom {
        display: block;
        margin: 50px auto 20px auto;
        width: 600px;
        height: 200px;
    }
    #go-to-top {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #064169;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        z-index: 1000;
        display: none;
        transition: background-color 0.3s;
    }
    #go-to-top:hover {
        background-color: #0a5a8a;
    }
    #go-to-top.show {
        display: block;
    }
    h1 { font-size: 5em !important; margin-bottom: 0.5em; font-weight: 700 !important; color: #064169; text-align: left; }
    h2 { font-size: 3.5em !important; margin-bottom: 0.5em; color: #064169; }
    h3 { font-size: 2.5em !important; margin-bottom: 0.5em; color: #064169; border-bottom: 3px solid #064169; padding-bottom: 0.2em; }
    h4 { font-size: 2em !important; margin-bottom: 0.5em; color: #064169; }
    p { font-size: 1.5em !important; line-height: 1.5; margin-bottom: 0.5em; }
    ul, ol { font-size: 1.5em !important; margin-left: 2em; margin-bottom: 0.5em; line-height: 1.5; display: inline-block; text-align: left; }
    table, tbody{ border: 1px outset; text-align : center: margin-left: inherit !important; }
    .plotly-graph-div, .vega-embed { margin: 20px auto !important; display: block; }
    .slide img:not(.slide-logo) {border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: block; margin: 20px auto; }
    #buttons { font-size: x-large !important; }

    </style>
    """
    return styles

def _get_scroll_script() -> str:
    """Returns JavaScript for the Go to Top button functionality."""
    script = """
    <script>
    var goToTopBtn = document.getElementById("go-to-top");

    window.onscroll = function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            goToTopBtn.classList.add("show");
        } else {
            goToTopBtn.classList.remove("show");
        }
    };

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    </script>
    """
    return script
############################################################################################################################

def _generate_table_of_contents(notebook_path:str)->str:
    """Finds all notebook headers in markdown cells and creates a table of contents with links to each section.
    Args: notebook_path: string path to .ipynb notebook
    Returns: String containing the table of contents.
    """
    with open(notebook_path, 'r', encoding = "utf-8") as f:
         nb = nbformat.read(f, as_version=4)
         
    table_of_contents = []
    
    # Iterating through notebook cells
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for line in lines:
                if line.startswith('##') and not line.startswith('###'):
                    # Counting number of hashes to detemine heading level
                    level = line.count('#')
                    title = line.strip('#').strip()
                    table_of_contents.append((title, level))
    toc_lines = ['<ul class="toc-list">']
    for title, level in table_of_contents:
        indent = '&nbsp;'
        if level >2: 
            indent = level*indent*2
        toc_lines.append(f"{indent}<a href='#{title.replace(' ', '-')}'>{title}</a>")
    toc_str = "<br>".join(toc_lines)
    return toc_str


def convert_notebook_to_html_string(notebook_path:str, author_name:str, exclude_input_cells=True, make_table_of_contents:bool=True)->str:
    """Takes a notebook file path, and converts to html using nbconvert.HtmlExporter
    Args: notebook_path:str, path to the notebook file
          exclude_input_cells:bool, whether to include the input cells
          make_table_of_contents:bool, whether to make & include a table of contents
    Returns: A string containing the notebook html
    """
    # Get package directory and load logo
    package_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(package_dir, 'assets')
    
    logo_base64 = ""
    logo_path = os.path.join(assets_dir, 'NS_IF_Logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_base64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    
    # Logo HTML
    logo_html = f'<a href="https://www.intelligencefunction.org" target="_blank"><img src="{logo_base64}" class="slide-logo" alt="Logo"></a>' if logo_base64 else ''
    logo_html_bottom = f'<a href="https://www.intelligencefunction.org" target="_blank"><img src="{logo_base64}" class="slide-logo-bottom" alt="Logo"></a>' if logo_base64 else ''
    
    # Read notebook to add website link
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Add website link after first # header
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('#') and not line.startswith('##'):
                    lines.insert(i + 1, '\n*Website: <a href="https://www.intelligencefunction.org" target="_blank">The Intelligence Function</a>*\n')
                    lines.insert(i + 2, f'\n<p>Author: {author_name}</p>')
                    cell.source = '\n'.join(lines)
                    break
            break

    html_exporter = HTMLExporter()

    if exclude_input_cells:
        # Exclude code cells from the output
        html_exporter.exclude_input = True

    # Convert the notebook to HTML
    (body, resources) = html_exporter.from_notebook_node(nb)
    
    # Scripts for Plotly plots
    plotly_script_tag = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>\n'

    # Scripts for UPSET ALTAIR plots
    vega_script_tag = """
                    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
                    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>   
                    """
    
    # Get custom CSS styles
    custom_styles = _get_custom_styles()
    
    # Get scroll-to-top JavaScript
    scroll_script = _get_scroll_script()
    
    if '<head>' in body:
        # Insert scripts and styles into the head section
        body = body.replace("<head>", f"<head>\n{plotly_script_tag}{vega_script_tag}\n{custom_styles}\n")
    else:
        # If no head tag, prepend everything
        body = plotly_script_tag + custom_styles + body

    # Add logo at the top of the body
    if '<body>' in body:
        body = body.replace('<body>', f'<body>\n{logo_html}\n')
    else:
        # If no body tag, prepend logo to content
        body = logo_html + body

    # Add Go to Top button
    go_to_top_button = '<button id="go-to-top" onclick="scrollToTop()">↑</button>\n'
    
    # Add button before closing body tag
    if '</body>' in body:
        body = body.replace('</body>', f'{go_to_top_button}{scroll_script}\n</body>')
    else:
        # If no body tag, append to the end
        body = body + go_to_top_button + scroll_script

    if make_table_of_contents:
        # Generating TOC
        toc = _generate_table_of_contents(notebook_path)
    else:
        return body

    # Combining TOC and Body
    body_with_toc = f"<div id = 'toc'><h3>Table of contents</h3>{toc}<hr></div> \n \n {body}{logo_html_bottom}<hr>"
    
    return body_with_toc


def write_notebook_to_html(notebook_content:str, output_file_path:str)->None:
    """Takes a notebook file as a string and writes this to a html file.
    Args: notebook_content:str, the html content of the notebook
          notebook_path:str, the path to save the notebook to, if this is .ipynb it will be changed to .html
    """
    if '.ipynb' in output_file_path:
        output_file_path = output_file_path.replace('.ipynb','.html')
    else:
        raise ValueError("{} is not a .ipynb file".format(output_file_path))
    # Write HTML content to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(notebook_content)
    
    return