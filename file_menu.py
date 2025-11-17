import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class FileMenu:
    def __init__(self, editor):
        self.editor = editor
        self.create_file_window()
        
    def create_file_window(self):
        """Create the file operations window"""
        self.file_window = ctk.CTkToplevel(self.editor.root)
        self.file_window.title("File Operations")
        self.file_window.geometry("600x700")  # Increased width to better utilize space
        self.file_window.resizable(True, True)  # Allow resizing
        
        # Center the window
        self.file_window.transient(self.editor.root)
        
        # Don't grab set immediately - this prevents reopening
        # self.file_window.grab_set()
        
        # Add close protocol
        self.file_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Create scrollable frame
        self.canvas_scroll = tk.Canvas(self.file_window, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.file_window, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas_scroll)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )
        
        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            self.canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas_scroll.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Pack scrollable area
        self.canvas_scroll.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Create main frame inside scrollable frame
        main_frame = ctk.CTkFrame(self.scrollable_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="File Operations", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create two-column layout
        left_column = ctk.CTkFrame(main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_column = ctk.CTkFrame(main_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Load Images Section (left column)
        self.create_load_section(left_column)
        
        # Image Stack Management Section (left column)
        self.create_stack_section(left_column)
        
        # Save Section (right column)
        self.create_save_section(right_column)
        
        # Reset Section (right column)
        self.create_reset_section(right_column)
    
    def close_window(self):
        """Close the file menu window"""
        # Unbind mouse wheel
        self.canvas_scroll.unbind_all("<MouseWheel>")
        self.file_window.destroy()
        
    def create_load_section(self, parent):
        """Create the load images section"""
        load_frame = ctk.CTkFrame(parent)
        load_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        load_label = ctk.CTkLabel(load_frame, text="Load Images", font=("Arial", 14, "bold"))
        load_label.pack(pady=5)
        
        # Load single image button
        load_single_btn = ctk.CTkButton(
            load_frame, 
            text="Load Single Image", 
            command=self.load_single_image
        )
        load_single_btn.pack(fill="x", padx=10, pady=5)
        
        # Load multiple images button
        load_multiple_btn = ctk.CTkButton(
            load_frame, 
            text="Load Multiple Images", 
            command=self.load_multiple_images
        )
        load_multiple_btn.pack(fill="x", padx=10, pady=5)
        
        # Load folder button
        load_folder_btn = ctk.CTkButton(
            load_frame, 
            text="Load Images from Folder", 
            command=self.load_images_from_folder
        )
        load_folder_btn.pack(fill="x", padx=10, pady=5)
        
    def create_stack_section(self, parent):
        """Create the image stack management section"""
        stack_frame = ctk.CTkFrame(parent)
        stack_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        stack_label = ctk.CTkLabel(stack_frame, text="Image Stack Management", font=("Arial", 14, "bold"))
        stack_label.pack(pady=5)
        
        # Current image info
        self.current_image_label = ctk.CTkLabel(stack_frame, text="No images loaded", font=("Arial", 10))
        self.current_image_label.pack(pady=5)
        
        # Stack control buttons
        bring_front_btn = ctk.CTkButton(
            stack_frame, 
            text="Bring to Front", 
            command=self.bring_to_front,
            state="disabled"
        )
        bring_front_btn.pack(fill="x", padx=10, pady=2)
        
        bring_back_btn = ctk.CTkButton(
            stack_frame, 
            text="Send to Back", 
            command=self.bring_to_back,
            state="disabled"
        )
        bring_back_btn.pack(fill="x", padx=10, pady=2)
        
        # Delete selected image button
        delete_btn = ctk.CTkButton(
            stack_frame, 
            text="Delete Selected Image", 
            command=self.delete_selected_image,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        delete_btn.pack(fill="x", padx=10, pady=2)
        
        # Store button references for enabling/disabling
        self.bring_front_btn = bring_front_btn
        self.bring_back_btn = bring_back_btn
        self.delete_btn = delete_btn
        
        # Image list
        self.create_image_list(stack_frame)
        
    def create_image_list(self, parent):
        """Create the image list display"""
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="x", padx=10, pady=5)
        
        list_label = ctk.CTkLabel(list_frame, text="Image Stack (top to bottom):", font=("Arial", 10))
        list_label.pack(pady=2)
        
        # Create listbox for images
        self.image_listbox = tk.Listbox(list_frame, height=8, selectmode="single")
        self.image_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind selection event
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
        
        # Update the list
        self.update_image_list()
        
    def create_save_section(self, parent):
        """Create the save images section"""
        save_frame = ctk.CTkFrame(parent)
        save_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        save_label = ctk.CTkLabel(save_frame, text="Save Images", font=("Arial", 14, "bold"))
        save_label.pack(pady=5)
        
        # Save current image button
        save_current_btn = ctk.CTkButton(
            save_frame, 
            text="Save Current Image", 
            command=self.save_current_image,
            state="disabled"
        )
        save_current_btn.pack(fill="x", padx=10, pady=2)
        
        # Save all as composite button
        save_composite_btn = ctk.CTkButton(
            save_frame, 
            text="Save All as Composite", 
            command=self.save_composite,
            state="disabled"
        )
        save_composite_btn.pack(fill="x", padx=10, pady=2)
        
        # Save canvas as image button
        save_canvas_btn = ctk.CTkButton(
            save_frame, 
            text="Save Canvas as Image", 
            command=self.save_canvas_as_image,
            fg_color="green",
            hover_color="darkgreen",
            state="disabled"
        )
        save_canvas_btn.pack(fill="x", padx=10, pady=2)
        
        # Store button references
        self.save_current_btn = save_current_btn
        self.save_composite_btn = save_composite_btn
        self.save_canvas_btn = save_canvas_btn
        
    def create_reset_section(self, parent):
        """Create the reset section"""
        reset_frame = ctk.CTkFrame(parent)
        reset_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        reset_label = ctk.CTkLabel(reset_frame, text="Reset", font=("Arial", 14, "bold"))
        reset_label.pack(pady=5)
        
        reset_btn = ctk.CTkButton(
            reset_frame, 
            text="Reset Canvas", 
            command=self.reset_canvas,
            fg_color="red",
            hover_color="darkred"
        )
        reset_btn.pack(fill="x", padx=10, pady=5)
        
    def load_single_image(self):
        """Load a single image file"""
        print(f"DEBUG: load_single_image called")
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            print(f"DEBUG: Selected file: {file_path}")
            self.editor.save_state()  # Save state for undo
            self.editor.add_image(file_path)
            self.update_image_list()
            self.update_buttons()
            print(f"DEBUG: Single image loaded successfully")
        else:
            print(f"DEBUG: No file selected")
            
    def load_multiple_images(self):
        """Load multiple image files"""
        print(f"DEBUG: load_multiple_images called")
        
        file_paths = filedialog.askopenfilenames(
            title="Select Multiple Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_paths:
            print(f"DEBUG: Selected {len(file_paths)} files")
            self.editor.save_state()  # Save state for undo
            for file_path in file_paths:
                print(f"DEBUG: Loading file: {file_path}")
                self.editor.add_image(file_path)
            self.update_image_list()
            self.update_buttons()
            print(f"DEBUG: Multiple images loaded successfully")
        else:
            print(f"DEBUG: No files selected")
            
    def load_images_from_folder(self):
        """Load all images from a selected folder"""
        print(f"DEBUG: load_images_from_folder called")
        
        folder_path = filedialog.askdirectory(title="Select Folder with Images")
        
        if folder_path:
            print(f"DEBUG: Selected folder: {folder_path}")
            image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
            image_files = []
            
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            print(f"DEBUG: Found {len(image_files)} image files in folder")
            
            if image_files:
                self.editor.save_state()  # Save state for undo
                for file_path in sorted(image_files):
                    print(f"DEBUG: Loading file: {file_path}")
                    self.editor.add_image(file_path)
                self.update_image_list()
                self.update_buttons()
                messagebox.showinfo("Success", f"Loaded {len(image_files)} images from folder")
                print(f"DEBUG: Folder images loaded successfully")
            else:
                messagebox.showwarning("No Images", "No image files found in the selected folder")
                print(f"DEBUG: No image files found in folder")
        else:
            print(f"DEBUG: No folder selected")
            
    def bring_to_front(self):
        """Bring selected image to front of stack"""
        print(f"DEBUG: bring_to_front called - selected_index: {self.editor.selected_image_index}")
        
        if self.editor.images and self.editor.selected_image_index >= 0:
            print(f"DEBUG: Bringing image {self.editor.selected_image_index} to front")
            self.editor.save_state()
            
            selected_index = self.editor.selected_image_index
            
            # Validate index
            if selected_index >= len(self.editor.images):
                selected_index = len(self.editor.images) - 1
                self.editor.selected_image_index = selected_index
            
            # Get the selected image
            selected_img = self.editor.images[selected_index]
            print(f"DEBUG: Selected image: {os.path.basename(selected_img['path'])}")
            
            # Remove from current position
            self.editor.images.pop(selected_index)
            print(f"DEBUG: Removed image from index {selected_index}")
            
            # Add to end (top of visual stack)
            self.editor.images.append(selected_img)
            print(f"DEBUG: Added image to end of stack at index {len(self.editor.images) - 1}")
            
            # Update selected index to point to the moved image
            self.editor.selected_image_index = len(self.editor.images) - 1
            
            # Update current_image_index if it was pointing to the moved image
            if self.editor.current_image_index == selected_index:
                self.editor.current_image_index = len(self.editor.images) - 1
            elif self.editor.current_image_index > selected_index:
                self.editor.current_image_index -= 1
            
            # Recreate image stack with correct order
            self.editor.image_stack = list(range(len(self.editor.images)))
            
            print(f"DEBUG: Updated indices - selected: {self.editor.selected_image_index}, current: {self.editor.current_image_index}")
            
            # Update canvas with new order
            self.editor.update_canvas()
            self.update_image_list()
            self.update_buttons()
            self.editor.update_image_info()
            
            # Ensure highlight is restored
            if self.editor.selected_image_index >= 0:
                self.editor.selected_image = self.editor.images[self.editor.selected_image_index]
                self.editor.highlight_selected_image()
                print(f"DEBUG: Highlight restored for moved image")
        else:
            print(f"DEBUG: Cannot bring to front - images: {len(self.editor.images)}, selected_index: {self.editor.selected_image_index}")
            
    def bring_to_back(self):
        """Send selected image to back of stack"""
        print(f"DEBUG: bring_to_back called - selected_index: {self.editor.selected_image_index}")
        
        if self.editor.images and self.editor.selected_image_index >= 0:
            print(f"DEBUG: Sending image {self.editor.selected_image_index} to back")
            self.editor.save_state()
            
            selected_index = self.editor.selected_image_index
            
            # Validate index
            if selected_index >= len(self.editor.images):
                selected_index = len(self.editor.images) - 1
                self.editor.selected_image_index = selected_index
                
            # Get the selected image
            selected_img = self.editor.images[selected_index]
            print(f"DEBUG: Selected image: {os.path.basename(selected_img['path'])}")
            
            # Remove from current position
            self.editor.images.pop(selected_index)
            print(f"DEBUG: Removed image from index {selected_index}")
            
            # Add to beginning (bottom of visual stack)
            self.editor.images.insert(0, selected_img)
            print(f"DEBUG: Added image to beginning of stack at index 0")
            
            # Update selected index to point to the moved image
            self.editor.selected_image_index = 0
            
            # Update current_image_index if it was pointing to the moved image
            if self.editor.current_image_index == selected_index:
                self.editor.current_image_index = 0
            elif self.editor.current_image_index < selected_index:
                self.editor.current_image_index += 1
            
            # Recreate image stack with correct order
            self.editor.image_stack = list(range(len(self.editor.images)))
            
            print(f"DEBUG: Updated indices - selected: {self.editor.selected_image_index}, current: {self.editor.current_image_index}")
            
            # Update canvas with new order
            self.editor.update_canvas()
            self.update_image_list()
            self.update_buttons()
            self.editor.update_image_info()
            
            # Ensure highlight is restored
            if self.editor.selected_image_index >= 0:
                self.editor.selected_image = self.editor.images[self.editor.selected_image_index]
                self.editor.highlight_selected_image()
                print(f"DEBUG: Highlight restored for moved image")
        else:
            print(f"DEBUG: Cannot send to back - images: {len(self.editor.images)}, selected_index: {self.editor.selected_image_index}")
            
    def delete_selected_image(self):
        """Delete the currently selected image"""
        print(f"DEBUG: delete_selected_image called - selected_index: {self.editor.selected_image_index}")
        
        if not self.editor.images or self.editor.selected_image_index < 0:
            print(f"DEBUG: Cannot delete - images: {len(self.editor.images)}, selected_index: {self.editor.selected_image_index}")
            return
            
        # Get the selected image info for confirmation
        selected_img = self.editor.images[self.editor.selected_image_index]
        filename = os.path.basename(selected_img['path'])
        
        # Ask for confirmation
        if messagebox.askyesno("Delete Image", f"Are you sure you want to delete '{filename}'?"):
            print(f"DEBUG: User confirmed deletion of image: {filename}")
            self.editor.save_state()  # Save state for undo
            
            # Remove the image from canvas
            if 'id' in selected_img:
                self.editor.canvas.delete(selected_img['id'])
                print(f"DEBUG: Removed image from canvas with ID: {selected_img['id']}")
            
            # Remove from images list
            self.editor.images.pop(self.editor.selected_image_index)
            print(f"DEBUG: Removed image from images list at index {self.editor.selected_image_index}")
            
            # Update indices
            if self.editor.current_image_index == self.editor.selected_image_index:
                self.editor.current_image_index = -1
            elif self.editor.current_image_index > self.editor.selected_image_index:
                self.editor.current_image_index -= 1
                
            # Reset selected image
            self.editor.selected_image_index = -1
            self.editor.selected_image = None
            
            # Clear highlight if any
            if self.editor.highlight_rect:
                self.editor.canvas.delete(self.editor.highlight_rect)
                self.editor.highlight_rect = None
            
            # Update UI
            self.editor.update_canvas()
            self.update_image_list()
            self.update_buttons()
            self.editor.update_image_info()
            self.editor.update_status(f"Deleted image: {filename}")
            
            print(f"DEBUG: Image deletion completed successfully")
        else:
            print(f"DEBUG: User cancelled image deletion")
            
    def on_image_select(self, event):
        """Handle image selection in listbox"""
        selection = self.image_listbox.curselection()
        print(f"DEBUG: Image selection event - selection: {selection}")
        
        if selection:
            # Convert from reverse order (top to bottom) to actual index
            list_index = selection[0]
            actual_index = len(self.editor.images) - 1 - list_index
            print(f"DEBUG: Converting list index {list_index} to actual index {actual_index}")
            
            self.editor.current_image_index = actual_index
            self.editor.update_image_info()
            print(f"DEBUG: Updated current image index to {actual_index}")
        else:
            print(f"DEBUG: No image selected in listbox")
            
    def save_current_image(self):
        """Save the currently selected image"""
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Current Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                current_img = self.editor.images[self.editor.current_image_index]['image']
                
                # Apply rotation if needed
                if self.editor.images[self.editor.current_image_index]['rotation'] != 0:
                    current_img = current_img.rotate(
                        self.editor.images[self.editor.current_image_index]['rotation'], 
                        expand=True
                    )
                
                current_img.save(file_path)
                self.editor.update_status(f"Saved: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                
    def save_composite(self):
        """Save all images as a composite image"""
        if not self.editor.images:
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Composite Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create a composite image from all visible images
                composite = Image.new('RGBA', (self.editor.canvas_width, self.editor.canvas_height), (255, 255, 255, 0))
                
                for img_data in self.editor.images:
                    if img_data['visible']:
                        img = img_data['image'].copy()
                        
                        # Apply rotation if needed
                        if img_data['rotation'] != 0:
                            img = img.rotate(img_data['rotation'], expand=True)
                        
                        # Convert to RGBA if needed
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Paste at position
                        x, y = img_data['position']
                        composite.paste(img, (x, y), img)
                
                composite.save(file_path)
                self.editor.update_status(f"Saved composite: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save composite: {str(e)}")
                
    def save_canvas_as_image(self):
        """Save the current canvas state as a single image file"""
        if not self.editor.images:
            messagebox.showwarning("No Images", "No images loaded on canvas")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Canvas as Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create a new image with canvas dimensions
                canvas_img = Image.new('RGBA', (self.editor.canvas_width, self.editor.canvas_height), (255, 255, 255, 0))
                
                # Process images in the order they appear on canvas (bottom to top)
                for img_data in self.editor.images:
                    if img_data['visible']:
                        img = img_data['image'].copy()
                        
                        # Apply rotation if needed
                        if img_data['rotation'] != 0:
                            img = img.rotate(img_data['rotation'], expand=True)
                        
                        # Convert to RGBA if needed
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        # Get position
                        x, y = img_data['position']
                        
                        # Ensure image fits within canvas bounds
                        if x >= 0 and y >= 0 and x < self.editor.canvas_width and y < self.editor.canvas_height:
                            # Calculate paste area
                            paste_x = max(0, x)
                            paste_y = max(0, y)
                            paste_width = min(img.width, self.editor.canvas_width - paste_x)
                            paste_height = min(img.height, self.editor.canvas_height - paste_y)
                            
                            if paste_width > 0 and paste_height > 0:
                                # Crop image if necessary
                                if paste_width < img.width or paste_height < img.height:
                                    img = img.crop((0, 0, paste_width, paste_height))
                                
                                # Paste image onto canvas
                                canvas_img.paste(img, (paste_x, paste_y), img)
                
                # Convert to RGB if saving as JPEG
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    # Create white background for JPEG
                    background = Image.new('RGB', canvas_img.size, (255, 255, 255))
                    background.paste(canvas_img, mask=canvas_img.split()[-1])  # Use alpha channel as mask
                    canvas_img = background
                
                # Save the image
                canvas_img.save(file_path)
                self.editor.update_status(f"Canvas saved as: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Canvas saved successfully as:\n{os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save canvas: {str(e)}")
                print(f"Canvas save error: {e}")
                import traceback
                traceback.print_exc()
                
    def reset_canvas(self):
        """Reset the canvas to empty state"""
        if self.editor.images:
            if messagebox.askyesno("Reset Canvas", "Are you sure you want to reset the canvas? This will remove all images."):
                self.editor.save_state()
                self.editor.images.clear()
                self.editor.current_image_index = -1
                self.editor.update_canvas()
                self.update_image_list()
                self.update_buttons()
                self.editor.update_image_info()
                self.editor.update_status("Canvas reset")
                
    def update_image_list(self):
        """Update the image listbox display"""
        print(f"DEBUG: Updating image list - total images: {len(self.editor.images)}")
        
        self.image_listbox.delete(0, tk.END)
        
        if self.editor.images:
            # Display images from top (last in list) to bottom (first in list)
            for i in range(len(self.editor.images) - 1, -1, -1):
                img_data = self.editor.images[i]
                filename = os.path.basename(img_data['path'])
                self.image_listbox.insert(0, filename)
                print(f"DEBUG: Added image {i} to list: {filename}")
                
            # Update current image label
            if self.editor.current_image_index >= 0:
                current_img = self.editor.images[self.editor.current_image_index]
                self.current_image_label.configure(text=f"Current: {os.path.basename(current_img['path'])}")
                print(f"DEBUG: Updated current image label to: {os.path.basename(current_img['path'])}")
            else:
                self.current_image_label.configure(text="No current image")
                print(f"DEBUG: No current image to display")
        else:
            self.current_image_label.configure(text="No images loaded")
            print(f"DEBUG: No images to display in list")
            
    def update_buttons(self):
        """Update button states based on current state"""
        has_images = len(self.editor.images) > 0
        has_current = self.editor.current_image_index >= 0
        has_selected = self.editor.selected_image_index >= 0
        
        print(f"DEBUG: Updating file menu buttons - has_images: {has_images}, has_current: {has_current}, has_selected: {has_selected}")
        
        # Stack management buttons - require selected image
        self.bring_front_btn.configure(state="normal" if has_selected else "disabled")
        self.bring_back_btn.configure(state="normal" if has_selected else "disabled")
        self.delete_btn.configure(state="normal" if has_selected else "disabled")
        
        # Save buttons
        self.save_current_btn.configure(state="normal" if has_current else "disabled")
        self.save_composite_btn.configure(state="normal" if has_images else "disabled")
        self.save_canvas_btn.configure(state="normal" if has_images else "disabled")
        
        print(f"DEBUG: File menu buttons updated successfully")
