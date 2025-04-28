import os
import shutil
import subprocess
import threading
import http.server
import socketserver

import pandas as pd # type: ignore
from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore


load_dotenv()
# === CONFIGURATION ===
API_KEY         = os.getenv("OPENAI_API_KEY")       # 🔐 Replace with your actual key
JMETER_BIN      = r"D:\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat"
JMETER_SCRIPT   = "TestPlanp9authwave.jmx"
RESULTS_FILE    = "results.jtl"
HTML_REPORT_DIR = "html-report"
HTTP_PORT       = 8000

# === STEP 1: Clean up previous artifacts ===
for path in (RESULTS_FILE, HTML_REPORT_DIR):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

# === STEP 2: Run JMeter Test Plan ===
print("🚀 Running JMeter test...")
jmeter_cmd = [
    JMETER_BIN,
    "-n",
    "-t", JMETER_SCRIPT,
    "-l", RESULTS_FILE,
    "-e", "-o", HTML_REPORT_DIR,
    "-Jjmeter.save.saveservice.output_format=csv",
    "-Jjmeter.save.saveservice.response_time=true"
]
subprocess.run(jmeter_cmd, check=True)
print(f"✅ JMeter run complete. CSV: {RESULTS_FILE}, HTML report: {HTML_REPORT_DIR}/index.html")

# === STEP 3: Serve HTML Report Locally ===
def serve_html_report(report_dir: str, port: int):
    import functools
    custom_handler = functools.partial(http.server.SimpleHTTPRequestHandler,directory=report_dir)
    httpd = socketserver.TCPServer(("", port), custom_handler)
    print(f"🌐 Serving HTML report on http://localhost:{port}/index.html")
    # Start as a non‑daemon thread so it lives beyond main work
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=False)
    server_thread.start()

serve_html_report(HTML_REPORT_DIR, HTTP_PORT)

# === STEP 4: Read & Aggregate the Full CSV ===
if not os.path.exists(RESULTS_FILE):
    print(f"❌ Results file '{RESULTS_FILE}' not found. Exiting.")
    exit(1)

print("📊 Reading and aggregating test results...")
df = pd.read_csv(RESULTS_FILE)

# Overall metrics
total_requests = len(df)
avg_rt         = df["elapsed"].mean()
max_rt         = df["elapsed"].max()
min_rt         = df["elapsed"].min()
error_count    = df[df["success"] == False].shape[0]
error_rate     = (error_count / total_requests) * 100

# Per‑sampler breakdown
grouped = (
    df.groupby("label")["elapsed"]
      .agg(requests="count", avg="mean", max="max", min="min")
      .reset_index()
)
summary_table = grouped.to_string(index=False)

# === STEP 5: Prepare Full‑Report Prompt for GPT ===
prompt = f"""
You are a performance testing expert. Here is a summary of an entire JMeter test run:

Test Summary:
- Total Requests: {total_requests}
- Avg Response Time: {avg_rt:.2f} ms
- Max Response Time: {max_rt:.2f} ms
- Min Response Time: {min_rt:.2f} ms
- Error Count: {error_count}
- Error Rate: {error_rate:.2f}%

Breakdown by sampler (label):
{summary_table}

Questions:
1. Which samplers are the slowest or most error‑prone?
2. Do these results indicate any performance bottlenecks?
3. What optimizations or fixes would you suggest?
4. What is the average throughput of each request?
5. Provide the minmum and maximum response time recorded?
6. Pridict the probable choke point by analyzing the result.
7. Prodict the amount of users the system can handle safely.
"""

# === STEP 6: Send to OpenAI & Print Analysis ===
print("🤖 Sending aggregated report to GPT-3.5-Turbo for analysis...")
client   = OpenAI(api_key=API_KEY)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a performance testing expert."},
        {"role": "user",   "content": prompt}
    ],
    max_tokens=700,
)

print("\n📈 GPT Analysis:")
print(response.choices[0].message.content)

# === STEP 7: Keep the server running until user is done ===
input("\nPress Enter to stop the HTTP server and exit…")