import customtkinter as ctk
from blackpearl_backend import (
    initialize_backend_token,initialize_backend_pass, send_message, set_user_status,
    active_users, get_active_users, msg_queue,assignusercolour,usrcolor,token,Password
)
from PIL import Image
import datetime


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

custom_font = ("Segoe UI", 30, 'bold')  # Increased font size
tabview._segmented_button.configure(font=("Segoe UI", 24, 'bold'))


usr_frame = ctk.CTkFrame(master=tabview.tab("Active Users"), width=1672, height=650, fg_color="#383838", corner_radius=10)
usr_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")



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
def messaging():
    global chat_text,msg_frame,messageentry,chat_frame, input_frame
    for widget in tabview.tab("Chat Room").winfo_children():
                widget.destroy()
    chat_frame = ctk.CTkScrollableFrame(master=tabview.tab("Chat Room"), width=1672, height=650, fg_color="#383838", corner_radius=10)
    chat_frame.pack(padx=10, pady=(5, 5), side="top", anchor="n")
# 'app' should be your main CTk window variable
    window.after(10, lambda: chat_frame._parent_canvas.yview_moveto(1.0))

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
    

def user_initialize():
    global authorized_uuid, send_icon

    for widget in tabview.tab("Chat Room").winfo_children():
        widget.destroy()

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
        if current_username in Password:
            if Password[current_username]["password"] == password:
               initialize_backend_pass(current_username)
               messaging()
               for widget in tabview.tab("Chat Room").winfo_children():
                 widget.destroy()
               
            else:
                error_label = ctk.CTkLabel(
                    master=join_page,
                    text="Wrong password! Try again. Or register with a new username.",
                    font=("Segoe UI", 16),
                    text_color="red"
                )
                error_label.pack(pady=10)   
        else:
            
            token = initialize_backend_token(current_username)
            Password[current_username] = {"password":password, "token": token}
            print(Password)
            for widget in tabview.tab("Chat Room").winfo_children():
                widget.destroy()
            
                    

          
            
            messaging()

    # Submit button
    submit_btn = ctk.CTkButton(
        master=join_page,
        text="",
        #text ="Sail Away!",
        image=join_image,
        width=300,
        height=70,
        #font=("Segoe UI", 15, 'bold'),
         
        
        command=submit_user
    )
    submit_btn.image = join_image
    submit_btn.pack(pady=20)

user_initialize()

    
window.mainloop()