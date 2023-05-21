from tkinter import *
import pygame
from tkinter import filedialog
import time
import os
from mutagen.mp3 import MP3
import tkinter as ttk

# Main Window
root = Tk()
root.title('MP3 Player')
root.geometry("500x450")
current_user = os.getlogin()
#Initialize Pygame Mixer
pygame.mixer.init()

# Set a song dictionary to match song names to their extracted paths
songs_dict = {}

# Get song time/length info
def play_time():
    song = song_box.get(ACTIVE)
    if song !="":
        current_time = pygame.mixer.music.get_pos() /1000

        # Convert time to a legible format
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

        #current_song = song_box.curselection()
        # Get song title from playlist

        # Add back on directory/folders 
    
        song_path= songs_dict[song]
        song = f'{song_path}/{song}.mp3'

        # Get the total song length
        song_mut = MP3(song)
        global song_length
        song_length = song_mut.info.length

        # Convert song length to legible format
        converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

        # Output song time to status time
        status_bar.config(text=f"Time Elapsed: {converted_current_time}  of  {converted_song_length}  ")
        # Update status bar time
        status_bar.after(1000, play_time)

        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, from_=0)
    else:
         status_bar.config(text=f"Time Elapsed: 00:00:00  of  00:00:00  ")

# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='/Users/'+ current_user + '/Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # Remove directory and file extension
    #song = song.replace("D:/Music and Podcasts/Music 2/", "")
    song_path = extract_song_path(song)
    song = extract_song_name(song)
    if song not in songs_dict.keys():
        songs_dict[song] = song_path
         # Add song to list
        song_box.insert(END, song)
    else:
        print("duplicate")
   

# Add Many Songs to Playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='/Users/'+ current_user + '/Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # Loop through song list, replace directory info
    for song in songs:
        #song = song.replace("D:/Music and Podcasts/Music 2/", "")
        song_path = extract_song_path(song)
        song = extract_song_name(song)
        if song not in songs_dict.keys():
            songs_dict[song] = song_path
             # Insert into playlist
            song_box.insert(END, song)
        else:
            print("duplicate")
       

# Play Selected Song
def play():
    song = song_box.get(ACTIVE)
    song_path = songs_dict[song]
    song = f'{song_path}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0)
    # Call the song timer info
    play_time()


# Stop Playing Current Song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    # Clear the status bar
    status_bar.config(text="")
    play_time()   

# Play the next song
def next_song():
    # Find current song index number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Get song title from playlist
    song = song_box.get(next_one)
    # Add back on directory/folders
    song_path = songs_dict[song] 
    song = f'{song_path}/{song}.mp3'
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
    song_path = songs_dict[song] 
    song = f'{song_path}/{song}.mp3'
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
    remove_song = song_box.get(ANCHOR)
    if remove_song != "":
        del songs_dict[remove_song]
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Delete all songs from playlist
def delete_all_songs():
    song_box.delete(0, END)
    songs_dict.clear()
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

def extract_song_name(file_path):
    song_name_ext = os.path.basename(file_path)
    song_name = song_name_ext.replace(".mp3", "")
    return song_name

def extract_song_path(file_path):
    song_dir = os.path.dirname(file_path)
    return song_dir

# Create Slider function
def slide(x):
    pass
    slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')

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

# Music Slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, command=slide, length=360)
my_slider.pack(pady=20)

# Create temp slider label
slider_label = ttk.Label(root, text=0)
slider_label.pack(pady=10)

root.mainloop()