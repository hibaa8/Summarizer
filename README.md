# **Book Summarizer**

A full-stack web application that enables users to browse books, view detailed summaries, and filter books by categories. Summaries are generated using generative AI models, providing engaging and insightful content.

---

## **Features**

- **Book Browsing**: View books in a responsive grid layout with images, titles, and authors.
- **Web Scraping**: 
  - Scraped the Amazon website to retrieve product URLs for books.
  - Scraped Project Gutenberg for metadata and full book text.
- **AI-Powered Summaries**: Generate detailed summaries for books using the Gemini 1.5 Flash model.
- **Filters and Search**:
  - Filter books by popular categories (e.g., Science Fiction, Romance).
  - Search books by keywords including title, author, language, category, etc
- **Book Details**: Click on any book to view its details, including language, category, image, and summary.
- **Responsive Design**: Works seamlessly on desktop and mobile devices.

---

## **Tech Stack**

### **Frontend**
- React
- CSS

### **Backend**
- Flask
- SQLite

### **AI Integration**
- **Generative AI (Gemini 1.5)**: 
  - Summaries include detailed descriptions of each chapter/section and key takeaways at the end.
  - **Prompt Engineering**: Designed a custom prompt to structure summaries logically and ensure readability and relevance.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/hibaa8/Summarizer.git
cd Summarizer
```

### **2. Backend Setup**

Navigate to the backend directory:
```bash
cd app/backend
```

Install the necessary requirements
```bash
pip install -r requirements.txt   
```

Run the Flask app:
```bash
flask run
```

### **3.Frontend Setup**

Open a new terminal window and navigate to the frontend directory:
```bash
cd app/frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm start
```

### **View the App**
Open your browser and navigate to: http://127.0.0.1:3000 
(flask server should be running on port 5000)
