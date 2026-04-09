import customtkinter as ctk
from blackpearl_backend import (
    initialize_backend, send_message, set_user_status,
    active_users, get_active_users, msg_queue,assignusercolour,usrcolor
)
from PIL import Image
import datetime


send_icon = None


window = ctk.CTk()
widthh = window.winfo_screenwidth()
heightt = window.winfo_screenheight()

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

chat_frame = ctk.CTkScrollableFrame(master=tabview.tab("Chat room"), width=1672, height=650, fg_color="#383838", corner_radius=10)
chat_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")
# 'app' should be your main CTk window variable
window.after(10, lambda: chat_frame._parent_canvas.yview_moveto(1.0))

usr_frame = ctk.CTkFrame(master=tabview.tab("Active users"), width=1672, height=650, fg_color="#383838", corner_radius=10)
usr_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")


input_frame = ctk.CTkFrame(master=tabview.tab("Chat room"), width=1672, height=60, fg_color="#383838", corner_radius=10)
input_frame.pack(padx=10, pady=(0, 10), side="bottom", anchor="s")
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=0)
input_frame.grid_propagate(False)
send_icon = ctk.CTkImage(
    light_image=Image.open(r"icons\send.png"),
    dark_image=Image.open(r"icons\send.png"),
    size=(30, 30))




def messaging():
    global chat_text,msg_frame,messageentry
    for widget in input_frame.winfo_children():
                widget.destroy()
   
    
    msg_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
    msg_frame.pack(fill="x", pady=5)
    chat_text = ctk.CTkLabel(
        msg_frame,
        wraplength=250,
        corner_radius=10,
        fg_color= "gray"
    )
                
    def chat_update(msgs): 
      global messageentry,chat_text
      
      send_message(msgs) 
      msgeee = msg_queue.get()
      msgs= msgeee.get('text', '')
      usr = msgeee.get('user', 'Unknown')
      assignusercolour(usr)
      usrlabel = ctk.CTkLabel(
        master=msg_frame,
        text=f"{usr} (You) {datetime.datetime.now().strftime('%H:%M:%S')}:",
        font=("Segoe UI", 16, 'bold'),
        fg_color="gray",
        corner_radius=10,
        text_color= usrcolor[current_username]
    )            
      chat_text = ctk.CTkLabel(
        msg_frame,
        text = f"{msgs}",
        wraplength=250,
        corner_radius=10,
        fg_color= "gray"
    )
      usrlabel.pack( anchor="w", padx=10)
      chat_text.pack( anchor="w", padx=10)
      chat_frame.update_idletasks()
      chat_frame._parent_canvas.yview_moveto(1.0)
      messageentry.delete(0, "end")
      messageentry.focus()            
    send_messagez = lambda: chat_update(messageentry.get().strip())      
    messageentry = ctk.CTkEntry(
            master=input_frame,
            placeholder_text_color="grey",text_color="white",
            placeholder_text="Message",
            font=("Segoe UI", 20)
        )
    messageentry.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    messageentry.bind("<Return>", lambda e: send_message(messageentry.get().strip()))
    send_btn = ctk.CTkButton(
            master=input_frame,
            image=send_icon,
            width=50,
            height=50,
            text="", 
            
            command=send_messagez
        )
    
    send_btn.image = send_icon
    send_btn.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    accept_messages()
def accept_messages():
        while not msg_queue.empty():
           msg = msg_queue.get()
           messg = msg.get('text', '')
           sndr = msg.get('user', 'Unknown')
           assignusercolour(sndr)
           sndrlabel = ctk.CTkLabel(
              master=msg_frame,
              text=f"{sndr} (You) {datetime.datetime.now().strftime('%H:%M:%S')}:",
              font=("Segoe UI", 16, 'bold'),
              fg_color="gray",
              corner_radius=10,
              text_color= usrcolor[sndr])
           
           chat_text = ctk.CTkLabel(
             msg_frame,
             text = messg,
             wraplength=250,
             corner_radius=10,
             fg_color= "gray"
             )
           sndrlabel.pack( anchor="w", padx=10)
           chat_text.pack( anchor="w", padx=10)
           chat_frame.update_idletasks()
           chat_frame._parent_canvas.yview_moveto(1.0)        
        window.after(100, accept_messages)
    
#def user_initialize():
def user_initialize():
    global authorized_uuid, send_icon

    
        
    for widget in chat_frame.winfo_children():
        widget.destroy()

    # Create label
    usrlabel = ctk.CTkLabel(
        master=chat_frame,
        text="Select Username",
        font=("Segoe UI", 24, 'bold')
    )
    usrlabel.pack(pady=5, padx=10, fill="x")

   
    authorized_uuid = ctk.CTkEntry(
        master=input_frame,
        fg_color="#3B3A3A",
        placeholder_text_color="grey",
        placeholder_text="Enter your username",
        font=("Segoe UI", 20)
    )
    authorized_uuid.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    def submit_user():
        global current_username
        current_username = authorized_uuid.get()
        
        if current_username in usr:
            error_label = ctk.CTkLabel(
                master=chat_frame,
                text="Username already exists, choose something unique",
                font=("Segoe UI", 16),
                text_color="red"
            )
            error_label.pack(pady=5)
        else:
            usr.append(current_username)
            initialize_backend(current_username)

            # Clear chat frame after success
            for widget in chat_frame.winfo_children():
                widget.destroy()
            for widget in input_frame.winfo_children():
                widget.destroy()
                    

           # Show confirmation in chat
            success_label = ctk.CTkLabel(
                master=chat_frame,
                text=f"Welcome, {current_username}!",
                font=("Segoe UI", 20)
            ) 
            success_label.pack(pady=20,expand=True)
            messaging()

    # Submit button
    submit_btn = ctk.CTkButton(
        master=input_frame,
        image=send_icon,
        width=50,
        height=50,
        text="", 
        
        command=submit_user
    )
    submit_btn.image = send_icon
    submit_btn.grid(row=0, column=1, padx=10, pady=5, sticky="e")

user_initialize()

    
window.mainloop()
