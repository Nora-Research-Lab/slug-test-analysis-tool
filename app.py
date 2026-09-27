import gradio as gr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import os
from slug_test_analysis_tool import (
    parse_data, compute_ln_ratio, linear_regression,
    hvorslev_k, bouwer_rice_k, generate_plot, classification_table
)

def process_inputs(r_val, r_unit, L, H0, aquifer_thickness, data_source, file):
    try:
        if data_source == "Paste data" and file is None:
            return "", "", None, "Please paste data or upload a file."
        if data_source == "Upload CSV" and file is not None:
            content = file.decode('utf-8') if isinstance(file, bytes) else str(file)
        else:
            content = file if file else ""
        if not content.strip():
            return "", "", None, "No data provided."

        time, ratio = parse_data(content)
        if len(time) < 2:
            return "", "", None, "Need at least two data points."
        if np.any(ratio <= 0):
            return "", "", None, "Head ratio H(t)/H0 must be > 0."

        K_h, slope, intercept, rsq, T0 = hvorslev_k(r_val, L, H0, time, ratio, r_unit)
        K_br = bouwer_rice_k(r_val, L, H0, time, ratio, aquifer_thickness, r_unit)

        result_text = (
            f"Hvorslev K: {K_h:.4e} m/s  (R² = {rsq:.4f})\n"
            f"Bouwer-Rice K: {K_br:.4e} m/s\n"
            f"Basic time lag T0 = {T0:.2f} s"
        )
        fig = generate_plot(time, ratio, slope, intercept, r_sq=rsq)
        classification = classification_table(K_h if K_h else K_br)

        # Build report text
        report_lines = [
            "Slug Test Analysis Report",
            "="*40,
            f"Well radius: {r_val} {r_unit}",
            f"Screen length: {L} m",
            f"Initial displacement H0: {H0} m",
            f"Aquifer thickness: {'Not specified' if aquifer_thickness is None else f'{aquifer_thickness} m'}",
            "",
            f"Hvorslev conductivity: {K_h:.4e} m/s" if K_h else "Hvorslev: could not compute",
            f"Bouwer-Rice conductivity: {K_br:.4e} m/s" if K_br else "Bouwer-Rice: could not compute",
            f"T0 = {T0:.2f} s",
            "",
            "Classification (Hvorslev):",
            classification
        ]
        report_str = "\n".join(report_lines)

        return result_text, classification, fig, report_str
    except Exception as e:
        return "", "", None, f"Error: {str(e)}"

def download_report(report_text):
    if not report_text:
        return None
    buf = io.BytesIO()
    buf.write(report_text.encode())
    buf.seek(0)
    return buf

with gr.Blocks(title="Slug Test Analysis Tool") as demo:
    gr.Markdown("# Slug Test Analysis Tool")
    gr.Markdown("Compute hydraulic conductivity from slug test data using Hvorslev and Bouwer-Rice methods.")
    
    with gr.Row():
        with gr.Column(scale=1):
            r_val = gr.Number(label="Well radius", value=0.05)
            r_unit = gr.Radio(choices=["m", "cm"], value="m", label="Radius unit")
            L = gr.Number(label="Screen length (m)", value=1.0)
            H0 = gr.Number(label="Initial displacement H0 (m)", value=0.5)
            aquifer_thickness = gr.Number(label="Aquifer thickness (m, optional)", value=None)
            data_source = gr.Radio(choices=["Paste data", "Upload CSV"], value="Paste data", label="Data input method")
            data_input = gr.TextArea(label="Paste time (s) and head ratio (H/H0) pairs, one per line, comma separated", lines=5, placeholder="0,1.0\n10,0.8\n20,0.6\n...")
            file_input = gr.File(label="Upload CSV (time,ratio without header)", file_types=[".csv"], type="binary")
            calc_btn = gr.Button("Calculate")
        
        with gr.Column(scale=2):
            output_text = gr.Textbox(label="Results", lines=4)
            classification = gr.Textbox(label="Material classification", lines=6)
            plot = gr.Plot(label="ln(H/H0) vs Time with regression line")
            report_download = gr.File(label="Download full report")

    calc_btn.click(
        fn=process_inputs,
        inputs=[r_val, r_unit, L, H0, aquifer_thickness, data_source, data_input if data_source.value == "Paste data" else file_input],
        outputs=[output_text, classification, plot, report_download]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
