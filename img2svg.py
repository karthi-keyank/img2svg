import os
from tkinter import Tk, filedialog, messagebox, Button
from PIL import Image
import base64


def convert_folder_images_to_svg():
    try:
        # Open file dialog to select a folder containing images
        source_folder = filedialog.askdirectory(title="Select Folder with Images")
        if not source_folder:
            return  # User cancelled folder selection

        # Open file dialog to select the output folder
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            return  # User cancelled output folder selection

        # Get all image files from the source folder
        image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

        if not image_files:
            messagebox.showinfo("No Images Found", "No PNG or JPG images found in the selected folder.")
            return

        for image_file in image_files:
            image_path = os.path.join(source_folder, image_file)

            try:
                with Image.open(image_path) as img:
                    img = img.convert('RGBA')

                    # Convert image to base64
                    with open(image_path, "rb") as image_file_obj:
                        encoded_string = base64.b64encode(image_file_obj.read()).decode('utf-8')

                    # Create a simple SVG wrapper
                    svg_content = f"""
                    <svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">
                        <image href="data:image/png;base64,{encoded_string}" width="100%" height="100%"/>
                    </svg>
                    """

                    # Create output path with the same name but .svg extension
                    output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + ".svg")

                    with open(output_path, "w") as svg_file:
                        svg_file.write(svg_content)

            except Exception as e:
                messagebox.showerror("Conversion Error", f"Failed to convert {image_file}: {e}")

        messagebox.showinfo("Success", f"All images successfully converted and saved to: {output_folder}")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = Tk()
    root.title("Batch Image to SVG Converter")
    root.geometry("300x150")

    convert_button = Button(root, text="Select Folder and Convert", command=convert_folder_images_to_svg)
    convert_button.pack(pady=20)

    root.mainloop()
