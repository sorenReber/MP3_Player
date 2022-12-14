from tkinter import *
import pygame
from tkinter import filedialog

# Main Window
root = Tk()
root.title('MP3 Player')
root.geometry("500x350")

#Initialize Pygame Mixer
pygame.mixer.init()

# Get song time/length info
def play_time():
    current_time = pygame.mixer.music.get_pos() /1000
    status_bar.config(text=current_time)
    # Update status bar time
    status_bar.after(1000, play_time)

# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='Libraries\Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # Remove directory and file extension
    song = song.replace("E:/Music and Podcasts/Music 2/", "")
    song = song.replace(".mp3", "")
    # Add song to list
    song_box.insert(END, song)

# Add Many Songs to Playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='Libraries\Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # Loop through song list, replace directory info
    for song in songs:
        song = song.replace("E:/Music and Podcasts/Music 2/", "")
        song = song.replace(".mp3", "")
        # Insert into playlist
        song_box.insert(END, song)

# Play Selected Song
def play():
    song = song_box.get(ACTIVE)
    song = f'E:/Music and Podcasts/Music 2/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0)
    # Call the song timer info
    play_time()

# Stop Playing Current Song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

# Play the next song
def next_song():
    # Find current song index number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Get song title from playlist
    song = song_box.get(next_one)
    # Add back on directory/folders 
    song = f'E:/Music and Podcasts/Music 2/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0)
    # Clear active selection in listbox
    song_box.select_clear(0, END)
    # Activate new song selection
    song_box.activate(next_one)
    # Set Active bar to next song
    song_box.selection_set(next_one, last=None)

# Play the previous song
def previous_song():
        # Find current song index number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]-1
    # Get song title from playlist
    song = song_box.get(next_one)
    # Add back on directory/folders 
    song = f'E:/Music and Podcasts/Music 2/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0)
    # Clear active selection in listbox
    song_box.select_clear(0, END)
    # Activate new song selection
    song_box.activate(next_one)
    # Set Active bar to next song
    song_box.selection_set(next_one, last=None)

# Delete a song
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Delete all songs from playlist
def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause the Current Song
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Create Playlist Box
song_box = Listbox(root, bg="black", fg="red", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Player Control Button Images
back_btn_img = PhotoImage(file='icons/previous.png')
forward_btn_img =PhotoImage(file='icons/next.png')
play_btn_img = PhotoImage(file='icons/forward.png')
pause_btn_img = PhotoImage(file='icons/pause.png')
stop_btn_img = PhotoImage(file='icons/stop.png')

# Create Player Control Frames
controls_frame = Frame(root)
controls_frame.pack()

# Create Player Control Buttons
back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command= previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

# Create Button Grid
back_btn.grid(row= 0, column=0) 
forward_btn.grid(row= 0, column=1)  
play_btn.grid(row= 0, column=2) 
pause_btn.grid(row= 0, column=3)  
stop_btn.grid(row= 0, column=4)  

# Create Menu
top_menu = Menu(root)
root.config(menu=top_menu)

# Menu: Add Song
add_song_menu = Menu(top_menu)
top_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add Many Songs to the Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(top_menu)
top_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

root.mainloop()