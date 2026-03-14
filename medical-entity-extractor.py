import re
import tkinter as tk
from tkinter import filedialog, messagebox

DISEASES = ["diabetes","dengue","malaria","covid","asthma","migraine","viral infection"]
SYMPTOMS = ["fever","cough","headache","fatigue","pain","nausea"]
DRUGS = ["paracetamol","insulin","aspirin","ibuprofen","sumatriptan"]
TESTS = ["mri","xray","blood test","ct scan","ultrasound"]

records = []
current_record = 0

def read_file(path):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()

def extract_entities(text):
    text = text.lower()
    results = {
        "DISEASE": [],
        "SYMPTOM": [],
        "DRUG": [],
        "TEST": []
    }

    for disease in DISEASES:
        if disease in text:
            results["DISEASE"].append(disease)

    for symptom in SYMPTOMS:
        if symptom in text:
            results["SYMPTOM"].append(symptom)

    for drug in DRUGS:
        if drug in text:
            results["DRUG"].append(drug)

    for test in TESTS:
        if test in text:
            results["TEST"].append(test)

    return results

def load_prescription():
    global records, current_record
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    text = read_file(file_path)
    records = text.split("Record")
    records = [r.strip() for r in records if r.strip() != ""]
    current_record = 0
    show_record()

def show_record():
    global current_record
    if current_record < len(records):
        prescription_text.delete("1.0", tk.END)
        prescription_text.insert(tk.END, "Record " + records[current_record])

def next_record():
    global current_record
    if current_record < len(records) - 1:
        current_record += 1
        show_record()
    else:
        messagebox.showinfo("End","No more records")

def run_extraction():
    text = prescription_text.get("1.0", tk.END)
    output_text.delete("1.0", tk.END)

    name = re.search(r'PATIENT_NAME:\s*([A-Za-z ]+)', text)
    age = re.search(r'AGE:\s*(\d+)', text)
    gender = re.search(r'GENDER:\s*(Male|Female)', text)
    date = re.search(r'DATE:\s*([0-9\-]+)', text)
    symptoms = re.search(r'SYMPTOMS:\s*([A-Za-z ,]+)', text)
    diagnosis = re.search(r'DIAGNOSIS:\s*([A-Za-z ]+)', text)
    medication = re.search(r'MEDICATION:\s*([A-Za-z0-9 ]+)', text)
    doctor = re.search(r'DOCTOR:\s*Dr\.?\s*([A-Za-z ]+)', text)
    hospital = re.search(r'HOSPITAL:\s*([A-Za-z ]+)', text)

    if name:
        output_text.insert(tk.END, "PATIENT NAME : " + name.group(1) + "\n")
    if age:
        output_text.insert(tk.END, "AGE : " + age.group(1) + "\n")
    if gender:
        output_text.insert(tk.END, "GENDER : " + gender.group(1) + "\n")
    if date:
        output_text.insert(tk.END, "DATE : " + date.group(1) + "\n")
    if symptoms:
        output_text.insert(tk.END, "SYMPTOMS : " + symptoms.group(1) + "\n")
    if diagnosis:
        output_text.insert(tk.END, "DIAGNOSIS : " + diagnosis.group(1) + "\n")
    if medication:
        output_text.insert(tk.END, "MEDICATION : " + medication.group(1) + "\n")
    if doctor:
        output_text.insert(tk.END, "DOCTOR : Dr. " + doctor.group(1) + "\n")
    if hospital:
        output_text.insert(tk.END, "HOSPITAL : " + hospital.group(1) + "\n")

    entities = extract_entities(text)
    for key,value in entities.items():
        if value:
            output_text.insert(tk.END, key + " : " + ", ".join(set(value)) + "\n")

window = tk.Tk()
window.title("Medical Prescription Entity Extractor")
window.geometry("700x500")

title = tk.Label(window,text="Medical Prescription Analyzer",font=("Arial",16))
title.pack(pady=10)

load_button = tk.Button(window,text="Load Prescription File",command=load_prescription)
load_button.pack()

next_button = tk.Button(window,text="Next Record",command=next_record)
next_button.pack(pady=5)

prescription_text = tk.Text(window,height=10,width=80)
prescription_text.pack(pady=10)

extract_button = tk.Button(window,text="Extract Medical Entities",command=run_extraction)
extract_button.pack(pady=5)

output_label = tk.Label(window,text="Extracted Entities:")
output_label.pack()

output_text = tk.Text(window,height=10,width=80)
output_text.pack(pady=10)

window.mainloop()