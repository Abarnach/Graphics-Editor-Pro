import customtkinter as ctk
import tkinter as tk
from PIL import Image
import requests
import io
import base64
import json
import os
import datetime
from io import BytesIO

class AIMenu:
    def __init__(self, editor):
        self.editor = editor
        self.api_key = None
        self.api_endpoint = None
        self.create_ai_window()
        
    def create_ai_window(self):
        """Create the AI tools window"""
        self.ai_window = ctk.CTkToplevel(self.editor.root)
        self.ai_window.title("AI Image Generator")
        self.ai_window.geometry("600x600")
        self.ai_window.resizable(True, True)
        
        # Center the window
        self.ai_window.transient(self.editor.root)
        
        # Create main container frame
        main_container = ctk.CTkFrame(self.ai_window)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(main_container, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(main_container, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Create main frame inside scrollable area
        main_frame = ctk.CTkFrame(self.scrollable_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="AI Image Generation", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # API Configuration Section
        self.create_api_config_section(main_frame)
        
        # Prompt Section
        self.create_prompt_section(main_frame)
        
        # Generation Settings Section
        self.create_generation_settings_section(main_frame)
        
        # Generation Section
        self.create_generation_section(main_frame)
        
        # History Section
        self.create_history_section(main_frame)
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def close_window(self):
        """Close the AI menu window"""
        self.ai_window.destroy()
        
    def create_api_config_section(self, parent):
        """Create the API configuration section"""
        api_frame = ctk.CTkFrame(parent)
        api_frame.pack(fill="x", padx=10, pady=10)
        
        api_label = ctk.CTkLabel(api_frame, text="API Configuration", font=("Arial", 14, "bold"))
        api_label.pack(pady=5)
        
        # API Key input
        key_frame = ctk.CTkFrame(api_frame)
        key_frame.pack(fill="x", padx=10, pady=5)
        
        key_label = ctk.CTkLabel(key_frame, text="API Key:", width=80)
        key_label.pack(side="left", padx=5)
        
        self.api_key_entry = ctk.CTkEntry(key_frame, show="*")
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # API Endpoint selection
        endpoint_frame = ctk.CTkFrame(api_frame)
        endpoint_frame.pack(fill="x", padx=10, pady=5)
        
        endpoint_label = ctk.CTkLabel(endpoint_frame, text="Service:", width=80)
        endpoint_label.pack(side="left", padx=5)
        
        self.service_var = tk.StringVar(value="local")
        print(f"DEBUG: Setting default service to: {self.service_var.get()}")
        service_combo = ctk.CTkComboBox(
            endpoint_frame, 
            values=["local", "stablehorde", "huggingface", "falai", "openai", "stability", "custom"],
            variable=self.service_var,
            command=self.on_service_change
        )
        service_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Custom endpoint input
        custom_endpoint_frame = ctk.CTkFrame(api_frame)
        custom_endpoint_frame.pack(fill="x", padx=10, pady=5)
        
        custom_endpoint_label = ctk.CTkLabel(custom_endpoint_frame, text="Custom URL:", width=80)
        custom_endpoint_label.pack(side="left", padx=5)
        
        self.custom_endpoint_entry = ctk.CTkEntry(custom_endpoint_frame)
        self.custom_endpoint_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Initially hide custom endpoint
        self.custom_endpoint_frame = custom_endpoint_frame
        self.custom_endpoint_frame.pack_forget()
        
        # Test connection button
        test_btn = ctk.CTkButton(
            api_frame, 
            text="Test Connection", 
            command=self.test_connection
        )
        test_btn.pack(fill="x", padx=10, pady=5)
        
    def create_prompt_section(self, parent):
        """Create the prompt input section"""
        prompt_frame = ctk.CTkFrame(parent)
        prompt_frame.pack(fill="x", padx=10, pady=10)
        
        prompt_label = ctk.CTkLabel(prompt_frame, text="Image Prompt", font=("Arial", 14, "bold"))
        prompt_label.pack(pady=5)
        
        # Prompt text area
        prompt_text_frame = ctk.CTkFrame(prompt_frame)
        prompt_text_frame.pack(fill="x", padx=10, pady=5)
        
        prompt_text_label = ctk.CTkLabel(prompt_text_frame, text="Describe the image you want:", font=("Arial", 10))
        prompt_text_label.pack(pady=2)
        
        self.prompt_text = ctk.CTkTextbox(prompt_text_frame, height=100)
        self.prompt_text.pack(fill="x", padx=5, pady=5)
        # Insert placeholder text
        self.prompt_text.insert("1.0", "Enter a detailed description of the image you want to generate...")
        
        # Negative prompt
        negative_frame = ctk.CTkFrame(prompt_frame)
        negative_frame.pack(fill="x", padx=10, pady=5)
        
        negative_label = ctk.CTkLabel(negative_frame, text="Negative Prompt:", font=("Arial", 10))
        negative_label.pack(pady=2)
        
        # Info label for different services
        self.info_label = ctk.CTkLabel(
            negative_frame, 
            text="Note: Stable Horde is free but has rate limits. If you get 429 error, wait a few minutes.", 
            font=("Arial", 8),
            text_color="gray"
        )
        self.info_label.pack(pady=2)
        
        self.negative_prompt_text = ctk.CTkTextbox(negative_frame, height=60)
        self.negative_prompt_text.pack(fill="x", padx=5, pady=5)
        # Insert placeholder text
        self.negative_prompt_text.insert("1.0", "Describe what you DON'T want in the image...")
        
        # Prompt examples
        examples_frame = ctk.CTkFrame(prompt_frame)
        examples_frame.pack(fill="x", padx=10, pady=5)
        
        examples_label = ctk.CTkLabel(examples_frame, text="Quick Prompts:", font=("Arial", 10, "bold"))
        examples_label.pack(pady=2)
        
        # Example buttons
        examples_buttons_frame = ctk.CTkFrame(examples_frame)
        examples_buttons_frame.pack(fill="x", padx=5, pady=2)
        
        example1_btn = ctk.CTkButton(
            examples_buttons_frame, 
            text="Landscape", 
            command=lambda: self.load_example_prompt("A beautiful mountain landscape at sunset with golden light, photorealistic, high quality"),
            width=80
        )
        example1_btn.pack(side="left", padx=2, pady=2)
        
        example2_btn = ctk.CTkButton(
            examples_buttons_frame, 
            text="Portrait", 
            command=lambda: self.load_example_prompt("A professional portrait of a person, studio lighting, high resolution, detailed"),
            width=80
        )
        example2_btn.pack(side="left", padx=2, pady=2)
        
        example3_btn = ctk.CTkButton(
            examples_buttons_frame, 
            text="Abstract", 
            command=lambda: self.load_example_prompt("Abstract geometric patterns, vibrant colors, modern art style, high quality"),
            width=80
        )
        example3_btn.pack(side="left", padx=2, pady=2)
        
        example4_btn = ctk.CTkButton(
            examples_buttons_frame, 
            text="Clear", 
            command=self.clear_prompts,
            width=80
        )
        example4_btn.pack(side="left", padx=2, pady=2)
        
    def create_generation_settings_section(self, parent):
        """Create the generation settings section"""
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        settings_label = ctk.CTkLabel(settings_frame, text="Generation Settings", font=("Arial", 14, "bold"))
        settings_label.pack(pady=5)
        
        # Image size
        size_frame = ctk.CTkFrame(settings_frame)
        size_frame.pack(fill="x", padx=10, pady=5)
        
        size_label = ctk.CTkLabel(size_frame, text="Image Size:", width=80)
        size_label.pack(side="left", padx=5)
        
        self.size_var = tk.StringVar(value="1024x1024")
        size_combo = ctk.CTkComboBox(
            size_frame, 
            values=["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"],
            variable=self.size_var
        )
        size_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Quality setting
        quality_frame = ctk.CTkFrame(settings_frame)
        quality_frame.pack(fill="x", padx=10, pady=5)
        
        quality_label = ctk.CTkLabel(quality_frame, text="Quality:", width=80)
        quality_label.pack(side="left", padx=5)
        
        self.quality_var = tk.StringVar(value="standard")
        quality_combo = ctk.CTkComboBox(
            quality_frame, 
            values=["standard", "hd"],
            variable=self.quality_var
        )
        quality_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Style setting
        style_frame = ctk.CTkFrame(settings_frame)
        style_frame.pack(fill="x", padx=10, pady=5)
        
        style_label = ctk.CTkLabel(style_frame, text="Style:", width=80)
        style_label.pack(side="left", padx=5)
        
        self.style_var = tk.StringVar(value="vivid")
        style_combo = ctk.CTkComboBox(
            style_frame, 
            values=["vivid", "natural"],
            variable=self.style_var
        )
        style_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Number of images
        count_frame = ctk.CTkFrame(settings_frame)
        count_frame.pack(fill="x", padx=10, pady=5)
        
        count_label = ctk.CTkLabel(count_frame, text="Count:", width=80)
        count_label.pack(side="left", padx=5)
        
        self.count_var = tk.StringVar(value="1")
        count_combo = ctk.CTkComboBox(
            count_frame, 
            values=["1", "2", "3", "4"],
            variable=self.count_var
        )
        count_combo.pack(side="left", fill="x", expand=True, padx=5)
        
    def create_generation_section(self, parent):
        """Create the generation section"""
        gen_frame = ctk.CTkFrame(parent)
        gen_frame.pack(fill="x", padx=10, pady=10)
        
        gen_label = ctk.CTkLabel(gen_frame, text="Generate Image", font=("Arial", 14, "bold"))
        gen_label.pack(pady=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            gen_frame, 
            text="Generate Image", 
            command=self.generate_image,
            fg_color="green"
        )
        self.generate_btn.pack(fill="x", padx=10, pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(gen_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(gen_frame, text="Ready to generate", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
    def create_history_section(self, parent):
        """Create the generation history section"""
        history_frame = ctk.CTkFrame(parent)
        history_frame.pack(fill="x", padx=10, pady=10)
        
        history_label = ctk.CTkLabel(history_frame, text="Generation History", font=("Arial", 14, "bold"))
        history_label.pack(pady=5)
        
        # History list
        history_list_frame = ctk.CTkFrame(history_frame)
        history_list_frame.pack(fill="x", padx=10, pady=5)
        
        self.history_listbox = tk.Listbox(history_list_frame, height=6, selectmode="single")
        self.history_list_frame = history_list_frame # Store the frame reference
        self.history_listbox.pack(fill="x", padx=5, pady=5)
        
        # Bind selection event
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        
        # History management buttons
        history_buttons_frame = ctk.CTkFrame(history_frame)
        history_buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # Load to canvas button
        self.load_to_canvas_btn = ctk.CTkButton(
            history_buttons_frame, 
            text="Load to Canvas", 
            command=self.load_to_canvas,
            state="disabled"
        )
        self.load_to_canvas_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            history_buttons_frame, 
            text="Delete", 
            command=self.delete_history_item,
            state="disabled",
            fg_color="red"
        )
        delete_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        # Store button references
        self.delete_btn = delete_btn
        
        # Clear all button
        clear_history_btn = ctk.CTkButton(
            history_frame, 
            text="Clear All History", 
            command=self.clear_history,
            fg_color="orange"
        )
        clear_history_btn.pack(fill="x", padx=10, pady=2)
        
        # Initialize history
        self.generation_history = []
        
    def on_service_change(self, value):
        """Handle service change"""
        if value == "custom":
            self.custom_endpoint_frame.pack(fill="x", padx=10, pady=5)
        else:
            self.custom_endpoint_frame.pack_forget()
            
        # Update info label based on selected service
        if hasattr(self, 'info_label'):
            if value == "local":
                self.info_label.configure(text="Note: Local generation - no internet required, uses your GPU/CPU. First run will download model (~4GB).")
            elif value == "stablehorde":
                self.info_label.configure(text="Note: Stable Horde is free but has rate limits. If you get 429 error, wait a few minutes.")
            elif value == "huggingface":
                self.info_label.configure(text="Note: Hugging Face requires API key. Get free key at huggingface.co")
            elif value == "falai":
                self.info_label.configure(text="Note: Fal.ai requires API key. Get free key at fal.ai")
            elif value == "openai":
                self.info_label.configure(text="Note: For OpenAI, negative prompt will be added to main prompt as 'Avoid: ...'")
            else:
                self.info_label.configure(text="")
            
    def test_connection(self):
        """Test API connection"""
        self.status_label.configure(text="Testing connection...")
        self.progress_bar.set(0.2)
        
        try:
            if self.service_var.get() == "local":
                # Test local generation (check if diffusers is available)
                try:
                    import sys
                    import os
                    print(f"DEBUG TEST CONNECTION:")
                    print(f"  Python executable: {sys.executable}")
                    print(f"  Python version: {sys.version}")
                    print(f"  Current working dir: {os.getcwd()}")
                    print(f"  Python path: {sys.path[:3]}...")
                    
                    # Test basic imports first
                    print("  Testing torch import...")
                    import torch
                    print(f"  SUCCESS: torch imported from: {torch.__file__}")
                    
                    print("  Testing diffusers import...")
                    from diffusers import StableDiffusionPipeline
                    print(f"  SUCCESS: diffusers imported")
                    
                    self.status_label.configure(text="Local generation ready!")
                    self.progress_bar.set(1.0)
                    self.editor.update_status("Local generation test successful - diffusers available")
                    print("  TEST CONNECTION: SUCCESS!")
                    
                except Exception as e:
                    import sys
                    import os
                    print(f"DEBUG TEST CONNECTION FAILED:")
                    print(f"  Python executable: {sys.executable}")
                    print(f"  Python version: {sys.version}")
                    print(f"  Current working dir: {os.getcwd()}")
                    print(f"  Python path: {sys.path[:3]}...")
                    print(f"  ERROR: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    self.status_label.configure(text=f"Local generation error: {str(e)}")
                    self.progress_bar.set(0)
                    self.editor.update_status(f"Local generation error: {str(e)}")
            elif self.service_var.get() == "stablehorde":
                # Test Stable Horde connection (no API key needed)
                response = requests.get("https://stablehorde.net/api/v2/status/models")
                if response.status_code == 200:
                    self.status_label.configure(text="Stable Horde connection successful!")
                    self.progress_bar.set(1.0)
                    self.editor.update_status("Stable Horde connection test successful")
                else:
                    self.status_label.configure(text=f"Stable Horde connection failed: {response.status_code}")
                    self.progress_bar.set(0)
                    self.editor.update_status(f"Stable Horde connection test failed: {response.status_code}")
            else:
                # Other services require API key
                api_key = self.api_key_entry.get().strip()
                if not api_key:
                    self.editor.update_status("Please enter an API key")
                    return
                    
                # Test with a simple request
                if self.service_var.get() == "openai":
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    response = requests.get("https://api.openai.com/v1/models", headers=headers)
                elif self.service_var.get() == "stability":
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    response = requests.get("https://api.stability.ai/v1/user/balance", headers=headers)
                else:
                    # Custom endpoint
                    custom_url = self.custom_endpoint_entry.get().strip()
                    if not custom_url:
                        self.editor.update_status("Please enter custom endpoint URL")
                        return
                        
                    headers = {"Authorization": f"Bearer {api_key}"}
                    response = requests.get(custom_url, headers=headers)
                    
                if response.status_code == 200:
                    self.status_label.configure(text="Connection successful!")
                    self.progress_bar.set(1.0)
                    self.editor.update_status("API connection test successful")
                else:
                    self.status_label.configure(text=f"Connection failed: {response.status_code}")
                    self.progress_bar.set(0)
                    self.editor.update_status(f"API connection test failed: {response.status_code}")
                
        except Exception as e:
            self.status_label.configure(text=f"Connection error: {str(e)}")
            self.progress_bar.set(0)
            self.editor.update_status(f"API connection test error: {str(e)}")
            
    def load_example_prompt(self, prompt):
        """Load an example prompt"""
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", prompt)
        
    def clear_prompts(self):
        """Clear all prompts"""
        self.prompt_text.delete("1.0", tk.END)
        self.negative_prompt_text.delete("1.0", tk.END)
        
    def generate_image(self):
        """Generate image using AI"""
        # Check if API key is needed
        if self.service_var.get() not in ["stablehorde", "local"]:
            api_key = self.api_key_entry.get().strip()
            if not api_key:
                self.editor.update_status("Please enter an API key")
                return
        else:
            api_key = None  # Stable Horde and local generation don't need API key
            
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            self.editor.update_status("Please enter a prompt")
            return
            
        # Disable generate button
        self.generate_btn.configure(state="disabled", text="Generating...")
        self.status_label.configure(text="Generating image...")
        self.progress_bar.set(0.1)
        
        try:
            if self.service_var.get() == "local":
                self.generate_local_image(prompt)
            elif self.service_var.get() == "stablehorde":
                self.generate_stablehorde_image(prompt)
            elif self.service_var.get() == "huggingface":
                self.generate_huggingface_image(prompt)
            elif self.service_var.get() == "falai":
                self.generate_falai_image(prompt)
            elif self.service_var.get() == "openai":
                self.generate_openai_image(api_key, prompt)
            elif self.service_var.get() == "stability":
                self.generate_stability_image(api_key, prompt)
            else:
                self.generate_custom_image(api_key, prompt)
                
        except Exception as e:
            self.status_label.configure(text=f"Generation error: {str(e)}")
            self.progress_bar.set(0)
            self.generate_btn.configure(state="normal", text="Generate Image")
            self.editor.update_status(f"Image generation error: {str(e)}")
            
    def generate_local_image(self, prompt):
        """Generate image using local Stable Diffusion model"""
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        try:
            import torch
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
            from PIL import Image
            import io
            
            self.progress_bar.set(0.2)
            self.status_label.configure(text="Loading model...")
            
            # Use smaller model for faster generation
            model_id = "stabilityai/stable-diffusion-2-1"
            
            # Load pipeline
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            pipe.enable_attention_slicing()
            
            # Move to GPU if available
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
                self.editor.update_status("Using GPU for generation")
            else:
                self.editor.update_status("Using CPU for generation (slower)")
            
            self.progress_bar.set(0.4)
            self.status_label.configure(text="Generating image...")
            
            # Map size to model format
            size_mapping = {
                "256x256": (256, 256),
                "512x512": (512, 512),
                "1024x1024": (512, 512),  # Limit to 512 for stability
                "1024x1792": (512, 768),
                "1792x1024": (768, 512)
            }
            
            selected_size = self.size_var.get()
            height, width = size_mapping.get(selected_size, (512, 512))
            
            # Generate image
            result = pipe(
                prompt,
                negative_prompt=negative_prompt if negative_prompt else None,
                num_inference_steps=20,
                guidance_scale=7.5,
                height=height,
                width=width
            )
            
            self.progress_bar.set(0.8)
            self.status_label.configure(text="Saving image...")
            
            # Get the generated image
            image = result.images[0]
            
            # Save image to file
            ai_folder = os.path.join(os.getcwd(), "ai_generated_images")
            if not os.path.exists(ai_folder):
                os.makedirs(ai_folder)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_generated_{timestamp}_1.png"
            filepath = os.path.join(ai_folder, filename)
            
            image.save(filepath)
            
            # Load image to canvas
            self.editor.add_image(filepath)
            
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Generation complete!")
            self.editor.update_status(f"Generated 1 image locally. Saved in: {ai_folder}")
            
        except Exception as e:
            self.status_label.configure(text=f"Local generation error: {str(e)}")
            self.progress_bar.set(0)
            self.editor.update_status(f"Local generation error: {str(e)}")
        finally:
            self.generate_btn.configure(state="normal", text="Generate Image")
            
    def generate_huggingface_image(self, prompt):
        """Generate image using Hugging Face (free, no API key required)"""
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Map size to Hugging Face format
        size_mapping = {
            "256x256": (256, 256),
            "512x512": (512, 512),
            "1024x1024": (512, 512),  # HF has limits, use 512x512
            "1024x1792": (512, 768),
            "1792x1024": (768, 512)
        }
        
        selected_size = self.size_var.get()
        width, height = size_mapping.get(selected_size, (512, 512))
        
        # Hugging Face request format
        data = {
            "inputs": prompt,
            "parameters": {
                "width": width,
                "height": height,
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        }
        
        if negative_prompt:
            data["parameters"]["negative_prompt"] = negative_prompt
            
        self.progress_bar.set(0.3)
        
        try:
            print(f"DEBUG: Hugging Face request URL: {url}")
            print(f"DEBUG: Hugging Face request headers: {headers}")
            print(f"DEBUG: Hugging Face request data: {data}")
            
            response = requests.post(url, headers=headers, json=data)
            print(f"DEBUG: Hugging Face response status: {response.status_code}")
            print(f"DEBUG: Hugging Face response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                # Hugging Face returns image data directly
                image_data = response.content
                print(f"DEBUG: Downloaded image data size: {len(image_data)} bytes")
                
                if len(image_data) > 1000:  # Valid image should be larger
                    # Save image to file
                    ai_folder = os.path.join(os.getcwd(), "ai_generated_images")
                    if not os.path.exists(ai_folder):
                        os.makedirs(ai_folder)
                        print(f"DEBUG: Created AI images folder: {ai_folder}")
                    
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ai_generated_{timestamp}_1.png"
                    filepath = os.path.join(ai_folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    print(f"DEBUG: Image saved to: {filepath}")
                    
                    # Process the image
                    self.process_image_data(image_data, f"Hugging Face - {prompt[:30]}...")
                    
                    self.progress_bar.set(1.0)
                    self.status_label.configure(text="Generation complete!")
                    self.editor.update_status(f"Generated 1 image via Hugging Face. Saved in: {ai_folder}")
                else:
                    self.status_label.configure(text="Invalid image data received")
                    self.progress_bar.set(0)
                    self.editor.update_status("Hugging Face returned invalid image data")
            elif response.status_code == 503:
                # Model is loading
                self.status_label.configure(text="Model is loading, please wait...")
                self.progress_bar.set(0.5)
                self.editor.update_status("Hugging Face model is loading. Please try again in a moment.")
            else:
                self.status_label.configure(text=f"Hugging Face error: {response.status_code}")
                self.progress_bar.set(0)
                self.editor.update_status(f"Hugging Face error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"DEBUG: Hugging Face error: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.configure(text=f"Hugging Face error: {str(e)}")
            self.progress_bar.set(0)
            self.editor.update_status(f"Hugging Face error: {str(e)}")
        finally:
            self.generate_btn.configure(state="normal", text="Generate Image")
            
    def generate_falai_image(self, prompt):
        """Generate image using Fal.ai (free, no API key required)"""
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        url = "https://fal.run/fal-ai/flux/schnell"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Map size to Fal.ai format
        size_mapping = {
            "256x256": "square_hd",
            "512x512": "square_hd", 
            "1024x1024": "square_hd",
            "1024x1792": "portrait_4_3",
            "1792x1024": "landscape_4_3"
        }
        
        selected_size = self.size_var.get()
        aspect_ratio = size_mapping.get(selected_size, "square_hd")
        
        # Fal.ai request format
        data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "num_inference_steps": 4,
            "enable_safety_checker": True
        }
        
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
            
        self.progress_bar.set(0.3)
        
        try:
            print(f"DEBUG: Fal.ai request URL: {url}")
            print(f"DEBUG: Fal.ai request headers: {headers}")
            print(f"DEBUG: Fal.ai request data: {data}")
            
            response = requests.post(url, headers=headers, json=data)
            print(f"DEBUG: Fal.ai response status: {response.status_code}")
            print(f"DEBUG: Fal.ai response text: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"DEBUG: Fal.ai full response: {result}")
                
                if "images" in result and result["images"]:
                    self.progress_bar.set(0.8)
                    self.status_label.configure(text="Processing generated image...")
                    
                    # Process the first image
                    image_url = result["images"][0]["url"]
                    print(f"DEBUG: Fal.ai image URL: {image_url}")
                    
                    # Download the image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        image_data = img_response.content
                        print(f"DEBUG: Downloaded image data size: {len(image_data)} bytes")
                        
                        # Save image to file
                        ai_folder = os.path.join(os.getcwd(), "ai_generated_images")
                        if not os.path.exists(ai_folder):
                            os.makedirs(ai_folder)
                            print(f"DEBUG: Created AI images folder: {ai_folder}")
                        
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"ai_generated_{timestamp}_1.png"
                        filepath = os.path.join(ai_folder, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(image_data)
                        print(f"DEBUG: Image saved to: {filepath}")
                        
                        # Process the image
                        self.process_image_data(image_data, f"Fal.ai - {prompt[:30]}...")
                        
                        self.progress_bar.set(1.0)
                        self.status_label.configure(text="Generation complete!")
                        self.editor.update_status(f"Generated 1 image via Fal.ai. Saved in: {ai_folder}")
                    else:
                        self.status_label.configure(text=f"Failed to download image: {img_response.status_code}")
                        self.progress_bar.set(0)
                        self.editor.update_status(f"Failed to download generated image: {img_response.status_code}")
                else:
                    self.status_label.configure(text="No images in response")
                    self.progress_bar.set(0)
                    self.editor.update_status("Fal.ai returned no images")
            else:
                self.status_label.configure(text=f"Fal.ai error: {response.status_code}")
                self.progress_bar.set(0)
                self.editor.update_status(f"Fal.ai error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"DEBUG: Fal.ai error: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.configure(text=f"Fal.ai error: {str(e)}")
            self.progress_bar.set(0)
            self.editor.update_status(f"Fal.ai error: {str(e)}")
        finally:
            self.generate_btn.configure(state="normal", text="Generate Image")
            
    def generate_stablehorde_image(self, prompt):
        """Generate image using Stable Horde (free, no API key required)"""
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        url = "https://stablehorde.net/api/v2/generate/async"
        headers = {
            "Content-Type": "application/json",
            "apikey": "0000000000"  # Anonymous key for Stable Horde
        }
        
        # Map size to Stable Horde format
        size_mapping = {
            "256x256": (256, 256),
            "512x512": (512, 512),
            "1024x1024": (1024, 1024),
            "1024x1792": (1024, 1792),
            "1792x1024": (1792, 1024)
        }
        
        selected_size = self.size_var.get()
        width, height = size_mapping.get(selected_size, (1024, 1024))
        
        # Stable Horde API v2 format - simplified working version
        data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": 20,
            "cfg_scale": 7.0,
            "sampler_name": "k_euler_a",
            "n": 1,
            "seed": -1
        }
        
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
            
        self.progress_bar.set(0.3)
        
        try:
            # Log the request for debugging
            print(f"DEBUG: Stable Horde request URL: {url}")
            print(f"DEBUG: Stable Horde request headers: {headers}")
            print(f"DEBUG: Stable Horde request data: {data}")
            
            # Submit generation request
            response = requests.post(url, headers=headers, json=data)
            
            print(f"DEBUG: Stable Horde response status: {response.status_code}")
            print(f"DEBUG: Stable Horde response text: {response.text}")
            
            if response.status_code == 202:
                result = response.json()
                generation_id = result["id"]
                
                self.progress_bar.set(0.5)
                self.status_label.configure(text="Waiting for generation to complete...")
                
                # Poll for completion
                self.poll_stablehorde_generation(generation_id)
            elif response.status_code == 429:
                # Rate limited on initial request
                self.status_label.configure(text="Rate limited. Please wait a moment and try again.")
                self.progress_bar.set(0)
                self.editor.update_status("Stable Horde is rate limited. Please try again in a few minutes.")
            else:
                error_msg = f"Stable Horde error: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('message', 'Unknown error')}"
                        # Log the full error for debugging
                        print(f"DEBUG: Stable Horde error details: {error_data}")
                    except:
                        error_msg += f" - {response.text}"
                        print(f"DEBUG: Stable Horde raw error: {response.text}")
                
                # Log the request data for debugging
                print(f"DEBUG: Stable Horde request data: {data}")
                        
                self.status_label.configure(text=error_msg)
                self.progress_bar.set(0)
                self.editor.update_status(error_msg)
                
        except Exception as e:
            self.status_label.configure(text=f"Stable Horde error: {str(e)}")
            self.progress_bar.set(0)
            self.editor.update_status(f"Stable Horde error: {str(e)}")
            
        # Re-enable generate button
        self.generate_btn.configure(state="normal", text="Generate Image")
        
    def poll_stablehorde_generation(self, generation_id):
        """Poll Stable Horde for generation completion"""
        url = f"https://stablehorde.net/api/v2/generate/status/{generation_id}"
        self.retry_count = 0
        self.max_retries = 5

        def check_status():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    result = response.json()
                    if result["done"]:
                        self.progress_bar.set(0.8)
                        self.status_label.configure(text="Downloading generated images...")

                        if "generations" not in result or not result["generations"]:
                            self.editor.update_status("No images generated - API returned empty result")
                            self.generate_btn.configure(state="normal", text="Generate Image")
                            return

                        for i, generation in enumerate(result["generations"]):
                            if generation.get("img"):
                                try:
                                    # Dekoduj base64 do bajtów
                                    image_data = base64.b64decode(generation["img"])
                                    # Otwórz obraz PIL z bajtów
                                    img = Image.open(BytesIO(image_data))
                                    img.load()  # Wymuś wczytanie, by złapać ewentualny błąd
                                    # Zapisz jako PNG
                                    ai_folder = os.path.join(os.getcwd(), "ai_generated_images")
                                    if not os.path.exists(ai_folder):
                                        os.makedirs(ai_folder)
                                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                    filename = f"ai_generated_{timestamp}_{i+1}.png"
                                    filepath = os.path.join(ai_folder, filename)
                                    img.save(filepath, format="PNG")
                                    # Dodaj do edytora
                                    self.editor.add_image(filepath)
                                    self.editor.update_status(f"AI image loaded: {filename}")
                                except Exception as e:
                                    self.editor.update_status(f"Error decoding generated image: {str(e)}")
                            else:
                                self.editor.update_status("API response missing image data")

                        self.progress_bar.set(1.0)
                        self.status_label.configure(text="Generation complete!")
                        ai_folder = os.path.join(os.getcwd(), "ai_generated_images")
                        self.editor.update_status(f"Generated {len(result['generations'])} images via Stable Horde. Saved in: {ai_folder}")
                        self.generate_btn.configure(state="normal", text="Generate Image")
                    else:
                        # Still processing, check again in 3 seconds
                        wait_time = result.get('wait_time', 0)
                        self.ai_window.after(3000, check_status)
                        self.status_label.configure(text=f"Generating... (Queue: {wait_time}s wait)")
                elif response.status_code == 429:
                    self.retry_count += 1
                    if self.retry_count <= self.max_retries:
                        wait_time = 10 + (self.retry_count * 5)
                        self.status_label.configure(text=f"Rate limited. Retrying in {wait_time}s... (Attempt {self.retry_count}/{self.max_retries})")
                        self.ai_window.after(wait_time * 1000, check_status)
                    else:
                        self.status_label.configure(text="Rate limited. Too many retries. Please try again later.")
                        self.progress_bar.set(0)
                        self.generate_btn.configure(state="normal", text="Generate Image")
                else:
                    error_msg = f"Error checking status: {response.status_code}"
                    if response.text:
                        try:
                            error_data = response.json()
                            error_msg += f" - {error_data.get('message', 'Unknown error')}"
                        except:
                            error_msg += f" - {response.text}"

                    self.status_label.configure(text=error_msg)
                    self.progress_bar.set(0)
                    self.generate_btn.configure(state="normal", text="Generate Image")
                    self.editor.update_status(error_msg)

            except Exception as e:
                self.status_label.configure(text=f"Error polling status: {str(e)}")
                self.progress_bar.set(0)
                self.generate_btn.configure(state="normal", text="Generate Image")
                self.editor.update_status(f"Error polling status: {str(e)}")

        # Start polling
        check_status()

    def generate_openai_image(self, api_key, prompt):
        """Generate image using OpenAI DALL-E"""
        # Note: OpenAI DALL-E 3 doesn't support negative_prompt parameter
        # We'll include negative prompt in the main prompt instead
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        # Combine main prompt with negative prompt if provided
        if negative_prompt:
            full_prompt = f"{prompt}. Avoid: {negative_prompt}"
        else:
            full_prompt = prompt
        
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": full_prompt,
            "size": self.size_var.get(),
            "quality": self.quality_var.get(),
            "style": self.style_var.get(),
            "n": int(self.count_var.get())
        }
            
        self.progress_bar.set(0.3)
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.progress_bar.set(0.7)
            
            # Process generated images
            for i, image_data in enumerate(result["data"]):
                image_url = image_data["url"]
                self.download_and_process_image(image_url, f"OpenAI DALL-E - {prompt[:30]}...")
                
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Generation complete!")
            self.editor.update_status(f"Generated {len(result['data'])} images")
        else:
            error_msg = f"OpenAI API error: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', 'Unknown error')}"
                except:
                    error_msg += f" - {response.text}"
                    
            self.status_label.configure(text=error_msg)
            self.progress_bar.set(0)
            self.editor.update_status(error_msg)
            
        # Re-enable generate button
        self.generate_btn.configure(state="normal", text="Generate Image")
        
    def generate_stability_image(self, api_key, prompt):
        """Generate image using Stability AI"""
        negative_prompt = self.negative_prompt_text.get("1.0", tk.END).strip()
        
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7,
            "height": int(self.size_var.get().split("x")[1]),
            "width": int(self.size_var.get().split("x")[0]),
            "samples": int(self.count_var.get()),
            "steps": 30
        }
        
        if negative_prompt:
            data["text_prompts"].append({
                "text": negative_prompt,
                "weight": -1.0
            })
            
        self.progress_bar.set(0.3)
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.progress_bar.set(0.7)
            
            # Process generated images
            for i, artifact in enumerate(result["artifacts"]):
                image_data = base64.b64decode(artifact["base64"])
                self.process_image_data(image_data, f"Stability AI - {prompt[:30]}...")
                
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Generation complete!")
            self.editor.update_status(f"Generated {len(result['artifacts'])} images")
        else:
            error_msg = f"Stability AI API error: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('message', 'Unknown error')}"
                except:
                    error_msg += f" - {response.text}"
                    
            self.status_label.configure(text=error_msg)
            self.progress_bar.set(0)
            self.editor.update_status(error_msg)
            
        # Re-enable generate button
        self.generate_btn.configure(state="normal", text="Generate Image")
        
    def generate_custom_image(self, api_key, prompt):
        """Generate image using custom API endpoint"""
        custom_url = self.custom_endpoint_entry.get().strip()
        if not custom_url:
            self.status_label.configure(text="Please enter custom endpoint URL")
            self.progress_bar.set(0)
            self.generate_btn.configure(state="normal", text="Generate Image")
            return
            
        # This is a placeholder for custom API integration
        # Users would need to implement their own API call logic here
        self.status_label.configure(text="Custom API not implemented")
        self.progress_bar.set(0)
        self.generate_btn.configure(state="normal", text="Generate Image")
        self.editor.update_status("Custom API integration not implemented")
        
    def download_and_process_image(self, image_url, prompt):
        """Download and process image from URL"""
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                self.process_image_data(image_data, prompt)
            else:
                self.editor.update_status(f"Failed to download image: {response.status_code}")
        except Exception as e:
            self.editor.update_status(f"Error downloading image: {str(e)}")
            
    def process_image_data(self, image_data, prompt):
        """Process generated image data"""
        try:
            print(f"DEBUG: Processing image data, size: {len(image_data)} bytes")
            
            # Try different approaches to load the image
            image = None
            
            # Method 1: Direct PIL load
            try:
                image = Image.open(io.BytesIO(image_data))
                print(f"DEBUG: Method 1 - PIL direct load successful: {image.size}, mode: {image.mode}")
            except Exception as e1:
                print(f"DEBUG: Method 1 failed: {e1}")
                
                # Method 2: Try to detect format manually
                try:
                    # Check if it's a valid image by looking at the header
                    if image_data.startswith(b'\x89PNG'):
                        print("DEBUG: Detected PNG format")
                    elif image_data.startswith(b'\xff\xd8\xff'):
                        print("DEBUG: Detected JPEG format")
                    elif image_data.startswith(b'RIFF') and b'WEBP' in image_data[:20]:
                        print("DEBUG: Detected WEBP format")
                    
                    # Try loading with different formats
                    for fmt in ['PNG', 'JPEG', 'WEBP', 'BMP']:
                        try:
                            image = Image.open(io.BytesIO(image_data), formats=[fmt])
                            print(f"DEBUG: Method 2 - Loaded as {fmt}: {image.size}, mode: {image.mode}")
                            break
                        except:
                            continue
                            
                except Exception as e2:
                    print(f"DEBUG: Method 2 failed: {e2}")
                    
                    # Method 3: Try to fix the data
                    try:
                        # Sometimes the data needs to be cleaned
                        cleaned_data = image_data.strip()
                        image = Image.open(io.BytesIO(cleaned_data))
                        print(f"DEBUG: Method 3 - Cleaned data load successful: {image.size}, mode: {image.mode}")
                    except Exception as e3:
                        print(f"DEBUG: Method 3 failed: {e3}")
                        raise e3
            
            if image is None:
                raise Exception("Could not load image with any method")
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print(f"DEBUG: Converted image to RGB mode")
            
            # Add to history
            history_item = {
                'image': image,
                'prompt': prompt,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.generation_history.append(history_item)
            self.update_history_list()
            
            # Auto-load to canvas (load the last generated image)
            self.load_latest_image_to_canvas()
            print(f"DEBUG: Image added to history and loaded to canvas")
                
        except Exception as e:
            print(f"DEBUG: Error processing image: {e}")
            import traceback
            traceback.print_exc()
            self.editor.update_status(f"Error processing generated image: {str(e)}")
            
    def update_history_list(self):
        """Update the history listbox"""
        self.history_listbox.delete(0, tk.END)
        
        for i, item in enumerate(self.generation_history):
            display_text = f"{i+1}. {item['prompt'][:40]}... ({item['timestamp']})"
            self.history_listbox.insert(tk.END, display_text)
            
    def on_history_select(self, event):
        """Handle history selection"""
        selection = self.history_listbox.curselection()
        if selection:
            self.load_to_canvas_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
        else:
            self.load_to_canvas_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            
    def load_latest_image_to_canvas(self):
        """Load the latest generated image to canvas"""
        if not self.generation_history:
            return
            
        try:
            # Get the latest image (last in history)
            history_item = self.generation_history[-1]
            
            # Save image temporarily
            temp_path = f"temp_ai_generated_latest.png"
            history_item['image'].save(temp_path)
            
            # Add to editor
            self.editor.add_image(temp_path)
            
            # Remove temporary file
            os.remove(temp_path)
            
            self.editor.update_status(f"Loaded AI-generated image: {history_item['prompt'][:30]}...")
            print(f"DEBUG: Latest image loaded to canvas successfully")
            
        except Exception as e:
            print(f"DEBUG: Error loading latest image to canvas: {e}")
            self.editor.update_status(f"Error loading image to canvas: {str(e)}")
    
    def load_to_canvas(self):
        """Load selected image to canvas"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        history_item = self.generation_history[index]
        
        try:
            # Save image temporarily
            temp_path = f"temp_ai_generated_{index}.png"
            history_item['image'].save(temp_path)
            
            # Add to editor
            self.editor.add_image(temp_path)
            
            # Remove temporary file
            os.remove(temp_path)
            
            self.editor.update_status(f"Loaded AI-generated image: {history_item['prompt'][:30]}...")
            
        except Exception as e:
            self.editor.update_status(f"Error loading image to canvas: {str(e)}")
            
    def delete_history_item(self):
        """Delete selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        
        # Remove from history
        self.generation_history.pop(index)
        
        # Update list
        self.update_history_list()
        
        # Reset button states
        self.load_to_canvas_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        
        self.editor.update_status("History item deleted")
        
    def clear_history(self):
        """Clear all generation history"""
        if self.generation_history:
            self.generation_history.clear()
            self.update_history_list()
            
            # Reset button states
            self.load_to_canvas_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            
            self.editor.update_status("Generation history cleared")
