import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json  # Pro ukládání naučených dat a úkolů
import os
import random  # Pro simulaci učení, pokud uživatel nezadá zpětnou vazbu
from tkinter import simpledialog

# Pevně dané ukázkové události
SAMPLE_EVENTS = [
    {"start": "2025-02-23T10:00:00", "end": "2025-02-23T11:00:00", "summary": "Schůzka s týmem"},
    {"start": "2025-02-23T14:00:00", "end": "2025-02-23T15:00:00", "summary": "Prezentace projektu"}
]

# Načtení nebo inicializace trvalých úkolů
TASKS_DATA_FILE = "timemaster_tasks.json"
if os.path.exists(TASKS_DATA_FILE):
    with open(TASKS_DATA_FILE, "r") as f:
        DEFAULT_TASKS = json.load(f)
else:
    DEFAULT_TASKS = ["Pracovat na projektu X", "Přečíst e-maily", "Příprava na schůzku", "Zavolat klientovi"]
    with open(TASKS_DATA_FILE, "w") as f:
        json.dump(DEFAULT_TASKS, f)

# Načtení nebo inicializace naučených dat (uloženo v souboru)
LEARNED_DATA_FILE = "timemaster_learned.json"
if os.path.exists(LEARNED_DATA_FILE):
    with open(LEARNED_DATA_FILE, "r") as f:
        learned_durations = json.load(f)
else:
    learned_durations = {
        "Pracovat na projektu X": 2.0,
        "Přečíst e-maily": 0.5,
        "Příprava na schůzku": 1.0,
        "Zavolat klientovi": 1.0
    }

def save_learned_durations():
    with open(LEARNED_DATA_FILE, "w") as f:
        json.dump(learned_durations, f)

def save_tasks():
    with open(TASKS_DATA_FILE, "w") as f:
        json.dump(DEFAULT_TASKS, f)

def update_learned_durations(task, actual_duration=None):
    # Simulace učení - upravujeme odhad na základě zpětné vazby od uživatele
    if task not in learned_durations:
        learned_durations[task] = 1.0  # Nový úkol má defaultně 1 hodinu
    
    if actual_duration is not None:
        # Uživatel zadal skutečnou dobu, aktualizujeme průměrem
        learned_durations[task] = (learned_durations[task] + actual_duration) / 2
        messagebox.showinfo("TimeMaster", f"Skvělá volba! Uložím si, že {task} trvá {actual_duration} hodin.")
    else:
        # Náhodný posun pro simulaci učení (pokud není zpětná vazba)
        learned_durations[task] += random.uniform(-0.2, 0.2)
        learned_durations[task] = max(0.5, min(3.0, learned_durations[task]))  # Omezení 0.5-3 hodiny
    save_learned_durations()

def parse_events(events):
    busy_slots = []
    for event in events:
        start = datetime.datetime.fromisoformat(event["start"])
        end = datetime.datetime.fromisoformat(event["end"])
        busy_slots.append((start, end, event["summary"]))
    return busy_slots

def analyze_schedule(busy_slots):
    free_slots = []
    day_start = datetime.datetime(2025, 2, 23, 8, 0, 0)
    day_end = datetime.datetime(2025, 2, 23, 18, 0, 0)
    
    current_time = day_start
    for busy_start, busy_end, _ in sorted(busy_slots, key=lambda x: x[0]):
        if current_time < busy_start:
            free_slots.append((current_time, busy_start))
        current_time = max(current_time, busy_end)
    
    if current_time < day_end:
        free_slots.append((current_time, day_end))
    
    return free_slots, busy_slots

def suggest_schedule(free_slots, tasks):
    schedule = []
    task_index = 0
    
    for slot_start, slot_end in free_slots:
        slot_duration = (slot_end - slot_start).total_seconds() / 3600
        while task_index < len(tasks) and slot_duration >= learned_durations.get(tasks[task_index], 1.0):
            task = tasks[task_index]
            duration = learned_durations[task]
            schedule.append(f"{slot_start.strftime('%H:%M')} - {task} ({duration:.1f}h)")
            slot_start += datetime.timedelta(hours=duration)
            slot_duration -= duration
            task_index += 1
            # Po naplánování se můžeme zeptat na zpětnou vazbu přes dialog
            if messagebox.askyesno("TimeMaster", f"Kolik času ti skutečně trval {task}?"):
                # Dialog pro zadání času v hodinách nebo minutách
                time_input = simpledialog.askstring("TimeMaster", "Zadej dobu trvání (např. '1.5' pro 1.5 hodiny nebo '90' pro 90 minut):", parent=root)
                if time_input:
                    try:
                        if "minut" in time_input.lower() or time_input.isdigit():
                            minutes = float(time_input.replace("minut", "").strip())
                            actual_duration = minutes / 60  # Převod minut na hodiny
                        else:
                            actual_duration = float(time_input)  # Předpokládáme hodiny
                        if 0.1 <= actual_duration <= 24.0:  # Omezení 6 minut až 24 hodin
                            update_learned_durations(task, actual_duration)
                        else:
                            messagebox.showwarning("TimeMaster", "Doba musí být mezi 6 minutami a 24 hodinami!")
                    except ValueError:
                        messagebox.showwarning("TimeMaster", "Neplatná hodnota! Zachovám původní odhad.")
                else:
                    update_learned_durations(task)  # Simulace učení bez zpětné vazby
    
    return schedule

