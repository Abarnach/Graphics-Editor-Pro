import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import math

class DrawMenu:
    def __init__(self, editor):
        self.editor = editor
        self.is_drawing_mode_active = False
        self.is_drawing_active = False
        self.is_erasing = False
        self.is_drawing_shapes = False
        self.current_shape = None
        self.drawing_points = []
        self.drawing_elements = []
        
        # Initialize colors and style
        self.line_color = "black"
        self.fill_color = "white"
        self.line_width = 2
        self.line_style = "solid"  # solid, dashed, dotted, dashdot
        
        self.create_draw_window()
        
    def create_draw_window(self):
        """Create the drawing tools window"""
        self.draw_window = ctk.CTkToplevel(self.editor.root)
        self.draw_window.title("Drawing Tools")
        self.draw_window.geometry("400x700")
        self.draw_window.resizable(False, False)
        
        # Center the window
        self.draw_window.transient(self.editor.root)
        
        # Add close protocol
        self.draw_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.draw_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="🎨 Drawing Tools", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Drawing Tools Section
        self.create_drawing_tools_section(main_frame)
        
        # Shape Tools Section
        self.create_shape_tools_section(main_frame)
        
        # Color Section
        self.create_color_section(main_frame)
        

        
        # Eraser Section
        self.create_eraser_section(main_frame)
        
        # Clear Section
        self.create_clear_section(main_frame)
        
        # Deactivate Section  
        self.create_deactivate_section(main_frame)
    
    def close_window(self):
        """Close the draw menu window"""
        if self.is_drawing_mode_active:
            self.stop_drawing_mode()
        self.draw_window.destroy()
        
    def create_drawing_tools_section(self, parent):
        """Create the drawing tools section"""
        tools_frame = ctk.CTkFrame(parent)
        tools_frame.pack(fill="x", padx=10, pady=10)
        
        tools_label = ctk.CTkLabel(tools_frame, text="Drawing Tools", font=("Arial", 14, "bold"))
        tools_label.pack(pady=5)
        
        # Start/Stop Draw Control
        control_frame = ctk.CTkFrame(tools_frame)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_draw_btn = ctk.CTkButton(
            control_frame,
            text="🎨 START DRAWING",
            command=self.start_drawing_mode,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_draw_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.stop_draw_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ STOP DRAWING",
            command=self.stop_drawing_mode,
            fg_color="red",
            hover_color="darkred"
        )
        self.stop_draw_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.stop_draw_btn.configure(state="disabled")
        
        # Drawing mode buttons
        drawing_frame = ctk.CTkFrame(tools_frame)
        drawing_frame.pack(fill="x", padx=10, pady=5)
        
        self.freehand_btn = ctk.CTkButton(
            drawing_frame, 
            text="✏️ Freehand", 
            command=self.activate_freehand_drawing,
            state="disabled"
        )
        self.freehand_btn.pack(fill="x", pady=2)
        
    def create_shape_tools_section(self, parent):
        """Create the line styles and width section"""
        shapes_frame = ctk.CTkFrame(parent)
        shapes_frame.pack(fill="x", padx=10, pady=10)
        
        shapes_label = ctk.CTkLabel(shapes_frame, text="Line Styles & Width", font=("Arial", 14, "bold"))
        shapes_label.pack(pady=5)
        
        # Line width
        width_frame = ctk.CTkFrame(shapes_frame)
        width_frame.pack(fill="x", padx=10, pady=5)
        
        width_label = ctk.CTkLabel(width_frame, text="Line Width:", width=80)
        width_label.pack(side="left", padx=5)
        
        self.width_slider = ctk.CTkSlider(
            width_frame, 
            from_=1, 
            to=20, 
            number_of_steps=19,
            command=self.on_width_change
        )
        self.width_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.width_slider.set(2)
        
        self.width_value_label = ctk.CTkLabel(width_frame, text="2", width=30)
        self.width_value_label.pack(side="right", padx=5)
        
        # Line style buttons
        style_buttons_frame = ctk.CTkFrame(shapes_frame)
        style_buttons_frame.pack(fill="x", padx=10, pady=5)
        
        self.solid_btn = ctk.CTkButton(
            style_buttons_frame,
            text="━━━ Solid",
            command=lambda: self.set_line_style("solid"),
            width=80,
            height=35,
            fg_color="green"
        )
        self.solid_btn.pack(side="left", padx=5, pady=2)
        
        self.dashed_btn = ctk.CTkButton(
            style_buttons_frame,
            text="┅┅┅ Dashed",
            command=lambda: self.set_line_style("dashed"),
            width=80,
            height=35
        )
        self.dashed_btn.pack(side="left", padx=5, pady=2)
        
        self.dotted_btn = ctk.CTkButton(
            style_buttons_frame,
            text="┄┄┄ Dotted",
            command=lambda: self.set_line_style("dotted"),
            width=80,
            height=35
        )
        self.dotted_btn.pack(side="left", padx=5, pady=2)
        
        self.dashdot_btn = ctk.CTkButton(
            style_buttons_frame,
            text="┅┄┅ Dashdot",
            command=lambda: self.set_line_style("dashdot"),
            width=80,
            height=35
        )
        self.dashdot_btn.pack(side="left", padx=5, pady=2)
        
    def create_color_section(self, parent):
        """Create the color section"""
        color_frame = ctk.CTkFrame(parent)
        color_frame.pack(fill="x", padx=10, pady=10)
        
        color_label = ctk.CTkLabel(color_frame, text="🎨 Colors", font=("Arial", 14, "bold"))
        color_label.pack(pady=5)
        
        # Current color display
        current_color_frame = ctk.CTkFrame(color_frame)
        current_color_frame.pack(fill="x", padx=10, pady=5)
        
        current_color_label = ctk.CTkLabel(current_color_frame, text="Current Color:", width=80)
        current_color_label.pack(side="left", padx=5)
        
        self.current_color_display = tk.Frame(current_color_frame, bg="black", width=60, height=30)
        self.current_color_display.pack(side="right", padx=5)
        
        # Professional color picker button
        ctk.CTkButton(color_frame, text="🎨 OPEN COLOR PICKER", command=self.open_professional_color_picker, fg_color="purple", height=40).pack(fill="x", padx=10, pady=5)
        
        # Quick preset colors
        presets_label = ctk.CTkLabel(color_frame, text="Quick Colors:", font=("Arial", 12))
        presets_label.pack(pady=5)
        
        presets_frame = ctk.CTkFrame(color_frame)
        presets_frame.pack(fill="x", padx=10, pady=5)
        
        # Basic colors
        basic_colors = ["red", "green", "blue", "black", "white", "yellow", "orange", "purple", "brown", "pink", "cyan", "magenta"]
        for i, color in enumerate(basic_colors):
            btn = ctk.CTkButton(
                presets_frame, 
                text="", 
                command=lambda c=color: self.set_line_color(c), 
                width=25, 
                height=25, 
                fg_color=color,
                corner_radius=3
            )
            btn.pack(side="left", padx=1, pady=1)
        
        # Additional colors frame
        additional_colors_frame = ctk.CTkFrame(color_frame)
        additional_colors_frame.pack(fill="x", padx=10, pady=5)
        
        additional_label = ctk.CTkLabel(additional_colors_frame, text="More Colors:", font=("Arial", 12))
        additional_label.pack(pady=5)
        
        # Additional colors
        additional_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
            "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
            "#F8C471", "#82E0AA", "#F1948A", "#85C1E9", "#D7BDE2"
        ]
        
        for i, color in enumerate(additional_colors):
            btn = ctk.CTkButton(
                additional_colors_frame, 
                text="", 
                command=lambda c=color: self.set_line_color(c), 
                width=25, 
                height=25, 
                fg_color=color,
                corner_radius=3
            )
            btn.pack(side="left", padx=1, pady=1)
        

    def create_eraser_section(self, parent):
        """Create the eraser section"""
        eraser_frame = ctk.CTkFrame(parent)
        eraser_frame.pack(fill="x", padx=10, pady=10)
        
        eraser_label = ctk.CTkLabel(eraser_frame, text="Eraser", font=("Arial", 14, "bold"))
        eraser_label.pack(pady=5)
        
        # Eraser button
        self.eraser_btn = ctk.CTkButton(
            eraser_frame, 
            text="🧽 Activate Eraser", 
            command=self.activate_eraser,
            fg_color="red"
        )
        self.eraser_btn.pack(fill="x", padx=10, pady=2)
        
        # Eraser size
        eraser_size_frame = ctk.CTkFrame(eraser_frame)
        eraser_size_frame.pack(fill="x", padx=10, pady=5)
        
        eraser_size_label = ctk.CTkLabel(eraser_size_frame, text="Eraser Size:", width=80)
        eraser_size_label.pack(side="left", padx=5)
        
        self.eraser_size_slider = ctk.CTkSlider(
            eraser_size_frame, 
            from_=5, 
            to=50, 
            number_of_steps=45,
            command=self.on_eraser_size_change
        )
        self.eraser_size_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.eraser_size_slider.set(20)
        
        self.eraser_size_value_label = ctk.CTkLabel(eraser_size_frame, text="20", width=30)
        self.eraser_size_value_label.pack(side="right", padx=5)
        
    def create_clear_section(self, parent):
        """Create the clear section"""
        clear_frame = ctk.CTkFrame(parent)
        clear_frame.pack(fill="x", padx=10, pady=10)
        
        clear_label = ctk.CTkLabel(clear_frame, text="Clear", font=("Arial", 14, "bold"))
        clear_label.pack(pady=5)
        
        # Clear all drawings button
        clear_all_btn = ctk.CTkButton(
            clear_frame, 
            text="🗑️ Clear All Drawings", 
            command=self.clear_all_drawings,
            fg_color="orange"
        )
        clear_all_btn.pack(fill="x", padx=10, pady=2)
        
        # Clear last drawing button
        clear_last_btn = ctk.CTkButton(
            clear_frame, 
            text="↩️ Clear Last Drawing", 
            command=self.clear_last_drawing
        )
        clear_last_btn.pack(fill="x", padx=10, pady=2)
        
    def create_deactivate_section(self, parent):
        """Create the deactivate section"""
        deactivate_frame = ctk.CTkFrame(parent)
        deactivate_frame.pack(fill="x", padx=10, pady=10)
        
        deactivate_label = ctk.CTkLabel(deactivate_frame, text="Deactivate", font=("Arial", 14, "bold"))
        deactivate_label.pack(pady=5)
        
        # Deactivate all drawing tools button
        deactivate_all_btn = ctk.CTkButton(
            deactivate_frame, 
            text="🚫 Deactivate All Drawing Tools", 
            command=self.deactivate_all_modes,
            fg_color="gray"
        )
        deactivate_all_btn.pack(fill="x", padx=10, pady=2)
        
    # COLOR FUNCTIONS
    def set_line_color(self, color):
        """Set line color directly"""
        print(f"DEBUG: set_line_color called with {color}!")
        self.line_color = color
        self.current_color_display.configure(bg=color)
        self.editor.update_status(f"✅ Line color set to {color}")
        print(f"DEBUG: Line color set to: {self.line_color}")
        
    def set_line_style(self, style):
        """Set line style (solid, dashed, dotted, dashdot)"""
        print(f"DEBUG: set_line_style called with {style}!")
        self.line_style = style
        
        # Update button colors
        self.solid_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dashed_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dotted_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dashdot_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Highlight selected style
        if style == "solid":
            self.solid_btn.configure(fg_color="green")
        elif style == "dashed":
            self.dashed_btn.configure(fg_color="green")
        elif style == "dotted":
            self.dotted_btn.configure(fg_color="green")
        elif style == "dashdot":
            self.dashdot_btn.configure(fg_color="green")
            
        self.editor.update_status(f"✅ Line style set to {style}")
        print(f"DEBUG: Line style set to: {self.line_style}")
        
    def get_dash_pattern(self):
        """Get dash pattern for current line style"""
        if self.line_style == "solid":
            return None
        elif self.line_style == "dashed":
            return (10, 5)
        elif self.line_style == "dotted":
            return (2, 3)
        elif self.line_style == "dashdot":
            return (10, 3, 2, 3)
        else:
            return None
            
    def get_dash_pattern_from_style(self, style):
        """Get dash pattern for a specific line style"""
        if style == "solid":
            return None
        elif style == "dashed":
            return (10, 5)
        elif style == "dotted":
            return (2, 3)
        elif style == "dashdot":
            return (10, 3, 2, 3)
        else:
            return None
        
    def open_professional_color_picker(self):
        """Open professional color picker with RGB sliders"""
        print("DEBUG: Opening professional color picker!")
        
        # Create color picker window
        self.color_picker_window = ctk.CTkToplevel(self.editor.root)
        self.color_picker_window.title("Professional Color Picker")
        self.color_picker_window.geometry("400x500")
        self.color_picker_window.resizable(False, False)
        self.color_picker_window.transient(self.editor.root)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.color_picker_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="🎨 Professional Color Picker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Color preview
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="x", padx=10, pady=10)
        
        preview_label = ctk.CTkLabel(preview_frame, text="Color Preview:", width=80)
        preview_label.pack(side="left", padx=5)
        
        self.color_preview = tk.Frame(preview_frame, bg="black", width=100, height=50)
        self.color_preview.pack(side="right", padx=5)
        
        # RGB Sliders
        rgb_frame = ctk.CTkFrame(main_frame)
        rgb_frame.pack(fill="x", padx=10, pady=10)
        
        rgb_label = ctk.CTkLabel(rgb_frame, text="RGB Values:", font=("Arial", 12, "bold"))
        rgb_label.pack(pady=5)
        
        # Red slider
        red_frame = ctk.CTkFrame(rgb_frame)
        red_frame.pack(fill="x", padx=10, pady=5)
        
        red_label = ctk.CTkLabel(red_frame, text="🔴 Red:", width=50)
        red_label.pack(side="left", padx=5)
        
        self.red_slider = ctk.CTkSlider(
            red_frame, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_color_preview
        )
        self.red_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.red_slider.set(0)
        
        self.red_value = ctk.CTkLabel(red_frame, text="0", width=30)
        self.red_value.pack(side="right", padx=5)
        
        # Green slider
        green_frame = ctk.CTkFrame(rgb_frame)
        green_frame.pack(fill="x", padx=10, pady=5)
        
        green_label = ctk.CTkLabel(green_frame, text="🟢 Green:", width=50)
        green_label.pack(side="left", padx=5)
        
        self.green_slider = ctk.CTkSlider(
            green_frame, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_color_preview
        )
        self.green_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.green_slider.set(0)
        
        self.green_value = ctk.CTkLabel(green_frame, text="0", width=30)
        self.green_value.pack(side="right", padx=5)
        
        # Blue slider
        blue_frame = ctk.CTkFrame(rgb_frame)
        blue_frame.pack(fill="x", padx=10, pady=5)
        
        blue_label = ctk.CTkLabel(blue_frame, text="🔵 Blue:", width=50)
        blue_label.pack(side="left", padx=5)
        
        self.blue_slider = ctk.CTkSlider(
            blue_frame, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_color_preview
        )
        self.blue_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.blue_slider.set(0)
        
        self.blue_value = ctk.CTkLabel(blue_frame, text="0", width=30)
        self.blue_value.pack(side="right", padx=5)
        
        # Hex value display
        hex_frame = ctk.CTkFrame(main_frame)
        hex_frame.pack(fill="x", padx=10, pady=10)
        
        hex_label = ctk.CTkLabel(hex_frame, text="Hex:", width=30)
        hex_label.pack(side="left", padx=5)
        
        self.hex_entry = ctk.CTkEntry(hex_frame, width=100)
        self.hex_entry.pack(side="left", padx=5)
        self.hex_entry.insert(0, "#000000")
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        apply_btn = ctk.CTkButton(
            buttons_frame, 
            text="✅ Apply Color", 
            command=self.apply_color_from_picker,
            fg_color="green"
        )
        apply_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="❌ Cancel", 
            command=self.color_picker_window.destroy,
            fg_color="red"
        )
        cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Initialize with current color
        self.initialize_color_picker()
        
    def update_color_preview(self, value):
        """Update color preview when sliders change"""
        r = int(self.red_slider.get())
        g = int(self.green_slider.get())
        b = int(self.blue_slider.get())
        
        # Update value labels
        self.red_value.configure(text=str(r))
        self.green_value.configure(text=str(g))
        self.blue_value.configure(text=str(b))
        
        # Convert to hex
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_color)
        
        # Update preview
        self.color_preview.configure(bg=hex_color)
        
    def initialize_color_picker(self):
        """Initialize color picker with current color"""
        # Parse current color
        if hasattr(self, 'line_color') and self.line_color != "black":
            try:
                # Try to parse hex color
                if self.line_color.startswith('#'):
                    hex_color = self.line_color[1:]
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    
                    self.red_slider.set(r)
                    self.green_slider.set(g)
                    self.blue_slider.set(b)
                    
                    self.red_value.configure(text=str(r))
                    self.green_value.configure(text=str(g))
                    self.blue_value.configure(text=str(b))
                    
                    self.hex_entry.delete(0, tk.END)
                    self.hex_entry.insert(0, self.line_color)
                    
                    self.color_preview.configure(bg=self.line_color)
            except:
                # If parsing fails, use black
                pass
        
    def apply_color_from_picker(self):
        """Apply the color from the color picker"""
        hex_color = self.hex_entry.get()
        if hex_color.startswith('#'):
            self.line_color = hex_color
            self.current_color_display.configure(bg=hex_color)
            self.editor.update_status(f"✅ Line color set to {hex_color}")
            print(f"DEBUG: Color applied: {hex_color}")
            self.color_picker_window.destroy()
        else:
            self.editor.update_status("❌ Invalid hex color format")
            
    def on_width_change(self, value):
        """Handle line width change"""
        self.line_width = int(value)
        self.width_value_label.configure(text=str(self.line_width))
        
    def on_eraser_size_change(self, value):
        """Handle eraser size change"""
        eraser_size = int(value)
        self.eraser_size_value_label.configure(text=str(eraser_size))
        
    # DRAWING MODE FUNCTIONS
    def start_drawing_mode(self):
        """Start drawing mode - enable all drawing tools"""
        self.is_drawing_mode_active = True
        self.start_draw_btn.configure(state="disabled")
        self.stop_draw_btn.configure(state="normal")
        
        # Enable all drawing mode buttons
        self.freehand_btn.configure(state="normal")
        
        # Enable style buttons
        self.solid_btn.configure(state="normal")
        self.dashed_btn.configure(state="normal")
        self.dotted_btn.configure(state="normal")
        self.dashdot_btn.configure(state="normal")
        
        self.editor.update_status("🎨 Drawing mode STARTED - choose a tool and start drawing! Drawing will continue until you press STOP DRAWING")
        
    def stop_drawing_mode(self):
        """Stop drawing mode - disable all drawing tools"""
        self.is_drawing_mode_active = False
        self.start_draw_btn.configure(state="normal")
        self.stop_draw_btn.configure(state="disabled")
        
        # Disable all drawing mode buttons
        self.freehand_btn.configure(state="disabled")
        
        # Disable style buttons
        self.solid_btn.configure(state="disabled")
        self.dashed_btn.configure(state="disabled")
        self.dotted_btn.configure(state="disabled")
        self.dashdot_btn.configure(state="disabled")
        
        # Deactivate all modes
        self.deactivate_all_modes()
        
        self.editor.update_status("⏹️ Drawing mode STOPPED - all drawing tools deactivated")
        
    # DRAWING ACTIVATION FUNCTIONS
    def activate_freehand_drawing(self):
        """Activate freehand drawing mode"""
        if not self.is_drawing_mode_active:
            return
        self.deactivate_all_modes()
        self.is_drawing_active = True
        self.current_shape = "freehand"
        self.freehand_btn.configure(fg_color="green")
        self.editor.update_status("✏️ Freehand drawing activated - click and drag to draw. Keep drawing mode active to draw continuously!")
        


        
    def activate_eraser(self):
        """Activate eraser mode"""
        if not self.is_drawing_mode_active:
            return
        self.deactivate_all_modes()
        self.is_erasing = True
        self.eraser_btn.configure(fg_color="green")
        self.editor.update_status("🧽 Eraser activated - click to erase drawings")
        
    def deactivate_all_modes(self):
        """Deactivate all drawing modes"""
        self.is_drawing_active = False
        self.is_drawing_shapes = False
        self.is_erasing = False
        self.drawing_points = []
        
        # Reset button colors
        self.freehand_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.eraser_btn.configure(fg_color="red")
        
        # Reset style button colors
        self.solid_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dashed_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dotted_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.dashdot_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
    # DRAWING FUNCTIONS
    def start_drawing(self, x, y):
        """Start drawing at the given position"""
        if not self.is_drawing_mode_active:
            return
            
        if self.is_drawing_active or self.is_drawing_shapes:
            # Always start fresh with new point
            self.drawing_points = [(x, y)]
            print(f"DEBUG: Started drawing at ({x}, {y}) for {self.current_shape}")
        else:
            print(f"DEBUG: Drawing mode not active")
            
    def continue_drawing(self, x, y):
        """Continue drawing to the given position"""
        if not self.is_drawing_mode_active:
            return
            
        print(f"DEBUG: continue_drawing called - is_drawing_active={self.is_drawing_active}, is_drawing_shapes={self.is_drawing_shapes}, current_shape={self.current_shape}, points={len(self.drawing_points)}")
            
        if (self.is_drawing_active or self.is_drawing_shapes):
            if self.current_shape == "freehand":
                # Freehand drawing - add point and draw immediately
                if len(self.drawing_points) == 0:
                    # Start new freehand drawing
                    self.drawing_points = [(x, y)]
                    print("DEBUG: Starting new freehand drawing")
                else:
                    # Continue existing freehand drawing
                    self.drawing_points.append((x, y))
                    print(f"DEBUG: Drawing freehand - added point ({x}, {y}), total points: {len(self.drawing_points)}")
                    # Draw line from previous point to current point
                    if len(self.drawing_points) >= 2:
                        prev_x, prev_y = self.drawing_points[-2]
                        dash_pattern = self.get_dash_pattern()
                        self.editor.canvas.create_line(
                            prev_x, prev_y, x, y,
                            fill=self.line_color,
                            width=self.line_width,
                            dash=dash_pattern,
                            tags="drawing"
                        )
                        
                        # Store freehand element after each line segment
                        element = {
                            'type': 'freehand_segment',
                            'start_x': prev_x,
                            'start_y': prev_y,
                            'end_x': x,
                            'end_y': y,
                            'color': self.line_color,
                            'width': self.line_width,
                            'style': self.line_style
                        }
                        self.drawing_elements.append(element)
                


    def draw_freehand(self):
        """Draw freehand line"""
        if len(self.drawing_points) >= 2:
            # Draw line segments
            dash_pattern = self.get_dash_pattern()
            for i in range(len(self.drawing_points) - 1):
                x1, y1 = self.drawing_points[i]
                x2, y2 = self.drawing_points[i + 1]
                
                self.editor.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=self.line_color,
                    width=self.line_width,
                    dash=dash_pattern,
                    tags="drawing"
                )
                
            # Store as freehand element
            element = {
                'type': 'freehand',
                'points': self.drawing_points.copy(),
                'color': self.line_color,
                'width': self.line_width,
                'style': self.line_style
            }
            self.drawing_elements.append(element)
            
        # DON'T clear drawing_points for freehand - keep them for continuous drawing
        # self.drawing_points = []
        
        # Update status to show drawing is ready for next stroke
        if len(self.drawing_points) >= 2:
            self.editor.update_status("✏️ Freehand stroke drawn! Click to start new stroke, or press STOP DRAWING to finish")
        
    def redraw_all_drawings(self):
        """Redraw all drawing elements on the canvas"""
        # Clear existing drawings
        self.editor.canvas.delete("drawing")
        
        # Redraw all drawing elements
        for element in self.drawing_elements:
            if element['type'] == 'freehand':
                points = element['points']
                dash_pattern = self.get_dash_pattern_from_style(element.get('style', 'solid'))
                for i in range(len(points) - 1):
                    x1, y1 = points[i]
                    x2, y2 = points[i + 1]
                    self.editor.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=element['color'],
                        width=element['width'],
                        dash=dash_pattern,
                        tags="drawing"
                    )
            elif element['type'] == 'freehand_segment':
                dash_pattern = self.get_dash_pattern_from_style(element.get('style', 'solid'))
                self.editor.canvas.create_line(
                    element['start_x'], element['start_y'],
                    element['end_x'], element['end_y'],
                    fill=element['color'],
                    width=element['width'],
                    dash=dash_pattern,
                    tags="drawing"
                )
        
        print(f"DEBUG: Redrew {len(self.drawing_elements)} drawing elements")
        
    def clear_all_drawings(self):
        """Clear all drawings from canvas"""
        self.editor.canvas.delete("drawing")
        self.drawing_elements = []
        self.editor.update_status("🗑️ All drawings cleared")
        
    def clear_last_drawing(self):
        """Clear the last drawing from canvas"""
        if self.drawing_elements:
            # Remove last element
            last_element = self.drawing_elements.pop()
            
            # Redraw all elements except the last one
            self.editor.canvas.delete("drawing")
            for element in self.drawing_elements:
                if element['type'] == 'freehand':
                    points = element['points']
                    dash_pattern = self.get_dash_pattern_from_style(element.get('style', 'solid'))
                    for i in range(len(points) - 1):
                        x1, y1 = points[i]
                        x2, y2 = points[i + 1]
                        self.editor.canvas.create_line(
                            x1, y1, x2, y2,
                            fill=element['color'],
                            width=element['width'],
                            dash=dash_pattern,
                            tags="drawing"
                        )
                elif element['type'] == 'freehand_segment':
                    dash_pattern = self.get_dash_pattern_from_style(element.get('style', 'solid'))
                    self.editor.canvas.create_line(
                        element['start_x'], element['start_y'],
                        element['end_x'], element['end_y'],
                        fill=element['color'],
                        width=element['width'],
                        dash=dash_pattern,
                        tags="drawing"
                    )

                        
            self.editor.update_status("↩️ Last drawing cleared")
