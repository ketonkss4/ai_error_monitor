# AI Error Monitoring System

The AI Error Monitoring System is designed to receive error reports when a program crashes and return recommendations to fix the error. This project is split into two main components: a FastAPI backend that handles error report submissions and a Next.js frontend for the user interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 12.x or higher
- npm or yarn

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
