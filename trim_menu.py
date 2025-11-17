import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import math

class TrimMenu:
    def __init__(self, editor):
        self.editor = editor
        self.is_cropping = False
        self.crop_start = None
        self.crop_end = None
        self.crop_rectangle = None
        self.create_trim_window()
        
    def create_trim_window(self):
        """Create the trim tools window"""
        self.trim_window = ctk.CTkToplevel(self.editor.root)
        self.trim_window.title("Trim & Crop Tools")
        self.trim_window.geometry("450x700")
        self.trim_window.resizable(False, False)
        
        # Center the window
        self.trim_window.transient(self.editor.root)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.trim_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Trim & Crop Tools", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Crop Section
        self.create_crop_section(main_frame)
        
        # Resize Section
        self.create_resize_section(main_frame)
        
        # Manual Adjust Section
        self.create_manual_adjust_section(main_frame)
        
        # Apply Section
        self.create_apply_section(main_frame)
    
    def close_window(self):
        """Close the trim menu window"""
        self.trim_window.destroy()
        
    def create_crop_section(self, parent):
        """Create the crop section"""
        crop_frame = ctk.CTkFrame(parent)
        crop_frame.pack(fill="x", padx=10, pady=10)
        
        crop_label = ctk.CTkLabel(crop_frame, text="Crop Tools", font=("Arial", 14, "bold"))
        crop_label.pack(pady=5)
        
        # Crop mode button
        self.crop_mode_btn = ctk.CTkButton(
            crop_frame, 
            text="Activate Crop Mode", 
            command=self.activate_crop_mode,
            fg_color="blue"
        )
        self.crop_mode_btn.pack(fill="x", padx=10, pady=5)
        
        # Instructions
        instructions_label = ctk.CTkLabel(
            crop_frame, 
            text="Click and drag on canvas to select crop area",
            font=("Arial", 10),
            text_color="gray"
        )
        instructions_label.pack(pady=5)
        
        # Crop coordinates display
        coords_frame = ctk.CTkFrame(crop_frame)
        coords_frame.pack(fill="x", padx=10, pady=5)
        
        coords_label = ctk.CTkLabel(coords_frame, text="Crop Area:", font=("Arial", 10, "bold"))
        coords_label.pack(pady=2)
        
        self.coords_display = ctk.CTkLabel(coords_frame, text="No selection", font=("Arial", 10))
        self.coords_display.pack(pady=2)
        
        # Manual crop coordinates
        manual_crop_frame = ctk.CTkFrame(crop_frame)
        manual_crop_frame.pack(fill="x", padx=10, pady=5)
        
        manual_label = ctk.CTkLabel(manual_crop_frame, text="Manual Crop:", font=("Arial", 10, "bold"))
        manual_label.pack(pady=2)
        
        # X1, Y1 coordinates
        coord1_frame = ctk.CTkFrame(manual_crop_frame)
        coord1_frame.pack(fill="x", padx=5, pady=2)
        
        x1_label = ctk.CTkLabel(coord1_frame, text="X1:", width=30)
        x1_label.pack(side="left", padx=2)
        
        self.x1_entry = ctk.CTkEntry(coord1_frame, width=60)
        self.x1_entry.pack(side="left", padx=2)
        
        y1_label = ctk.CTkLabel(coord1_frame, text="Y1:", width=30)
        y1_label.pack(side="left", padx=2)
        
        self.y1_entry = ctk.CTkEntry(coord1_frame, width=60)
        self.y1_entry.pack(side="left", padx=2)
        
        # X2, Y2 coordinates
        coord2_frame = ctk.CTkFrame(manual_crop_frame)
        coord2_frame.pack(fill="x", padx=5, pady=2)
        
        x2_label = ctk.CTkLabel(coord2_frame, text="X2:", width=30)
        x2_label.pack(side="left", padx=2)
        
        self.x2_entry = ctk.CTkEntry(coord2_frame, width=60)
        self.x2_entry.pack(side="left", padx=2)
        
        y2_label = ctk.CTkLabel(coord2_frame, text="Y2:", width=30)
        y2_label.pack(side="left", padx=2)
        
        self.y2_entry = ctk.CTkEntry(coord2_frame, width=60)
        self.y2_entry.pack(side="left", padx=2)
        
        # Manual crop button
        manual_crop_btn = ctk.CTkButton(
            manual_crop_frame, 
            text="Crop by Coordinates", 
            command=self.crop_by_coordinates
        )
        manual_crop_btn.pack(fill="x", padx=5, pady=5)
        
    def create_resize_section(self, parent):
        """Create the resize section"""
        resize_frame = ctk.CTkFrame(parent)
        resize_frame.pack(fill="x", padx=10, pady=10)
        
        resize_label = ctk.CTkLabel(resize_frame, text="Resize Tools", font=("Arial", 14, "bold"))
        resize_label.pack(pady=5)
        
        # Width and height inputs
        dimensions_frame = ctk.CTkFrame(resize_frame)
        dimensions_frame.pack(fill="x", padx=10, pady=5)
        
        # Width
        width_frame = ctk.CTkFrame(dimensions_frame)
        width_frame.pack(fill="x", pady=2)
        
        width_label = ctk.CTkLabel(width_frame, text="Width:", width=60)
        width_label.pack(side="left", padx=5)
        
        self.width_entry = ctk.CTkEntry(width_frame)
        self.width_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Height
        height_frame = ctk.CTkFrame(dimensions_frame)
        height_frame.pack(fill="x", pady=2)
        
        height_label = ctk.CTkLabel(height_frame, text="Height:", width=60)
        height_label.pack(side="left", padx=5)
        
        self.height_entry = ctk.CTkEntry(height_frame)
        self.height_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Maintain aspect ratio checkbox
        aspect_frame = ctk.CTkFrame(dimensions_frame)
        aspect_frame.pack(fill="x", pady=2)
        
        self.maintain_aspect_var = tk.BooleanVar(value=True)
        aspect_check = ctk.CTkCheckBox(
            aspect_frame, 
            text="Maintain Aspect Ratio", 
            variable=self.maintain_aspect_var
        )
        aspect_check.pack(side="left", padx=5)
        
        # Resize button
        resize_btn = ctk.CTkButton(
            resize_frame, 
            text="Resize Image", 
            command=self.resize_image
        )
        resize_btn.pack(fill="x", padx=10, pady=5)
        
        # Percentage resize
        percentage_frame = ctk.CTkFrame(resize_frame)
        percentage_frame.pack(fill="x", padx=10, pady=5)
        
        percentage_label = ctk.CTkLabel(percentage_frame, text="Scale by Percentage:", font=("Arial", 10, "bold"))
        percentage_label.pack(pady=2)
        
        # Percentage slider
        percent_slider_frame = ctk.CTkFrame(percentage_frame)
        percent_slider_frame.pack(fill="x", padx=5, pady=2)
        
        percent_label = ctk.CTkLabel(percent_slider_frame, text="Scale:", width=50)
        percent_label.pack(side="left", padx=5)
        
        self.percent_slider = ctk.CTkSlider(
            percent_slider_frame, 
            from_=25, 
            to=400, 
            number_of_steps=375,
            command=self.on_percent_change
        )
        self.percent_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.percent_slider.set(100)  # 100% będzie na środku zakresu 25-400
        
        self.percent_value_label = ctk.CTkLabel(percent_slider_frame, text="100%", width=50)
        self.percent_value_label.pack(side="right", padx=5)
        
        # Apply percentage resize button
        percent_resize_btn = ctk.CTkButton(
            percentage_frame, 
            text="Apply Percentage Resize", 
            command=self.resize_by_percentage
        )
        percent_resize_btn.pack(fill="x", padx=5, pady=5)
        
    def create_manual_adjust_section(self, parent):
        """Create the manual adjust section"""
        adjust_frame = ctk.CTkFrame(parent)
        adjust_frame.pack(fill="x", padx=10, pady=10)
        
        adjust_label = ctk.CTkLabel(adjust_frame, text="Manual Adjustments", font=("Arial", 14, "bold"))
        adjust_label.pack(pady=5)
        
        # Position adjustments
        position_frame = ctk.CTkFrame(adjust_frame)
        position_frame.pack(fill="x", padx=10, pady=5)
        
        position_label = ctk.CTkLabel(position_frame, text="Image Position:", font=("Arial", 10, "bold"))
        position_label.pack(pady=2)
        
        # X position
        x_pos_frame = ctk.CTkFrame(position_frame)
        x_pos_frame.pack(fill="x", pady=2)
        
        x_pos_label = ctk.CTkLabel(x_pos_frame, text="X:", width=30)
        x_pos_label.pack(side="left", padx=5)
        
        self.x_pos_entry = ctk.CTkEntry(x_pos_frame)
        self.x_pos_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Y position
        y_pos_frame = ctk.CTkFrame(position_frame)
        y_pos_frame.pack(fill="x", pady=2)
        
        y_pos_label = ctk.CTkLabel(y_pos_frame, text="Y:", width=30)
        y_pos_label.pack(side="left", padx=5)
        
        self.y_pos_entry = ctk.CTkEntry(y_pos_frame)
        self.y_pos_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Apply position button
        apply_pos_btn = ctk.CTkButton(
            position_frame, 
            text="Apply Position", 
            command=self.apply_position
        )
        apply_pos_btn.pack(fill="x", padx=5, pady=5)
        
        # Reset position button
        reset_pos_btn = ctk.CTkButton(
            position_frame, 
            text="Reset to Center", 
            command=self.reset_to_center
        )
        reset_pos_btn.pack(fill="x", padx=5, pady=5)
        
    def create_apply_section(self, parent):
        """Create the apply section"""
        apply_frame = ctk.CTkFrame(parent)
        apply_frame.pack(fill="x", padx=10, pady=10)
        
        apply_label = ctk.CTkLabel(apply_frame, text="Apply Operations", font=("Arial", 14, "bold"))
        apply_label.pack(pady=5)
        
        # Apply to current image
        apply_current_btn = ctk.CTkButton(
            apply_frame, 
            text="Apply to Current Image", 
            command=self.apply_to_current,
            state="disabled"
        )
        apply_current_btn.pack(fill="x", padx=10, pady=2)
        
        # Apply to all images
        apply_all_btn = ctk.CTkButton(
            apply_frame, 
            text="Apply to All Images", 
            command=self.apply_to_all,
            state="disabled"
        )
        apply_all_btn.pack(fill="x", padx=10, pady=2)
        
        # Store button references
        self.apply_current_btn = apply_current_btn
        self.apply_all_btn = apply_all_btn
        
        # Update button states
        self.update_apply_buttons()
        
    def activate_crop_mode(self):
        """Activate crop mode"""
        if self.is_cropping:
            self.deactivate_crop_mode()
        else:
            self.is_cropping = True
            self.crop_mode_btn.configure(fg_color="green", text="Deactivate Crop Mode")
            self.editor.update_status("Crop mode activated - click and drag to select area")
            
    def deactivate_crop_mode(self):
        """Deactivate crop mode"""
        self.is_cropping = False
        self.crop_mode_btn.configure(fg_color="blue", text="Activate Crop Mode")
        self.crop_start = None
        self.crop_end = None
        
        # Remove crop rectangle from canvas
        if self.crop_rectangle:
            self.editor.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None
            
        self.coords_display.configure(text="No selection")
        self.editor.update_status("Crop mode deactivated")
        
    def start_crop_selection(self, x, y):
        """Start crop selection at position"""
        if not self.is_cropping:
            return
            
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        self.crop_start = (x, y)
        self.crop_end = None
        
        # Remove previous crop rectangle
        if self.crop_rectangle:
            self.editor.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None
            
    def continue_crop_selection(self, x, y):
        """Continue crop selection to position"""
        if not self.is_cropping or not self.crop_start:
            return
            
        self.crop_end = (x, y)
        
        # Remove previous crop rectangle
        if self.crop_rectangle:
            self.editor.canvas.delete(self.crop_rectangle)
            
        # Draw new crop rectangle
        start_x, start_y = self.crop_start
        end_x, end_y = self.crop_end
        
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)
        
        self.crop_rectangle = self.editor.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="red",
            width=2,
            dash=(5, 5),
            tags="crop"
        )
        
        # Update coordinates display
        self.coords_display.configure(text=f"({x1}, {y1}) to ({x2}, {y2})")
        
        # Update manual coordinate entries
        self.x1_entry.delete(0, tk.END)
        self.x1_entry.insert(0, str(x1))
        self.y1_entry.delete(0, tk.END)
        self.y1_entry.insert(0, str(y1))
        self.x2_entry.delete(0, tk.END)
        self.x2_entry.insert(0, str(x2))
        self.y2_entry.delete(0, tk.END)
        self.y2_entry.insert(0, str(y2))
        
    def stop_crop_selection(self):
        """Stop crop selection"""
        self.is_cropping = False
        if self.crop_rectangle:
            x1, y1, x2, y2 = self.editor.canvas.coords(self.crop_rectangle)
            img_data = self.editor.images[self.editor.selected_image_index]
            img_x, img_y = img_data['position']
            crop_x1 = int(x1 - img_x)
            crop_y1 = int(y1 - img_y)
            crop_x2 = int(x2 - img_x)
            crop_y2 = int(y2 - img_y)
            if crop_x2 > crop_x1 and crop_y2 > crop_y1:
                self.crop_image(crop_x1, crop_y1, crop_x2, crop_y2)
            self.editor.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None
        
    def crop_by_coordinates(self):
        """Crop image by manually entered coordinates"""
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            self.editor.update_status("Invalid coordinates")
            return
            
        if x1 >= x2 or y1 >= y2:
            self.editor.update_status("Invalid crop area")
            return
            
        self.crop_image(x1, y1, x2, y2)
        
    def crop_image(self, x1, y1, x2, y2):
        """Przytnij wybrany obraz na podstawie współrzędnych"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            return

        self.editor.save_state()
        img_data = self.editor.images[self.editor.selected_image_index]
        img = img_data['image']

        # Upewnij się, że współrzędne są w zakresie obrazu
        x1 = max(0, min(x1, img.width))
        x2 = max(0, min(x2, img.width))
        y1 = max(0, min(y1, img.height))
        y2 = max(0, min(y2, img.height))

        if x2 <= x1 or y2 <= y1:
            self.editor.update_status("Invalid crop area")
            return

        cropped = img.crop((x1, y1, x2, y2))
        img_data['image'] = cropped
        img_data['width'], img_data['height'] = cropped.width, cropped.height
        img_data['photo'] = ImageTk.PhotoImage(cropped)
        # Przesuń obraz na środek
        x = (self.editor.canvas_width - cropped.width) // 2
        y = (self.editor.canvas_height - cropped.height) // 2
        img_data['position'] = (x, y)

        self.editor.update_canvas()
        self.editor.update_status("Image cropped")
        
    def resize_image(self):
        """Resize image by width and height"""
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
        except ValueError:
            self.editor.update_status("Invalid dimensions")
            return
            
        if new_width <= 0 or new_height <= 0:
            self.editor.update_status("Dimensions must be positive")
            return
            
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        self.editor.save_state()
        
        current_img_data = self.editor.images[self.editor.current_image_index]
        img = current_img_data['image'].copy()
        
        try:
            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Update the image
            current_img_data['image'] = resized_img
            
            # Update canvas
            self.editor.update_canvas()
            
            self.editor.update_status(f"Image resized to {new_width}x{new_height}")
            
        except Exception as e:
            self.editor.update_status(f"Error resizing image: {str(e)}")
            
    def on_percent_change(self, value):
        """Handle percentage slider change with real-time scaling"""
        percentage = int(value)
        self.percent_value_label.configure(text=f"{percentage}%")
        
        # Apply real-time scaling if an image is selected
        if (self.editor.images and 
            self.editor.selected_image_index >= 0 and 
            self.editor.selected_image_index < len(self.editor.images)):
            
            self.apply_real_time_scaling(percentage)
        
    def apply_real_time_scaling(self, percentage):
        """Apply real-time scaling to selected image"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            return

        img_data = self.editor.images[self.editor.selected_image_index]
        
        # Use original image for scaling to avoid cumulative scaling
        if 'original_image' not in img_data:
            img_data['original_image'] = img_data['image'].copy()
        
        original_img = img_data['original_image']
        
        try:
            # Calculate new dimensions based on original image
            orig_width = original_img.width
            orig_height = original_img.height
            new_width = max(1, int(orig_width * percentage / 100))
            new_height = max(1, int(orig_height * percentage / 100))

            if new_width <= 0 or new_height <= 0:
                return

            # Scale from original image
            resized_img = original_img.resize((new_width, new_height), Image.LANCZOS)
            img_data['image'] = resized_img
            img_data['width'], img_data['height'] = resized_img.width, resized_img.height
            img_data['photo'] = ImageTk.PhotoImage(resized_img)
            
            # Center the image
            x = (self.editor.canvas_width - resized_img.width) // 2
            y = (self.editor.canvas_height - resized_img.height) // 2
            img_data['position'] = (x, y)

            self.editor.update_canvas()
            self.editor.update_status(f"Scale: {percentage}% ({new_width}x{new_height})")

        except Exception as e:
            self.editor.update_status(f"Error scaling image: {str(e)}")

    def resize_by_percentage(self):
        """Resize selected image by percentage (saves state)"""
        percentage = int(self.percent_slider.get())
        if percentage == 100:
            return

        if not self.editor.images or self.editor.selected_image_index < 0:
            return

        # Save state before applying final resize
        self.editor.save_state()
        
        # Apply the scaling (this will use the current slider value)
        self.apply_real_time_scaling(percentage)
            
    def apply_position(self):
        """Apply position to current image"""
        try:
            new_x = int(self.x_pos_entry.get())
            new_y = int(self.y_pos_entry.get())
        except ValueError:
            self.editor.update_status("Invalid position")
            return
            
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        self.editor.save_state()
        
        current_img_data = self.editor.images[self.editor.current_image_index]
        current_img_data['position'] = (new_x, new_y)
        
        # Update canvas
        self.editor.update_canvas()
        
        self.editor.update_status(f"Image moved to ({new_x}, {new_y})")
        
    def reset_to_center(self):
        """Reset image position to center of canvas"""
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        self.editor.save_state()
        
        current_img_data = self.editor.images[self.editor.current_image_index]
        img = current_img_data['image']
        
        # Calculate center position
        center_x = (self.editor.canvas_width - img.width) // 2
        center_y = (self.editor.canvas_height - img.height) // 2
        
        current_img_data['position'] = (center_x, center_y)
        
        # Update canvas
        self.editor.update_canvas()
        
        # Update position entries
        self.x_pos_entry.delete(0, tk.END)
        self.x_pos_entry.insert(0, str(center_x))
        self.y_pos_entry.delete(0, tk.END)
        self.y_pos_entry.insert(0, str(center_y))
        
        self.editor.update_status("Image centered")
        
    def apply_to_current(self):
        """Apply operations to current image"""
        if not self.editor.images or self.editor.current_image_index < 0:
            return
            
        # This is already handled by the individual functions
        pass
        
    def apply_to_all(self):
        """Apply operations to all images"""
        if not self.editor.images:
            return
            
        # Get current settings
        try:
            new_width = int(self.width_entry.get()) if self.width_entry.get() else None
            new_height = int(self.height_entry.get()) if self.height_entry.get() else None
            percentage = int(self.percent_slider.get()) if self.percent_slider.get() else 100
        except ValueError:
            self.editor.update_status("Invalid values")
            return
            
        if not new_width and not new_height and percentage == 100:
            return
            
        self.editor.save_state()
        
        try:
            for img_data in self.editor.images:
                img = img_data['image'].copy()
                
                # Apply percentage resize if specified
                if percentage != 100:
                    new_w = int(img.width * percentage / 100)
                    new_h = int(img.height * percentage / 100)
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                # Apply specific dimensions if specified
                if new_width and new_height:
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                elif new_width:
                    # Maintain aspect ratio
                    ratio = new_width / img.width
                    new_h = int(img.height * ratio)
                    img = img.resize((new_width, new_h), Image.Resampling.LANCZOS)
                elif new_height:
                    # Maintain aspect ratio
                    ratio = new_height / img.height
                    new_w = int(img.width * ratio)
                    img = img.resize((new_w, new_height), Image.Resampling.LANCZOS)
                    
                img_data['image'] = img
                
            # Update canvas
            self.editor.update_canvas()
            
            self.editor.update_status("Applied resize to all images")
            
        except Exception as e:
            self.editor.update_status(f"Error resizing all images: {str(e)}")
            
    def update_apply_buttons(self):
        """Update button states"""
        has_images = len(self.editor.images) > 0
        has_current = self.editor.current_image_index >= 0
        
        self.apply_current_btn.configure(state="normal" if has_current else "disabled")
        self.apply_all_btn.configure(state="normal" if has_images else "disabled")
        
    def handle_canvas_events(self, event_type, x, y):
        """Handle canvas events for crop selection"""
        if event_type == "click":
            self.start_crop_selection(x, y)
        elif event_type == "drag":
            self.continue_crop_selection(x, y)
        elif event_type == "release":
            self.stop_crop_selection()
