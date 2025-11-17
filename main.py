import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import numpy as np

# Import menu modules
from file_menu import FileMenu
from filters_menu import FiltersMenu
from draw_menu import DrawMenu
from text_menu import TextMenu
from rotate_menu import RotateMenu
from trim_menu import TrimMenu
from ai_menu import AIMenu
from batch_menu import BatchMenu
from advanced_batch_menu import AdvancedBatchMenu

class GraphicsEditor:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Graphics Editor Pro")
        self.root.geometry("1600x1000")  # Increased window size
        
        # Initialize variables
        self.images = []  # Stack of loaded images
        self.current_image_index = -1
        self.canvas_width = 1200  # Increased canvas size
        self.canvas_height = 800
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create canvas
        self.create_canvas()
        
        # Create right panel for tools
        self.create_right_panel()
        
        # Initialize undo/redo
        self.undo_stack = []
        self.redo_stack = []
        
        # Image management
        self.selected_image = None  # Currently selected image
        self.selected_image_index = -1  # Index of selected image in stack
        
        # Image highlighting and dragging
        self.highlight_rect = None  # Rectangle for highlighting selected image
        self.is_dragging = False  # Flag for drag operation
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Initialize menus
        self.init_menus()
        
        # Don't save initial state yet - wait until first image is loaded
        
    def create_menu_bar(self):
        """Create the main menu bar with all menu options"""
        self.menu_frame = ctk.CTkFrame(self.main_frame, height=50)
        self.menu_frame.pack(fill="x", pady=(0, 10))
        
        # Create menu buttons
        self.file_btn = ctk.CTkButton(self.menu_frame, text="File", command=self.show_file_menu)
        self.file_btn.pack(side="left", padx=5, pady=5)
        
        self.filters_btn = ctk.CTkButton(self.menu_frame, text="Filters", command=self.show_filters_menu)
        self.filters_btn.pack(side="left", padx=5, pady=5)
        
        self.draw_btn = ctk.CTkButton(self.menu_frame, text="Draw", command=self.show_draw_menu)
        self.draw_btn.pack(side="left", padx=5, pady=5)
        
        self.text_btn = ctk.CTkButton(self.menu_frame, text="Add Text", command=self.show_text_menu)
        self.text_btn.pack(side="left", padx=5, pady=5)
        
        self.rotate_btn = ctk.CTkButton(self.menu_frame, text="Rotate", command=self.show_rotate_menu)
        self.rotate_btn.pack(side="left", padx=5, pady=5)
        
        self.trim_btn = ctk.CTkButton(self.menu_frame, text="Trim", command=self.show_trim_menu)
        self.trim_btn.pack(side="left", padx=5, pady=5)
        
        self.ai_btn = ctk.CTkButton(self.menu_frame, text="AI", command=self.show_ai_menu)
        self.ai_btn.pack(side="left", padx=5, pady=5)
        
        self.batch_btn = ctk.CTkButton(self.menu_frame, text="Batch", command=self.show_batch_menu)
        self.batch_btn.pack(side="left", padx=5, pady=5)
        
        self.advanced_batch_btn = ctk.CTkButton(self.menu_frame, text="Advanced Batch", command=self.show_advanced_batch_menu)
        self.advanced_batch_btn.pack(side="left", padx=5, pady=5)
        
        # Undo/Redo buttons
        self.undo_btn = ctk.CTkButton(self.menu_frame, text="Undo", command=self.undo, state="disabled")
        self.undo_btn.pack(side="right", padx=5, pady=5)
        
        self.redo_btn = ctk.CTkButton(self.menu_frame, text="Redo", command=self.redo, state="disabled")
        self.redo_btn.pack(side="right", padx=5, pady=5)
        
    def create_canvas(self):
        """Create the main canvas for image editing"""
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.canvas_width, 
            height=self.canvas_height,
            bg="white",
            relief="sunken",
            bd=2
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
    def create_right_panel(self):
        """Create the right panel for tools and options"""
        self.right_panel = ctk.CTkFrame(self.main_frame, width=300)
        self.right_panel.pack(side="right", fill="y", padx=(10, 0))
        
        # Title for right panel
        self.tools_label = ctk.CTkLabel(self.right_panel, text="Tools & Options", font=("Arial", 16, "bold"))
        self.tools_label.pack(pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(self.right_panel, text="Ready", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Image info
        self.image_info_label = ctk.CTkLabel(self.right_panel, text="No images loaded", font=("Arial", 10))
        self.image_info_label.pack(pady=5)
        
        # Tools section (will be populated by menu modules)
        self.tools_frame = ctk.CTkFrame(self.right_panel)
        self.tools_frame.pack(fill="x", pady=10)

    def init_menus(self):
        """Initialize all menu modules"""
        # Don't initialize menus immediately - only when needed
        self.file_menu = None
        self.filters_menu = None
        self.draw_menu = None
        self.text_menu = None
        self.rotate_menu = None
        self.trim_menu = None
        self.ai_menu = None
        self.batch_menu = None
        self.advanced_batch_menu = None

    def show_file_menu(self):
        """Show file menu options"""
        # Always create new menu window
        try:
            if self.file_menu is not None:
                self.file_menu.file_window.destroy()
        except:
            pass
        self.file_menu = FileMenu(self)
        
    def show_filters_menu(self):
        """Show filters menu options"""
        # Always create new menu window
        try:
            if self.filters_menu is not None:
                self.filters_menu.filters_window.destroy()
        except:
            pass
        self.filters_menu = FiltersMenu(self)
        
    def show_draw_menu(self):
        """Show draw menu options"""
        # Always create new menu window
        try:
            if self.draw_menu is not None:
                self.draw_menu.draw_window.destroy()
        except:
            pass
        self.draw_menu = DrawMenu(self)
        
    def show_text_menu(self):
        """Show text menu options"""
        # Always create new menu window
        try:
            if self.text_menu is not None:
                self.text_menu.text_window.destroy()
        except:
            pass
        self.text_menu = TextMenu(self)
        
    def show_rotate_menu(self):
        """Show rotate menu options"""
        # Always create new menu window
        try:
            if self.rotate_menu is not None:
                self.rotate_menu.rotate_window.destroy()
        except:
            pass
        self.rotate_menu = RotateMenu(self)
        
    def show_trim_menu(self):
        """Show trim menu options"""
        # Always create new menu window
        try:
            if self.trim_menu is not None:
                self.trim_menu.trim_window.destroy()
        except:
            pass
        self.trim_menu = TrimMenu(self)
        
    def show_ai_menu(self):
        """Show AI menu options"""
        # Always create new menu window
        try:
            if self.ai_menu is not None:
                self.ai_menu.ai_window.destroy()
        except:
            pass
        self.ai_menu = AIMenu(self)

    def show_batch_menu(self):
        """Show batch processing menu options"""
        # Always create new menu window
        try:
            if self.batch_menu is not None:
                self.batch_menu.batch_window.destroy()
        except:
            pass
        self.batch_menu = BatchMenu(self)

    def show_advanced_batch_menu(self):
        """Show advanced batch processing menu options"""
        # Always create new menu window
        try:
            if self.advanced_batch_menu is not None:
                self.advanced_batch_menu.advanced_batch_window.destroy()
        except:
            pass
        self.advanced_batch_menu = AdvancedBatchMenu(self)

    def clear_tools_panel(self):
        """Clear the tools panel"""
        for widget in self.tools_frame.winfo_children():
            widget.destroy()

    def on_canvas_click(self, event):
        """Handle canvas click events"""
        x, y = event.x, event.y
        print(f"DEBUG: on_canvas_click called at ({x}, {y})")
        print(f"DEBUG: Total images: {len(self.images)}")
        
        # Check if any menu mode is active
        if self.draw_menu and (self.draw_menu.is_drawing_active or self.draw_menu.is_drawing_shapes):
            print(f"DEBUG: Draw menu active, calling start_drawing")
            self.draw_menu.start_drawing(x, y)
        elif self.text_menu and hasattr(self.text_menu, 'is_adding_text') and self.text_menu.is_adding_text:
            print(f"DEBUG: Text menu active, calling add_text_at_position")
            self.text_menu.add_text_at_position(x, y)
        elif self.rotate_menu and hasattr(self.rotate_menu, 'is_rotating') and self.rotate_menu.is_rotating:
            print(f"DEBUG: Rotate menu active, calling start_mouse_rotation")
            self.rotate_menu.start_mouse_rotation(x, y)
        elif self.trim_menu and hasattr(self.trim_menu, 'is_cropping') and self.trim_menu.is_cropping:
            print(f"DEBUG: Trim menu active, calling start_crop_selection")
            self.trim_menu.start_crop_selection(x, y)
        else:
            print(f"DEBUG: No menu mode active, selecting image")
            # Default behavior: select image
            self.select_image_at_position(x, y)
            
            print(f"DEBUG: After select_image_at_position - selected_index: {self.selected_image_index}, selected_image: {self.selected_image is not None}")
            
            # Now check if we actually selected an image and if click is on it
            if self.selected_image_index >= 0 and self.selected_image:
                # Check if click is actually on the selected image
                img_x = self.selected_image['position'][0]
                img_y = self.selected_image['position'][1]
                img_width = self.selected_image['width']
                img_height = self.selected_image['height']
                
                print(f"DEBUG: Image bounds - x: [{img_x}, {img_x + img_width}], y: [{img_y}, {img_y + img_height}]")
                print(f"DEBUG: Click at ({x}, {y}) - checking if within bounds")
                
                if (img_x <= x <= img_x + img_width and 
                    img_y <= y <= img_y + img_height):
                    print(f"DEBUG: Click is on image, starting drag")
                    self.start_image_drag(x, y)
                else:
                    print(f"DEBUG: Click is not on image, not starting drag")
            else:
                print(f"DEBUG: No image selected, cannot start drag")

    def on_canvas_drag(self, event):
        """Handle canvas drag events"""
        x, y = event.x, event.y
        print(f"DEBUG: on_canvas_drag called at ({x}, {y})")
        print(f"DEBUG: is_dragging: {self.is_dragging}, selected_image: {self.selected_image is not None}")
        
        # Check if any menu mode is active
        if self.draw_menu and (self.draw_menu.is_drawing_active or self.draw_menu.is_drawing_shapes):
            print(f"DEBUG: Draw menu active, calling continue_drawing")
            self.draw_menu.continue_drawing(x, y)
        elif self.rotate_menu and hasattr(self.rotate_menu, 'is_rotating') and self.rotate_menu.is_rotating:
            print(f"DEBUG: Rotate menu active, calling continue_mouse_rotation")
            self.rotate_menu.continue_mouse_rotation(x, y)
        elif self.trim_menu and hasattr(self.trim_menu, 'is_cropping') and self.trim_menu.is_cropping:
            print(f"DEBUG: Trim menu active, calling continue_crop_selection")
            self.trim_menu.continue_crop_selection(x, y)
        elif self.is_dragging and self.selected_image:
            print(f"DEBUG: Image dragging active, calling continue_image_drag")
            # Continue dragging selected image
            self.continue_image_drag(x, y)
        else:
            print(f"DEBUG: No active mode, is_dragging: {self.is_dragging}, selected_image: {self.selected_image is not None}")

    def on_canvas_release(self, event):
        """Handle canvas release events"""
        # Check if any menu mode is active
        if self.rotate_menu and hasattr(self.rotate_menu, 'is_rotating') and self.rotate_menu.is_rotating:
            self.rotate_menu.stop_mouse_rotation()
        elif self.trim_menu and hasattr(self.trim_menu, 'is_cropping') and self.trim_menu.is_cropping:
            self.trim_menu.stop_crop_selection()
        elif self.is_dragging:
            # Stop dragging selected image
            self.stop_image_drag()

    def add_image(self, image_path):
        """Add a new image to the stack"""
        try:
            print(f"DEBUG: Adding image: {image_path}")
            
            # Load image
            img = Image.open(image_path)
            print(f"DEBUG: Image loaded: mode={img.mode}, size={img.size}")
            
            # Scale image to fit canvas if too large
            try:
                img.thumbnail((self.canvas_width, self.canvas_height), Image.Resampling.LANCZOS)
            except AttributeError:
                # Fallback for older Pillow versions
                img.thumbnail((self.canvas_width, self.canvas_height), Image.LANCZOS)
            
            print(f"DEBUG: After thumbnail: size={img.size}")
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Calculate position to center image on canvas
            x = (self.canvas_width - img.width) // 2
            y = (self.canvas_height - img.height) // 2
            
            print(f"DEBUG: Image position: ({x}, {y})")
            
            # Add to images stack
            image_id = self.canvas.create_image(x, y, anchor="nw", image=photo)
            
            image_data = {
                'image': img,
                'original_image': img.copy(),  # Store original for scaling functionality
                'photo': photo,
                'path': image_path,
                'position': (x, y),
                'rotation': 0,
                'visible': True,
                'id': image_id,
                'width': img.width,
                'height': img.height
            }
            
            print(f"DEBUG: Image data created - width: {img.width}, height: {img.height}, position: ({x}, {y})")
            
            self.images.append(image_data)
            print(f"DEBUG: Image added to stack at index {len(self.images) - 1}")
            

            self.current_image_index = len(self.images) - 1
            
            # Save initial state if this is the first image
            if len(self.images) == 1 and len(self.undo_stack) == 0:
                # Save empty state first
                initial_state = {
                    'images': [],
                    'current_index': -1,
                    'selected_image_index': -1
                }
                self.undo_stack.append(initial_state)
                print("DEBUG: Initial state saved")
            
            self.update_canvas()
            self.update_status(f"Loaded: {os.path.basename(image_path)}")
            self.update_image_info()
            
            # Update menu button states
            if self.filters_menu:
                self.filters_menu.update_apply_buttons()
            if self.rotate_menu:
                self.rotate_menu.update_apply_buttons()
            if self.trim_menu:
                self.trim_menu.update_apply_buttons()
            
            # Save state for undo/redo
            self.save_state()
            
            print(f"DEBUG: Image loading completed successfully")
            
        except Exception as e:
            print(f"DEBUG: Error loading image: {e}")
            import traceback
            traceback.print_exc()
            self.update_status(f"Error loading image: {str(e)}")
            
    def update_canvas(self):
        """Update the canvas with current images"""
        print(f"DEBUG: Updating canvas with {len(self.images)} images")
        
        # Store current highlight info
        current_highlight = None
        if self.highlight_rect:
            current_highlight = self.canvas.coords(self.highlight_rect)
            self.canvas.delete(self.highlight_rect)
            self.highlight_rect = None
            print(f"DEBUG: Stored highlight coordinates: {current_highlight}")
        
        # Clear canvas and recreate all images to ensure proper layering
        self.canvas.delete("all")
        
        for i, img_data in enumerate(self.images):
            if img_data['visible']:
                print(f"DEBUG: Processing image {i}: pos={img_data['position']}, size=({img_data['width']}, {img_data['height']})")
                
                # Apply rotation if needed
                img = img_data['image']
                if img_data['rotation'] != 0:
                    try:
                        img = img.rotate(img_data['rotation'], expand=True)
                        print(f"DEBUG: Applied rotation {img_data['rotation']}° to image {i}")
                    except TypeError:
                        # Fallback for older Pillow versions
                        img = img.rotate(img_data['rotation'], expand=True)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                img_data['photo'] = photo  # Keep reference
                
                # Create new image on canvas
                x, y = img_data['position']
                image_id = self.canvas.create_image(x, y, anchor="nw", image=photo, tags=f"image_{i}")
                img_data['id'] = image_id
                
                # Update width and height if they changed
                img_data['width'] = img.width
                img_data['height'] = img.height
                
                print(f"DEBUG: Created image {i} on canvas at ({x}, {y}) with ID {image_id}")
        
        # Restore drawings if draw menu exists and has drawings
        if hasattr(self, 'draw_menu') and self.draw_menu and hasattr(self.draw_menu, 'drawing_elements'):
            print(f"DEBUG: Restoring {len(self.draw_menu.drawing_elements)} drawing elements")
            self.draw_menu.redraw_all_drawings()
        
        # Restore text if text menu exists and has text
        if hasattr(self, 'text_menu') and self.text_menu and hasattr(self.text_menu, 'text_elements'):
            print(f"DEBUG: Restoring {len(self.text_menu.text_elements)} text elements")
            self.text_menu.redraw_all_text()
        
        # Restore highlight if image is selected
        if self.selected_image_index >= 0 and self.selected_image_index < len(self.images):
            self.selected_image = self.images[self.selected_image_index]
            self.highlight_selected_image()
            print(f"DEBUG: Restored highlight for selected image {self.selected_image_index}")
        else:
            print(f"DEBUG: No highlight restored - selected_index: {self.selected_image_index}, total_images: {len(self.images)}")
                
    def update_status(self, message):
        """Update status label"""
        print(f"DEBUG: Status update: {message}")
        self.status_label.configure(text=message)
        
    def update_image_info(self):
        """Update image information display"""
        print(f"DEBUG: update_image_info called - total images: {len(self.images)}, selected: {self.selected_image_index}")
        
        if self.images:
            info = f"Images: {len(self.images)}\n"
            if self.selected_image_index >= 0:
                info += f"Selected: Image {self.selected_image_index + 1}"
                print(f"DEBUG: Image {self.selected_image_index + 1} is selected")
            else:
                info += "No image selected"
                print(f"DEBUG: No image is selected")
            self.image_info_label.configure(text=info)
        else:
            self.image_info_label.configure(text="No images loaded")
            print(f"DEBUG: No images loaded")
            
    def save_state(self):
        """Save current state for undo"""
        print(f"DEBUG: Saving state - total images: {len(self.images)}, selected_index: {self.selected_image_index}")
        
        # Deep copy image data
        images_copy = []
        for img_data in self.images:
            img_copy = {
                'image': img_data['image'].copy(),
                'photo': img_data['photo'],  # This will be recreated when needed
                'path': img_data['path'],
                'position': img_data['position'],
                'rotation': img_data['rotation'],
                'visible': img_data['visible'],
                'width': img_data['width'],
                'height': img_data['height']
            }
            if 'id' in img_data:
                img_copy['id'] = img_data['id']
            images_copy.append(img_copy)
        
        state = {
            'images': images_copy,
            'current_index': self.current_image_index,
            'selected_image_index': self.selected_image_index
        }
        self.undo_stack.append(state)
        self.redo_stack.clear()  # Clear redo when new action is performed
        
        print(f"DEBUG: State saved - undo stack size: {len(self.undo_stack)}")
        
        # Enable/disable undo/redo buttons
        self.undo_btn.configure(state="normal" if len(self.undo_stack) > 1 else "disabled")
        self.redo_btn.configure(state="disabled")
        
    def undo(self):
        """Undo last action"""
        print(f"DEBUG: Undo called - undo stack size: {len(self.undo_stack)}")
        
        if len(self.undo_stack) > 1:  # Need at least 2 states to undo
            print(f"DEBUG: Performing undo operation")
            
            # Save current state to redo (but first take a fresh snapshot)
            current_images_copy = []
            for img_data in self.images:
                img_copy = {
                    'image': img_data['image'].copy(),
                    'photo': img_data['photo'],
                    'path': img_data['path'],
                    'position': img_data['position'],
                    'rotation': img_data['rotation'],
                    'visible': img_data['visible'],
                    'width': img_data['width'],
                    'height': img_data['height']
                }
                if 'id' in img_data:
                    img_copy['id'] = img_data['id']
                current_images_copy.append(img_copy)
            
            current_state = {
                'images': current_images_copy,
                'current_index': self.current_image_index,
                'selected_image_index': self.selected_image_index
            }
            self.redo_stack.append(current_state)
            print(f"DEBUG: Current state saved to redo stack")
            
            # Restore previous state
            state = self.undo_stack.pop()
            print(f"DEBUG: Restoring previous state")
            
            # Clear current canvas
            self.canvas.delete("all")
            
            # Restore images and recreate them on canvas
            self.images = []
            for img_data in state['images']:
                # Recreate PhotoImage
                photo = ImageTk.PhotoImage(img_data['image'])
                img_data['photo'] = photo
                
                # Create image on canvas
                x, y = img_data['position']
                image_id = self.canvas.create_image(x, y, anchor="nw", image=photo)
                img_data['id'] = image_id
                
                self.images.append(img_data)
            
            self.current_image_index = state['current_index']

            self.selected_image_index = state['selected_image_index']
            
            print(f"DEBUG: State restored - images: {len(self.images)}, selected: {self.selected_image_index}")
            
            # Restore selection and highlight
            if self.selected_image_index >= 0 and self.selected_image_index < len(self.images):
                self.selected_image = self.images[self.selected_image_index]
                self.highlight_selected_image()
            else:
                self.clear_image_highlight()
                self.selected_image = None
            
            self.update_image_info()
            
            # Update button states
            self.undo_btn.configure(state="normal" if len(self.undo_stack) > 1 else "disabled")
            self.redo_btn.configure(state="normal" if self.redo_stack else "disabled")
            
            print(f"DEBUG: Undo completed successfully")
        else:
            print(f"DEBUG: Cannot undo - insufficient states in stack")
            
    def redo(self):
        """Redo last undone action"""
        print(f"DEBUG: Redo called - redo stack size: {len(self.redo_stack)}")
        
        if self.redo_stack:
            print(f"DEBUG: Performing redo operation")
            
            # Save current state to undo (take fresh snapshot)
            current_images_copy = []
            for img_data in self.images:
                img_copy = {
                    'image': img_data['image'].copy(),
                    'photo': img_data['photo'],
                    'path': img_data['path'],
                    'position': img_data['position'],
                    'rotation': img_data['rotation'],
                    'visible': img_data['visible'],
                    'width': img_data['width'],
                    'height': img_data['height']
                }
                if 'id' in img_data:
                    img_copy['id'] = img_data['id']
                current_images_copy.append(img_copy)
            
            current_state = {
                'images': current_images_copy,
                'current_index': self.current_image_index,
                'selected_image_index': self.selected_image_index
            }
            self.undo_stack.append(current_state)
            print(f"DEBUG: Current state saved to undo stack")
            
            # Restore redo state
            state = self.redo_stack.pop()
            print(f"DEBUG: Restoring redo state")
            
            # Clear current canvas
            self.canvas.delete("all")
            
            # Restore images and recreate them on canvas
            self.images = []
            for img_data in state['images']:
                # Recreate PhotoImage
                photo = ImageTk.PhotoImage(img_data['image'])
                img_data['photo'] = photo
                
                # Create image on canvas
                x, y = img_data['position']
                image_id = self.canvas.create_image(x, y, anchor="nw", image=photo)
                img_data['id'] = image_id
                
                self.images.append(img_data)
            
            self.current_image_index = state['current_index']

            self.selected_image_index = state['selected_image_index']
            
            print(f"DEBUG: State restored - images: {len(self.images)}, selected: {self.selected_image_index}")
            
            # Restore selection and highlight
            if self.selected_image_index >= 0 and self.selected_image_index < len(self.images):
                self.selected_image = self.images[self.selected_image_index]
                self.highlight_selected_image()
            else:
                self.clear_image_highlight()
                self.selected_image = None
            
            self.update_image_info()
            
            # Update button states
            self.undo_btn.configure(state="normal" if len(self.undo_stack) > 1 else "disabled")
            self.redo_btn.configure(state="normal" if self.redo_stack else "disabled")
            
            print(f"DEBUG: Redo completed successfully")
        else:
            print(f"DEBUG: Cannot redo - redo stack is empty")

    def select_image_at_position(self, x, y):
        """Select image at given canvas coordinates"""
        # Find which image was clicked
        clicked_image_index = -1
        
        print(f"DEBUG: Checking for image at position ({x}, {y})")
        print(f"DEBUG: Total images: {len(self.images)}")
        
        # Check images in reverse order (top to bottom visually)
        for i in range(len(self.images) - 1, -1, -1):
            image_data = self.images[i]
            img_x = image_data['position'][0]
            img_y = image_data['position'][1]
            img_width = image_data['width']
            img_height = image_data['height']
            
            print(f"DEBUG: Image {i}: pos=({img_x}, {img_y}), size=({img_width}, {img_height})")
            print(f"DEBUG: Click at ({x}, {y}) - checking bounds: x in [{img_x}, {img_x + img_width}], y in [{img_y}, {img_y + img_height}]")
            
            if (img_x <= x <= img_x + img_width and 
                img_y <= y <= img_y + img_height):
                clicked_image_index = i
                print(f"DEBUG: Found image {i} at position ({x}, {y})")
                break
        
        # Update selection
        if clicked_image_index != self.selected_image_index:
            print(f"DEBUG: Changing selection from {self.selected_image_index} to {clicked_image_index}")
            
            # Clear previous selection
            if self.selected_image_index >= 0 and self.selected_image_index < len(self.images):
                self.clear_image_highlight()
            
            self.selected_image_index = clicked_image_index
            if clicked_image_index >= 0 and clicked_image_index < len(self.images):
                self.selected_image = self.images[clicked_image_index]
                self.highlight_selected_image()
                print(f"DEBUG: Selected image {clicked_image_index}: {self.selected_image['path']}")
            else:
                self.selected_image = None
                print(f"DEBUG: No image selected")
            
            self.update_image_info()
            
            # Update menu button states when selection changes
            try:
                if self.file_menu and hasattr(self.file_menu, 'file_window'):
                    self.file_menu.update_buttons()
            except Exception as e:
                print(f"DEBUG: Error updating file menu buttons: {e}")
            
            # Update other menu button states
            try:
                if self.filters_menu and hasattr(self.filters_menu, 'filters_window'):
                    self.filters_menu.update_apply_buttons()
            except Exception as e:
                print(f"DEBUG: Error updating filters menu buttons: {e}")
            try:
                if self.rotate_menu and hasattr(self.rotate_menu, 'rotate_window'):
                    self.rotate_menu.update_apply_buttons()
            except Exception as e:
                print(f"DEBUG: Error updating rotate menu buttons: {e}")
            try:
                if self.trim_menu and hasattr(self.trim_menu, 'trim_window'):
                    self.trim_menu.update_apply_buttons()
            except Exception as e:
                print(f"DEBUG: Error updating trim menu buttons: {e}")
        else:
            print(f"DEBUG: Selection unchanged: {self.selected_image_index}")

    def highlight_selected_image(self):
        """Highlight the currently selected image with a dashed border"""
        print(f"DEBUG: Highlighting selected image at index {self.selected_image_index}")
        
        if self.selected_image and self.selected_image_index >= 0:
            # Remove previous highlight if exists
            if self.highlight_rect:
                self.canvas.delete(self.highlight_rect)
                print(f"DEBUG: Removed previous highlight {self.highlight_rect}")
            
            # Create dashed border around selected image
            x = self.selected_image['position'][0]
            y = self.selected_image['position'][1]
            width = self.selected_image['width']
            height = self.selected_image['height']
            
            print(f"DEBUG: Creating highlight at ({x}, {y}) with size ({width}, {height})")
            
            # Create dashed rectangle
            self.highlight_rect = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                outline="red",
                width=2,
                dash=(5, 5)
            )
            
            # Bring highlight to front
            self.canvas.tag_raise(self.highlight_rect)
            print(f"DEBUG: Created highlight rectangle with ID {self.highlight_rect}")
        else:
            print(f"DEBUG: Cannot highlight - selected_image: {self.selected_image}, selected_index: {self.selected_image_index}")

    def clear_image_highlight(self):
        """Clear the image highlight"""
        if self.highlight_rect:
            print(f"DEBUG: Clearing highlight rectangle {self.highlight_rect}")
            self.canvas.delete(self.highlight_rect)
            self.highlight_rect = None
        else:
            print(f"DEBUG: No highlight to clear")

    def start_image_drag(self, x, y):
        """Start dragging the selected image"""
        print(f"DEBUG: start_image_drag called at ({x}, {y})")
        print(f"DEBUG: selected_image: {self.selected_image is not None}, selected_index: {self.selected_image_index}, total_images: {len(self.images)}")
        
        if (self.selected_image and self.selected_image_index >= 0 and 
            self.selected_image_index < len(self.images)):
            
            print(f"DEBUG: Starting drag at ({x}, {y}) for image {self.selected_image_index}")
            self.is_dragging = True
            self.drag_start_x = x
            self.drag_start_y = y
            self.drag_offset_x = x - self.selected_image['position'][0]
            self.drag_offset_y = y - self.selected_image['position'][1]
            
            print(f"DEBUG: Drag offsets: x={self.drag_offset_x}, y={self.drag_offset_y}")
            
            # Change cursor to indicate dragging
            self.canvas.configure(cursor="fleur")
            print(f"DEBUG: Drag started successfully - is_dragging: {self.is_dragging}")
        else:
            print(f"DEBUG: Cannot start drag - selected_image: {self.selected_image}, selected_index: {self.selected_image_index}, total_images: {len(self.images)}")
            if self.selected_image_index >= 0 and self.selected_image_index < len(self.images):
                print(f"DEBUG: Image at index exists: {self.images[self.selected_image_index]}")
            # Reset dragging state if validation fails
            self.is_dragging = False
            print(f"DEBUG: Drag start failed - is_dragging reset to: {self.is_dragging}")

    def continue_image_drag(self, x, y):
        """Continue dragging the selected image"""
        if self.is_dragging and self.selected_image and self.selected_image_index >= 0:
            print(f"DEBUG: Continuing drag to ({x}, {y})")
            
            # Verify the selected image still exists
            if self.selected_image_index >= len(self.images):
                print(f"DEBUG: Selected image index out of range, stopping drag")
                self.stop_image_drag()
                return
            
            # Calculate new position
            new_x = x - self.drag_offset_x
            new_y = y - self.drag_offset_y
            
            # Ensure image stays within canvas bounds
            new_x = max(0, min(new_x, self.canvas_width - self.selected_image['width']))
            new_y = max(0, min(new_y, self.canvas_height - self.selected_image['height']))
            
            print(f"DEBUG: Moving image from {self.selected_image['position']} to ({new_x}, {new_y})")
            
            # Move image on canvas
            try:
                self.canvas.coords(self.selected_image['id'], new_x, new_y)  # <-- poprawka
                
                # Update image data
                self.selected_image['position'] = (new_x, new_y)
                
                # Update highlight position
                if self.highlight_rect:
                    self.canvas.coords(self.highlight_rect, 
                                     new_x, new_y, 
                                     new_x + self.selected_image['width'], 
                                     new_y + self.selected_image['height'])
                    # Ensure highlight stays on top
                    self.canvas.tag_raise(self.highlight_rect)
                    
            except Exception as e:
                print(f"DEBUG: Error during drag: {e}")
                self.stop_image_drag()
        else:
            print(f"DEBUG: Cannot continue drag - is_dragging: {self.is_dragging}, selected_image: {self.selected_image}, selected_index: {self.selected_image_index}")
            if self.is_dragging:
                self.stop_image_drag()
            # Reset dragging state if validation fails
            self.is_dragging = False

    def stop_image_drag(self):
        """Stop dragging the selected image"""
        if self.is_dragging:
            print(f"DEBUG: Stopping image drag")
            self.is_dragging = False
            self.canvas.configure(cursor="")
            
            # Save state for undo/redo
            self.save_state()
        else:
            print(f"DEBUG: No drag to stop")

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GraphicsEditor()
    app.run()
