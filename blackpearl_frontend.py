import customtkinter as ctk
from blackpearl_backendV1 import * 
import time




widthh = ctk.CTk().winfo_screenwidth()
heightt = ctk.CTk().winfo_screenheight()
window = ctk.CTk()
window.title("Black Pearl")
window.after(0, lambda: window.wm_state('zoomed'))
window.iconbitmap('icons\\whitepearl.ico')
usr = []
tabview = ctk.CTkTabview(master=window, segmented_button_fg_color="#242323", height=heightt-90, width=widthh-50)
tabview.pack(padx=20, pady=10)
tabview.add("Chat room")
tabview.add("Active users")

custom_font = ("Segoe UI", 30, 'bold')  # Increased font size
tabview._segmented_button.configure(font=("Segoe UI", 24, 'bold'))

chat_frame = ctk.CTkFrame(master=tabview.tab("Chat room"), width=1672, height=650, fg_color="#383838", corner_radius=10)
chat_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")

usr_frame = ctk.CTkFrame(master=tabview.tab("Active users"), width=1672, height=650, fg_color="#383838", corner_radius=10)
usr_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")


input_frame = ctk.CTkFrame(master=tabview.tab("Chat room"), width=1672, height=50, fg_color="#383838", corner_radius=10)
input_frame.pack(padx=10, pady=(0, 10), side="bottom", anchor="s")

#def user_initialize():
def user_initialize():
    # Clear previous widgets
    for widget in chat_frame.winfo_children():
        widget.destroy()

    # Create label
    usrlabel = ctk.CTkLabel(
        master=chat_frame,
        text="Username",
        font=("Segoe UI", 24, 'bold')
    )
    usrlabel.pack(pady=10)

   
    authorized_uuid = ctk.CTkEntry(
        master=chat_frame,
        width=1600,
        font=("Segoe UI", 20)
    )
    authorized_uuid.pack(pady=10)

    def submit_user():
        username = authorized_uuid.get()

        if username in usr:
            error_label = ctk.CTkLabel(
                master=chat_frame,
                text="Username already exists, choose something unique",
                font=("Segoe UI", 16),
                text_color="red"
            )
            error_label.pack(pady=5)
        else:
            usr.append(username)
            print(usr)

            # Clear chat frame after success
            for widget in chat_frame.winfo_children():
                widget.destroy()

            # Show confirmation in chat
            success_label = ctk.CTkLabel(
                master=chat_frame,
                text=f"Welcome, {username}!",
                font=("Segoe UI", 20)
            )
            success_label.pack(pady=20)

    # Submit button
    submit_btn = ctk.CTkButton(
        master=chat_frame,
        text="Submit",
        command=submit_user
    )
    submit_btn.pack(pady=10)
    
    #cvvv
user_initialize()
    
window.mainloop()
