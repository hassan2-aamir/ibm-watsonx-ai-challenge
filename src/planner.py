WATSONX_API_KEY="tF1v1VZvm8lkubHuIP9LsIHniE21BUWKczrtwJ7lNoEG"
WATSONX_PROJECT_ID="8384c46f-b31e-4e1a-a8ef-c0decbf6cf01"

import requests
import gradio as gr

# Model and project settings
MODEL_ID = "ibm/granite-3-8b-instruct"
API_KEY = WATSONX_API_KEY
URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
PROJECT_ID = WATSONX_PROJECT_ID
ACCESS_TOKEN = "eyJraWQiOiIyMDI1MDEzMDA4NDQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBRREVNIiwiaWQiOiJJQk1pZC02OTQwMDBRREVNIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNzRlZjcxMWMtOWI2Ny00ZDEyLWI2ZWEtMWE4Y2Y5MGM2MTgxIiwiaWRlbnRpZmllciI6IjY5NDAwMFFERU0iLCJnaXZlbl9uYW1lIjoiSGFzc2FuIiwiZmFtaWx5X25hbWUiOiJBYW1pciIsIm5hbWUiOiJIYXNzYW4gQWFtaXIiLCJlbWFpbCI6ImhhYW1pci5ic2NzMjNzZWVjc0BzZWVjcy5lZHUucGsiLCJzdWIiOiJoYWFtaXIuYnNjczIzc2VlY3NAc2VlY3MuZWR1LnBrIiwiYXV0aG4iOnsic3ViIjoiaGFhbWlyLmJzY3MyM3NlZWNzQHNlZWNzLmVkdS5wayIsImlhbV9pZCI6IklCTWlkLTY5NDAwMFFERU0iLCJuYW1lIjoiSGFzc2FuIEFhbWlyIiwiZ2l2ZW5fbmFtZSI6Ikhhc3NhbiIsImZhbWlseV9uYW1lIjoiQWFtaXIiLCJlbWFpbCI6ImhhYW1pci5ic2NzMjNzZWVjc0BzZWVjcy5lZHUucGsifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiNzRjODEwYThiZTEyNDI1Nzg0NmMzMTBmOTRhYWRlZWMiLCJpbXNfdXNlcl9pZCI6IjEzMzA2Mzc0IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyOTY4ODM0In0sImlhdCI6MTc0MDI1MDI5NywiZXhwIjoxNzQwMjUzODk3LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.PzHLRjEgL24If7n1kpWxHPuppmavCGR86KC9PzHx35snhxJ9ahioIBgachadLqFKANANpra6bnqhxI7bbF7MVpHEWVMTGuBUHzKc8G0_2uC4_cOR1Xp5bEEA3fFRbfLfPP6nmZwgCqHX5wEuIl3zs3zMNT8EPNy2fxTwoMPK3OVAEI7Ti4fSxtdJkQfb-rSp5IHJ_VvN6v-C0GEOW7631UU_w8bv0Ge7ze4BszTuiSLtzmOzjaYry3QSBJ5ziq9BEQdu9FvhI3R0uDcSP4TOD9rE-31bf9VLFzaFm5EJM5y3Oyd5oTD2ZFjdtacXUMhZQZsZ39bNqUO1KBfE_6wv1g"
AUTH_URL = "https://iam.cloud.ibm.com/identity/token"


