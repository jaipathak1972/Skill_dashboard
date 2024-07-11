# Job Skill Data Analysis Dashboard

This is a Dash web application for analyzing job skills and related data. The dashboard provides various visualizations, including bar charts, pie charts, sunburst charts, and treemaps, to explore the distribution and relationships of job roles, companies, locations, and skills.

## Features

- Distribution of job roles and job pay
- Top 20 companies by job pay
- Distribution of companies by size
- Job roles by primary skill category
- Interactive filters and sliders for customized analysis

## Installation

### Prerequisites

- Python 3.7+
- Required packages listed in `requirements.txt`

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/job-skill-data-analysis.git
    cd job-skill-data-analysis
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Place your data file (`result.xlsx`) in the root directory.

## Running the App Locally

1. Run the Dash app:

    ```sh
    python app.py
    ```

2. Open a web browser and go to `https://skill-dashboard-5.onrender.com` to view the dashboard.

## Deploying on Render

1. Create a new web service on Render and connect it to your GitHub repository.

2. In the **Build Command** field, enter:

    ```sh
    pip install -r requirements.txt
    ```

3. In the **Start Command** field, enter:

    ```sh
    python app.py
    ```

4. Set up any necessary environment variables, such as `PYTHON_VERSION`, if required.

Screen shots of the dashboard 
1. Pie charts 
![image](https://github.com/jaipathak1972/Skill_dashboard/assets/64726553/848bdaa2-dec7-416f-8eac-343b74af4535)
2. Interactive StackBar  Graph and Bar Graph 
![image](https://github.com/jaipathak1972/Skill_dashboard/assets/64726553/5d29389c-e4c5-4b52-801f-bf22d3f01abf)
3. Interactive Hunburst Graph and  Tree Graph
![image](https://github.com/jaipathak1972/Skill_dashboard/assets/64726553/b8358fc3-7450-4ba3-9ac3-03c71f9d6506)
