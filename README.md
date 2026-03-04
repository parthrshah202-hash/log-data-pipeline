# 📊 Server Log Analysis Pipeline

A modular Python pipeline for analyzing server log data with automated reporting and visualization.

**Live Demo:** View Dashboard (link)

---

## Overview

This project processes server log data through a 4-stage pipeline:

* **Ingest** → Load and clean raw CSV data
* **Transform** → Aggregate into 5 metric dimensions
* **Analyze** → Generate text reports with insights
* **Visualize** → Create 9 charts and interactive dashboard

Built as a first-year project to learn data engineering and analysis.

---

## ⚙️ Tech Stack

* **Data Processing:** Python, Pandas, NumPy
* **Visualization:** Matplotlib
* **Dashboard:** Streamlit
* **PDF Generation:** FPDF2

---

## Installation

```bash
git clone https://github.com/parthrshah202-hash/log-data-pipeline.git
cd log-data-pipeline
pip install -r requirements.txt
```

---

## Usage

### Run the pipeline:

```bash
python Processing/ingest.py
python Processing/transform.py
python Processing/analyze.py
python Processing/visualize.py
python report.py              # Optional: Generate PDF
```


---

### View dashboard:

```bash
streamlit run dashboard.py
```

Opens at:

```
http://localhost:8501
```

---

## 📁 Project Structure

```
log-data-pipeline/
├── Data/
│   ├── RAW/              # Source data
│   ├── CLEANED/          # After cleaning
│   └── Transformed/      # Aggregated metrics
├── Processing/
│   ├── ingest.py         # Data loading & cleaning
│   ├── transform.py      # Metric generation
│   ├── analyze.py        # Text reports
│   └── visualize.py      # Chart creation
├── Outputs/
│   ├── Reports/          # Text analysis
│   └── Charts/           # Visualizations
├── dashboard.py          # Streamlit interface
├── report.py             # PDF generation
├── Final_Report.pdf  
└── requirements.txt
```

---

## Analysis Dimensions

1. **User Metrics** – Activity patterns, success rates, bandwidth
2. **Endpoint Analysis** – Performance, error rates
3. **Hourly Patterns** – Traffic distribution by hour
4. **Daily Trends** – Request volumes over time
5. **HTTP Methods** – Method distribution and performance

---

## 🎓 What I Learned

* Building modular data pipelines
* Pandas aggregation and transformation
* Creating 8 different chart types with Matplotlib
* Building dashboards with Streamlit (learned from official docs)
* Statistical analysis (outlier detection, trend analysis)
* Reading documentation instead of relying on tutorials

---

## Future Improvements

* File upload for custom datasets
* Real-time log streaming
* Interactive filters in dashboard
* Support for multiple log formats

---

## 👤 Author

**Parth Shah**
First Year BTech - Computer Engineering, PICT Pune

GitHub: @parthrshah202-hash
LinkedIn: https://www.linkedin.com/in/parth-shah-26154a372/

---

Built as a learning project | February 2026

---