def add_permanent_task():
    new_task = simpledialog.askstring("TimeMaster", "Zadej nový trvalý úkol (např. 'Napsat zprávu'):", parent=root)
    if new_task and new_task not in DEFAULT_TASKS:
        DEFAULT_TASKS.append(new_task)
        update_learned_durations(new_task)  # Inicializace nového úkolu
        save_tasks()
        messagebox.showinfo("TimeMaster", f"Přidal jsem '{new_task}' do trvalých úkolů.")
    elif new_task in DEFAULT_TASKS:
        messagebox.showwarning("TimeMaster", "Tento úkol již existuje!")

def show_plan():
    busy_slots = parse_events(SAMPLE_EVENTS)
    free_slots, busy_slots = analyze_schedule(busy_slots)
    tasks = DEFAULT_TASKS.copy()
    
    # Přidání nového úkolu
    new_task = task_entry.get().strip()
    if new_task:
        tasks.append(new_task)
        task_entry.delete(0, tk.END)
        # Simulace učení pro nový úkol
        update_learned_durations(new_task)
        messagebox.showinfo("TimeMaster", f"Přidal jsem úkol '{new_task}'. Zatím odhaduji 1 hodinu.")

    suggested_plan = suggest_schedule(free_slots, tasks)
    
    # Aktualizace rozvrhu
    schedule_listbox.delete(0, tk.END)
    for start, end, summary in busy_slots:
        schedule_listbox.insert(tk.END, f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}: {summary}")
        schedule_listbox.itemconfig(tk.END, {'fg': '#FF5555'})
    
    # Aktualizace plánu
    plan_listbox.delete(0, tk.END)
    for plan_item in suggested_plan:
        plan_listbox.insert(tk.END, plan_item)
        plan_listbox.itemconfig(tk.END, {'fg': '#55AA55'})
    
    # Nenaplánované úkoly
    remaining_tasks = tasks[len(suggested_plan):]
    remaining_listbox.delete(0, tk.END)
    for task in remaining_tasks:
        remaining_listbox.insert(tk.END, f"- {task} ({learned_durations.get(task, 1.0):.1f}h)")
        remaining_listbox.itemconfig(tk.END, {'fg': '#FFAA00'})

# Vytvoření hlavního okna
root = tk.Tk()
root.title("TimeMaster")
root.geometry("400x550")  # Zmenšené okno
root.configure(bg="#E8ECEF")

# Hlavička (jednoduchá modrá)
header_frame = tk.Frame(root, bg="#00A1D6", height=50)  # Menší výška hlavičky
header_frame.pack(fill="x")
title_label = tk.Label(header_frame, text="TimeMaster", font=("Helvetica", 16, "bold"), fg="white", bg="#00A1D6")
title_label.pack(pady=5)

# Sekce pro vstup
input_frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10, relief="flat", borderwidth=1, highlightbackground="#D3DCE6", highlightthickness=1)
input_frame.pack(fill="x", padx=10, pady=5)
task_label = tk.Label(input_frame, text="Přidat úkol", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#333")
task_label.pack(anchor="w")
task_entry = ttk.Entry(input_frame, width=30, font=("Helvetica", 10))
task_entry.pack(pady=3)
generate_button = ttk.Button(input_frame, text="Vygenerovat plán", command=show_plan)
generate_button.pack(pady=3)
add_task_button = ttk.Button(input_frame, text="Přidat trvalý úkol", command=add_permanent_task)
add_task_button.pack(pady=3)  # Nové tlačítko pro přidání trvalého úkolu

# Sekce rozvrhu
schedule_frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10, relief="flat", borderwidth=1, highlightbackground="#D3DCE6", highlightthickness=1)
schedule_frame.pack(fill="x", padx=10, pady=5)
schedule_label = tk.Label(schedule_frame, text="Aktuální rozvrh", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#333")
schedule_label.pack(anchor="w")
schedule_listbox = tk.Listbox(schedule_frame, height=4, width=40, font=("Helvetica", 10), bg="#F9FAFB", relief="flat", borderwidth=0)
schedule_listbox.pack(fill="x", pady=3)

# Sekce plánu
plan_frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10, relief="flat", borderwidth=1, highlightbackground="#D3DCE6", highlightthickness=1)
plan_frame.pack(fill="x", padx=10, pady=5)
plan_label = tk.Label(plan_frame, text="Navržený plán", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#333")
plan_label.pack(anchor="w")
plan_listbox = tk.Listbox(plan_frame, height=6, width=40, font=("Helvetica", 10), bg="#F9FAFB", relief="flat", borderwidth=0)
plan_listbox.pack(fill="x", pady=3)

# Sekce nenaplánovaných úkolů
remaining_frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10, relief="flat", borderwidth=1, highlightbackground="#D3DCE6", highlightthickness=1)
remaining_frame.pack(fill="x", padx=10, pady=5)
remaining_label = tk.Label(remaining_frame, text="Nenaplánované úkoly", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#333")
remaining_label.pack(anchor="w")
remaining_listbox = tk.Listbox(remaining_frame, height=2, width=40, font=("Helvetica", 10), bg="#F9FAFB", relief="flat", borderwidth=0)
remaining_listbox.pack(fill="x", pady=3)

# Spuštění aplikace
root.mainloop()