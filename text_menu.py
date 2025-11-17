import customtkinter as ctk
import tkinter as tk
from tkinter import font, colorchooser
import os

class TextMenu:
    def __init__(self, editor):
        self.editor = editor
        self.is_adding_text = False
        self.text_elements = []
        self.create_text_window()
        
    def create_text_window(self):
        """Create the text tools window"""
        self.text_window = ctk.CTkToplevel(self.editor.root)
        self.text_window.title("Text Tools")
        self.text_window.geometry("450x700")
        self.text_window.resizable(False, False)
        
        # Center the window
        self.text_window.transient(self.editor.root)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.text_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Text Tools", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Text Input Section
        self.create_text_input_section(main_frame)
        
        # Text Properties Section
        self.create_text_properties_section(main_frame)
        
        # Text Management Section
        self.create_text_management_section(main_frame)
        self.create_position_section(main_frame)  # <-- dodaj to tutaj!
    
    def close_window(self):
        """Close the text menu window"""
        self.text_window.destroy()
        
    def create_text_input_section(self, parent):
        """Create the text input section"""
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        input_label = ctk.CTkLabel(input_frame, text="Text Input", font=("Arial", 14, "bold"))
        input_label.pack(pady=5)
        
        # Text entry
        text_entry_frame = ctk.CTkFrame(input_frame)
        text_entry_frame.pack(fill="x", padx=10, pady=5)
        
        text_label = ctk.CTkLabel(text_entry_frame, text="Text:", width=50)
        text_label.pack(side="left", padx=5)
        
        self.text_entry = ctk.CTkEntry(text_entry_frame)
        self.text_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Add text button
        add_text_btn = ctk.CTkButton(
            input_frame, 
            text="Add Text to Canvas", 
            command=self.activate_text_mode
        )
        add_text_btn.pack(fill="x", padx=10, pady=5)
        
    def create_text_properties_section(self, parent):
        """Create the text properties section"""
        props_frame = ctk.CTkFrame(parent)
        props_frame.pack(fill="x", padx=10, pady=10)
        
        props_label = ctk.CTkLabel(props_frame, text="Text Properties", font=("Arial", 14, "bold"))
        props_label.pack(pady=5)
        
        # Font family
        font_frame = ctk.CTkFrame(props_frame)
        font_frame.pack(fill="x", padx=10, pady=5)
        
        font_label = ctk.CTkLabel(font_frame, text="Font:", width=60)
        font_label.pack(side="left", padx=5)
        
        # Get available fonts
        available_fonts = list(font.families())
        available_fonts.sort()
        
        self.font_var = tk.StringVar(value="Arial")
        font_combo = ctk.CTkComboBox(
            font_frame, 
            values=available_fonts,
            variable=self.font_var,
            command=self.on_font_change
        )
        font_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Font size
        size_frame = ctk.CTkFrame(props_frame)
        size_frame.pack(fill="x", padx=10, pady=5)
        
        size_label = ctk.CTkLabel(size_frame, text="Size:", width=60)
        size_label.pack(side="left", padx=5)
        
        self.size_slider = ctk.CTkSlider(
            size_frame, 
            from_=8, 
            to=72, 
            number_of_steps=64,
            command=self.on_size_change
        )
        self.size_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.size_slider.set(16)
        
        self.size_value_label = ctk.CTkLabel(size_frame, text="16", width=30)
        self.size_value_label.pack(side="right", padx=5)
        
        # Text color
        color_frame = ctk.CTkFrame(props_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        color_label = ctk.CTkLabel(color_frame, text="Color:", width=60)
        color_label.pack(side="left", padx=5)
        
        self.color_btn = ctk.CTkButton(
            color_frame, 
            text="Choose", 
            command=self.choose_text_color,
            width=80
        )
        self.color_btn.pack(side="right", padx=5)
        
        self.color_display = tk.Frame(color_frame, bg="black", width=30, height=20)
        self.color_display.pack(side="right", padx=5)
        
        # Initialize color
        self.text_color = "black"
        
        # Text style options
        style_frame = ctk.CTkFrame(props_frame)
        style_frame.pack(fill="x", padx=10, pady=5)
        
        style_label = ctk.CTkLabel(style_frame, text="Style:", width=60)
        style_label.pack(side="left", padx=5)
        
        # Bold checkbox
        self.bold_var = tk.BooleanVar()
        bold_check = ctk.CTkCheckBox(
            style_frame, 
            text="Bold", 
            variable=self.bold_var,
            command=self.on_style_change
        )
        bold_check.pack(side="left", padx=5)
        
        # Italic checkbox
        self.italic_var = tk.BooleanVar()
        italic_check = ctk.CTkCheckBox(
            style_frame, 
            text="Italic", 
            variable=self.italic_var,
            command=self.on_style_change
        )
        italic_check.pack(side="left", padx=5)
        
        # Underline checkbox
        self.underline_var = tk.BooleanVar()
        underline_check = ctk.CTkCheckBox(
            style_frame, 
            text="Underline", 
            variable=self.underline_var,
            command=self.on_style_change
        )
        underline_check.pack(side="left", padx=5)
        
        # Text alignment
        align_frame = ctk.CTkFrame(props_frame)
        align_frame.pack(fill="x", padx=10, pady=5)
        
        align_label = ctk.CTkLabel(align_frame, text="Align:", width=60)
        align_label.pack(side="left", padx=5)
        
        self.align_var = tk.StringVar(value="left")
        align_combo = ctk.CTkComboBox(
            align_frame, 
            values=["left", "center", "right"],
            variable=self.align_var,
            command=self.on_align_change
        )
        align_combo.pack(side="left", fill="x", expand=True, padx=5)
        
    def create_text_management_section(self, parent):
        """Create the text management section"""
        manage_frame = ctk.CTkFrame(parent)
        manage_frame.pack(fill="x", padx=10, pady=10)
        
        manage_label = ctk.CTkLabel(manage_frame, text="Text Management", font=("Arial", 14, "bold"))
        manage_label.pack(pady=5)
        
        # Text list
        list_frame = ctk.CTkFrame(manage_frame)
        list_frame.pack(fill="x", padx=10, pady=5)
        
        list_label = ctk.CTkLabel(list_frame, text="Text Elements:", font=("Arial", 10))
        list_label.pack(pady=2)
        
        # Create listbox for text elements
        self.text_listbox = tk.Listbox(list_frame, height=6, selectmode="single")
        self.text_listbox.pack(fill="x", padx=5, pady=5)
        
        # Bind selection event
        self.text_listbox.bind('<<ListboxSelect>>', self.on_text_select)
        
        # Management buttons
        buttons_frame = ctk.CTkFrame(manage_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            buttons_frame, 
            text="Edit Selected", 
            command=self.edit_selected_text,
            state="disabled"
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            buttons_frame, 
            text="Delete Selected", 
            command=self.delete_selected_text,
            state="disabled",
            fg_color="red"
        )
        delete_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        # Store button references
        self.edit_btn = edit_btn
        self.delete_btn = delete_btn
        
        # Clear all button
        clear_all_btn = ctk.CTkButton(
            manage_frame, 
            text="Clear All Text", 
            command=self.clear_all_text,
            fg_color="orange"
        )
        clear_all_btn.pack(fill="x", padx=10, pady=2)
        
    def create_position_section(self, parent):
        """Create the position section"""
        pos_frame = ctk.CTkFrame(parent)
        pos_frame.pack(fill="x", padx=10, pady=10)
        
        pos_label = ctk.CTkLabel(pos_frame, text="Position", font=("Arial", 14, "bold"))
        pos_label.pack(pady=5)
        
        # X coordinate
        x_frame = ctk.CTkFrame(pos_frame)
        x_frame.pack(fill="x", padx=10, pady=5)
        
        x_label = ctk.CTkLabel(x_frame, text="X:", width=30)
        x_label.pack(side="left", padx=5)
        
        self.x_entry = ctk.CTkEntry(x_frame)
        self.x_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Y coordinate
        y_frame = ctk.CTkFrame(pos_frame)
        y_frame.pack(fill="x", padx=10, pady=5)
        
        y_label = ctk.CTkLabel(y_frame, text="Y:", width=30)
        y_label.pack(side="left", padx=5)
        
        self.y_entry = ctk.CTkEntry(y_frame)
        self.y_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Add text at coordinates button
        add_at_coords_btn = ctk.CTkButton(
            pos_frame, 
            text="Add Text at Coordinates", 
            command=self.add_text_at_coordinates
        )
        add_at_coords_btn.pack(fill="x", padx=10, pady=5)
        
        # Instructions
        instructions_label = ctk.CTkLabel(
            pos_frame, 
            text="Or click on canvas to add text at mouse position",
            font=("Arial", 10),
            text_color="gray"
        )
        instructions_label.pack(pady=5)
        
    def activate_text_mode(self):
        """Activate text adding mode"""
        self.is_adding_text = True
        self.editor.update_status("Kliknij na canvas, aby dodać tekst")
        
    def add_text_at_position(self, x, y):
        """Add text at the given position"""
        if not self.is_adding_text:
            return

        text = self.text_entry.get().strip()
        if not text:
            self.editor.update_status("Wpisz tekst przed dodaniem!")
            self.is_adding_text = False
            return

        self.editor.save_state()

        # Create text element
        text_element = {
            'text': text,
            'x': x,
            'y': y,
            'font_family': self.font_var.get(),
            'font_size': int(self.size_slider.get()),
            'color': self.text_color,
            'bold': self.bold_var.get(),
            'italic': self.italic_var.get(),
            'underline': self.underline_var.get(),
            'align': self.align_var.get()
        }

        self.text_elements.append(text_element)
        self.redraw_all_text()  # <-- zamiast self.add_text_to_canvas(text_element)
        self.update_text_list()
        self.update_buttons()

        # Wyłącz tryb dodawania tekstu po dodaniu
        self.is_adding_text = False
        self.editor.update_status(f"Dodano tekst: {text}")
        
    def add_text_at_coordinates(self):
        """Add text at specified coordinates"""
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
        except ValueError:
            self.editor.update_status("Invalid coordinates")
            return
            
        text = self.text_entry.get().strip()
        if not text:
            return
            
        self.editor.save_state()
        
        # Create text element
        text_element = {
            'text': text,
            'x': x,
            'y': y,
            'font_family': self.font_var.get(),
            'font_size': int(self.size_slider.get()),
            'color': self.text_color,
            'bold': self.bold_var.get(),
            'italic': self.italic_var.get(),
            'underline': self.underline_var.get(),
            'align': self.align_var.get()
        }
        
        self.text_elements.append(text_element)
        self.redraw_all_text()  # <-- zamiast self.add_text_to_canvas(text_element)
        self.update_text_list()
        self.update_buttons()
        
        # Clear entries
        self.text_entry.delete(0, tk.END)
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)
        
        self.editor.update_status(f"Added text at ({x}, {y}): {text}")
        
    def add_text_to_canvas(self, text_element):
        """Add text element to the canvas"""
        # Create font configuration
        font_config = []
        if text_element['bold']:
            font_config.append('bold')
        if text_element['italic']:
            font_config.append('italic')
            
        # Create font
        font_obj = font.Font(
            family=text_element['font_family'],
            size=text_element['font_size'],
            weight='bold' if text_element['bold'] else 'normal',
            slant='italic' if text_element['italic'] else 'roman'
        )
        
        # Create text on canvas
        text_id = self.editor.canvas.create_text(
            text_element['x'], text_element['y'],
            text=text_element['text'],
            font=font_obj,
            fill=text_element['color'],
            anchor="nw",
            tags="text"
        )
        
        # Store canvas ID with text element
        text_element['canvas_id'] = text_id
        
        # Add underline if needed
        if text_element['underline']:
            # Get text bounding box
            bbox = self.editor.canvas.bbox(text_id)
            if bbox:
                x1, y1, x2, y2 = bbox
                underline_id = self.editor.canvas.create_line(
                    x1, y2 + 2, x2, y2 + 2,
                    fill=text_element['color'],
                    width=1,
                    tags="text"
                )
                text_element['underline_id'] = underline_id
                
    def redraw_all_text(self):
        """Redraw all text elements on the canvas"""
        # Clear existing text
        self.editor.canvas.delete("text")
        
        # Redraw all text elements
        for text_element in self.text_elements:
            self.add_text_to_canvas(text_element)
            
    def update_text_list(self):
        """Update the text listbox display"""
        self.text_listbox.delete(0, tk.END)
        
        for i, text_element in enumerate(self.text_elements):
            # Truncate text if too long
            display_text = text_element['text']
            if len(display_text) > 30:
                display_text = display_text[:27] + "..."
                
            self.text_listbox.insert(tk.END, f"{i+1}. {display_text}")
            
    def on_text_select(self, event):
        """Handle text selection in listbox"""
        selection = self.text_listbox.curselection()
        if selection:
            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
        else:
            self.edit_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            
    def edit_selected_text(self):
        """Edit the selected text element"""
        selection = self.text_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        text_element = self.text_elements[index]
        
        # Create edit dialog
        self.create_edit_dialog(text_element, index)
        
    def create_edit_dialog(self, text_element, index):
        """Create dialog to edit text element"""
        edit_window = ctk.CTkToplevel(self.text_window)
        edit_window.title("Edit Text")
        edit_window.geometry("400x500")
        edit_window.resizable(False, False)
        
        edit_window.transient(self.text_window)
        edit_window.grab_set()
        
        # Create main frame
        main_frame = ctk.CTkFrame(edit_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Edit Text", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Text entry
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="x", padx=10, pady=5)
        
        text_label = ctk.CTkLabel(text_frame, text="Text:", width=50)
        text_label.pack(side="left", padx=5)
        
        edit_text_entry = ctk.CTkEntry(text_frame)
        edit_text_entry.insert(0, text_element['text'])
        edit_text_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Position entries
        pos_frame = ctk.CTkFrame(main_frame)
        pos_frame.pack(fill="x", padx=10, pady=5)
        
        x_label = ctk.CTkLabel(pos_frame, text="X:", width=30)
        x_label.pack(side="left", padx=5)
        
        x_entry = ctk.CTkEntry(pos_frame, width=80)
        x_entry.insert(0, str(text_element['x']))
        x_entry.pack(side="left", padx=5)
        
        y_label = ctk.CTkLabel(pos_frame, text="Y:", width=30)
        y_label.pack(side="left", padx=5)
        
        y_entry = ctk.CTkEntry(pos_frame, width=80)
        y_entry.insert(0, str(text_element['y']))
        y_entry.pack(side="left", padx=5)
        
        # Font properties
        font_frame = ctk.CTkFrame(main_frame)
        font_frame.pack(fill="x", padx=10, pady=5)
        
        font_label = ctk.CTkLabel(font_frame, text="Font:", width=60)
        font_label.pack(side="left", padx=5)
        
        available_fonts = list(font.families())
        available_fonts.sort()
        
        edit_font_var = tk.StringVar(value=text_element['font_family'])
        edit_font_combo = ctk.CTkComboBox(
            font_frame, 
            values=available_fonts,
            variable=edit_font_var
        )
        edit_font_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Size
        size_frame = ctk.CTkFrame(main_frame)
        size_frame.pack(fill="x", padx=10, pady=5)
        
        size_label = ctk.CTkLabel(size_frame, text="Size:", width=60)
        size_label.pack(side="left", padx=5)
        
        edit_size_var = tk.StringVar(value=str(text_element['font_size']))
        edit_size_combo = ctk.CTkComboBox(
            size_frame, 
            values=[str(i) for i in range(8, 73, 2)],
            variable=edit_size_var
        )
        edit_size_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Color
        color_frame = ctk.CTkFrame(main_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        color_label = ctk.CTkLabel(color_frame, text="Color:", width=60)
        color_label.pack(side="left", padx=5)
        
        edit_color_btn = ctk.CTkButton(
            color_frame, 
            text="Choose", 
            command=lambda: self.choose_edit_color(edit_color_display),
            width=80
        )
        edit_color_btn.pack(side="right", padx=5)
        
        edit_color_display = tk.Frame(color_frame, bg=text_element['color'], width=30, height=20)
        edit_color_display.pack(side="right", padx=5)
        
        # Style checkboxes
        style_frame = ctk.CTkFrame(main_frame)
        style_frame.pack(fill="x", padx=10, pady=5)
        
        edit_bold_var = tk.BooleanVar(value=text_element['bold'])
        edit_bold_check = ctk.CTkCheckBox(style_frame, text="Bold", variable=edit_bold_var)
        edit_bold_check.pack(side="left", padx=5)
        
        edit_italic_var = tk.BooleanVar(value=text_element['italic'])
        edit_italic_check = ctk.CTkCheckBox(style_frame, text="Italic", variable=edit_italic_var)
        edit_italic_check.pack(side="left", padx=5)
        
        edit_underline_var = tk.BooleanVar(value=text_element['underline'])
        edit_underline_check = ctk.CTkCheckBox(style_frame, text="Underline", variable=edit_underline_var)
        edit_underline_check.pack(side="left", padx=5)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        save_btn = ctk.CTkButton(
            buttons_frame, 
            text="Save Changes", 
            command=lambda: self.save_text_changes(
                index, edit_text_entry.get(), x_entry.get(), y_entry.get(),
                edit_font_var.get(), edit_size_var.get(), edit_color_display.cget('bg'),
                edit_bold_var.get(), edit_italic_var.get(), edit_underline_var.get(),
                edit_window
            )
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=edit_window.destroy
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=2)
        
    def choose_edit_color(self, color_display):
        """Choose color for text editing"""
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            color_display.configure(bg=color)
            
    def save_text_changes(self, index, new_text, new_x, new_y, new_font, new_size, 
                         new_color, new_bold, new_italic, new_underline, edit_window):
        """Save changes to text element"""
        try:
            new_x = int(new_x)
            new_y = int(new_y)
            new_size = int(new_size)
        except ValueError:
            self.editor.update_status("Invalid values")
            return
            
        self.editor.save_state()
        
        # Update text element
        self.text_elements[index].update({
            'text': new_text,
            'x': new_x,
            'y': new_y,
            'font_family': new_font,
            'font_size': new_size,
            'color': new_color,
            'bold': new_bold,
            'italic': new_italic,
            'underline': new_underline
        })
        
        # Redraw text
        self.redraw_all_text()
        self.update_text_list()
        
        edit_window.destroy()
        self.editor.update_status("Text updated")
        
    def delete_selected_text(self):
        """Delete the selected text element"""
        selection = self.text_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        
        self.editor.save_state()
        
        # Remove text element
        self.text_elements.pop(index)
        
        # Redraw text
        self.redraw_all_text()
        self.update_text_list()
        self.update_buttons()
        
        self.editor.update_status("Text deleted")
        
    def clear_all_text(self):
        """Clear all text elements"""
        if self.text_elements:
            self.editor.save_state()
            self.text_elements.clear()
            self.editor.canvas.delete("text")
            self.update_text_list()
            self.update_buttons()
            self.editor.update_status("All text cleared")
            
    def update_buttons(self):
        """Update button states"""
        has_text = len(self.text_elements) > 0
        
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        
    def choose_text_color(self):
        """Choose text color"""
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_color = color
            self.color_display.configure(bg=color)
            
    def on_font_change(self, value):
        """Handle font change"""
        pass  # Font is applied when adding text
        
    def on_size_change(self, value):
        """Handle size change"""
        self.size_value_label.configure(text=str(int(value)))
        
    def on_style_change(self):
        """Handle style change"""
        pass  # Styles are applied when adding text
        
    def on_align_change(self, value):
        """Handle alignment change"""
        pass  # Alignment is applied when adding text
