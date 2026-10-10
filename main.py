
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Image variables
original_image = None
result_image = None
logo_image = None
preview_image = None


# Upload original image
def upload_image():
    global original_image, result_image

    filename = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.webp")
        ]
    )

    if filename:
        try:
            original_image = Image.open(filename).convert("RGBA")
            result_image = None
            show_preview(original_image)
        except (OSError, ValueError) as error:
            messagebox.showerror("Error", f"Could not open image:\n{error}")


# Upload logo
def upload_logo():
    global logo_image

    filename = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.webp")
        ]
    )

    if filename:
        try:
            logo_image = Image.open(filename).convert("RGBA")
            messagebox.showinfo("Success", "Logo uploaded!")
        except (OSError, ValueError) as error:
            messagebox.showerror("Error", f"Could not open logo:\n{error}")


# Apply text watermark
def add_text_watermark():
    global result_image

    if original_image is None:
        messagebox.showwarning("Missing Image", "Please upload an image first.")
        return

    text = text_input.get().strip()

    if not text:
        messagebox.showwarning("Missing Text", "Please enter watermark text.")
        return

    image = original_image.copy()
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    margin = max(20, image.width // 40)
    font_size = max(30, image.width // 20)

    try:
        font = ImageFont.truetype(
            "C:/Windows/Fonts/arial.ttf", font_size
        )
    except OSError:
        font = ImageFont.load_default(size=font_size)

    draw.text(
        (margin, margin),
        text,
        font=font,
        fill="white",
        stroke_width=2,
        stroke_fill="black"
    )

    result_image = Image.alpha_composite(image, overlay)
    show_preview(result_image)


# Apply logo watermark
def add_logo_img():
    global result_image

    if original_image is None:
        messagebox.showwarning("Missing Image", "Please upload an image first.")
        return

    if logo_image is None:
        messagebox.showwarning("Missing Logo", "Please upload a logo first.")
        return

    image = original_image.copy()
    logo = logo_image.copy()

    # Logo can occupy up to 20% of the image dimensions
    logo_size = (
        max(1, image.width // 5),
        max(1, image.height // 5)
    )
    logo.thumbnail(logo_size, Image.Resampling.LANCZOS)

    margin = max(10, image.width // 50)

    x = image.width - logo.width - margin
    y = image.height - logo.height - margin

    # Preserve the logo's transparency
    image.paste(logo, (x, y), logo)

    result_image = image
    show_preview(result_image)


# Display image preview
def show_preview(image):
    global preview_image

    preview_image = image.copy()
    preview_image.thumbnail((700, 350), Image.Resampling.LANCZOS)

    preview_image = ImageTk.PhotoImage(preview_image)
    preview.configure(image=preview_image, text="")


# Save watermarked image
def save_image():
    if result_image is None:
        messagebox.showwarning(
            "No Result",
            "Please apply a text or logo watermark first."
        )
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG image", "*.png"),
            ("JPEG image", "*.jpg *.jpeg")
        ]
    )

    if not path:
        return

    try:
        image = result_image
        extension = path.lower().rsplit(".", 1)[-1]

        if extension in ("jpg", "jpeg"):
            image = image.convert("RGB")

        image.save(path)
        messagebox.showinfo("Saved", "Watermarked image saved successfully!")

    except (OSError, ValueError) as error:
        messagebox.showerror("Save Error", f"Could not save image:\n{error}")


# Main window
window = tk.Tk()
window.title("Image Watermark Studio")
window.geometry("900x700")
window.minsize(650, 550)
window.configure(bg="#E0FFFF", padx=20, pady=20)

# Responsive grid columns
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(5, weight=1)

# Heading
label_app = tk.Label(
    window,
    text="Image Watermark Studio",
    font=("Times New Roman", 22, "bold"),
    fg="black",
    bg="#E0FFFF"
)
label_app.grid(
    row=0, column=0, columnspan=2,
    pady=(0, 25)
)

# Upload buttons
button_upload = tk.Button(
    window,
    text="Upload Image",
    command=upload_image
)
button_upload.grid(
    row=1, column=0, padx=10, pady=8, sticky="ew"
)

button_logo = tk.Button(
    window,
    text="Upload Logo",
    command=upload_logo
)
button_logo.grid(
    row=1, column=1, padx=10, pady=8, sticky="ew"
)

# Watermark text label
text_1 = tk.Label(
    window,
    text="Watermark text:",
    font=("Times New Roman", 16),
    fg="black",
    bg="#E0FFFF"
)
text_1.grid(
    row=2, column=0, padx=10, pady=8, sticky="e"
)

# Watermark text input
text_input = tk.Entry(
    window,
    font=("Times New Roman", 15)
)
text_input.insert(0, "alan_park_07")
text_input.grid(
    row=2, column=1, padx=10, pady=8, sticky="ew"
)

# Apply watermark buttons
button_apply_watermark = tk.Button(
    window,
    text="Apply Text Watermark",
    command=add_text_watermark
)
button_apply_watermark.grid(
    row=3, column=0, padx=5, pady=8, sticky="ew"
)

button_apply_logo = tk.Button(
    window,
    text="Apply Logo",
    command=add_logo_img
)
button_apply_logo.grid(
    row=3, column=1, padx=5, pady=8, sticky="ew"
)

# Save button
button_save = tk.Button(
    window,
    text="Save Watermarked Image",
    command=save_image
)
button_save.grid(
    row=4, column=0, columnspan=2,
    padx=10, pady=8, sticky="ew"
)

# Image preview
preview = tk.Label(
    window,
    text="Upload an image to begin",
    font=("Times New Roman", 16),
    fg="black",
    bg="white",
    anchor="center"
)
preview.grid(
    row=5, column=0, columnspan=2,
    padx=10, pady=10, sticky="nsew"
)

window.mainloop()