def get_access_token(api_key):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(AUTH_URL, headers=headers, data=data, timeout=(10, 30))  # Increased timeout
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def create_project_overview(title, description, feedback="", history=[]):
    # Get access token
    access_token = get_access_token(API_KEY)
    
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Construct the prompt with history
    history_text = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in history])
    if len(history_text) == 0:
        prompt = f"""
User: Title: {title}
Description: {description}

Please provide a detailed project overview for the above application. The overview should include the following sections:

1. **Purpose and Goals**:
   - What is the primary purpose of the app?
   - What are the main goals the app aims to achieve?

2. **Key Features and Functionalities**:
   - List the key features and functionalities of the app.
   - Describe how each feature will benefit the users.

3. **Target Audience**:
   - Who are the primary users of the app?
   - What are the demographics and characteristics of the target audience?

4. **Competitive Analysis**:
   - Identify existing apps that are similar to this app.
   - Highlight the unique selling points (USPs) that differentiate this app from competitors.

5. **Success Criteria**:
   - Define the metrics and indicators that will be used to measure the success of the app.
   - Describe the expected outcomes and impact of the app.

Please ensure the project overview is comprehensive and provides a clear understanding of the app's purpose, features, target audience, competitive landscape, and success criteria."""
    else:
        prompt = f"""
{history_text}

User: {feedback}

Generate the complete project overview again with the feedback provided above."""

    print(prompt)
    # Request payload
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 4096,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID
    }

    try:
        # Make API request
        response = requests.post(URL, headers=headers, json=payload, timeout=(10, 60))  # Increased timeout
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('results', [{}])[0].get('generated_text', 'No response generated')
            history.append({"user": f"Title: {title}\nDescription: {description}", "ai": generated_text})
            return generated_text, history
        else:
            return f"Error: {response.status_code} - {response.text}", history
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}", history

def design_project(overview, feedback="", history=[]):
    # Get access token
    access_token = get_access_token(API_KEY)
    
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Construct the prompt with history
    history_text = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in history])
    if len(history_text) == 0:
        prompt = f"""
Project Overview: {overview}

Please provide a detailed design plan for the above application. The design plan should include the following sections:

1. **System Architecture**:
   - Describe the overall system architecture.

2. **Database Design**:
   - Define the database schema.

3. **API Design**:
   - List the APIs that will be required.
   - Provide details on each API endpoint, including request and response formats.

4. **UI/UX Design**:
   - Describe the user interface and user experience design principles.
   - Include wireframes and mockups for key screens.

5. **Scalability and Performance**:
   - Describe how the system will handle scalability and performance.
   - Include strategies for load balancing, caching, and optimizing performance.

6. **Integration Points**:
   - Identify any third-party services or systems that need to be integrated.
   - Provide details on how these integrations will be handled.

7. **Deployment Architecture**:
   - Describe the deployment architecture.
   - Include details on the environments (development, staging, production) and the deployment process.

Please ensure the design plan is comprehensive and provides a clear understanding of the system architecture, database design, API design, UI/UX design, scalability, integration points, and deployment architecture."""
    else:
        prompt = f"""
{history_text}

User: {feedback}

Generate the complete design plan again with the feedback provided above."""

    print(prompt)
    # Request payload
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 4096,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID
    }

    try:
        # Make API request
        response = requests.post(URL, headers=headers, json=payload, timeout=(10, 300))  # Increased timeout
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('results', [{}])[0].get('generated_text', 'No response generated')
            history.append({"user": f"Overview: {overview}\n", "ai": generated_text})
            return generated_text, history
        else:
            return f"Error: {response.status_code} - {response.text}", history
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}", history

