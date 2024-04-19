import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Chat Client")

        self.username = simpledialog.askstring("Username", "Enter your username", parent=self.master)
        if not self.username:
            self.username = "Anonymous"

        # Chat log
        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', height=10, width=50)
        self.chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Message entry
        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.grid(row=1, column=0, padx=10, pady=10)
        self.msg_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Socket setup
        self.setup_connection()

    def setup_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 9999))
        threading.Thread(target=self.receive_message, daemon=True).start()

    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client_socket.send(full_message.encode())
            self.msg_entry.delete(0, tk.END)

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.update_chat_log(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.client_socket.close()
                break

    def update_chat_log(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
