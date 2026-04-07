import customtkinter as ctk

widthh = ctk.CTk().winfo_screenwidth()
heightt = ctk.CTk().winfo_screenheight()
window = ctk.CTk()
window.title("Black Pearl")
window.after(0, lambda: window.wm_state('zoomed'))
window.iconbitmap('icons\\whitepearl.ico')

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


window.mainloop()
