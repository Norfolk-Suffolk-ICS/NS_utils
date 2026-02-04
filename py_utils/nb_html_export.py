import nbformat
from nbconvert import HTMLExporter

__all__ = ["convert_notebook_to_html_string","write_notebook_to_html"]

def _generate_table_of_contents(notebook_path:str)->str:
    """Finds all notebook headers in markdown cells and creates a table of contents 
    with links to each section.
    Args:
        notebook_path: string path to .ipynb notebook

    Returns:
        String containing the table of contents.
    """

    with open(notebook_path, 'r', encoding = "utf-8") as f:
         nb = nbformat.read(f, as_version=4)
         
    table_of_contents = []
    
    # Iterating through notebook cells
    for cell in nb['cells']:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for line in lines:
                if line.startswith('##'):
                    # Counting number of hashes to detemine heading level
                    level = line.count('#')
                    title = line.strip('#').strip()
                    table_of_contents.append((title, level))

    toc_lines = []
    for title, level in table_of_contents:
        indent = '&nbsp;'
        if level >2: 
            indent = level*indent*2
        toc_lines.append(f"{indent}<a href='#{title.replace(' ', '-')}'>{title}</a>")

    toc_str = "<br>".join(toc_lines)
    return toc_str


def convert_notebook_to_html_string(notebook_path:str, 
                                    exclude_input_cells=True,
                                    make_table_of_contents:bool=True)->str:
    """Takes a notebook file path, and converts to html using nbconvert.HtmlExporter
    Args:
        notebook path:str, path to the notebook file
        exclude_input_cells:bool, whether to include the input cells
        make_table_of_contents:bool, whether to make & include a table of contents

    Returns:
        A string containing the notebook html
    """
    # Creating HTML exporter instance
    html_exporter = HTMLExporter()

    if exclude_input_cells:
        # Exclude code cells from the output
        html_exporter.exclude_input = True

    # Convert the notebook to HTML
    (body, resources) = html_exporter.from_filename(notebook_path)
    
    plotly_script_tag = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>\n'
    
    if '<head>' in body:
        body = body.replace("<head>", f"<head>\n {plotly_script_tag}")
    else:
        body = plotly_script_tag + body

    if make_table_of_contents:
        # Generating TOC
        toc = _generate_table_of_contents(notebook_path)
    else:
        return body

    # Combining TOC and Body
    body_with_toc = f"<div id = 'toc'><h3>Table of contents</h3>{toc}<hr></div> \n \n {body}"
    
    return body_with_toc


def write_notebook_to_html(notebook_content:str, notebook_path:str)->None:
    """
    Takes a notebook file as a string and writes this to a html file.
    Args:
        notebook_content:str, the html content of the notebook
        notebook_path:str, the path to save the notebook to, if this is .ipynb it will be changed to .html
    """
    if '.ipynb' in notebook_path:
        output_file_path = notebook_path.replace('.ipynb','.html')
    else:
        raise ValueError("{} is not a .ipynb file".format(notebook_path))
    # Write HTML content to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(notebook_content)
    
    return