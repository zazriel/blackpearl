import customtkinter as ctk
from blackpearl_backend import (
    initialize_backend_token, send_message, 
     msg_queue,assignusercolour,usrcolor,current_username
)
from PIL import Image
import datetime
import json
import bcrypt

active_users = []

 
send_icon = None
pearl_image = None
join_image = None

window = ctk.CTk()
widthh = window.winfo_screenwidth()
heightt = window.winfo_screenheight()

window.title("Black Pearl")
window.after(0, lambda: window.wm_state('zoomed'))
window.iconbitmap('icons\\whitepearl.ico')



tabview = ctk.CTkTabview(master=window, segmented_button_fg_color="#242323", height=heightt-90, width=widthh-50)
tabview.pack(padx=20, pady=10)
tabview.add("Chat Room")
tabview.add("Active Users")

custom_font = ("Segoe UI", 30, 'bold') 
tabview._segmented_button.configure(font=("Segoe UI", 24, 'bold'))


usr_frame = ctk.CTkFrame(master=tabview.tab("Active Users"), width=1672, height=650, fg_color="#383838", corner_radius=10)
usr_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")
usr_frame.pack_propagate(False)

def update_active_users():
    for widget in usr_frame.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(
            master=usr_frame,
            text=f"Active:",
            font=custom_font,
            fg_color="transparent",
            corner_radius=10,
            text_color= "white"
        )
    label.pack(pady=10, padx=10, anchor="w")
    for user in list(set(active_users)):
        
        user_label = ctk.CTkLabel(
            master=usr_frame,
            text=f"{user}",
            font=("Segoe UI", 25, 'bold'),
            fg_color="dark gray",
            corner_radius=10,
            text_color= usrcolor[user]
        )
        user_label.pack(pady=5, padx=10, anchor="w")    
    window.after(1000, update_active_users) 
    
def clear_active_users():
    active_users.clear()
    window.after(60000, clear_active_users)
    
update_active_users()
clear_active_users()

    
send_icon = ctk.CTkImage(
    light_image=Image.open(r"icons\send.png"),
    dark_image=Image.open(r"icons\send.png"),
    size=(30, 30))

pearl_image =  ctk.CTkImage(
      light_image=Image.open(r"icons\blackpearllogo.png"),
      dark_image=Image.open(r"icons\blackpearllogo.png"),
    size=(300, 300))

join_image = ctk.CTkImage(
    light_image=Image.open(r"icons\wjoin.png"),
    dark_image=Image.open(r"icons\wjoin.png"),
    size=(60, 60))
def scroll_to_bottom():
    try:
        if not chat_frame.winfo_exists():
            return

        canvas = getattr(chat_frame, "_parent_canvas", None)

        if canvas and canvas.winfo_exists():
            canvas.yview_moveto(1.0)

    except:
        pass
    
