import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

class FiltersMenu:
    def __init__(self, editor):
        self.editor = editor
        self.create_filters_window()
        
    def create_filters_window(self):
        """Create the filters window"""
        self.filters_window = ctk.CTkToplevel(self.editor.root)
        self.filters_window.title("Image Filters")
        self.filters_window.geometry("500x700")
        self.filters_window.resizable(False, False)
        
        # Center the window
        self.filters_window.transient(self.editor.root)
        
        # Add close protocol
        self.filters_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.filters_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Image Filters", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Standard Filters Section
        self.create_standard_filters_section(main_frame)
        
        # Custom RGB Section
        self.create_custom_rgb_section(main_frame)
        
        # Apply buttons
        self.create_apply_buttons(main_frame)
    
    def close_window(self):
        """Close the filters menu window"""
        self.filters_window.destroy()
        
    def create_standard_filters_section(self, parent):
        """Create the standard filters section"""
        filters_frame = ctk.CTkFrame(parent)
        filters_frame.pack(fill="x", padx=10, pady=10)
        
        filters_label = ctk.CTkLabel(filters_frame, text="Standard Filters", font=("Arial", 14, "bold"))
        filters_label.pack(pady=5)
        
        # Filter buttons grid
        filters_grid = ctk.CTkFrame(filters_frame)
        filters_grid.pack(fill="x", padx=10, pady=5)
        
        # Row 1
        sepia_btn = ctk.CTkButton(
            filters_grid, 
            text="Sepia", 
            command=lambda: self.apply_filter("sepia"),
            width=100
        )
        sepia_btn.grid(row=0, column=0, padx=5, pady=5)
        
        grayscale_btn = ctk.CTkButton(
            filters_grid, 
            text="Grayscale", 
            command=lambda: self.apply_filter("grayscale"),
            width=100
        )
        grayscale_btn.grid(row=0, column=1, padx=5, pady=5)
        
        invert_btn = ctk.CTkButton(
            filters_grid, 
            text="Invert", 
            command=lambda: self.apply_filter("invert"),
            width=100
        )
        invert_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Row 2
        darker_btn = ctk.CTkButton(
            filters_grid, 
            text="Darker", 
            command=lambda: self.apply_filter("darker"),
            width=100
        )
        darker_btn.grid(row=1, column=0, padx=5, pady=5)
        
        lighter_btn = ctk.CTkButton(
            filters_grid, 
            text="Lighter", 
            command=lambda: self.apply_filter("lighter"),
            width=100
        )
        lighter_btn.grid(row=1, column=1, padx=5, pady=5)
        
        contrast_btn = ctk.CTkButton(
            filters_grid, 
            text="High Contrast", 
            command=lambda: self.apply_filter("contrast"),
            width=100
        )
        contrast_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Row 3
        blur_btn = ctk.CTkButton(
            filters_grid, 
            text="Blur", 
            command=lambda: self.apply_filter("blur"),
            width=100
        )
        blur_btn.grid(row=2, column=0, padx=5, pady=5)
        
        sharpen_btn = ctk.CTkButton(
            filters_grid, 
            text="Sharpen", 
            command=lambda: self.apply_filter("sharpen"),
            width=100
        )
        sharpen_btn.grid(row=2, column=1, padx=5, pady=5)
        
        edge_btn = ctk.CTkButton(
            filters_grid, 
            text="Edge Detect", 
            command=lambda: self.apply_filter("edge"),
            width=100
        )
        edge_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # Row 4
        emboss_btn = ctk.CTkButton(
            filters_grid, 
            text="Emboss", 
            command=lambda: self.apply_filter("emboss"),
            width=100
        )
        emboss_btn.grid(row=3, column=0, padx=5, pady=5)
        
        posterize_btn = ctk.CTkButton(
            filters_grid, 
            text="Posterize", 
            command=lambda: self.apply_filter("posterize"),
            width=100
        )
        posterize_btn.grid(row=3, column=1, padx=5, pady=5)
        
        solarize_btn = ctk.CTkButton(
            filters_grid, 
            text="Solarize", 
            command=lambda: self.apply_filter("solarize"),
            width=100
        )
        solarize_btn.grid(row=3, column=2, padx=5, pady=5)
        
    def create_custom_rgb_section(self, parent):
        """Create the custom RGB adjustment section"""
        rgb_frame = ctk.CTkFrame(parent)
        rgb_frame.pack(fill="x", padx=10, pady=10)
        
        rgb_label = ctk.CTkLabel(rgb_frame, text="Custom RGB Adjustments", font=("Arial", 14, "bold"))
        rgb_label.pack(pady=5)
        
        # Red channel
        red_frame = ctk.CTkFrame(rgb_frame)
        red_frame.pack(fill="x", padx=10, pady=5)
        
        red_label = ctk.CTkLabel(red_frame, text="Red:", width=50)
        red_label.pack(side="left", padx=5)
        
        self.red_slider = ctk.CTkSlider(
            red_frame, 
            from_=0.0, 
            to=2.0, 
            number_of_steps=200,
            command=self.on_rgb_change
        )
        self.red_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.red_slider.set(1.0)
        
        self.red_value_label = ctk.CTkLabel(red_frame, text="1.0", width=30)
        self.red_value_label.pack(side="right", padx=5)
        
        # Green channel
        green_frame = ctk.CTkFrame(rgb_frame)
        green_frame.pack(fill="x", padx=10, pady=5)
        
        green_label = ctk.CTkLabel(green_frame, text="Green:", width=50)
        green_label.pack(side="left", padx=5)
        
        self.green_slider = ctk.CTkSlider(
            green_frame, 
            from_=0.0, 
            to=2.0, 
            number_of_steps=200,
            command=self.on_rgb_change
        )
        self.green_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.green_slider.set(1.0)
        
        self.green_value_label = ctk.CTkLabel(green_frame, text="1.0", width=30)
        self.green_value_label.pack(side="right", padx=5)
        
        # Blue channel
        blue_frame = ctk.CTkFrame(rgb_frame)
        blue_frame.pack(fill="x", padx=10, pady=5)
        
        blue_label = ctk.CTkLabel(blue_frame, text="Blue:", width=50)
        blue_label.pack(side="left", padx=5)
        
        self.blue_slider = ctk.CTkSlider(
            blue_frame, 
            from_=0.0, 
            to=2.0, 
            number_of_steps=200,
            command=self.on_rgb_change
        )
        self.blue_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.blue_slider.set(1.0)
        
        self.blue_value_label = ctk.CTkLabel(blue_frame, text="1.0", width=30)
        self.blue_value_label.pack(side="right", padx=5)
        
        # Brightness and contrast
        bc_frame = ctk.CTkFrame(rgb_frame)
        bc_frame.pack(fill="x", padx=10, pady=5)
        
        # Brightness
        brightness_label = ctk.CTkLabel(bc_frame, text="Brightness:", width=70)
        brightness_label.pack(side="left", padx=5)
        
        self.brightness_slider = ctk.CTkSlider(
            bc_frame, 
            from_=0.0, 
            to=2.0, 
            number_of_steps=200,
            command=self.on_rgb_change
        )
        self.brightness_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.brightness_slider.set(1.0)
        
        self.brightness_value_label = ctk.CTkLabel(bc_frame, text="1.0", width=30)
        self.brightness_value_label.pack(side="right", padx=5)
        
        # Contrast
        contrast_frame = ctk.CTkFrame(rgb_frame)
        contrast_frame.pack(fill="x", padx=10, pady=5)
        
        contrast_label = ctk.CTkLabel(contrast_frame, text="Contrast:", width=70)
        contrast_label.pack(side="left", padx=5)
        
        self.contrast_slider = ctk.CTkSlider(
            contrast_frame, 
            from_=0.0, 
            to=2.0, 
            number_of_steps=200,
            command=self.on_rgb_change
        )
        self.contrast_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.contrast_slider.set(1.0)
        
        self.contrast_value_label = ctk.CTkLabel(contrast_frame, text="1.0", width=30)
        self.contrast_value_label.pack(side="right", padx=5)
        
        # Live preview checkbox
        self.live_preview_var = ctk.BooleanVar(value=True)
        live_preview_checkbox = ctk.CTkCheckBox(
            rgb_frame,
            text="Live Preview (zmiany na żywo)",
            variable=self.live_preview_var,
            command=self.toggle_live_preview
        )
        live_preview_checkbox.pack(fill="x", padx=10, pady=5)
        
        # Reset RGB button
        reset_rgb_btn = ctk.CTkButton(
            rgb_frame, 
            text="Reset RGB Values", 
            command=self.reset_rgb_values
        )
        reset_rgb_btn.pack(fill="x", padx=10, pady=5)
        
    def create_apply_buttons(self, parent):
        """Create the apply filter buttons"""
        apply_frame = ctk.CTkFrame(parent)
        apply_frame.pack(fill="x", padx=10, pady=10)
        
        apply_label = ctk.CTkLabel(apply_frame, text="Apply Filters", font=("Arial", 14, "bold"))
        apply_label.pack(pady=5)
        
        # Target selection frame
        target_frame = ctk.CTkFrame(apply_frame)
        target_frame.pack(fill="x", padx=10, pady=5)
        
        target_label = ctk.CTkLabel(target_frame, text="Apply to:", font=("Arial", 12))
        target_label.pack(side="left", padx=5)
        
        # Target selection variable
        self.target_var = ctk.StringVar(value="current")
        
        # Radio buttons for target selection
        current_radio = ctk.CTkRadioButton(
            target_frame, 
            text="Current Image", 
            variable=self.target_var, 
            value="current"
        )
        current_radio.pack(side="left", padx=10)
        
        all_radio = ctk.CTkRadioButton(
            target_frame, 
            text="All Images", 
            variable=self.target_var, 
            value="all"
        )
        all_radio.pack(side="left", padx=10)
        
        # Apply to current image
        apply_current_btn = ctk.CTkButton(
            apply_frame, 
            text="Apply to Current Image", 
            command=self.apply_rgb_to_current,
            state="disabled"
        )
        apply_current_btn.pack(fill="x", padx=10, pady=2)
        
        # Apply to all images
        apply_all_btn = ctk.CTkButton(
            apply_frame, 
            text="Apply to All Images", 
            command=self.apply_rgb_to_all,
            state="disabled"
        )
        apply_all_btn.pack(fill="x", padx=10, pady=2)
        
        # Store button references
        self.apply_current_btn = apply_current_btn
        self.apply_all_btn = apply_all_btn
        
        # Reset filters section
        reset_frame = ctk.CTkFrame(apply_frame)
        reset_frame.pack(fill="x", padx=10, pady=10)
        
        reset_label = ctk.CTkLabel(reset_frame, text="Reset Options", font=("Arial", 12, "bold"))
        reset_label.pack(pady=5)
        
        # Undo last filter button
        undo_btn = ctk.CTkButton(
            reset_frame, 
            text="Undo Last Action (Ctrl+Z)", 
            command=self.editor.undo,
            fg_color="#ff6b6b",
            hover_color="#ff5252"
        )
        undo_btn.pack(fill="x", padx=10, pady=2)
        
        # Reset all filters on selected image
        reset_selected_btn = ctk.CTkButton(
            reset_frame, 
            text="Reset Selected Image to Original", 
            command=self.reset_selected_to_original,
            fg_color="#ffa726",
            hover_color="#ff9800"
        )
        reset_selected_btn.pack(fill="x", padx=10, pady=2)
        
        # Update button states
        self.update_apply_buttons()
        
    def on_rgb_change(self, value):
        """Handle RGB slider changes"""
        # Update value labels
        self.red_value_label.configure(text=f"{self.red_slider.get():.1f}")
        self.green_value_label.configure(text=f"{self.green_slider.get():.1f}")
        self.blue_value_label.configure(text=f"{self.blue_slider.get():.1f}")
        self.brightness_value_label.configure(text=f"{self.brightness_slider.get():.1f}")
        self.contrast_value_label.configure(text=f"{self.contrast_slider.get():.1f}")
        
        # Apply live preview if there's a selected image and live preview is enabled
        if (self.editor.images and self.editor.selected_image_index >= 0 and 
            hasattr(self, 'live_preview_var') and self.live_preview_var.get()):
            self.apply_live_preview()
        
    def reset_rgb_values(self):
        """Reset all RGB sliders to default values"""
        self.red_slider.set(1.0)
        self.green_slider.set(1.0)
        self.blue_slider.set(1.0)
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        
        # Update labels
        self.on_rgb_change(0)
        
        # Restore original image colors
        if self.editor.images and self.editor.selected_image_index >= 0:
            self.restore_original_colors()
        
    def apply_live_preview(self):
        """Apply RGB adjustments for live preview without saving state"""
        try:
            selected_img_data = self.editor.images[self.editor.selected_image_index]
            
            # Get original image for preview
            if 'original_image' in selected_img_data:
                img = selected_img_data['original_image'].copy()
            else:
                img = selected_img_data['image'].copy()
            
            # Apply RGB adjustments
            img = self.apply_rgb_adjustments(img)
            
            # Update image for preview (don't save state)
            selected_img_data['image'] = img
            self.editor.update_canvas()
            
        except Exception as e:
            print(f"Error in live preview: {e}")
        
    def restore_original_colors(self):
        """Restore original image colors"""
        try:
            selected_img_data = self.editor.images[self.editor.selected_image_index]
            
            if 'original_image' in selected_img_data:
                selected_img_data['image'] = selected_img_data['original_image'].copy()
                self.editor.update_canvas()
                self.editor.update_status("RGB values reset - original colors restored")
            else:
                self.editor.update_status("Original image not available")
                
        except Exception as e:
            print(f"Error restoring colors: {e}")
        
    def toggle_live_preview(self):
        """Toggle live preview on/off"""
        if self.live_preview_var.get():
            self.editor.update_status("Live preview enabled - changes visible immediately")
            # Apply current RGB values if there's a selected image
            if self.editor.images and self.editor.selected_image_index >= 0:
                self.apply_live_preview()
        else:
            self.editor.update_status("Live preview disabled - click Apply to see changes")
        
    def apply_filter(self, filter_type):
        """Apply a standard filter to images based on target selection"""
        print(f"DEBUG: Applying filter '{filter_type}'")
        print(f"DEBUG: Total images: {len(self.editor.images)}")
        print(f"DEBUG: Selected image index: {self.editor.selected_image_index}")
        print(f"DEBUG: Target: {self.target_var.get()}")
        
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        target = self.target_var.get()
        
        if target == "current":
            # Check if there's a selected image
            if self.editor.selected_image_index < 0:
                self.editor.update_status("No image selected. Click on an image first.")
                return
        else:
            # Check if there are any images
            if len(self.editor.images) == 0:
                self.editor.update_status("No images loaded")
                return
            
        self.editor.save_state()
        
        try:
            if target == "current":
                # Apply to selected image only
                selected_img_data = self.editor.images[self.editor.selected_image_index]
                print(f"DEBUG: Applying to selected image at index {self.editor.selected_image_index}")
                img = selected_img_data['image'].copy()
                img = self.apply_filter_to_image(img, filter_type)
                selected_img_data['image'] = img
                self.editor.update_status(f"Applied {filter_type} filter to selected image")
            else:
                # Apply to all images
                print(f"DEBUG: Applying to all {len(self.editor.images)} images")
                for i, img_data in enumerate(self.editor.images):
                    img = img_data['image'].copy()
                    img = self.apply_filter_to_image(img, filter_type)
                    img_data['image'] = img
                self.editor.update_status(f"Applied {filter_type} filter to all images")
                
            self.editor.update_canvas()
            
            # Update button states after applying filter
            self.update_apply_buttons()
            
        except Exception as e:
            self.editor.update_status(f"Error applying filter: {str(e)}")
            print(f"Filter error: {e}")
            import traceback
            traceback.print_exc()
            
    def apply_filter_to_image(self, img, filter_type):
        """Apply a specific filter to an image"""
        print(f"DEBUG: Applying filter '{filter_type}' to image with mode '{img.mode}' and size {img.size}")
        
        try:
            if filter_type == "sepia":
                result = self.apply_sepia_filter(img)
            elif filter_type == "grayscale":
                result = img.convert('L').convert('RGB')
            elif filter_type == "invert":
                result = ImageOps.invert(img)
            elif filter_type == "darker":
                enhancer = ImageEnhance.Brightness(img)
                result = enhancer.enhance(0.5)
            elif filter_type == "lighter":
                enhancer = ImageEnhance.Brightness(img)
                result = enhancer.enhance(1.5)
            elif filter_type == "contrast":
                enhancer = ImageEnhance.Contrast(img)
                result = enhancer.enhance(2.0)
            elif filter_type == "blur":
                result = img.filter(ImageFilter.BLUR)
            elif filter_type == "sharpen":
                result = img.filter(ImageFilter.SHARPEN)
            elif filter_type == "edge":
                result = img.filter(ImageFilter.FIND_EDGES)
            elif filter_type == "emboss":
                result = img.filter(ImageFilter.EMBOSS)
            elif filter_type == "posterize":
                result = img.quantize(colors=8).convert('RGB')
            elif filter_type == "solarize":
                result = ImageOps.solarize(img, threshold=128)
            else:
                print(f"DEBUG: Unknown filter type '{filter_type}'")
                result = img
                
            print(f"DEBUG: Filter '{filter_type}' applied successfully, result mode: '{result.mode}', size: {result.size}")
            return result
            
        except Exception as e:
            print(f"DEBUG: Error applying filter '{filter_type}': {e}")
            import traceback
            traceback.print_exc()
            return img
            
    def apply_sepia_filter(self, img):
        """Apply sepia filter to image"""
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Convert to numpy array
        img_array = np.array(img)
        
        # Sepia transformation matrix
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        # Apply transformation
        sepia_img = np.dot(img_array, sepia_matrix.T)
        
        # Clip values to 0-255 range
        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
        
        return Image.fromarray(sepia_img)
        
    def apply_rgb_to_current(self):
        """Apply custom RGB adjustments to selected image"""
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        if self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected. Click on an image first.")
            return
            
        self.editor.save_state()
        
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        img = selected_img_data['image'].copy()
        
        try:
            # Apply RGB adjustments
            img = self.apply_rgb_adjustments(img)
            
            # Update the image
            selected_img_data['image'] = img
            self.editor.update_canvas()
            self.editor.update_status("Applied custom RGB adjustments to selected image")
            
            # Update button states
            self.update_apply_buttons()
            
        except Exception as e:
            self.editor.update_status(f"Error applying RGB adjustments: {str(e)}")
            print(f"RGB error: {e}")
            
    def apply_rgb_to_all(self):
        """Apply custom RGB adjustments to all images"""
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        self.editor.save_state()
        
        try:
            for img_data in self.editor.images:
                img = img_data['image'].copy()
                img = self.apply_rgb_adjustments(img)
                img_data['image'] = img
                
            self.editor.update_canvas()
            self.editor.update_status("Applied custom RGB adjustments to all images")
            
            # Update button states
            self.update_apply_buttons()
            
        except Exception as e:
            self.editor.update_status(f"Error applying RGB adjustments: {str(e)}")
            print(f"RGB all error: {e}")
            

    def apply_rgb_adjustments(self, img):
        """Apply RGB adjustments to an image"""
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Get current values
        red_factor = self.red_slider.get()
        green_factor = self.green_slider.get()
        blue_factor = self.blue_slider.get()
        brightness_factor = self.brightness_slider.get()
        contrast_factor = self.contrast_slider.get()
        
        # Apply brightness first
        if brightness_factor != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            
        # Apply contrast
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            
        # Apply RGB channel adjustments
        if red_factor != 1.0 or green_factor != 1.0 or blue_factor != 1.0:
            # Convert to numpy array
            img_array = np.array(img)
            
            # Apply RGB factors
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * red_factor, 0, 255)
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * green_factor, 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * blue_factor, 0, 255)
            
            img = Image.fromarray(img_array.astype(np.uint8))
            
        return img
        
    def reset_selected_to_original(self):
        """Reset selected image to its original state"""
        if not self.editor.images:
            self.editor.update_status("No images loaded")
            return
            
        if self.editor.selected_image_index < 0:
            self.editor.update_status("No image selected. Click on an image first.")
            return
            
        self.editor.save_state()
        
        # Get the selected image data
        selected_img_data = self.editor.images[self.editor.selected_image_index]
        
        # Reset to original image if available
        if 'original_image' in selected_img_data:
            selected_img_data['image'] = selected_img_data['original_image'].copy()
            self.editor.update_canvas()
            self.editor.update_status("Reset selected image to original state")
            
            # Update button states
            self.update_apply_buttons()
        else:
            self.editor.update_status("Original image data not available")
        
    def update_apply_buttons(self):
        """Update the state of apply buttons"""
        has_images = len(self.editor.images) > 0
        has_selected = self.editor.selected_image_index >= 0
        
        print(f"DEBUG: Updating filter buttons - has_images: {has_images}, has_selected: {has_selected}")
        print(f"DEBUG: Total images: {len(self.editor.images)}, selected_index: {self.editor.selected_image_index}")
        
        try:
            current_state = "normal" if has_selected else "disabled"
            all_state = "normal" if has_images else "disabled"
            
            print(f"DEBUG: Setting current button to: {current_state}, all button to: {all_state}")
            
            self.apply_current_btn.configure(state=current_state)
            self.apply_all_btn.configure(state=all_state)
            
            print(f"DEBUG: Filter buttons updated successfully")
            
        except Exception as e:
            print(f"Error updating filter buttons: {e}")
            import traceback
            traceback.print_exc()
