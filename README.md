# ⚡ OpenEV-RL: EV Routing Under Stochastic Weather

A reinforcement-learning environment that simulates electric vehicle routing
under battery constraints, traffic pressure, and stochastic weather regimes.

## ✨ Motivation
Real EVs face:
- unpredictable weather affecting efficiency  
- changing traffic  
- battery depletion dynamics  

Frontier models should learn adaptive energy-aware driving policies.

---

# 🧠 Observation Space (4-D)
1. **battery** (float)  
2. **distance_left** (float)  
3. **traffic_factor** (float)  
4. **weather_idx** (0=clear,1=cloudy,2=rain)

---

# 🎮 Action Space
Continuous scalar **a ∈ [0,1]**  
- 0 = minimal speed  
- 1 = aggressive driving  

---

# 🧩 Task Difficulties
### Easy  
Short trip, high battery.

### Medium  
Longer trip, heavier traffic.

### Hard  
Long route, low battery, **weather mode transitions**:
- clear → cloudy → rain transitions with P=0.2

This is mild frontier-level stochastic optimization.

---

# 🏗 Running Locally
pip install -r requirements.txt
streamlit run gui.py


---

# 🧪 API (FastAPI)

GET /reset/{env}
GET /step/{env}/{action}


---

# 🏁 Baseline Scores
Random agent:
- easy: 0.25  
- medium: 0.10  
- hard: 0.05  

---

# ⚙ Included
- Streamlit GUI  
- FastAPI backend  
- OpenENV-compliant structure  
- Inference script  
- Dockerfile