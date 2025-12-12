# Multi Domain Intelligence Platform  

A versatile web platform built with Python and Streamlit that helps users explore and analyze multiple domains: cybersecurity incidents, datasets, and IT support tickets. It also includes a built-in AI assistant to provide guidance and insights. Perfect for learning, analysis, and decision-making.  

---

## Features  

- **Secure login system** – Users can register and log in with roles like Analyst, Admin, or Manager.  
- **Cybersecurity dashboard** – Track and analyze incidents with severity levels and status updates.  
- **Data exploration** – View datasets, calculate sizes, and perform simple analytics.  
- **IT support management** – Open, assign, and close tickets, keeping track of priority and status.  
- **Interactive dashboards** – Beautiful charts and tables using Plotly for visual insights.  
- **AI assistant** – Ask questions or get suggestions related to security or datasets.  

---

## Project Structure  

Here’s a quick overview of how the project is organized:  
multi_domain_platform

├── models/                  
│   ├── __init__.py

│   ├── user.py

│   ├── security_incident.py

│   ├── dataset.py

│   └── it_ticket.py

├── services/                
│   ├── __init__.py

│   ├── database_manager.py

│   ├── auth_manager.py

│   └── ai_assistant.py

├── database/                
│   ├── db.py

│   └── platform.db

├── pages/                   
│   ├── 1_Dashboard.py

│   ├── 2_Cybersecurity.py

│   ├── 3_Data_Science.py

│   ├── 4_IT_Operations.py

│   └── 5_🤖_AI_Assistant.py

├── .streamlit/              
│   └── secrets.toml

├── Home.py  

├── requirements.txt         
└── README.md

---

## Installation & Setup  

Follow these steps to get the app running on your machine:  

1. **Clone the repo**:  
```bash
git clone https://github.com/gladnessMaduhu/CW2_M01018772_CST1510.git
cd C:\Users\Hp\PycharmProjects\CW2_M01018772_CST1510\multi_domain_platform
``` 

2. **Create and activate a virtual environment**:  
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
``` 
3. **Install dependencies**:

pip install -r requirements.txt

4. **Add your API key in .streamlit/secret.toml**: 

GEMINI_API_KEY = "your_new_api_key_here"

5. **Run the app**:

streamlit run Home.py 

6. **open in browser** 
 
streamlit will open the app or you can navigate to the provided local URL

**Technologies Used**

python 3.10+,
streamlit,
SQLite,
Pandas,
Ploty/ Matplotlib ( for visualization),
Gemini AI ( for AI assistant). 

**contributor name is GLADNESS MADUHU, STUDENT ID = M01018772**


