# Smart Email Priority Sorter

### Quick Start
```bash
python -m venv .venv && source .venv/bin/activate 
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords
python -m pip install joblib
python -m src.train_classifier          
streamlit run app.py



# Smart Email Priority Sorter 📧  

An AI-powered app that reads your emails and automatically sorts them by **priority and action urgency** using NLP + Machine Learning.  
Built with **Python, Streamlit, Gmail API, and SQLite.**

---

## 🚀 Quick Start

### ✅ Requirements
- Python 3.11  
- Internet connection  
- Gmail API credentials (for live mode)

---

### ⚙️ Setup (Windows)
```powershell
git clone https://github.com/swarrajjoshi/smart-email-priority.git
cd smart-email-priority
./setup.ps1
