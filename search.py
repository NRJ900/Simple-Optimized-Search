import requests
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import webbrowser
import os

CONFIG_FILE = "config.txt"

# Initialize CustomTkinter Theme
ctk.set_appearance_mode("System")  # System, Dark, Light
ctk.set_default_color_theme("blue")

# Function to check API key
def get_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            api_key = file.read().strip()
        if api_key:
            return api_key

    # First-time setup: Ask user for API key
    messagebox.showinfo("Welcome", "Set up your API key.\nSign up here: https://serpapi.com/")
    api_key = simpledialog.askstring("Enter API Key", "🔑 Enter your SerpAPI Key:", show="*")

    if not api_key:
        messagebox.showerror("Error", "API key is required.")
        exit()

    with open(CONFIG_FILE, "w") as file:
        file.write(api_key)

    messagebox.showinfo("Success", "✅ API Key saved!\nRestarting program...")
    root.destroy()
    os.system("python " + __file__)  # Restart program
    exit()

# Function to perform Google search using SerpAPI
def google_search():
    question = entry.get().strip()
    if not question:
        messagebox.showwarning("Input Error", "Please enter a question!")
        return

    search_button.configure(text="🔎 Searching...", state=tk.DISABLED)

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": question,
        "api_key": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch results: {e}")
        return
    finally:
        search_button.configure(text="Search", state=tk.NORMAL)

    results_box.config(state="normal")
    results_box.delete("1.0", "end")

    # Extract featured snippet (Direct Answer)
    answer = data.get("answer_box", {}).get("snippet") or data.get("answer_box", {}).get("answer")
    if answer:
        results_box.insert("end", "✅ Featured Answer:\n", "bold")
        results_box.insert("end", answer + "\n\n")

    # Extract top search results (Titles & Links)
    results = data.get("organic_results", [])
    if not results:
        results_box.insert("end", "❌ No results found.\n")
        return

    results_box.insert("end", "🔍 Top Search Results:\n", "bold")
    for idx, result in enumerate(results[:5], start=1):
        title = result.get("title", "No Title")
        link = result.get("link", "#")

        results_box.insert("end", f"{idx}. {title}\n", "bold")
        results_box.insert("end", f"   🔗 {link}\n", "link")
        results_box.insert("end", "\n")

    results_box.config(state="disabled")

# Function to open links on click
def open_link(event):
    tag_ranges = results_box.tag_ranges("current")
    
    if not tag_ranges:  # If no link was clicked, do nothing
        return  

    start, end = tag_ranges  # Unpack safely
    url = results_box.get(start, end)

    if url.startswith("http"):
        webbrowser.open(url)


# UI Setup
root = ctk.CTk()
root.title("🔍 Google Search Answer Bot")
root.geometry("720x550")

# Check API Key
API_KEY = get_api_key()

title_label = ctk.CTkLabel(root, text="🔍 Google Search Answer Bot", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

entry = ctk.CTkEntry(root, font=("Arial", 14), width=450, height=40)
entry.pack(pady=5)

search_button = ctk.CTkButton(root, text="Search", font=("Arial", 14, "bold"), command=google_search, width=120)
search_button.pack(pady=5)

# Frame for output box & scrollbar
output_frame = ctk.CTkFrame(root, fg_color="transparent")  
output_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Custom scrollbar
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

# Using ScrolledText with a transparent background
results_box = tk.Text(
    output_frame, 
    font=("Arial", 12), 
    wrap="word", 
    bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],  # Matches UI background
    fg="white",  # Text color
    bd=0,  # No border
    relief="flat",  # Flat design
    yscrollcommand=scrollbar.set
)
results_box.pack(fill="both", expand=True)

# Link scrollbar with text box
scrollbar.config(command=results_box.yview)

# Buttons Frame
buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
buttons_frame.pack(pady=10)

close_button = ctk.CTkButton(buttons_frame, text="❌ Close", font=("Arial", 12), command=root.quit, width=100, fg_color="red")
close_button.grid(row=0, column=0, padx=10)

# Text styling
results_box.tag_configure("bold", font=("Arial", 12, "bold"))
results_box.tag_configure("link", foreground="lightblue", underline=True)
results_box.tag_bind("link", "<Button-1>", open_link)

root.mainloop()
