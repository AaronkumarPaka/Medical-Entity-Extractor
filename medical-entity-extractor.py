import re
import tkinter as tk
from tkinter import filedialog, messagebox

# -----------------------------
# Medical Dictionaries
# -----------------------------

DISEASES = ["diabetes","dengue","malaria","covid","asthma"]
SYMPTOMS = ["fever","cough","headache","fatigue","pain"]
DRUGS = ["paracetamol","insulin","aspirin","ibuprofen"]
TESTS = ["mri","xray","blood test","ct scan","ultrasound"]

# -----------------------------
# Read Prescription File
# -----------------------------

def read_file(path):
    with open(path,"r") as f:
        return f.read()

# -----------------------------
# Preprocess Text
# -----------------------------

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]',' ',text)
    tokens = text.split()
    return tokens

# -----------------------------
# Entity Extraction
# -----------------------------

def extract_entities(text):

    tokens = preprocess(text)

    results = {
        "DISEASE": [],
        "SYMPTOM": [],
        "DRUG": [],
        "TEST": []
    }

    for token in tokens:

        if token in DISEASES:
            results["DISEASE"].append(token)

        if token in SYMPTOMS:
            results["SYMPTOM"].append(token)

        if token in DRUGS:
            results["DRUG"].append(token)

        if token in TESTS:
            results["TEST"].append(token)

    return results

# -----------------------------
# UI Functions
# -----------------------------

def load_prescription():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    text = read_file(file_path)

    prescription_text.delete("1.0", tk.END)
    prescription_text.insert(tk.END, text)

def run_extraction():

    text = prescription_text.get("1.0", tk.END)

    entities = extract_entities(text)

    output_text.delete("1.0", tk.END)

    for key,value in entities.items():

        if value:
            output_text.insert(tk.END, key + " : " + ", ".join(set(value)) + "\n")

# -----------------------------
# UI Layout
# -----------------------------

window = tk.Tk()
window.title("Medical Prescription Entity Extractor")
window.geometry("700x500")

title = tk.Label(window,text="Medical Prescription Analyzer",font=("Arial",16))
title.pack(pady=10)

load_button = tk.Button(window,text="Load Prescription File",command=load_prescription)
load_button.pack()

prescription_text = tk.Text(window,height=10,width=80)
prescription_text.pack(pady=10)

extract_button = tk.Button(window,text="Extract Medical Entities",command=run_extraction)
extract_button.pack(pady=5)

output_label = tk.Label(window,text="Extracted Entities:")
output_label.pack()

output_text = tk.Text(window,height=10,width=80)
output_text.pack(pady=10)

window.mainloop()
