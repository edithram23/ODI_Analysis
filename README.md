---

# Gemini Pro Cricket ODI Dataset Project

## Overview
This project utilizes Gemini Pro for querying a Cricket ODI dataset. It includes backend preprocessing tasks, SQL database integration, and frontend development for user interaction.

## Backend
- **Preprocessing**: The dataset is preprocessed for better compatibility with Gemini Pro.
- **SQL Database**: The preprocessed dataset is stored in a SQL database for easy access.
- **Gemini Model**: Gemini Pro is used to fetch the model for query processing.
- **Prompt Generation**: Prompts are generated based on user input,currently focusing on batting and batting stats.
- **TFIDF**: TFIDF is used to extract player names from user input for more accurate queries.

## Frontend
- **React**: The frontend is developed using React for dynamic user interaction.
- **HTML/CSS**: Beautiful CSS is implemented to enhance the user interface.
- **User Input**: Users can type their questions in a text box.
- **Output Display**: The output of the queries is displayed below the text box for easy readability.

## Technologies Used
- **Backend**: Flask, Python
- **Frontend**: React, JavaScript, HTML, CSS
- **Database**: SQL
- **Deployment**: AWS, Azure, Docker containers
- **Other**: Gemini Pro

## How to Run
1. Clone this repository.
2. Install the required dependencies using `npm install`.
3. Add your Gemini API key in the API.env file
4. Start the frontend server using `npm start`.
5. Ensure the backend server server.py is running to fetch the Gemini model and process queries.

## Ongoing works
1. Working on Bowling datasets and merging them to the database

---
### Reference image
- **Q&A**
![image](https://github.com/edithram23/ODI_Analysis/assets/106003437/f9c98c11-549e-4921-89ce-df344ddb9f9b)
- **Comparison**
![image](https://github.com/user-attachments/assets/c13779b9-017f-417b-bfc1-3cdaa9e934d9)
![image](https://github.com/user-attachments/assets/c0cdf296-5588-441e-bb07-316d23204eee)
