# 🏇 EquiCast AI
### Artificial Intelligence for the Sport of Kings

**EquiCast AI** is a Python-based horse racing analytics platform that combines machine learning, probabilistic simulation, and race dynamics via Monte Claro simulations to explore thoroughbred racing and breeding performance.

The platform currently features **Furlong Lab**, an interactive race simulation and analytics tool, alongside **Stallion Sync**, an upcoming pedigree and breeding intelligence product.

**Version:** 1.0  
**Status:** Furlong Lab functional | Stallion Sync coming soon

---

## 🚀 Products

### 🏁 Furlong Lab — Race Prediction & Simulation

Furlong Lab combines a Random Forest machine learning model with Monte Carlo simulations to estimate race outcomes and account for varying racing conditions.

**Key features:**
- Machine learning-based horse performance rankings
- Configurable Monte Carlo simulations (up to 20,000 iterations)
- Simulated win, top-three finish, and DNF probabilities
- Race dynamics including pace adjustments, traffic, speed duels, and stumbles
- Individual horse analysis with model-generated explanations
- Machine Learning vs. Monte Carlo ranking comparisons
- Downloadable simulation results
- Interactive Streamlit analytics dashboard

Furlong Lab currently supports three thoroughbred races.

### 🧬 Stallion Sync — Pedigree & Breeding Intelligence

Stallion Sync is a planned analytics product focused on pedigree evaluation, breeding intelligence, and stallion valuation.

**Status:** Coming in a future release.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development language |
| scikit-learn | Random Forest machine learning |
| NumPy | Numerical computation and simulation |
| pandas | Data processing and analysis |
| Streamlit | Multipage web application and interactive dashboard |
| Matplotlib | Data visualization |
| joblib | Model serialization and loading |
| CSS3 | Custom UI styling, branding, and page-specific themes |


---

## 🧠 How Furlong Lab Works

**1. Historical race data**

Historical thoroughbred racing data is used to train the machine learning model and support performance analysis.

**2. Machine learning prediction**

A Random Forest model generates predicted horse performance scores and baseline rankings by comparing the horse's stats to those of horses in past races and compares with their perfromance.

**3. Monte Carlo simulation**

Thousands of simulated race scenarios introduce randomness and race dynamics such as pace interactions, traffic disruptions, and stumbles.

**4. Probability estimation**

Aggregated simulation outcomes produce estimated win probabilities, top-three probabilities, and DNF rates.

**5. Interactive analysis**

Users can compare rankings, examine individual horse performance, inspect simulation adjustments, and export results.

---

## 💻 Running Locally

Clone the repository:

```bash
git clone https://github.com/shaikh1427/EQUICASTAI.git
cd EQUICASTAI
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app/app.py
```

The application should open in your browser.

---

## 📁 Project Structure

```text
EQUICASTAI/
├── .streamlit/
│   └── config.toml
├── app/
│   ├── app.py
│   └── pages/
│       ├── home.py
│       ├── furlong_lab.py
│       └── stallion_sync.py
├── assets/
│   ├── EquicastAI/
│   ├── FurlongLab/
│   ├── StallionSync/
│   ├── furlong_lab.css
│   └── stallion_sync.css
├── data/
├── models/
├── notebooks/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚠️ Model Limitations

Furlong Lab produces simulated probabilities rather than guaranteed race outcomes.

Predictions depend on the available historical data, model assumptions, input features, and stochastic simulation behavior. Results should be interpreted as experimental analytical estimates rather than calibrated real-world probabilities.

The platform is designed for racing analytics, education, and technical experimentation, NOT wagering recommendations.

---

## ⏳ Future Development

**V2 and beyond:**
- Stallion Sync: pedigree and breeding intelligence
- Doc Hooves: interactive AI assistant
- Expanded racing datasets
- Further model validation and analytics improvements

---

## 👨‍💻 Author

**Abdullah Shaikh**  
Mechanical Engineering — Virginia Tech

Developed as a personal passion project combining a lieflong love of horse racing with machine learning, probabilistic modeling, simulation, and software development.

---

*EquiCast AI V1.0 — Artificial Intelligence for the Sport of Kings.*