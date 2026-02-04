# Suffolk and North East Essex Integrated Care System
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/pypi/pyversions/SNEE_utils.svg)](https://pypi.org/project/SNEE_utils/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)


## SNEE_utils
SNEE_utils is a Python package designed for reuse by analysts within the Suffolk and North East Essex (SNEE) Intelligence Function. All repositories within this organisation are developed and maintained by analysts based in the [SNEE Intelligence function](https://www.sneeics.org.uk/can-do-health-and-care/creative/knowledge-and-intelligence/) hub. The package includes two sub-packages:
<br>


## Submodules & Tools

### 1. Python Utility Functions : py_utils
- nb_html_export.py --> This python file contains a set of convenience function to convert notebook to html and add table of contents. This primarily used nbconvert to perform the conversion and bs4 to insert the table of contents.
- snowflake_sql.py --> This python file contains a set of functions to establish connection with snowflake database and load/save data from sql files.
- utils.py --> This python file contains reusable analytical functions.

### 2. SNEE Stylings : snee_styles
- A Python package containing useful functions for implementing Suffolk and North East Essex (SNEE) Intelligence Function style.


## Installation: How do I install SNEE_utils?
`SNEE_utils` is a parent package that holds both the child packages namely: `py_utils` and `SNEE_styles` Python packages. Installation is using pip:
- It is recommended to use a Virtual Environment
- This will then install the module in your environment, optionally specifying the version

```
pip install git+https://github.com/SNEE-ICS/SNEE_Utils.git
```
or optionally specifying a version:

```
pip install git+https://github.com/SNEE-ICS/SNEE_Utils.git@v0.0.6
```


## How to use py_utils and snee_styles ?
Once the parent package is installed, to use the py_utils or SNEE_styles package in your notebook, use:

#### Example: py_utils
```python
from py_utils import nb_html_export, snowflake_sql 

my_notebook = "Report.ipynb"

# By default this will include table of contents and exclude inputs (code)
formatted_html_with_table_of_contents = nb_html_export.convert_notebook_to_html_string(my_notebook)

# This saves the notebook down to the original file name, but with .html
nb_html_export.write_notebook_to_html(formatted_html_with_table_of_contents, my_notebook)


sql_engine = snowflake_sql.create_snowflake_sql_engine(profile_env = 'prd')  # You can input 'prd' or 'dev' depending on the instance you want to connect

df = snowflake_sql.load_data_try_parquet_first(
    sql_engine=engine,
    sql_path="../test_data.sql",
    parquet_path='data_file_name.parquet'
)

df.head()
```

#### Example: SNEE_styles
```python
# For Matplotlib and Seaborn Plots
from snee_styles import mpl_styles
mpl_styles()

# For Plotly Plots
from snee_styles import plotly_style
plotly_style()
```

> ⚠️ For Jupyter Notebooks--> Please make sure you run `from snee_styles import mpl_style, plotly_style` and `mpl_style()` `plotly_style` in **code cells** as shown above. 



## What chart types can use SNEE IF Styles?
- Line plots
- Scatter plots
- Bubble plots
- Bar charts
- Pie charts
- Histograms and distribution plots
- 3D surface plots
- Stream plots
- Polar plots

## Examples

To run the examples in [`example.ipynb`](https://github.com/SNEE-ICS/SNEE_Utils/blob/main/snee_styles/example.ipynb), install the required packages using ``pip install -r requirements.txt`` in a Python virtual environment of your choice.

```python
import matplotlib.pyplot as plt
from snee_styles import mpl_style

def plot():
    mpl_style()
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # the following functions are defined in example.ipynb 
    line_plot(axes[0, 0])
    scatter_plot(axes[0, 1])
    distribution_plot(axes[1, 0])
    ax = plt.subplot(2, 2, 4, projection='polar')
    polar_plot(ax)

plot()
```

### Seaborn or Matplotlib

![png](https://github.com/SNEE-ICS/SNEE_Utils/blob/main/snee_styles/examples/sample_plots.png)

### Plotly

Plotly example plots can be viewed by clicking the link below:

[Line Plot](snee_styles/examples/0.plotly.html)<br>
[Scatter Plot](snee_styles/examples/1.plotly.html)<br>
[Distribution Plot](snee_styles/examples/2.plotly.html)<br>

## What license do you use?

QB Styles is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
<br>
Contributions to code and issues are welcome.
<hr>

<!--add more documentation on each module below here.
Please follow the same format -->
## Contributing

1. Add a feature branch (branch from main/master) eg. `feature/common_transformations`
    - Create a [virtual environment](https://git.apps.axym.co.uk/snee.SNEE_ICB/AxymPyTools/wiki/Python-virtual-environments) specifically for this task in an empty directory.
    - install using 'develop' mode `pip install -e pip install git+https://git.apps.axym.co.uk/snee.SNEE_ICB/AxymPyTools.git@feature/your-feature-branch`
2. Please add any contributions to modules or packages within `app/axym_pytools/src`.
    - Use the google style guide.
    - Make every effort to make non-breaking changes.
    - If you have to alter existing tests to make them pass, your changes are probably breaking!
    - Update any new dependencies in setup.py
3. Write tests in `app/axym_pytools/tests` using the pytest framework. 
    - Ensure as much coverage as possible.
    - Ensure tests are running and screengrab passed tests for submission with PR.
    - TODO: Test automation and formatting pre-commit hooks.
4. Register methods/classes in `app/axym_pytools/__init__py` by importing them, this allows access under the axym_pytools namespace.
    - At the top of your modules, add `__all__` to register your functions/classes in the module.
    - these can be imported using `from .src.my_module import *` in the `__init__.py` file.
5. Add your name to `setup.py` if this is your first contribution.
6. Add any specific contributing packages to `setup.py` eg. pinned pandas versions.
7. Increment version in `setup.py`, `readme.me` this file
8. Submit pull request for peer review to release branch with release tags.
    - for example `release/v0.0.6`
9. Create release on gitea, with release notes.
8. Once completed, pull request to main/master to keep 'production' branch up to date.


### Testing
- Shell command:
    - To run pytest, first ensure it is installed in the development environment, and use the following command:
    ```cmd
    pytest . 
    ```
This will run all the tests and give feedback via the command prompt/shell.
- VSCode:
 - To set up in VSCode, Just select 'pytest' as the test framework when prompted and the root directory (`.`). 
 - There is a `pytest.ini` file in the project root which handles configuration, for more advanced methods, consult the documentation.
