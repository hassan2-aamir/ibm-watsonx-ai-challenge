# IBM Watsonx AI Challenge

This project is designed to generate project overviews, design plans, and implementation plans using IBM Watsonx AI. The application leverages Gradio for the user interface and IBM Watsonx API for generating content.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd ibm-watsonx-ai-challenge
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Set your IBM Watsonx API credentials in a `.env` file:
    ```env
    WATSONX_API_KEY=your_api_key
    WATSONX_PROJECT_ID=your_project_id
    ```

2. Run the application:
    ```sh
    python src/planner.py
    ```

3. Open the Gradio interface in your browser and follow the prompts to generate project overviews, design plans, and implementation plans.

## Project Structure

```
ibm-watsonx-ai-challenge/
├── src/
│   └── planner.py
├── .gitignore
├── requirements.txt
├── .env
└── README.md
```

- `src/planner.py`: Main script containing the logic for generating project overviews, design plans, and implementation plans.
- `.gitignore`: Specifies files and directories to be ignored by git.
- `requirements.txt`: Lists the dependencies required for the project.
- `.env`: Contains the IBM Watsonx API credentials.
- `README.md`: Provides an overview and instructions for the project.
