"""TROUBLESHOOTING INDEX GENERATOR"""

import contextlib
import re
import sys
import threading
import tkinter.font as tkfont
from pathlib import Path
from tkinter import TclError, filedialog, messagebox
from tkinter import scrolledtext as st

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import BOTH, BOTTOM, DISABLED, END, LEFT, TOP, WORD, E, W, X

CUSTOM_TBUTTON = "Custom.TButton"
FOLDER_PATH = Path()


def import_tm_folder():
    """
    Starts a new thread to scan the IADS directory in the background.

    This function creates and starts a new thread that runs the `open_iads_dir` function,
    allowing the folder scanning process to occur without blocking the main program flow.

    Returns:
        None
    """
    thread = threading.Thread(target=open_files_dir)
    thread.start()


def open_files_dir() -> None:
    """
    Opens a file explorer for the user to choose a folder,
    scans all of the TS files, displays a list of the TS files, and
    displays a preview of the final TS Index WP. If a folder is
    selected, it updates the global FOLDER_PATH variable and calls
    the scan_iads_folder function to process the folder. Finally, it
    enables the update button.
    Returns:
        None
    """
    textbox.delete("1.0", END)
    global FOLDER_PATH
    FOLDER_PATH = Path(filedialog.askdirectory())

    if FOLDER_PATH.exists():
        scan_files_folder(FOLDER_PATH)
        # # Measure the time taken for 10 executions of scan_iads_folder
        # execution_time: float = timeit.timeit(
        #     "scan_iads_folder(FOLDER_PATH)", globals=globals(), number=10
        # )
        # logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        # logging.info("Execution time: %s seconds", execution_time)
    update_btn.configure(state="normal")


def generate_ts_index():
    """Generate the TS Index Work Package."""


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(getattr(sys, "_MEIPASS", Path.cwd()))
    except AttributeError:
        base_path = (
            Path.cwd()
        )  # Path to the current working directory, equivalent to os.path.abspath(".")

    return base_path / relative_path  # Use the '/' operator to join paths in pathlib


# Initialize main window with ttkbootstrap style
root = ttk.Window("TROUBLESHOOTING INDEX GENERATOR", "darkly")
root.resizable(True, True)
root.geometry("1400x800")

ICON_BITMAP = "logo_TRG.ico"
# Set the window icon
with contextlib.suppress(TclError):
    root.iconbitmap(ICON_BITMAP)

IMAGE_PATH = "logo_TRG_text.png"
image_path = resource_path(IMAGE_PATH)
image = Image.open(IMAGE_PATH).convert("RGBA")

# Resize the image
NEW_WIDTH = 350  # Adjust this to make it longer
original_width, original_height = image.size
aspect_ratio = original_height / original_width
new_height = int(NEW_WIDTH * aspect_ratio)
image_resized = image.resize((NEW_WIDTH, new_height), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(image_resized)

# Create a custom style for the buttons with the dominant color
DOMINANT_COLOR = "#2067AD"
SUBORDINATE_COLOR = "#FFFFFF"
trg_style = ttk.Style()
trg_style.configure(
    CUSTOM_TBUTTON,
    font=("Helvetica", 14, "bold"),
    padding=10,
    relief="flat",
    foreground=SUBORDINATE_COLOR,
    background=DOMINANT_COLOR,
)

# Top frame for buttons and image
frame_top = ttk.Frame(root)
frame_top.pack(side=TOP, fill=X, padx=10, pady=(10, 0))

# Bottom frame for ScrolledText
frame_btm = ttk.Frame(root)
frame_btm.pack(side=BOTTOM, fill=BOTH, expand=True, padx=10, pady=10)

# "IMPORT TM FOLDER" button with custom color
import_btn = ttk.Button(
    frame_top,
    text="Import TM Folder",
    command=scan_folder_in_background,
    style=CUSTOM_TBUTTON,
)
import_btn.grid(row=0, column=0, padx=(0, 5), pady=5, sticky=W)

# "GENERATE TS INDEX" button with custom color
update_btn = ttk.Button(
    frame_top,
    text="Generate TS Index",
    command=generate_ts_index,
    state=DISABLED,
    style=CUSTOM_TBUTTON,
)
update_btn.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Add empty space between buttons and the image
frame_top.columnconfigure(2, weight=1)

# Label to display the image on the far right
img_label = ttk.Label(frame_top, image=img)  # type: ignore
# Keep a reference to avoid garbage collection
img_label.image = img  # type: ignore
img_label.grid(row=0, column=3, padx=0, pady=5, sticky=E)

# ScrolledText widget for log output or entity text display
textbox = st.ScrolledText(
    master=frame_btm,
    font=("Monaco", 12),
    wrap=WORD,
    highlightthickness=1,
)
textbox.pack(side=LEFT, fill=BOTH, expand=True)

# Configure the font and tabs for the ScrolledText widget
font = tkfont.Font(font=textbox["font"])
tab = font.measure("    ")  # Measure the size of 4 spaces
textbox.configure(tabs=tab)

# Start the main event loop
root.mainloop()
