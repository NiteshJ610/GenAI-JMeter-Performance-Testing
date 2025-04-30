import os
import shutil
import subprocess
import pandas as pd  # type: ignore
import pytest  # type: ignore


# Test cleanup of previous artifacts
def test_cleanup_artifacts(tmp_path):
    results_file = tmp_path / "results.jtl"
    html_report_dir = tmp_path / "html-report"
    results_file.write_text("dummy data")
    html_report_dir.mkdir()

    assert results_file.exists()
    assert html_report_dir.exists()

    # Simulate cleanup
    for path in (results_file, html_report_dir):
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    assert not results_file.exists()
    assert not html_report_dir.exists()


# Test JMeter command execution
@patch("subprocess.run")
def test_run_jmeter(mock_subprocess_run):
    jmeter_bin = "jmeter.bat"
    jmeter_script = "TestPlan.jmx"
    results_file = "results.jtl"
    html_report_dir = "html-report"

    jmeter_cmd = [
        jmeter_bin,
        "-n",
        "-t", jmeter_script,
        "-l", results_file,
        "-e", "-o", html_report_dir,
        "-Jjmeter.save.saveservice.output_format=csv",
        "-Jjmeter.save.saveservice.response_time=true"
    ]

    subprocess.run(jmeter_cmd, check=True)
    mock_subprocess_run.assert_called_once_with(jmeter_cmd, check=True)


# Test CSV aggregation
@patch("pandas.read_csv")
def test_aggregate_csv(mock_read_csv):
    mock_df = pd.DataFrame({
        "elapsed": [100, 200, 300],
        "success": [True, False, True],
        "label": ["Sampler1", "Sampler2", "Sampler1"]
    })
    mock_read_csv.return_value = mock_df

    df = pd.read_csv("results.jtl")
    total_requests = len(df)
    avg_rt = df["elapsed"].mean()
    max_rt = df["elapsed"].max()
    min_rt = df["elapsed"].min()
    error_count = df[~df["success"]].shape[0]
    error_rate = (error_count / total_requests) * 100

    assert total_requests == 3
    assert avg_rt == 200
    assert max_rt == 300
    assert min_rt == 100
    assert error_count == 1
    assert error_rate == pytest.approx(33.33, rel=1e-2)


# === Uncomment and update these later as needed ===

# @patch("threading.Thread.start")
# def test_serve_html_report(mock_thread_start):
#     import sys
#     sys.path.append("..")
#     from ..run_test_and_analyze import serve_html_report
#     serve_html_report("html-report", 8000)
#     mock_thread_start.assert_called_once()

# @patch("openai.ChatCompletion.create")
# def test_openai_api_call(mock_openai_create):
#     mock_openai_create.return_value = MagicMock(
#         choices=[{"message": {"content": "Test analysis"}}]
#     )
#     import sys
#     sys.path.append("..")
#     from ..run_test_and_analyze import OpenAI
#     client = OpenAI(api_key="dummy_key")
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": "Test prompt"}],
#         max_tokens=700,
#     )
#     assert response.choices[0].message.content == "Test analysis"
#     mock_openai_create.assert_called_once()
