import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import os
from datetime import datetime
from PIL import ImageTk

class BatchMenu:
    def __init__(self, editor):
        self.editor = editor
        self.create_batch_window()
        
    def create_batch_window(self):
        """Create the batch processing window"""
        self.batch_window = ctk.CTkToplevel(self.editor.root)
        self.batch_window.title("Batch Image Processing")
        self.batch_window.geometry("600x700")  # Reduced size
        self.batch_window.resizable(True, True)  # Allow resizing
        
        # Center the window
        self.batch_window.transient(self.editor.root)
        
        # Add close protocol
        self.batch_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Create main scrollable frame
        main_canvas = tk.Canvas(self.batch_window)
        scrollbar = tk.Scrollbar(self.batch_window, orient="vertical", command=main_canvas.yview)
        self.main_frame = ctk.CTkFrame(main_canvas)
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the frame
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="Batch Image Processing", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_label = ctk.CTkLabel(self.main_frame, text="Automatically generate multiple variations of your image", font=("Arial", 12))
        desc_label.pack(pady=5)
        
        # Quick Start Guide
        self.create_quick_start_guide(self.main_frame)
        
        # Source image selection
        self.create_source_section(self.main_frame)
        
        # Processing options
        self.create_processing_section(self.main_frame)
        
        # Output settings
        self.create_output_section(self.main_frame)
        
        # Preview section
        self.create_preview_section(self.main_frame)
        
        # Control buttons
        self.create_control_buttons(self.main_frame)
        
        # Update scroll region
        self.main_frame.update_idletasks()
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
    def close_window(self):
        """Close the batch menu window"""
        self.batch_window.destroy()
        
    def create_quick_start_guide(self, parent):
        """Create a quick start guide section"""
        guide_frame = ctk.CTkFrame(parent)
        guide_frame.pack(fill="x", padx=10, pady=10)
        
        guide_label = ctk.CTkLabel(guide_frame, text="Quick Start Guide", font=("Arial", 14, "bold"))
        guide_label.pack(pady=5)
        
        guide_text = (
            "1. Load an image using the 'Load New Image' button or the File menu.\n"
            "2. Select the image you want to process in the 'Source Image' section.\n"
            "3. Enable the processing options you want (Rotation, Scale, Filters, Color).\n"
            "4. Configure the output settings (directory, format, naming pattern).\n"
            "5. Click 'Update Preview' to see what will be generated.\n"
            "6. Click 'Start Batch Processing' to begin.\n\n"
            "You can also use the 'Select Source Image' button to manually select an image from the loaded images."
        )
        guide_text_label = ctk.CTkLabel(guide_frame, text=guide_text, font=("Arial", 10), justify="left")
        guide_text_label.pack(pady=5)
        
    def create_source_section(self, parent):
        """Create the source image selection section"""
        source_frame = ctk.CTkFrame(parent)
        source_frame.pack(fill="x", padx=10, pady=10)
        
        source_label = ctk.CTkLabel(source_frame, text="Source Image", font=("Arial", 14, "bold"))
        source_label.pack(pady=5)
        
        # Source image info
        self.source_info = ctk.CTkLabel(source_frame, text="No image selected", font=("Arial", 10))
        self.source_info.pack(pady=5)
        
        # Instructions label
        instructions_label = ctk.CTkLabel(
            source_frame, 
            text="First load an image using the File menu, then select it here for batch processing", 
            font=("Arial", 10),
            text_color="gray"
        )
        instructions_label.pack(pady=5)

        # --- NOWY KOD: miniatury do wyboru ---
        if self.editor.images:
            thumbs_frame = ctk.CTkFrame(source_frame)
            thumbs_frame.pack(pady=5)
            for idx, img_data in enumerate(self.editor.images):
                thumb = img_data['image'].copy()
                thumb.thumbnail((60, 60))
                thumb_img = ImageTk.PhotoImage(thumb)
                lbl = tk.Label(thumbs_frame, image=thumb_img, borderwidth=2, relief="solid", cursor="hand2")
                lbl.image = thumb_img  # zapobiega usunięciu z pamięci
                lbl.grid(row=0, column=idx, padx=4, pady=2)
                lbl.bind("<Button-1>", lambda e, i=idx: self.select_source_image_by_index(i))
        # --- KONIEC NOWEGO KODU ---

        # Button frame
        button_frame = ctk.CTkFrame(source_frame)
        button_frame.pack(pady=5)
        
        # Select source button
        select_btn = ctk.CTkButton(
            button_frame,
            text="Select Source Image",
            command=self.select_source_image,
            width=150
        )
        select_btn.pack(side="left", padx=5)
        
        # Load image button (opens file dialog directly)
        load_btn = ctk.CTkButton(
            button_frame,
            text="Load New Image",
            command=self.load_image_directly,
            width=150
        )
        load_btn.pack(side="left", padx=5)

    def create_processing_section(self, parent):
        """Create the processing options section"""
        processing_frame = ctk.CTkFrame(parent)
        processing_frame.pack(fill="x", padx=10, pady=10)
        
        processing_label = ctk.CTkLabel(processing_frame, text="Processing Options", font=("Arial", 14, "bold"))
        processing_label.pack(pady=5)
        
        # Create scrollable frame for options
        self.options_canvas = tk.Canvas(processing_frame, height=300)
        scrollbar = tk.Scrollbar(processing_frame, orient="vertical", command=self.options_canvas.yview)
        self.options_frame = ctk.CTkFrame(self.options_canvas)
        
        self.options_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        self.options_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the frame
        self.options_canvas.create_window((0, 0), window=self.options_frame, anchor="nw")
        
        # Rotation variations
        self.create_rotation_variations()
        
        # Scale variations
        self.create_scale_variations()
        
        # Filter variations
        self.create_filter_variations()
        
        # Color variations
        self.create_color_variations()
        
        # Update scroll region
        self.options_frame.update_idletasks()
        self.options_canvas.configure(scrollregion=self.options_canvas.bbox("all"))
        
    def create_rotation_variations(self):
        """Create rotation variation options"""
        rotation_frame = ctk.CTkFrame(self.options_frame)
        rotation_frame.pack(fill="x", padx=10, pady=5)
        
        rotation_label = ctk.CTkLabel(rotation_frame, text="Rotation Variations", font=("Arial", 12, "bold"))
        rotation_label.pack(pady=5)
        
        # Enable rotation checkbox
        self.rotation_enabled = ctk.CTkCheckBox(rotation_frame, text="Enable rotation variations")
        self.rotation_enabled.pack(pady=2)
        
        # Rotation angles
        angles_frame = ctk.CTkFrame(rotation_frame)
        angles_frame.pack(fill="x", padx=10, pady=5)
        
        angles_label = ctk.CTkLabel(angles_frame, text="Angles (degrees):")
        angles_label.pack(side="left", padx=5)
        
        self.rotation_angles = ctk.CTkEntry(angles_frame, placeholder_text="90, 180, 270")
        self.rotation_angles.pack(side="left", padx=5, fill="x", expand=True)
        self.rotation_angles.insert(0, "90, 180, 270")
        
    def create_scale_variations(self):
        """Create scale variation options"""
        scale_frame = ctk.CTkFrame(self.options_frame)
        scale_frame.pack(fill="x", padx=10, pady=5)
        
        scale_label = ctk.CTkLabel(scale_frame, text="Scale Variations", font=("Arial", 12, "bold"))
        scale_label.pack(pady=5)
        
        # Enable scale checkbox
        self.scale_enabled = ctk.CTkCheckBox(scale_frame, text="Enable scale variations")
        self.scale_enabled.pack(pady=2)
        
        # Scale factors
        scale_factors_frame = ctk.CTkFrame(scale_frame)
        scale_factors_frame.pack(fill="x", padx=10, pady=5)
        
        scale_factors_label = ctk.CTkLabel(scale_factors_frame, text="Scale factors:")
        scale_factors_label.pack(side="left", padx=5)
        
        self.scale_factors = ctk.CTkEntry(scale_factors_frame, placeholder_text="0.5, 0.75, 1.25, 1.5")
        self.scale_factors.pack(side="left", padx=5, fill="x", expand=True)
        self.scale_factors.insert(0, "0.5, 0.75, 1.25, 1.5")
        
    def create_filter_variations(self):
        """Create filter variation options"""
        filter_frame = ctk.CTkFrame(self.options_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        filter_label = ctk.CTkLabel(filter_frame, text="Filter Variations", font=("Arial", 12, "bold"))
        filter_label.pack(pady=5)
        
        # Enable filters checkbox
        self.filters_enabled = ctk.CTkCheckBox(filter_frame, text="Enable filter variations")
        self.filters_enabled.pack(pady=2)
        
        # Filter selection
        filters_frame = ctk.CTkFrame(filter_frame)
        filters_frame.pack(fill="x", padx=10, pady=5)
        
        # Create checkboxes for each filter
        self.filter_vars = {}
        filters = [
            ("sepia", "Sepia"),
            ("grayscale", "Grayscale"),
            ("invert", "Invert"),
            ("blur", "Blur"),
            ("sharpen", "Sharpen"),
            ("emboss", "Emboss"),
            ("edge_enhance", "Edge Enhance")
        ]
        
        for i, (filter_name, filter_label) in enumerate(filters):
            var = ctk.CTkCheckBox(filters_frame, text=filter_label)
            var.pack(anchor="w", padx=5, pady=2)
            self.filter_vars[filter_name] = var
            
    def create_color_variations(self):
        """Create color variation options"""
        color_frame = ctk.CTkFrame(self.options_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        color_label = ctk.CTkLabel(color_frame, text="Color Variations", font=("Arial", 12, "bold"))
        color_label.pack(pady=5)
        
        # Enable color variations checkbox
        self.color_enabled = ctk.CTkCheckBox(color_frame, text="Enable color variations")
        self.color_enabled.pack(pady=2)
        
        # Brightness variations
        brightness_frame = ctk.CTkFrame(color_frame)
        brightness_frame.pack(fill="x", padx=10, pady=5)
        
        brightness_label = ctk.CTkLabel(brightness_frame, text="Brightness factors:")
        brightness_label.pack(side="left", padx=5)
        
        self.brightness_factors = ctk.CTkEntry(brightness_frame, placeholder_text="0.7, 1.3")
        self.brightness_factors.pack(side="left", padx=5, fill="x", expand=True)
        self.brightness_factors.insert(0, "0.7, 1.3")
        
        # Contrast variations
        contrast_frame = ctk.CTkFrame(color_frame)
        contrast_frame.pack(fill="x", padx=10, pady=5)
        
        contrast_label = ctk.CTkLabel(contrast_frame, text="Contrast factors:")
        contrast_label.pack(side="left", padx=5)
        
        self.contrast_factors = ctk.CTkEntry(contrast_frame, placeholder_text="0.8, 1.2")
        self.contrast_factors.pack(side="left", padx=5, fill="x", expand=True)
        self.contrast_factors.insert(0, "0.8, 1.2")
        
    def create_output_section(self, parent):
        """Create the output settings section"""
        output_frame = ctk.CTkFrame(parent)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        output_label = ctk.CTkLabel(output_frame, text="Output Settings", font=("Arial", 14, "bold"))
        output_label.pack(pady=5)
        
        # Output directory
        output_dir_frame = ctk.CTkFrame(output_frame)
        output_dir_frame.pack(fill="x", padx=10, pady=5)
        
        output_dir_label = ctk.CTkLabel(output_dir_frame, text="Output directory:")
        output_dir_label.pack(side="left", padx=5)
        
        # Get current working directory for default path
        current_dir = os.getcwd()
        default_output = os.path.join(current_dir, "batch_output")
        
        self.output_dir = ctk.CTkEntry(output_dir_frame, placeholder_text=default_output)
        self.output_dir.pack(side="left", padx=5, fill="x", expand=True)
        self.output_dir.insert(0, default_output)
        
        # Add browse button for output directory
        browse_btn = ctk.CTkButton(
            output_dir_frame,
            text="Browse",
            command=self.browse_output_directory,
            width=80
        )
        browse_btn.pack(side="right", padx=5)
        
        # Show full path info
        path_info_label = ctk.CTkLabel(
            output_frame, 
            text=f"Images will be saved to: {default_output}",
            font=("Arial", 10),
            text_color="blue"
        )
        path_info_label.pack(pady=2)
        
        # File format
        format_frame = ctk.CTkFrame(output_frame)
        format_frame.pack(fill="x", padx=10, pady=5)
        
        format_label = ctk.CTkLabel(format_frame, text="Output format:")
        format_label.pack(side="left", padx=5)
        
        self.output_format = ctk.CTkComboBox(format_frame, values=["PNG", "JPEG", "BMP"])
        self.output_format.pack(side="left", padx=5)
        self.output_format.set("PNG")
        
        # Naming pattern
        naming_frame = ctk.CTkFrame(output_frame)
        naming_frame.pack(fill="x", padx=10, pady=5)
        
        naming_label = ctk.CTkLabel(naming_frame, text="Naming pattern:")
        naming_label.pack(side="left", padx=5)
        
        self.naming_pattern = ctk.CTkEntry(naming_frame, placeholder_text="{original}_{variation}_{index}")
        self.naming_pattern.pack(side="left", padx=5, fill="x", expand=True)
        self.naming_pattern.insert(0, "{original}_{variation}_{index}")
        
        # Naming pattern help
        naming_help_label = ctk.CTkLabel(
            output_frame,
            text="Available placeholders: {original}, {variation}, {index}",
            font=("Arial", 9),
            text_color="gray"
        )
        naming_help_label.pack(pady=2)
        
    def create_preview_section(self, parent):
        """Create the preview section"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="x", padx=10, pady=10)
        
        preview_label = ctk.CTkLabel(preview_frame, text="Preview", font=("Arial", 14, "bold"))
        preview_label.pack(pady=5)
        
        # Preview info
        self.preview_info = ctk.CTkLabel(preview_frame, text="No variations configured", font=("Arial", 10))
        self.preview_info.pack(pady=5)
        
        # Update preview button
        update_preview_btn = ctk.CTkButton(
            preview_frame,
            text="Update Preview",
            command=self.update_preview,
            width=120
        )
        update_preview_btn.pack(pady=5)
        
    def create_control_buttons(self, parent):
        """Create the control buttons"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Process button
        self.process_btn = ctk.CTkButton(
            buttons_frame,
            text="Start Batch Processing",
            command=self.start_batch_processing,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.process_btn.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(buttons_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(buttons_frame, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
    def select_source_image(self):
        """Select the source image for batch processing"""
        if not self.editor.images:
            self.show_error(
                "No images loaded.\n\n"
                "To use batch processing:\n"
                "1. Click 'Load New Image' to load an image directly, OR\n"
                "2. Use the File menu to load images first, then return here\n\n"
                "Once an image is loaded, you can select it for batch processing."
            )
            return
            
        # Use the currently selected image or the last loaded image
        if self.editor.selected_image:
            self.source_image = self.editor.selected_image
            self.source_image_index = self.editor.selected_image_index
        else:
            self.source_image = self.editor.images[-1]
            self.source_image_index = len(self.editor.images) - 1
            
        # Update source info
        filename = os.path.basename(self.source_image['path'])
        self.source_info.configure(text=f"Selected: {filename}")
        
    def update_preview(self):
        """Update the preview of what will be generated"""
        if not hasattr(self, 'source_image'):
            self.show_error("Please select a source image first.")
            return
            
        variations = []
        
        # Count rotation variations
        if self.rotation_enabled.get():
            try:
                angles = [float(x.strip()) for x in self.rotation_angles.get().split(',')]
                variations.extend([f"Rotate {angle}°" for angle in angles])
            except:
                pass
                
        # Count scale variations
        if self.scale_enabled.get():
            try:
                scales = [float(x.strip()) for x in self.scale_factors.get().split(',')]
                variations.extend([f"Scale {scale}x" for scale in scales])
            except:
                pass
                
        # Count filter variations
        if self.filters_enabled.get():
            for filter_name, var in self.filter_vars.items():
                if var.get():
                    variations.append(f"Filter: {filter_name}")
                    
        # Count color variations
        if self.color_enabled.get():
            try:
                brightness = [float(x.strip()) for x in self.brightness_factors.get().split(',')]
                variations.extend([f"Brightness {b}" for b in brightness])
            except:
                pass
                
            try:
                contrast = [float(x.strip()) for x in self.contrast_factors.get().split(',')]
                variations.extend([f"Contrast {c}" for c in contrast])
            except:
                pass
                
        if variations:
            total = len(variations)
            self.preview_info.configure(text=f"Will generate {total} variations:\n" + "\n".join(variations[:5]) + ("..." if total > 5 else ""))
        else:
            self.preview_info.configure(text="No variations configured")
            
    def browse_output_directory(self):
        """Browse for output directory"""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(
            title="Select Output Directory for Batch Processing"
        )
        
        if directory:
            self.output_dir.delete(0, "end")
            self.output_dir.insert(0, directory)
            
            # Update path info
            for widget in self.output_dir.master.master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Images will be saved to:" in widget.cget("text"):
                    widget.configure(text=f"Images will be saved to: {directory}")
                    break
    
    def start_batch_processing(self):
        """Start the batch processing"""
        if not hasattr(self, 'source_image'):
            self.show_error("Please select a source image first.")
            return
            
        # Get processing options
        variations = self.get_processing_variations()
        if not variations:
            self.show_error("No variations configured. Please enable at least one processing option.")
            return
            
        # Create output directory
        output_dir = self.output_dir.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                self.show_info(f"Created output directory: {output_dir}")
            except Exception as e:
                self.show_error(f"Failed to create output directory: {e}")
                return
            
        # Show where files will be saved
        self.show_info(f"Starting batch processing...\nFiles will be saved to:\n{output_dir}")
            
        # Start processing
        self.process_variations(variations, output_dir)
        
    def get_processing_variations(self):
        """Get the list of processing variations to apply"""
        variations = []
        
        # Rotation variations
        if self.rotation_enabled.get():
            try:
                angles = [float(x.strip()) for x in self.rotation_angles.get().split(',')]
                for angle in angles:
                    variations.append(('rotation', angle))
            except:
                pass
                
        # Scale variations
        if self.scale_enabled.get():
            try:
                scales = [float(x.strip()) for x in self.scale_factors.get().split(',')]
                for scale in scales:
                    variations.append(('scale', scale))
            except:
                pass
                
        # Filter variations
        if self.filters_enabled.get():
            for filter_name, var in self.filter_vars.items():
                if var.get():
                    variations.append(('filter', filter_name))
                    
        # Color variations
        if self.color_enabled.get():
            try:
                brightness = [float(x.strip()) for x in self.brightness_factors.get().split(',')]
                for b in brightness:
                    variations.append(('brightness', b))
            except:
                pass
                
            try:
                contrast = [float(x.strip()) for x in self.contrast_factors.get().split(',')]
                for c in contrast:
                    variations.append(('contrast', c))
            except:
                pass
                
        return variations
        
    def process_variations(self, variations, output_dir):
        """Process all variations"""
        total_variations = len(variations)
        self.progress_bar.set(0)
        self.status_label.configure(text="Processing...")
        self.process_btn.configure(state="disabled")
        
        # Get original image
        original_path = self.source_image['path']
        original_name = os.path.splitext(os.path.basename(original_path))[0]
        
        # Process each variation
        for i, (variation_type, variation_value) in enumerate(variations):
            try:
                # Load original image
                img = Image.open(original_path)
                
                # Apply variation
                processed_img = self.apply_variation(img, variation_type, variation_value)
                
                # Generate filename
                filename = self.generate_filename(original_name, variation_type, variation_value, i)
                output_path = os.path.join(output_dir, filename)
                
                # Save processed image
                processed_img.save(output_path, self.output_format.get())
                
                # Update progress
                progress = (i + 1) / total_variations
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Processed {i+1}/{total_variations}: {variation_type}")
                
                # Update GUI
                self.batch_window.update()
                
            except Exception as e:
                print(f"Error processing variation {variation_type}: {e}")
                
        # Complete
        self.status_label.configure(text=f"Completed! Generated {total_variations} variations in {output_dir}")
        
        # Show completion message with file location
        completion_message = (
            f"Batch processing completed successfully!\n\n"
            f"Generated {total_variations} image variations\n"
            f"Files saved to:\n{output_dir}\n\n"
            f"Click 'Open Folder' to view the results"
        )
        
        # Create completion window with open folder button
        completion_window = ctk.CTkToplevel(self.batch_window)
        completion_window.title("Batch Processing Complete")
        completion_window.geometry("500x300")
        completion_window.resizable(False, False)
        
        # Center the window
        completion_window.transient(self.batch_window)
        
        # Success message
        success_label = ctk.CTkLabel(completion_window, text="✅ Batch Processing Complete!", font=("Arial", 16, "bold"))
        success_label.pack(pady=20)
        
        # Details
        details_label = ctk.CTkLabel(completion_window, text=completion_message, font=("Arial", 12), justify="left")
        details_label.pack(pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(completion_window)
        button_frame.pack(pady=20)
        
        # Open folder button
        open_folder_btn = ctk.CTkButton(
            button_frame,
            text="Open Output Folder",
            command=lambda: self.open_output_folder(output_dir),
            width=150
        )
        open_folder_btn.pack(side="left", padx=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=completion_window.destroy,
            width=100
        )
        close_btn.pack(side="left", padx=10)
        
        self.process_btn.configure(state="normal")
        
    def apply_variation(self, img, variation_type, variation_value):
        """Apply a specific variation to an image"""
        if variation_type == 'rotation':
            return img.rotate(variation_value, expand=True)
            
        elif variation_type == 'scale':
            width, height = img.size
            new_width = int(width * variation_value)
            new_height = int(height * variation_value)
            return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        elif variation_type == 'filter':
            if variation_value == 'sepia':
                return self.apply_sepia_filter(img)
            elif variation_value == 'grayscale':
                return img.convert('L').convert('RGB')
            elif variation_value == 'invert':
                return ImageOps.invert(img)
            elif variation_value == 'blur':
                return img.filter(ImageFilter.BLUR)
            elif variation_value == 'sharpen':
                return img.filter(ImageFilter.SHARPEN)
            elif variation_value == 'emboss':
                return img.filter(ImageFilter.EMBOSS)
            elif variation_value == 'edge_enhance':
                return img.filter(ImageFilter.EDGE_ENHANCE)
                
        elif variation_type == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(variation_value)
            
        elif variation_type == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(variation_value)
            
        return img
        
    def apply_sepia_filter(self, img):
        """Apply sepia filter to image"""
        img_array = np.array(img)
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        sepia_img = np.dot(img_array, sepia_matrix.T)
        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
        return Image.fromarray(sepia_img)
        
    def generate_filename(self, original_name, variation_type, variation_value, index):
        """Generate filename for processed image"""
        pattern = self.naming_pattern.get()
        
        # Replace placeholders
        filename = pattern.replace("{original}", original_name)
        filename = filename.replace("{variation}", f"{variation_type}_{variation_value}")
        filename = filename.replace("{index}", str(index))
        
        # Add extension
        extension = self.output_format.get().lower()
        if extension == "jpeg":
            extension = "jpg"
        filename += f".{extension}"
        
        return filename
        
    def show_error(self, message):
        """Show error message"""
        error_window = ctk.CTkToplevel(self.batch_window)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        
        error_label = ctk.CTkLabel(error_window, text=message, font=("Arial", 12))
        error_label.pack(expand=True)
        
        ok_btn = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        ok_btn.pack(pady=10)

    def load_image_directly(self):
        """Load an image directly from the batch menu"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Image for Batch Processing",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Add image to editor
            self.editor.add_image(file_path)
            
            # Now select it as source
            self.select_source_image()
            
            # Show success message
            filename = os.path.basename(file_path)
            self.show_info(f"Image '{filename}' loaded and selected for batch processing")
        else:
            print("DEBUG: No file selected in load_image_directly")
    
    def open_output_folder(self, folder_path):
        """Open the output folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # macOS and Linux
                import subprocess
                subprocess.run(['open', folder_path])  # macOS
            else:  # Linux
                import subprocess
                subprocess.run(['xdg-open', folder_path])
        except Exception as e:
            self.show_error(f"Could not open folder: {e}\n\nPlease navigate to:\n{folder_path}")
    
    def show_info(self, message):
        """Show info message"""
        info_window = ctk.CTkToplevel(self.batch_window)
        info_window.title("Information")
        info_window.geometry("400x200")
        info_window.resizable(False, False)
        
        info_label = ctk.CTkLabel(info_window, text=message, font=("Arial", 12))
        info_label.pack(expand=True)
        
        ok_btn = ctk.CTkButton(info_window, text="OK", command=info_window.destroy)
        ok_btn.pack(pady=10)

    def select_source_image_by_index(self, idx):
        """Ustaw wybrane zdjęcie jako źródłowe do batcha po kliknięciu miniatury"""
        self.source_image = self.editor.images[idx]
        self.source_image_index = idx
        filename = os.path.basename(self.source_image['path'])
        self.source_info.configure(text=f"Selected: {filename}")
        # Zaznacz w głównym edytorze
        self.editor.selected_image_index = idx
        self.editor.selected_image = self.editor.images[idx]
        self.editor.update_canvas()
        self.editor.update_image_info()
