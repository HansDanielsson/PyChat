import tkinter as tk
import pymongo

# Connect to mongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["PyChat"]
message_col = db["messages"]

# Tkinter GUI
root = tk.Tk()
root.title("PyChat")

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

def send_message():
    message = entry.get()
    if message:
        message_col.insert_one({"text": message})
        entry.delete(0, tk.END)
        fetch_message()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

messages_label = tk.Label(root, text="Messages:\n", justify="left")
messages_label.pack(pady=5)

def fetch_message():
    messages = message_col.find().sort("_id", -1)
    messages_label.config(text="Messages:\n" + "\n".join(f"- {m['text']}" for m in messages))
    root.after(2000, fetch_message)  # Refresh every second

fetch_message()
root.mainloop()