# AI Error Monitoring System

The AI Error Monitoring System is designed to receive error reports when a program crashes and return recommendations to fix the error. 
The system will receive error reports from its /error-report POST endpoint upon which it will show error received to the frontend-ui chat window interface. Then the error will be processed and a message from the AI system will show in the chat window with the explanation for the error along with the proposed plan for the solution. The chat bubble will have button options to accept the solution, provide feedback, or ignore. 

This project is split into two main components: a FastAPI backend that handles error report submissions and a Next.js frontend for the user interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 12.x or higher
- npm or yarn
- ANTHROPIC_API_KEY and OPENAI_API_KEY API in .env folder

### Installation

1. **Clone the repository**

2. **Set up the backend (FastAPI)**

Navigate to the backend directory and install the required Python dependencies.

```bash
cd backend
pip install -r requirements.txt
```

3. **Set up the frontend (Next.js)**

Navigate to the frontend directory and install the required Node.js dependencies.

```bash
cd ../frontend-ui
npm install
# or
yarn install
```

### Running the Application

1. **Start the FastAPI server**

From the backend directory, run the FastAPI server.

```bash
uvicorn main:app --reload
```

The FastAPI server will start on `http://localhost:8000`. The `--reload` flag enables hot reloading during development.

2. **Start the Next.js frontend**

Open a new terminal window or tab, navigate to the frontend-ui directory, and start the Next.js development server.

```bash
npm run dev
# or
yarn dev
```

The Next.js application will start on `http://localhost:3000`.

## Using the Application
- Navigate to `http://localhost:3000` in your browser to access the frontend UI.
- To submit an error report, use the `/error-report` POST endpoint on the FastAPI server (`http://localhost:8000/error-report`). You can use tools like Postman or cURL for this purpose.

## Submitting Error Reports Programmatically

To integrate the AI Error Monitoring System into your application, wrap the code you want to monitor in a try-catch block. Save the stack trace to a text file and send the location path of that error report to the `/error-report` endpoint.

### Examples

#### Python

```python
import requests
import traceback

try:
    # Your code here
    1 / 0  # Example error
except Exception as e:
    error_report = traceback.format_exc()
    with open("error_report.txt", "w") as file:
        file.write(error_report)
    response = requests.post("http://localhost:8000/error-report", json={"location": "error_report.txt"})
    print(response.json())
```

#### JavaScript (Node.js)

```javascript
const fs = require('fs');
const axios = require('axios');

try {
    // Your code here
    throw new Error('Example error'); // Example error
} catch (error) {
    fs.writeFileSync('error_report.txt', error.stack);
    axios.post('http://localhost:8000/error-report', { location: 'error_report.txt' })
        .then(response => console.log(response.data))
        .catch(error => console.error(error));
}
```

#### Java

```java
import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class ErrorReportExample {
    public static void main(String[] args) {
        try {
            // Your code here
            throw new Exception("Example error"); // Example error
        } catch (Exception e) {
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            String errorReport = sw.toString();

            try (PrintWriter out = new PrintWriter("error_report.txt")) {
                out.println(errorReport);
            } catch (Exception fileException) {
                fileException.printStackTrace();
            }

            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:8000/error-report"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString("{\"location\":\"error_report.txt\"}"))
                    .build();

            try {
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                System.out.println(response.body());
            } catch (Exception httpException) {
                httpException.printStackTrace();
            }
        }
    }
}
```

These examples demonstrate how to catch errors, save them to a file, and then send a POST request to the `/error-report` endpoint with the location of the error report file.
