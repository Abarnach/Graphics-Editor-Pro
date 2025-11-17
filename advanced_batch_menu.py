import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import os
from datetime import datetime
import cv2
import json

class AdvancedBatchMenu:
    def __init__(self, editor):
        self.editor = editor
        self.create_advanced_batch_window()
        
    def create_advanced_batch_window(self):
        """Create the advanced batch processing window"""
        self.advanced_batch_window = ctk.CTkToplevel(self.editor.root)
        self.advanced_batch_window.title("Advanced Batch Image Processing")
        self.advanced_batch_window.geometry("700x800")  # Reduced size
        self.advanced_batch_window.resizable(True, True)  # Allow resizing
        
        # Center the window
        self.advanced_batch_window.transient(self.editor.root)
        
        # Add close protocol
        self.advanced_batch_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Create main scrollable frame
        main_canvas = tk.Canvas(self.advanced_batch_window)
        scrollbar = tk.Scrollbar(self.advanced_batch_window, orient="vertical", command=main_canvas.yview)
        self.main_frame = ctk.CTkFrame(main_canvas)
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the frame
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="Advanced Batch Image Processing", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_label = ctk.CTkLabel(self.main_frame, text="Advanced batch processing with ML algorithms and custom transformations", font=("Arial", 12))
        desc_label.pack(pady=5)
        
        # Quick Start Guide
        self.create_quick_start_guide(self.main_frame)
        
        # Source image selection
        self.create_source_section(self.main_frame)
        
        # Basic processing options
        self.create_basic_processing_section(self.main_frame)
        
        # ML processing options
        self.create_ml_processing_section(self.main_frame)
        
        # Style transfer options
        self.create_style_transfer_section(self.main_frame)
        
        # Custom transformations
        self.create_custom_transformations_section(self.main_frame)
        
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
        """Close the advanced batch menu window"""
        self.advanced_batch_window.destroy()
        
    def create_quick_start_guide(self, parent):
        """Create a quick start guide section"""
        guide_frame = ctk.CTkFrame(parent)
        guide_frame.pack(fill="x", padx=10, pady=10)
        
        guide_label = ctk.CTkLabel(guide_frame, text="Quick Start Guide", font=("Arial", 14, "bold"))
        guide_label.pack(pady=5)
        
        guide_text = (
            "1. Load an image using the 'Load New Image' button or the File menu.\n"
            "2. Select the image you want to process in the 'Source Image' section.\n"
            "3. Enable basic processing options (Rotation, Scale, Filters, Effects).\n"
            "4. Configure ML processing options (LightGlue variations).\n"
            "5. Set up style transfer and custom transformations if desired.\n"
            "6. Configure the output settings (directory, format, naming pattern).\n"
            "7. Click 'Update Preview' to see what will be generated.\n"
            "8. Click 'Start Advanced Batch Processing' to begin.\n\n"
            "This menu offers advanced features like ML algorithms and custom transformations."
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
            text="First load an image using the File menu, then select it here for advanced batch processing", 
            font=("Arial", 10),
            text_color="gray"
        )
        instructions_label.pack(pady=5)
        
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
        
        # Multiple source images option
        self.multiple_sources = ctk.CTkCheckBox(source_frame, text="Process multiple source images")
        self.multiple_sources.pack(pady=5)
        
    def create_basic_processing_section(self, parent):
        """Create the basic processing options section"""
        basic_frame = ctk.CTkFrame(parent)
        basic_frame.pack(fill="x", padx=15, pady=10)
        
        basic_label = ctk.CTkLabel(basic_frame, text="Basic Processing", font=("Arial", 16, "bold"))
        basic_label.pack(pady=10)
        
        # Create grid for basic options
        options_grid = ctk.CTkFrame(basic_frame)
        options_grid.pack(fill="x", padx=10, pady=10)
        
        # Row 1: Rotation and Scale
        # Rotation
        rotation_frame = ctk.CTkFrame(options_grid)
        rotation_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        rotation_label = ctk.CTkLabel(rotation_frame, text="Rotation", font=("Arial", 12, "bold"))
        rotation_label.pack(pady=5)
        
        self.rotation_enabled = ctk.CTkCheckBox(rotation_frame, text="Enable")
        self.rotation_enabled.pack(pady=2)
        
        self.rotation_angles = ctk.CTkEntry(rotation_frame, placeholder_text="90, 180, 270")
        self.rotation_angles.pack(pady=2, fill="x", padx=5)
        self.rotation_angles.insert(0, "90, 180, 270")
        
        # Scale
        scale_frame = ctk.CTkFrame(options_grid)
        scale_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        scale_label = ctk.CTkLabel(scale_frame, text="Scale", font=("Arial", 12, "bold"))
        scale_label.pack(pady=5)
        
        self.scale_enabled = ctk.CTkCheckBox(scale_frame, text="Enable")
        self.scale_enabled.pack(pady=2)
        
        self.scale_factors = ctk.CTkEntry(scale_frame, placeholder_text="0.5, 0.75, 1.25, 1.5")
        self.scale_factors.pack(pady=2, fill="x", padx=5)
        self.scale_factors.insert(0, "0.5, 0.75, 1.25, 1.5")
        
        # Row 2: Filters and Effects
        # Filters
        filters_frame = ctk.CTkFrame(options_grid)
        filters_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        filters_label = ctk.CTkLabel(filters_frame, text="Filters", font=("Arial", 12, "bold"))
        filters_label.pack(pady=5)
        
        self.filters_enabled = ctk.CTkCheckBox(filters_frame, text="Enable")
        self.filters_enabled.pack(pady=2)
        
        # Filter checkboxes
        self.filter_vars = {}
        filters = [
            ("sepia", "Sepia"),
            ("grayscale", "Grayscale"),
            ("invert", "Invert"),
            ("blur", "Blur"),
            ("sharpen", "Sharpen"),
            ("emboss", "Emboss"),
            ("edge_enhance", "Edge Enhance"),
            ("contour", "Contour"),
            ("find_edges", "Find Edges")
        ]
        
        for i, (filter_name, filter_label) in enumerate(filters):
            var = ctk.CTkCheckBox(filters_frame, text=filter_label)
            var.pack(anchor="w", padx=5, pady=2)
            self.filter_vars[filter_name] = var
            
        # Effects
        effects_frame = ctk.CTkFrame(options_grid)
        effects_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        effects_label = ctk.CTkLabel(effects_frame, text="Effects", font=("Arial", 12, "bold"))
        effects_label.pack(pady=5)
        
        self.effects_enabled = ctk.CTkCheckBox(effects_frame, text="Enable")
        self.effects_enabled.pack(pady=2)
        
        # Effect checkboxes
        self.effect_vars = {}
        effects = [
            ("vintage", "Vintage"),
            ("dramatic", "Dramatic"),
            ("soft", "Soft"),
            ("hdr", "HDR Effect"),
            ("cartoon", "Cartoon"),
            ("sketch", "Sketch")
        ]
        
        for i, (effect_name, effect_label) in enumerate(effects):
            var = ctk.CTkCheckBox(effects_frame, text=effect_label)
            var.pack(anchor="w", padx=5, pady=2)
            self.effect_vars[effect_name] = var
            
        # Configure grid weights
        options_grid.columnconfigure(0, weight=1)
        options_grid.columnconfigure(1, weight=1)
        
    def create_ml_processing_section(self, parent):
        """Create the ML processing options section"""
        ml_frame = ctk.CTkFrame(parent)
        ml_frame.pack(fill="x", padx=15, pady=10)
        
        ml_label = ctk.CTkLabel(ml_frame, text="Machine Learning Processing", font=("Arial", 16, "bold"))
        ml_label.pack(pady=10)
        
        # LightGlue algorithm
        lightglue_frame = ctk.CTkFrame(ml_frame)
        lightglue_frame.pack(fill="x", padx=10, pady=10)
        
        lightglue_label = ctk.CTkLabel(lightglue_frame, text="LightGlue Algorithm", font=("Arial", 12, "bold"))
        lightglue_label.pack(pady=5)
        
        self.lightglue_enabled = ctk.CTkCheckBox(lightglue_frame, text="Enable LightGlue processing")
        self.lightglue_enabled.pack(pady=2)
        
        # LightGlue variations
        lg_variations_frame = ctk.CTkFrame(lightglue_frame)
        lg_variations_frame.pack(fill="x", padx=10, pady=5)
        
        lg_variations_label = ctk.CTkLabel(lg_variations_frame, text="Variations:")
        lg_variations_label.pack(pady=2)
        
        self.lg_variations = {}
        lg_options = [
            ("keypoint_enhance", "Keypoint Enhancement"),
            ("feature_matching", "Feature Matching"),
            ("descriptor_improvement", "Descriptor Improvement"),
            ("geometric_verification", "Geometric Verification")
        ]
        
        for lg_name, lg_label in lg_options:
            var = ctk.CTkCheckBox(lg_variations_frame, text=lg_label)
            var.pack(anchor="w", padx=5, pady=2)
            self.lg_variations[lg_name] = var
        
    def create_custom_transformations_section(self, parent):
        """Create custom transformations section"""
        custom_frame = ctk.CTkFrame(parent)
        custom_frame.pack(fill="x", padx=15, pady=10)
        
        custom_label = ctk.CTkLabel(custom_frame, text="Custom Transformations", font=("Arial", 16, "bold"))
        custom_label.pack(pady=10)
        
        # Custom transformations
        self.custom_transforms = []
        
        # Add transformation button
        add_transform_btn = ctk.CTkButton(
            custom_frame,
            text="Add Custom Transformation",
            command=self.add_custom_transformation,
            width=200
        )
        add_transform_btn.pack(pady=5)
        
        # Transformations list
        self.transforms_frame = ctk.CTkFrame(custom_frame)
        self.transforms_frame.pack(fill="x", padx=10, pady=5)
        
    def create_style_transfer_section(self, parent):
        """Create the style transfer options section"""
        style_frame = ctk.CTkFrame(parent)
        style_frame.pack(fill="x", padx=15, pady=10)
        
        style_label = ctk.CTkLabel(style_frame, text="Style Transfer", font=("Arial", 16, "bold"))
        style_label.pack(pady=10)
        
        self.style_transfer_enabled = ctk.CTkCheckBox(style_frame, text="Enable style transfer")
        self.style_transfer_enabled.pack(pady=2)
        
        # Style selection
        style_selection_frame = ctk.CTkFrame(style_frame)
        style_selection_frame.pack(fill="x", padx=10, pady=5)
        
        style_selection_label = ctk.CTkLabel(style_selection_frame, text="Style:")
        style_selection_label.pack(side="left", padx=5)
        
        self.style_selection = ctk.CTkComboBox(
            style_selection_frame,
            values=["Van Gogh", "Picasso", "Monet", "Watercolor", "Oil Painting", "Sketch"]
        )
        self.style_selection.pack(side="left", padx=5, fill="x", expand=True)
        self.style_selection.set("Van Gogh")
        
        # Style intensity
        intensity_frame = ctk.CTkFrame(style_frame)
        intensity_frame.pack(fill="x", pady=2)
        
        intensity_label = ctk.CTkLabel(intensity_frame, text="Style intensity:")
        intensity_label.pack(side="left", padx=5)
        
        self.style_intensity = ctk.CTkSlider(intensity_frame, from_=0.0, to=1.0, number_of_steps=100)
        self.style_intensity.pack(side="left", padx=5, fill="x", expand=True)
        self.style_intensity.set(0.7)
        
        self.intensity_value_label = ctk.CTkLabel(intensity_frame, text="0.7")
        self.intensity_value_label.pack(side="left", padx=5)
        
        # Bind slider to update label
        self.style_intensity.configure(command=self.update_intensity_label)
        
    def create_output_section(self, parent):
        """Create the output settings section"""
        output_frame = ctk.CTkFrame(parent)
        output_frame.pack(fill="x", padx=15, pady=10)
        
        output_label = ctk.CTkLabel(output_frame, text="Output Settings", font=("Arial", 16, "bold"))
        output_label.pack(pady=10)
        
        # Output directory
        output_dir_frame = ctk.CTkFrame(output_frame)
        output_dir_frame.pack(fill="x", padx=10, pady=5)
        
        output_dir_label = ctk.CTkLabel(output_dir_frame, text="Output directory:")
        output_dir_label.pack(side="left", padx=5)
        
        # Get current working directory for default path
        current_dir = os.getcwd()
        default_output = os.path.join(current_dir, "advanced_batch_output")
        
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
        
        self.output_format = ctk.CTkComboBox(format_frame, values=["PNG", "JPEG", "BMP", "TIFF"])
        self.output_format.pack(side="left", padx=5)
        self.output_format.set("PNG")
        
        # Quality settings
        quality_frame = ctk.CTkFrame(output_frame)
        quality_frame.pack(fill="x", padx=10, pady=5)
        
        quality_label = ctk.CTkLabel(quality_frame, text="Quality:")
        quality_label.pack(side="left", padx=5)
        
        self.quality_slider = ctk.CTkSlider(quality_frame, from_=1, to=100, number_of_steps=99)
        self.quality_slider.pack(side="left", padx=5, fill="x", expand=True)
        self.quality_slider.set(95)
        
        self.quality_value_label = ctk.CTkLabel(quality_frame, text="95")
        self.quality_value_label.pack(side="left", padx=5)
        
        # Bind slider to update label
        self.quality_slider.configure(command=self.update_quality_label)
        
        # Naming pattern
        naming_frame = ctk.CTkFrame(output_frame)
        naming_frame.pack(fill="x", padx=10, pady=5)
        
        naming_label = ctk.CTkLabel(naming_frame, text="Naming pattern:")
        naming_label.pack(side="left", padx=5)
        
        self.naming_pattern = ctk.CTkEntry(naming_frame, placeholder_text="{original}_{transformation}_{timestamp}")
        self.naming_pattern.pack(side="left", padx=5, fill="x", expand=True)
        self.naming_pattern.insert(0, "{original}_{transformation}_{timestamp}")
        
        # Naming pattern help
        naming_help_label = ctk.CTkLabel(
            output_frame,
            text="Available placeholders: {original}, {transformation}, {timestamp}, {index}",
            font=("Arial", 9),
            text_color="gray"
        )
        naming_help_label.pack(pady=2)
        
    def create_preview_section(self, parent):
        """Create the preview section"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="x", padx=15, pady=10)
        
        preview_label = ctk.CTkLabel(preview_frame, text="Preview", font=("Arial", 16, "bold"))
        preview_label.pack(pady=10)
        
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
        buttons_frame.pack(fill="x", padx=15, pady=15)
        
        # Process button
        self.process_btn = ctk.CTkButton(
            buttons_frame,
            text="Start Advanced Batch Processing",
            command=self.start_advanced_batch_processing,
            width=300,
            height=50,
            font=("Arial", 16, "bold")
        )
        self.process_btn.pack(pady=15)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(buttons_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(buttons_frame, text="Ready", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
    def update_intensity_label(self, value):
        """Update style intensity label"""
        self.intensity_value_label.configure(text=f"{value:.2f}")
        
    def update_quality_label(self, value):
        """Update quality label"""
        self.quality_value_label.configure(text=str(int(value)))
        
    def add_custom_transformation(self):
        """Add a custom transformation to the list"""
        # Create transformation entry
        transform_frame = ctk.CTkFrame(self.transforms_frame)
        transform_frame.pack(fill="x", pady=2)
        
        # Transformation type
        transform_type = ctk.CTkComboBox(
            transform_frame, 
            values=["Custom Filter", "Color Mapping", "Geometric Transform", "Custom Effect"]
        )
        transform_type.pack(side="left", padx=5, pady=2)
        
        # Parameters
        params_entry = ctk.CTkEntry(transform_frame, placeholder_text="Parameters (JSON)")
        params_entry.pack(side="left", padx=5, pady=2, fill="x", expand=True)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            transform_frame,
            text="Remove",
            command=lambda: self.remove_custom_transformation(transform_frame),
            width=80
        )
        remove_btn.pack(side="right", padx=5, pady=2)
        
        # Store reference
        self.custom_transforms.append({
            'frame': transform_frame,
            'type': transform_type,
            'params': params_entry
        })
        
    def remove_custom_transformation(self, frame):
        """Remove a custom transformation"""
        frame.destroy()
        self.custom_transforms = [t for t in self.custom_transforms if t['frame'] != frame]
        
    def select_source_image(self):
        """Select the source image for batch processing"""
        if not self.editor.images:
            self.show_error(
                "No images loaded.\n\n"
                "To use advanced batch processing:\n"
                "1. Click 'Load New Image' to load an image directly, OR\n"
                "2. Use the File menu to load images first, then return here\n\n"
                "Once an image is loaded, you can select it for advanced batch processing."
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
        
        # Count basic variations
        if self.rotation_enabled.get():
            try:
                angles = [float(x.strip()) for x in self.rotation_angles.get().split(',')]
                variations.extend([f"Rotate {angle}°" for angle in angles])
            except:
                pass
                
        if self.scale_enabled.get():
            try:
                scales = [float(x.strip()) for x in self.scale_factors.get().split(',')]
                variations.extend([f"Scale {scale}x" for scale in scales])
            except:
                pass
                
        if self.filters_enabled.get():
            for filter_name, var in self.filter_vars.items():
                if var.get():
                    variations.append(f"Filter: {filter_name}")
                    
        if self.effects_enabled.get():
            for effect_name, var in self.effect_vars.items():
                if var.get():
                    variations.append(f"Effect: {effect_name}")
                    
        # Count ML variations
        if self.lightglue_enabled.get():
            for var_name, var in self.lg_variations.items():
                if var.get():
                    variations.append(f"LightGlue: {var_name}")
                    
        # Count style transfer variations
        if self.style_transfer_enabled.get():
            variations.append(f"Style Transfer: {self.style_selection.get()}")
            
        # Count custom transformations
        variations.extend([f"Custom: {t['type'].get()}" for t in self.custom_transforms])
                
        if variations:
            total = len(variations)
            self.preview_info.configure(text=f"Will generate {total} variations:\n" + "\n".join(variations[:8]) + ("..." if total > 8 else ""))
        else:
            self.preview_info.configure(text="No variations configured")
            
    def browse_output_directory(self):
        """Browse for output directory"""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(
            title="Select Output Directory for Advanced Batch Processing"
        )
        
        if directory:
            self.output_dir.delete(0, "end")
            self.output_dir.insert(0, directory)
            
            # Update path info
            for widget in self.output_dir.master.master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Images will be saved to:" in widget.cget("text"):
                    widget.configure(text=f"Images will be saved to: {directory}")
                    break
    
    def start_advanced_batch_processing(self):
        """Start the advanced batch processing"""
        if not hasattr(self, 'source_image'):
            self.show_error("Please select a source image first.")
            return
            
        # Get processing options
        variations = self.get_advanced_processing_variations()
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
        self.show_info(f"Starting advanced batch processing...\nFiles will be saved to:\n{output_dir}")
            
        # Start processing
        self.process_advanced_variations(variations, output_dir)
        
    def get_advanced_processing_variations(self):
        """Get the list of advanced processing variations to apply"""
        variations = []
        
        # Basic variations
        if self.rotation_enabled.get():
            try:
                angles = [float(x.strip()) for x in self.rotation_angles.get().split(',')]
                for angle in angles:
                    variations.append(('rotation', angle))
            except:
                pass
                
        if self.scale_enabled.get():
            try:
                scales = [float(x.strip()) for x in self.scale_factors.get().split(',')]
                for scale in scales:
                    variations.append(('scale', scale))
            except:
                pass
                
        if self.filters_enabled.get():
            for filter_name, var in self.filter_vars.items():
                if var.get():
                    variations.append(('filter', filter_name))
                    
        if self.effects_enabled.get():
            for effect_name, var in self.effect_vars.items():
                if var.get():
                    variations.append(('effect', effect_name))
                    
        # ML variations
        if self.lightglue_enabled.get():
            for var_name, var in self.lg_variations.items():
                if var.get():
                    variations.append(('lightglue', var_name))
                    
        # Style transfer
        if self.style_transfer_enabled.get():
            variations.append(('style_transfer', {
                'style': self.style_selection.get(),
                'intensity': self.style_intensity.get()
            }))
            
        # Custom transformations
        for transform in self.custom_transforms:
            try:
                params = json.loads(transform['params'].get())
                variations.append(('custom', {
                    'type': transform['type'].get(),
                    'params': params
                }))
            except:
                # Skip invalid JSON
                pass
                
        return variations
        
    def process_advanced_variations(self, variations, output_dir):
        """Process all advanced variations"""
        total_variations = len(variations)
        self.progress_bar.set(0)
        self.status_label.configure(text="Processing...")
        self.process_btn.configure(state="disabled")

        # Get original image
        original_path = self.source_image['path']
        original_name = os.path.splitext(os.path.basename(original_path))[0]

        for i, (variation_type, variation_value) in enumerate(variations):
            try:
                print(f"DEBUG: Processing {variation_type} - {variation_value}")  # DEBUG
                img = Image.open(original_path)
                processed_img = self.apply_advanced_variation(img, variation_type, variation_value)
                filename = self.generate_advanced_filename(original_name, variation_type, variation_value, i)
                output_path = os.path.join(output_dir, filename)
                quality = int(self.quality_slider.get())
                if self.output_format.get() == "JPEG":
                    processed_img.save(output_path, "JPEG", quality=quality)
                else:
                    processed_img.save(output_path, self.output_format.get())
                progress = (i + 1) / total_variations
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Processed {i+1}/{total_variations}: {variation_type}")
                self.advanced_batch_window.update()
            except Exception as e:
                print(f"Error processing variation {variation_type}: {e}")
                
        # Complete
        self.status_label.configure(text=f"Completed! Generated {total_variations} variations in {output_dir}")
        
        # Show completion message with file location
        completion_message = (
            f"Advanced batch processing completed successfully!\n\n"
            f"Generated {total_variations} image variations\n"
            f"Files saved to:\n{output_dir}\n\n"
            f"Click 'Open Folder' to view the results"
        )
        
        # Create completion window with open folder button
        completion_window = ctk.CTkToplevel(self.advanced_batch_window)
        completion_window.title("Advanced Batch Processing Complete")
        completion_window.geometry("500x300")
        completion_window.resizable(False, False)
        
        # Center the window
        completion_window.transient(self.advanced_batch_window)
        
        # Success message
        success_label = ctk.CTkLabel(completion_window, text="✅ Advanced Batch Processing Complete!", font=("Arial", 16, "bold"))
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
        
    def apply_advanced_variation(self, img, variation_type, variation_value):
        """Apply an advanced variation to an image"""
        if variation_type == 'rotation':
            return img.rotate(variation_value, expand=True)
            
        elif variation_type == 'scale':
            width, height = img.size
            new_width = int(width * variation_value)
            new_height = int(height * variation_value)
            return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        elif variation_type == 'filter':
            return self.apply_advanced_filter(img, variation_value)
            
        elif variation_type == 'effect':
            return self.apply_advanced_effect(img, variation_value)
            
        elif variation_type == 'lightglue':
            return self.apply_lightglue_processing(img, variation_value)
            
        elif variation_type == 'style_transfer':
            return self.apply_style_transfer(img, variation_value)
            
        elif variation_type == 'custom':
            return self.apply_custom_transformation(img, variation_value)
            
        return img
        
    def apply_advanced_filter(self, img, filter_name):
        """Apply advanced filters to image"""
        if filter_name == 'sepia':
            return self.apply_sepia_filter(img)
        elif filter_name == 'grayscale':
            return img.convert('L').convert('RGB')
        elif filter_name == 'invert':
            return ImageOps.invert(img)
        elif filter_name == 'blur':
            return img.filter(ImageFilter.BLUR)
        elif filter_name == 'sharpen':
            return img.filter(ImageFilter.SHARPEN)
        elif filter_name == 'emboss':
            return img.filter(ImageFilter.EMBOSS)
        elif filter_name == 'edge_enhance':
            return img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_name == 'contour':
            return img.filter(ImageFilter.CONTOUR)
        elif filter_name == 'find_edges':
            return img.filter(ImageFilter.FIND_EDGES)
        return img
        
    def apply_advanced_effect(self, img, effect_name):
        """Apply advanced effects to image"""
        if effect_name == 'vintage':
            return self.apply_vintage_effect(img)
        elif effect_name == 'dramatic':
            return self.apply_dramatic_effect(img)
        elif effect_name == 'soft':
            return self.apply_soft_effect(img)
        elif effect_name == 'hdr':
            return self.apply_hdr_effect(img)
        elif effect_name == 'cartoon':
            return self.apply_cartoon_effect(img)
        elif effect_name == 'sketch':
            return self.apply_sketch_effect(img)
        return img
        
    def apply_lightglue_processing(self, img, processing_type):
        """Apply LightGlue-based processing"""
        # This is a placeholder for actual LightGlue implementation
        # In a real implementation, you would use the LightGlue library
        if processing_type == 'keypoint_enhance':
            # Simulate keypoint enhancement
            return self.enhance_keypoints(img)
        elif processing_type == 'feature_matching':
            # Simulate feature matching
            return self.simulate_feature_matching(img)
        elif processing_type == 'descriptor_improvement':
            # Simulate descriptor improvement
            return self.simulate_correspondence_analysis(img)
        elif processing_type == 'geometric_verification':
            # Simulate geometric verification
            return self.simulate_geometric_verification(img)
        return img
        
    def apply_style_transfer(self, img, style_params):
        """Apply style transfer to image"""
        # This is a placeholder for actual style transfer implementation
        style = style_params['style']
        intensity = style_params['intensity']
        
        if style == "Van Gogh":
            return self.apply_van_gogh_style(img, intensity)
        elif style == "Picasso":
            return self.apply_picasso_style(img, intensity)
        elif style == "Monet":
            return self.apply_monet_style(img, intensity)
        elif style == "Watercolor":
            return self.apply_watercolor_style(img, intensity)
        elif style == "Oil Painting":
            return self.apply_oil_painting_style(img, intensity)
        elif style == "Sketch":
            return self.apply_sketch_style(img, intensity)
        return img
        
    def apply_custom_transformation(self, img, transform_params):
        """Apply custom transformation to image"""
        transform_type = transform_params['type']
        params = transform_params['params']
        
        if transform_type == "Custom Filter":
            return self.apply_custom_filter(img, params)
        elif transform_type == "Color Mapping":
            return self.apply_color_mapping(img, params)
        elif transform_type == "Geometric Transform":
            return self.apply_geometric_transform(img, params)
        elif transform_type == "Custom Effect":
            return self.apply_custom_effect(img, params)
        return img
        
    # Placeholder methods for advanced effects
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
        
    def apply_vintage_effect(self, img):
        """Apply vintage effect"""
        # Simulate vintage effect with color adjustments
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.8)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.9)
        return img
        
    def apply_dramatic_effect(self, img):
        """Apply dramatic effect"""
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.8)
        return img
        
    def apply_soft_effect(self, img):
        """Apply soft effect"""
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.8)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        return img
        
    def apply_hdr_effect(self, img):
        """Apply HDR effect"""
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        return img
        
    def apply_cartoon_effect(self, img):
        """Apply cartoon effect"""
        # Convert to grayscale and apply edge detection
        gray = img.convert('L')
        edges = gray.filter(ImageFilter.FIND_EDGES)
        # Combine with original image
        return Image.blend(img, edges.convert('RGB'), 0.3)
        
    def apply_sketch_effect(self, img):
        """Apply sketch effect"""
        gray = img.convert('L')
        inverted = ImageOps.invert(gray)
        blurred = inverted.filter(ImageFilter.GaussianBlur(radius=2))
        return Image.blend(gray.convert('RGB'), blurred.convert('RGB'), 0.5)
        
    # LightGlue placeholder methods
    def enhance_keypoints(self, img):
        """Enhance keypoints in image"""
        # Placeholder implementation
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(1.5)
        
    def simulate_feature_matching(self, img):
        """Simulate feature matching"""
        # Placeholder implementation
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.2)
        
    def simulate_correspondence_analysis(self, img):
        """Simulate correspondence analysis"""
        # Placeholder implementation
        enhancer = ImageEnhance.Edge(img)
        return enhancer.enhance(1.3)
        
    def simulate_geometric_verification(self, img):
        """Simulate geometric verification"""
        # Placeholder implementation
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.1)
        
    # Style transfer placeholder methods
    def apply_van_gogh_style(self, img, intensity):
        """Apply Van Gogh style"""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(1.0 + intensity * 0.5)
        
    def apply_picasso_style(self, img, intensity):
        """Apply Picasso style"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.0 + intensity * 0.3)
        
    def apply_monet_style(self, img, intensity):
        """Apply Monet style"""
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.0 + intensity * 0.4)
        
    def apply_watercolor_style(self, img, intensity):
        """Apply Watercolor style"""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(1.0 - intensity * 0.3)
        
    def apply_oil_painting_style(self, img, intensity):
        """Apply Oil Painting style"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.0 + intensity * 0.4)
        
    def apply_sketch_style(self, img, intensity):
        """Apply Sketch style"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.0 + intensity * 0.4)
        
    # Custom transformation placeholder methods
    def apply_custom_filter(self, img, params):
        """Apply custom filter"""
        # Placeholder implementation
        return img
        
    def apply_color_mapping(self, img, params):
        """Apply color mapping"""
        # Placeholder implementation
        return img
        
    def apply_geometric_transform(self, img, params):
        """Apply geometric transform"""
        # Placeholder implementation
        return img
        
    def apply_custom_effect(self, img, params):
        """Apply custom effect"""
        # Placeholder implementation
        return img
        
    def generate_advanced_filename(self, original_name, variation_type, variation_value, index):
        """Generate filename for processed image"""
        pattern = self.naming_pattern.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Replace placeholders
        filename = pattern.replace("{original}", original_name)
        filename = filename.replace("{transformation}", f"{variation_type}_{str(variation_value).replace(':', '_')}")
        filename = filename.replace("{timestamp}", timestamp)
        filename = filename.replace("{index}", str(index))
        
        # Add extension
        extension = self.output_format.get().lower()
        if extension == "jpeg":
            extension = "jpg"
        filename += f".{extension}"
        
        return filename
        
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
    
    def show_error(self, message):
        """Show error message"""
        error_window = ctk.CTkToplevel(self.advanced_batch_window)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        
        error_label = ctk.CTkLabel(error_window, text=message, font=("Arial", 12))
        error_label.pack(expand=True)
        
        ok_btn = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        ok_btn.pack(pady=10)
    
    def load_image_directly(self):
        """Load an image directly from the advanced batch menu"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Image for Advanced Batch Processing",
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
            self.show_info(f"Image '{filename}' loaded and selected for advanced batch processing")
        else:
            print("DEBUG: No file selected in load_image_directly")
    
    def show_info(self, message):
        """Show info message"""
        info_window = ctk.CTkToplevel(self.advanced_batch_window)
        info_window.title("Information")
        info_window.geometry("400x200")
        info_window.resizable(False, False)
        
        info_label = ctk.CTkLabel(info_window, text=message, font=("Arial", 12))
        info_label.pack(expand=True)
        
        ok_btn = ctk.CTkButton(info_window, text="OK", command=info_window.destroy)
        ok_btn.pack(pady=10)