def messaging():
    global chat_text,msg_frame,messageentry,chat_frame, input_frame
    
    for widget in tabview.tab("Chat Room").winfo_children():
                widget.destroy()
    chat_frame = ctk.CTkScrollableFrame(master=tabview.tab("Chat Room"), width=1672, height=650, fg_color="#383838", corner_radius=10)
    chat_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")

    chat_frame.update_idletasks()
    window.after(10, lambda: scroll_to_bottom())

    input_frame = ctk.CTkFrame(master=tabview.tab("Chat Room"), width=1672, height=60, fg_color="#383838", corner_radius=10)
    input_frame.pack(padx=10, pady=(0, 10), side="bottom", anchor="s")
    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_columnconfigure(1, weight=0)
    input_frame.grid_propagate(False)
    
    success_label = ctk.CTkLabel(
                master=chat_frame,
                text=f"Ahoy! {current_username} officially joined the crew. Adventure awaits!",
                font=("Segoe UI", 20)
            ) 
    success_label.pack(pady=20,expand=True)
    
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
      active_users.append(usr)
      usrlabel = ctk.CTkLabel(
        master=msg_frame,
        text=f"{usr} (You) {datetime.datetime.now().strftime('%H:%M:%S')}:",
        font=("Segoe UI", 16, 'bold'),
        fg_color="transparent",
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
      usrlabel.pack( anchor="e", padx=10)
      chat_text.pack( anchor="e", padx=10)
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
    messageentry.bind("<Return>", lambda e:(send_message(messageentry.get().strip()),messageentry.delete(0, "end"),messageentry.focus()))
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
           PREFIX = "+--/@@SYNC@@/**/*"
           if messg.startswith(PREFIX):
            recievesecrets(messg)
           else: 
            assignusercolour(sndr)
            active_users.append(sndr)
            sndrlabel = ctk.CTkLabel(
               master=msg_frame,
               text=f"{sndr} (You) {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:",
               font=("Segoe UI", 16, 'bold'),
               fg_color="transparent",
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
   

def insider_info(username1,hash1):     
 send_message(f"+--/@@SYNC@@/**/*{username1}|{hash1}")
 window.after (10000, insider_info, username1,hash1)
   
def recievesecrets(text,filename="users.json"):
   payload = text.replace("+--/@@SYNC@@/**/*", "", 1) 
   try:
         username, phash = payload.split("|", 1)
   except ValueError:
         print("Received malformed sync message.")
         return
   with open(filename, "r") as file:
             data = json.load(file)  
   if username not in data:
     data[username] = phash  
     
    
     data[username] = phash
     with open(filename, "w") as file:
         json.dump(data, file, indent=4)
def user_initialize():
    global authorized_uuid, send_icon, join_page,password_entry
    data = {}
    with open("users.json", "w") as file:
      json.dump(data, file, indent=4)
    
    join_page = ctk.frame = ctk.CTkFrame(master=tabview.tab("Chat Room"), width=widthh-200, height=heightt-200, fg_color="#383838", corner_radius=10)
    join_page.pack(padx=10, pady=(5, 5),  anchor="center")
    join_page.pack_propagate(False)
    
    pearl_label = ctk.CTkLabel(join_page, image=pearl_image, text="")
    pearl_label.image = pearl_image
    pearl_label.pack(pady=10)
    welcome_label = ctk.CTkLabel(
        master=join_page,
        text="The Black Pearl",
        font=(custom_font))
    welcome_label.pack(pady=10)
    authorized_uuid = ctk.CTkEntry(
        master=join_page,
        placeholder_text_color="grey",text_color="white",
        placeholder_text="Username",
        font=("Segoe UI", 20),
        width=300
    )
    authorized_uuid.pack(pady=10)     
    password_entry = ctk.CTkEntry(
        master=join_page,
        placeholder_text_color="grey",text_color="white",
        placeholder_text="Password",
        font=("Segoe UI", 20),
        show="*",
        width=300
    )
    def toggle_password_visibility():
        if password_entry.cget("show") == "*":
         password_entry.configure(show="")
        else:
          password_entry.configure(show="*")
         
    password_entry.pack(pady=10)
    
    show_pass = ctk.CTkCheckBox(
        master=join_page,
        text="Show Password",
        command=toggle_password_visibility
    )
    show_pass.pack(pady=10)    
    def submit_user():
        global current_username 
        current_username = authorized_uuid.get()  
        password = password_entry.get()
        set_user(current_username, password)
        
        

    # Submit button
    submit_btn = ctk.CTkButton(
        master=join_page,
        text="",
        image=join_image,
        width=300,
        height=70,
        command=submit_user
    )
    submit_btn.image = join_image
    submit_btn.pack(pady=20)

def set_user(username, password, filename="users.json"):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Load existing data safely
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if username in data:
        login_user(username, password, filename=filename)
    else:
      data[username] = hashed
      username1 = username
      hash1 = hashed
      
      insider_info(username1,hash1)  
      initialize_backend_token(username)  
      send_message(f"{username} has joined the crew!")
      for widget in tabview.tab("Chat Room").winfo_children():
            widget.destroy()         
      messaging()
      
def login_user(username, password, filename="users.json"):
    global current_username 
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users found ")
        return False

    if username not in data:
        print("User not found ")
        return False

    stored_hash = data[username].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        initialize_backend_token(username)
       
        insider_info(username,stored_hash.decode('utf-8'))  
        send_message(f"{username} has joined the crew!") 
        for widget in tabview.tab("Chat Room").winfo_children():
            widget.destroy()         
        messaging()
         
        
    else:
        password_entry.delete(0,"end")
        password_entry.focus()
        password_entry.configure(border_color="red")
        
user_initialize()

    
window.mainloop()