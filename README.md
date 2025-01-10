# **Book Summarizer and Recommendation System**

This project is a full-stack  web application that allows users to browse books, view detailed summaries, and filter books by categories. The summaries are generated using generative AI models, providing users with engaging and insightful content.

## **Features**

- **Book Browsing**: View books in a responsive grid layout with images, titles, and authors.
- **AI-Powered Summaries**: Generate detailed summaries for books using the Gemini 1.5 Flash model.
- **Filters and Search**:
  - Filter books by popular categories (e.g., Science Fiction, Romance, etc.).
  - Search books by title or author.
- **Book Details**: Click on any book to view its details, including language, category, image, and summary.
- **Responsive Design**: Works seamlessly on desktop and mobile devices.

## **Tech Stack**

### **Frontend**
- **React**: Interactive user interface and components.
- **CSS**: Styling for responsiveness and clean layout.

### **Backend**
- **Flask**: Python-based web framework for the API and database integration.
- **SQLite**: Lightweight relational database for storing book metadata.

### **AI Integration**
- **Generative AI (Gemini 1.5)**: Used prompt engineering to generate detailed and organized book summaries that covered each chapter/section of the book and had key takeaways at the end.

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/hibaa8/Summarizer.git
cd Summarizer
```

### **2. Backend Setup**
Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Initialize the database:
```bash
flask db upgrade
```
Run the Flask app:
```bash
flask run
```

### **3.Frontend Setup**

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:
```
```bash
npm start
```

### **View the App**
Open your browser and navigate to: http://127.0.0.1:3000 
(assuming that the flask server is running on port 5000)

## **Usage**
- **Browse Books**: Explore books displayed in a grid layout.
- **Filter Books**: Use the sidebar filters to sort books by popular categories.
- **Search Books**: Use the search bar to find books by title or author.
- **View Detailed Summary**: Click on any book card to be directed to a seperate page that showcases book metadata and the LLM-generated summary.

 

