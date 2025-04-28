# GenAI-JMeter-Performance-Testing 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/) [![JMeter](https://img.shields.io/badge/JMeter-5.6.3-orange.svg)](https://jmeter.apache.org/)

An end-to-end automation framework that integrates **Apache JMeter** with **OpenAI’s GPT-3.5 Turbo** to run performance tests, generate reports, and get AI-powered insights.

## 📚 Project Description

This project simplifies performance testing by automating:

- Execution of JMeter `.jmx` test plpucans via Python
- Generation of both CSV (`.jtl`) and HTML reports
- Parsing and aggregation of test results with Pandas
- Sending summarized metrics to GPT-3.5-Turbo for analysis
- Suggestions on bottlenecks, optimizations, throughput, and capacity
- Secure API key management via a `.env` file

## 🛠 Features

- **Automated Test Runs**: Non-GUI JMeter execution from a Python script
- **Report Generation**: Auto-generated HTML dashboard + CSV data
- **AI Analysis**: GPT-3.5-Turbo inspects aggregated metrics and offers actionable recommendations
- **Local Hosting**: Serves HTML report at `http://localhost:8000` for easy viewing
- **Secure Secrets**: `.env` file pattern and `.gitignore` to protect API keys
- **Clean Code**: Modular, well-documented, beginner-friendly

## ⚙️ Technologies Used

- **Language**: Python 3.11
- **Performance Tool**: Apache JMeter 5.6.3
- **AI**: OpenAI GPT-3.5 Turbo API
- **Data Processing**: Pandas
- **Env Management**: python-dotenv
- **Version Control**: Git & GitHub

## 🚀 Quick Start

1. **Clone the repo**  
   git clone https://github.com/your-username/GenAI-JMeter-Performance-Testing.git cd GenAI-JMeter-Performance-Testing

2. **(Optional) Create a virtual environment**  
   python -m venv .venv .venv\Scripts\activate # Windows source .venv/bin/activate # macOS/Linux

3. **Install dependencies**  
   pip install -r requirements.txt

4. **Add your OpenAI key**  
   Create a file named `.env` in the project root containing:  
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

5. **Place your JMeter test plan**  
   Put your `.jmx` file (e.g. `TestPlanp9authwave.jmx`) in this folder, or update `JMETER_SCRIPT` in `run_test_and_analyze.py`.

6. **Run the automation**  
   python run_test_and_analyze.py

7. **View the report & analysis**

- **Browser**: http://localhost:8000/index.html
- **Console**: AI insights printed after test run

## 📈 Architecture

```mermaid
flowchart TD
A[User: .jmx Test Plan] --> B[Python Script]
B --> C[JMeter CLI Execution]
C --> D[CSV (.jtl) & HTML Report]
D --> E[Pandas Aggregation]
E --> F[OpenAI GPT-3.5 Analysis]
F --> G[Console Insights + Hosted HTML]





**📅 Roadmap & Future Improvements**
Support dynamic thread/ramp-up parameters via CLI args or config

Slack/Email notifications with AI summary

Historical trend dashboard (store past runs)

GPT-driven .jmx generation from API definitions (Swagger/Postman)
```

📄 License
This project is licensed under the MIT License.

✨ Author
Nitesh Jaiswal
<a href="https://linkedin.com/in/your-linkedin-id" target="_blank" rel="noopener">
Connect with me on LinkedIn
</a>