def code_project(design, feedback="", history=[]):
    # Get access token
    access_token = get_access_token(API_KEY)
    
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Construct the prompt with history
    history_text = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in history])
    if len(history_text) == 0:
        prompt = f"""
Design Plan: {design}

Based on the provided design plan, please select the appropriate technology stack, describe the directory structure and file structure, and list all the modules needed for coding. The response should include the following sections:

1. **Technology Stack**:
   - Select the appropriate programming languages, frameworks, and tools for the backend, frontend, database, and other components.
   - Justify the selection of each technology.

2. **Directory Structure**:
   - Describe the overall directory structure of the project.
   - Include directories for the backend, frontend, database, and other components.

3. **File Structure**:
   - Describe the file structure within each directory.
   - Include key files and their purposes, such as configuration files, source code files, and documentation files.

4. **Modules Needed**:
   - List all the modules needed for coding the project.
   - Provide a brief description of the purpose of each module.

Please ensure the response is comprehensive and provides a clear understanding of the technology stack, directory structure, file structure, and modules required to implement the design."""
    else:
        prompt = f"""
{history_text}

User: {feedback}

Based on the provided design plan and the feedback, please select the appropriate technology stack, describe the directory structure and file structure, and list all the modules needed for coding. The response should include the following sections:

1. **Technology Stack**:
   - Select the appropriate programming languages, frameworks, and tools for the backend, frontend, database, and other components.
   - Justify the selection of each technology.

2. **Directory Structure**:
   - Describe the overall directory structure of the project.
   - Include directories for the backend, frontend, database, and other components.

3. **File Structure**:
   - Describe the file structure within each directory.
   - Include key files and their purposes, such as configuration files, source code files, and documentation files.

4. **Modules Needed**:
   - List all the modules needed for coding the project.
   - Provide a brief description of the purpose of each module.

Please ensure the response is comprehensive and provides a clear understanding of the technology stack, directory structure, file structure, and modules required to implement the design."""

    # Request payload
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 4096,
            "min_new_tokens": 50,
            "repetition_penalty": 1.2
        },
        "project_id": PROJECT_ID
    }
    print(prompt)
    try:
        # Make API request
        response = requests.post(URL, headers=headers, json=payload, timeout=(10, 300))
        print(response.json())  # Debugging: Print the response
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('results', [{}])[0].get('generated_text', 'No response generated')
            history.append({"user": f"Design: {design}\n", "ai": generated_text})
            return generated_text, history
        else:
            return f"Error: {response.status_code} - {response.text}", history
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}", history

# Create Gradio interface
with gr.Blocks() as interface:
    title_input = gr.Textbox(label="Title", placeholder="Enter the title of the project")
    description_input = gr.Textbox(label="Description", lines=10, placeholder="Enter the description of the project")
    feedback_input = gr.Textbox(label="Feedback", lines=5, placeholder="Provide feedback to improve the overview after first generating initial overview")
    overview_output = gr.Textbox(label="App Overview")
    generate_button = gr.Button("Generate Overview")
    regenerate_button = gr.Button("Regenerate Overview with Feedback")

    design_output = gr.Textbox(label="Design Plan")
    feedback_design_input = gr.Textbox(label="Feedback", lines=5, placeholder="Provide feedback to improve the design plan after first generated design")
    design_button = gr.Button("Generate Design Plan using your last generated overview")
    regenerate_design_button = gr.Button("Regenerate and improve Plan with Feedback")

    code_output = gr.Textbox(label="Codes")
    feedback_code_input = gr.Textbox(label="Feedback", lines=5, placeholder="Provide feedback to improve the codes after first generated design")
    code_button = gr.Button("Generate codes using your last generated design plan")
    regenerate_code_button = gr.Button("Regenerate and improve Codes with Feedback")


    # Separate chat histories for each stage
    chat_history_overview = gr.State([])
    chat_history_design = gr.State([])
    chat_history_code = gr.State([])


    generate_button.click(create_project_overview, inputs=[title_input, description_input, gr.Textbox(value="", visible=False), gr.State([])], outputs=[overview_output, chat_history_overview])
    regenerate_button.click(create_project_overview, inputs=[title_input, description_input, feedback_input, chat_history_overview], outputs=[overview_output, chat_history_overview])
    design_button.click(design_project, inputs=[overview_output, gr.Textbox(value="", visible=False), gr.State([])], outputs=[design_output, chat_history_design])
    regenerate_design_button.click(design_project, inputs=[overview_output, feedback_design_input, chat_history_design], outputs=[design_output, chat_history_design])
    code_button.click(code_project, inputs=[design_output, gr.Textbox(value="", visible=False), gr.State([])], outputs=[code_output, chat_history_code])
    regenerate_code_button.click(code_project, inputs=[design_output, feedback_code_input, chat_history_code], outputs=[code_output, chat_history_code])

# Launch the interface
if __name__ == "__main__":
    interface.launch()