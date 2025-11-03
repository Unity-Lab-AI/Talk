# Talk to Unity

This project is a simple, voice-controlled AI assistant that runs in your web browser.

## Prerequisites

Before you begin, ensure you have the following:

*   **A modern web browser:** Chrome, Edge, or Safari are recommended. Firefox is not fully supported due to limitations in the Web Speech API.
*   **A secure connection:** The application must be run from a secure context (`https` or `localhost`).
*   **A microphone:** Required for voice input.
*   **Python 3:** Used to run a simple web server and install dependencies.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Unity-Lab-AI/Talk-to-Unity.git
    cd Talk-to-Unity
    ```

2.  **Install dependencies:**
    This project uses Playwright for testing. Install the necessary dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the web server:**
    You can use Python's built-in HTTP server to run the application locally:
    ```bash
    python -m http.server 8000
    ```

4.  **Open the application:**
    Open your web browser and navigate to `http://localhost:8000`.

## How to Use

1.  The landing page will check if your browser meets the requirements.
2.  If all checks pass, click the "Launch" button to start the AI assistant.
3.  Click the microphone button to unmute and start speaking.

## File Structure

| File              | Purpose                                                 |
| ----------------- | ------------------------------------------------------- |
| `index.html`      | The main HTML file for the application.                 |
| `indexAI.html`    | The HTML for the AI assistant interface.                |
| `style.css`       | The main stylesheet for the application.                |
| `styleAI.css`     | The stylesheet for the AI assistant interface.          |
| `app.js`          | The main JavaScript file for the application logic.     |
| `landing.js`      | The JavaScript file for the landing page.               |
| `vosklet-adapter.js` | An adapter for the Vosklet speech recognition library. |
| `ai-instruct.txt` | A text file containing the AI's system prompt.          |
| `requirements.txt`| A list of Python dependencies for the project.          |

## Feedback and Contributions

*   For issues and feedback, please open an issue on the [GitHub repository](https://github.com/Unity-Lab-AI/Talk-to-Unity/issues).
*   Contributions are welcome! Please feel free to submit a pull request.