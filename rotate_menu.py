import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps
import math

class RotateMenu:
    def __init__(self, editor):
        self.editor = editor
        self.is_rotating = False
        self.rotation_start = None
        self.rotation_center = None
        self.create_rotate_window()
        
    def create_rotate_window(self):
        """Create the rotate tools window"""
        self.rotate_window = ctk.CTkToplevel(self.editor.root)
        self.rotate_window.title("Rotation Tools")
        self.rotate_window.geometry("400x600")
        self.rotate_window.resizable(False, False)
        
        # Center the window
        self.rotate_window.transient(self.editor.root)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.rotate_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Rotation Tools", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Quick Rotation Section
        self.create_quick_rotation_section(main_frame)
        
        # Custom Rotation Section
        self.create_custom_rotation_section(main_frame)
        
        # Mouse Rotation Section
        self.create_mouse_rotation_section(main_frame)
        
        # Mirror Section
        self.create_mirror_section(main_frame)
        
        # Apply Section
        self.create_apply_section(main_frame)
    
    def close_window(self):
        """Close the rotate menu window"""
        self.rotate_window.destroy()
        
    def create_quick_rotation_section(self, parent):
        """Create the quick rotation section"""
        quick_frame = ctk.CTkFrame(parent)
        quick_frame.pack(fill="x", padx=10, pady=10)
        
        quick_label = ctk.CTkLabel(quick_frame, text="Quick Rotation", font=("Arial", 14, "bold"))
        quick_label.pack(pady=5)
        
        # Quick rotation buttons grid
        buttons_grid = ctk.CTkFrame(quick_frame)
        buttons_grid.pack(fill="x", padx=10, pady=5)
        
        # Row 0 - Rotate Selected Image
        selected_label = ctk.CTkLabel(buttons_grid, text="Rotate Selected Image:", font=("Arial", 10, "bold"))
        selected_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Row 1
        rotate_90_btn = ctk.CTkButton(
            buttons_grid, 
            text="Rotate 90°", 
            command=lambda: self.rotate_image(90),
            width=100
        )
        rotate_90_btn.grid(row=0, column=0, padx=5, pady=5)
        
        rotate_180_btn = ctk.CTkButton(
            buttons_grid, 
            text="Rotate 180°", 
            command=lambda: self.rotate_image(180),
            width=100
        )
        rotate_180_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Row 2
        rotate_270_btn = ctk.CTkButton(
            buttons_grid, 
            text="Rotate 270°", 
            command=lambda: self.rotate_image(270),
            width=100
        )
        rotate_270_btn.grid(row=1, column=0, padx=5, pady=5)
        
        rotate_360_btn = ctk.CTkButton(
            buttons_grid, 
            text="Rotate 360°", 
            command=lambda: self.rotate_image(360),
            width=100
        )
        rotate_360_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Row 3 - Rotate All Images
        all_label = ctk.CTkLabel(buttons_grid, text="Rotate All Images:", font=("Arial", 10, "bold"))
        all_label.grid(row=2, column=0, columnspan=2, pady=(10, 5))
        
        # Row 4
        rotate_all_90_btn = ctk.CTkButton(
            buttons_grid, 
            text="All +90°", 
            command=lambda: self.rotate_all_images(90),
            width=100,
            fg_color="orange"
        )
        rotate_all_90_btn.grid(row=3, column=0, padx=5, pady=5)
        
        rotate_all_180_btn = ctk.CTkButton(
            buttons_grid, 
            text="All +180°", 
            command=lambda: self.rotate_all_images(180),
            width=100,
            fg_color="orange"
        )
        rotate_all_180_btn.grid(row=3, column=1, padx=5, pady=5)
        
        # Row 5 - Rotate Canvas
        canvas_label = ctk.CTkLabel(buttons_grid, text="Rotate Canvas:", font=("Arial", 10, "bold"))
        canvas_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))
        
        # Row 6
        rotate_canvas_90_btn = ctk.CTkButton(
            buttons_grid, 
            text="Canvas +90°", 
            command=lambda: self.rotate_canvas(90),
            width=100,
            fg_color="purple"
        )
        rotate_canvas_90_btn.grid(row=5, column=0, padx=5, pady=5)
        
        rotate_canvas_180_btn = ctk.CTkButton(
            buttons_grid, 
            text="Canvas +180°", 
            command=lambda: self.rotate_canvas(180),
            width=100,
            fg_color="purple"
        )
        rotate_canvas_180_btn.grid(row=5, column=1, padx=5, pady=5)
        
    def create_custom_rotation_section(self, parent):
        """Create the custom rotation section"""
        custom_frame = ctk.CTkFrame(parent)
        custom_frame.pack(fill="x", padx=10, pady=10)
        
        custom_label = ctk.CTkLabel(custom_frame, text="Custom Rotation", font=("Arial", 14, "bold"))
        custom_label.pack(pady=5)
        
        # Angle input
        angle_frame = ctk.CTkFrame(custom_frame)
        angle_frame.pack(fill="x", padx=10, pady=5)
        
        angle_label = ctk.CTkLabel(angle_frame, text="Angle:", width=60)
        angle_label.pack(side="left", padx=5)
        
        self.angle_entry = ctk.CTkEntry(angle_frame)
        self.angle_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Rotate button
        rotate_custom_btn = ctk.CTkButton(
            custom_frame, 
            text="Rotate by Custom Angle", 
            command=self.rotate_by_custom_angle
        )
        rotate_custom_btn.pack(fill="x", padx=10, pady=5)
        
        # Angle slider
        slider_frame = ctk.CTkFrame(custom_frame)
        slider_frame.pack(fill="x", padx=10, pady=5)
        
        slider_label = ctk.CTkLabel(slider_frame, text="Angle Slider:", width=80)
        slider_label.pack(side="left", padx=5)
        
        self.angle_slider = ctk.CTkSlider(
            slider_frame, 
            from_=-180, 
            to=180, 
            number_of_steps=360,
            command=self.on_angle_slider_change
        )
        self.angle_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.angle_slider.set(0)
        
        self.angle_slider_value_label = ctk.CTkLabel(slider_frame, text="0°", width=40)
        self.angle_slider_value_label.pack(side="right", padx=5)
        
        # Apply slider rotation button
        apply_slider_btn = ctk.CTkButton(
            custom_frame, 
            text="Apply Slider Rotation", 
            command=self.apply_slider_rotation
        )
        apply_slider_btn.pack(fill="x", padx=10, pady=5)
        
    def create_mouse_rotation_section(self, parent):
        """Create the mouse rotation section"""
        mouse_frame = ctk.CTkFrame(parent)
        mouse_frame.pack(fill="x", padx=10, pady=10)
        
        mouse_label = ctk.CTkLabel(mouse_frame, text="Mouse Rotation", font=("Arial", 14, "bold"))
        mouse_label.pack(pady=5)
        
        # Mouse rotation button
        self.mouse_rotate_btn = ctk.CTkButton(
            mouse_frame, 
            text="Activate Mouse Rotation", 
            command=self.activate_mouse_rotation,
            fg_color="blue"
        )
        self.mouse_rotate_btn.pack(fill="x", padx=10, pady=5)
        
        # Instructions
        instructions_label = ctk.CTkLabel(
            mouse_frame, 
            text="Click and drag on canvas to rotate",
            font=("Arial", 10),
            text_color="gray"
        )
        instructions_label.pack(pady=5)
        
        # Rotation center options
        center_frame = ctk.CTkFrame(mouse_frame)
        center_frame.pack(fill="x", padx=10, pady=5)
        
        center_label = ctk.CTkLabel(center_frame, text="Rotation Center:", width=100)
        center_label.pack(side="left", padx=5)
        
        self.center_var = tk.StringVar(value="image_center")
        center_combo = ctk.CTkComboBox(
            center_frame, 
            values=["image_center", "canvas_center", "mouse_position"],
            variable=self.center_var,
            command=self.on_center_change
        )
        center_combo.pack(side="left", fill="x", expand=True, padx=5)
        
    def create_mirror_section(self, parent):
        """Create the mirror section"""
        mirror_frame = ctk.CTkFrame(parent)
        mirror_frame.pack(fill="x", padx=10, pady=10)
        
        mirror_label = ctk.CTkLabel(mirror_frame, text="Mirror Operations", font=("Arial", 14, "bold"))
        mirror_label.pack(pady=5)
        
        # Mirror buttons
        mirror_horizontal_btn = ctk.CTkButton(
            mirror_frame, 
            text="Flip Horizontal", 
            command=lambda: self.mirror_image("horizontal")
        )
        mirror_horizontal_btn.pack(fill="x", padx=10, pady=2)
        
        mirror_vertical_btn = ctk.CTkButton(
            mirror_frame, 
            text="Flip Vertical", 
            command=lambda: self.mirror_image("vertical")
        )
        mirror_vertical_btn.pack(fill="x", padx=10, pady=2)
        
        mirror_both_btn = ctk.CTkButton(
            mirror_frame, 
            text="Flip Both", 
            command=lambda: self.mirror_image("both")
        )
        mirror_both_btn.pack(fill="x", padx=10, pady=2)
        
    def create_apply_section(self, parent):
        """Create the apply section"""
        apply_frame = ctk.CTkFrame(parent)
        apply_frame.pack(fill="x", padx=10, pady=10)
        
        apply_label = ctk.CTkLabel(apply_frame, text="Apply Rotation", font=("Arial", 14, "bold"))
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
        
    def rotate_image(self, angle):
        """Rotate selected image by specified angle"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for rotation")
            return
            
        self.editor.save_state()
        
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        selected_img_data['rotation'] = (selected_img_data['rotation'] + angle) % 360
        
        self.editor.update_canvas()
        self.editor.update_status(f"Rotated selected image by {angle}°")
        
    def rotate_all_images(self, angle):
        """Rotate all images by specified angle"""
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        self.editor.save_state()
        
        for img_data in self.editor.images:
            img_data['rotation'] = (img_data['rotation'] + angle) % 360
        
        self.editor.update_canvas()
        self.editor.update_status(f"Rotated all images by {angle}°")
        
    def rotate_canvas(self, angle):
        """Rotate the entire canvas (all images together)"""
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        self.editor.save_state()
        
        # Calculate canvas center
        canvas_center_x = self.editor.canvas_width // 2
        canvas_center_y = self.editor.canvas_height // 2
        
        for img_data in self.editor.images:
            # Get current position
            img_x, img_y = img_data['position']
            
            # Calculate offset from center
            offset_x = img_x - canvas_center_x
            offset_y = img_y - canvas_center_y
            
            # Apply rotation to offset
            import math
            rad_angle = math.radians(angle)
            new_offset_x = offset_x * math.cos(rad_angle) - offset_y * math.sin(rad_angle)
            new_offset_y = offset_x * math.sin(rad_angle) + offset_y * math.cos(rad_angle)
            
            # Calculate new position
            new_x = canvas_center_x + new_offset_x
            new_y = canvas_center_y + new_offset_y
            
            # Update position
            img_data['position'] = (new_x, new_y)
            
            # Also rotate the image itself
            img_data['rotation'] = (img_data['rotation'] + angle) % 360
        
        self.editor.update_canvas()
        self.editor.update_status(f"Rotated entire canvas by {angle}°")
        
    def rotate_by_custom_angle(self):
        """Rotate selected image by custom angle from entry"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for rotation")
            return
            
        try:
            angle = float(self.angle_entry.get())
        except ValueError:
            self.editor.update_status("Invalid angle value")
            return
            
        if angle == 0:
            self.editor.update_status("Angle cannot be 0")
            return
            
        self.editor.save_state()
        
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        selected_img_data['rotation'] = (selected_img_data['rotation'] + angle) % 360
        
        self.editor.update_canvas()
        self.editor.update_status(f"Rotated selected image by {angle}°")
        
        # Clear entry
        self.angle_entry.delete(0, tk.END)
        
    def on_angle_slider_change(self, value):
        """Handle angle slider change"""
        self.angle_slider_value_label.configure(text=f"{int(value)}°")
        
    def apply_slider_rotation(self):
        """Apply rotation from slider to selected image"""
        angle = int(self.angle_slider.get())
        if angle == 0:
            return
            
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for rotation")
            return
            
        self.editor.save_state()
        
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        selected_img_data['rotation'] = (selected_img_data['rotation'] + angle) % 360
        
        self.editor.update_canvas()
        self.editor.update_status(f"Applied slider rotation: {angle}° to selected image")
        
        # Reset slider
        self.angle_slider.set(0)
        self.angle_slider_value_label.configure(text="0°")
        
    def activate_mouse_rotation(self):
        """Activate mouse rotation mode"""
        if self.is_rotating:
            self.deactivate_mouse_rotation()
        else:
            self.is_rotating = True
            self.mouse_rotate_btn.configure(fg_color="green", text="Deactivate Mouse Rotation")
            self.editor.update_status("Mouse rotation mode activated - click and drag on canvas")
            
    def deactivate_mouse_rotation(self):
        """Deactivate mouse rotation mode"""
        self.is_rotating = False
        self.mouse_rotate_btn.configure(fg_color="blue", text="Activate Mouse Rotation")
        self.rotation_start = None
        self.rotation_center = None
        self.editor.update_status("Mouse rotation mode deactivated")
        
    def on_center_change(self, value):
        """Handle rotation center change"""
        pass  # Center is applied when rotating
        
    def start_mouse_rotation(self, x, y):
        """Start mouse rotation at position"""
        if not self.is_rotating:
            return
            
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for mouse rotation")
            return
            
        self.rotation_start = (x, y)
        
        # Determine rotation center
        center_type = self.center_var.get()
        if center_type == "image_center":
            selected_img = self.editor.images[self.editor.selected_image_index]
            img_x, img_y = selected_img['position']
            img_width = selected_img['image'].width
            img_height = selected_img['image'].height
            self.rotation_center = (img_x + img_width // 2, img_y + img_height // 2)
        elif center_type == "canvas_center":
            self.rotation_center = (self.editor.canvas_width // 2, self.editor.canvas_height // 2)
        else:  # mouse_position
            self.rotation_center = (x, y)
            
    def continue_mouse_rotation(self, x, y):
        """Continue mouse rotation to position"""
        if not self.is_rotating or not self.rotation_start or not self.rotation_center:
            return
            
        # Calculate angle
        start_x, start_y = self.rotation_start
        center_x, center_y = self.rotation_center
        
        # Calculate angles
        start_angle = math.atan2(start_y - center_y, start_x - center_x)
        current_angle = math.atan2(y - center_y, x - center_x)
        
        # Calculate rotation difference
        rotation_diff = math.degrees(current_angle - start_angle)
        
        # Apply rotation
        if abs(rotation_diff) > 1:  # Only rotate if significant change
            self.editor.save_state()
            
            selected_img_data = self.editor.images[self.editor.selected_image_index]
            selected_img_data['rotation'] = (selected_img_data['rotation'] + rotation_diff) % 360
            
            self.editor.update_canvas()
            
            # Update start position for smooth rotation
            self.rotation_start = (x, y)
            
    def stop_mouse_rotation(self):
        """Stop mouse rotation"""
        if self.is_rotating:
            self.rotation_start = None
            self.rotation_center = None
            
    def mirror_image(self, direction):
        """Mirror selected image in specified direction"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for mirroring")
            return
            
        self.editor.save_state()
        
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        img = selected_img_data['image'].copy()
        
        try:
            if direction == "horizontal":
                img = ImageOps.mirror(img)
            elif direction == "vertical":
                img = ImageOps.flip(img)
            elif direction == "both":
                img = ImageOps.mirror(ImageOps.flip(img))
                
            # Update the image
            selected_img_data['image'] = img
            self.editor.update_canvas()
            self.editor.update_status(f"Selected image flipped {direction}")
            
        except Exception as e:
            self.editor.update_status(f"Error flipping image: {str(e)}")
            
    def apply_to_current(self):
        """Apply rotation to selected image"""
        if not self.editor.images or self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected for rotation")
            return
            
        # This is already handled by the rotation functions
        pass
        
    def apply_to_all(self):
        """Apply rotation to all images"""
        if not self.editor.images:
            return
            
        # Get current rotation settings
        try:
            angle = float(self.angle_entry.get()) if self.angle_entry.get() else 0
        except ValueError:
            # Try getting from slider if entry is empty
            angle = self.angle_slider.get()
            
        if angle == 0:
            self.editor.update_status("No angle specified for rotation")
            return
            
        self.editor.save_state()
        
        try:
            for img_data in self.editor.images:
                img_data['rotation'] = (img_data['rotation'] + angle) % 360
                
            self.editor.update_canvas()
            self.editor.update_status(f"Applied {angle}° rotation to all images")
            
            # Clear entry and reset slider
            self.angle_entry.delete(0, tk.END)
            self.angle_slider.set(0)
            self.angle_slider_value_label.configure(text="0°")
            
        except Exception as e:
            self.editor.update_status(f"Error rotating all images: {str(e)}")
            
    def update_apply_buttons(self):
        """Update button states"""
        has_images = len(self.editor.images) > 0
        has_selected = self.editor.selected_image_index >= 0
        
        self.apply_current_btn.configure(state="normal" if has_selected else "disabled")
        self.apply_all_btn.configure(state="normal" if has_images else "disabled")
        
    def handle_canvas_events(self, event_type, x, y):
        """Handle canvas events for mouse rotation"""
        if event_type == "click":
            self.start_mouse_rotation(x, y)
        elif event_type == "drag":
            self.continue_mouse_rotation(x, y)
        elif event_type == "release":
            self.stop_mouse_rotation()
