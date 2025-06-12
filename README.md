
# 🍽️ Frugal Foodie: A Cost-Based Restaurant Clustering and Location-Based Recommendation System

**Frugal Foodie** is a cost-based restaurant clustering and location-based recommendation system that helps users discover restaurants that match both their **budget** and **geographic location**.

It combines **unsupervised machine learning (K-Means Clustering)** and **Google’s Geolocation APIs** to deliver intelligent, fast, and personalized restaurant recommendations.

---

## 🚀 Features

- 🔍 Clusters restaurants by **cost-per-person** using **K-Means**
- 📍 Uses **Google Geocoding and Places APIs** to locate nearby restaurants
- 💡 Suggests restaurants based on real-time **location and budget**
- 🖥️ Built with **Flask** and a simple, intuitive web interface
- ✅ Filters out irrelevant options and reduces decision fatigue

---

## 🛠️ Tech Stack

- Python 3
- Flask
- HTML/CSS/JavaScript
- Google Places API & Geocoding API
- Pandas, Scikit-learn
- Jupyter Notebook (for initial model testing)
- Zomato Bangalore Dataset (from Kaggle)

---

## 📁 Project Structure

```bash
├── app.py                  # Flask backend (replace with your API keys)
├── templates/
│   └── index.html          # Frontend form and results
├── static/
│   ├── style.css           # CSS for styling    
│   └── background.jpg      # background image for website
├── dataset/
│   └── zomato.csv          # Zomato dataset
├── requirements.txt        # installing dependencies
├── README.md               
```

---

## 🔑 API Keys Required

To use the Google Maps APIs, you need to add your **Google API keys** in the `app.py` file.

Download the zomato dataset from Kaggle - https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data

### ⚠️ Note:
**DO NOT commit your original API keys to GitHub** — keep them private and secure.

In `app.py`, look for:
```python
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
```
Replace `"YOUR_API_KEY_HERE"` with your actual key.

---

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
  git clone https://github.com/yourusername/Frugal-Foodie-A-Cost-Based-Restaurant-Clustering-and-Location-Based-Recommendation-System.git
  cd Frugal-Foodie-A-Cost-Based-Restaurant-Clustering-and-Location-Based-Recommendation-System
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key** to `app.py` where indicated.

5. **Run the app**
   ```bash
   python app.py
   ```

6. **Open in your browser**
   ```
   http://127.0.0.1:5000
   ```



## 🙌 Contributors

- Diya K Bhat  
- Vivin Jayanth A M  
- Samarth S L  
- Sudarshan D J  



---

## 📄 License

This project is for educational and demonstration purposes only.

---

## 🌐 Citation

Published in the **Journal of Emerging Technologies and Innovative Research (JETIR)**  
**May 2025, Volume 12, Issue 5**

---

## 📬 Feedback

Feel free to open issues or submit pull requests.  
We welcome suggestions to improve functionality and UI/UX!
