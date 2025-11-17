# Graphics-Editor-Pro
Graphics Editor Pro is a modular Python desktop app for image editing and creation using CustomTkinter. Features include drawing, filters, text editing, cropping, resizing, rotation, layer management, batch processing, and AI-based image generation from text prompts.

## Quick summary
Entry point: main.py - launches the GUI and orchestrates all menus and canvas operations.
Each feature lives in a separate module (e.g. filters_menu.py, draw_menu.py) that is instantiated from main.py when the related menu is opened.
Outputs are saved to folders such as batch_output, advanced_batch_output, and ai_generated_images.

## Requirements
Python 3.8+ (project was also tested with Python 3.7–3.11 for local Stable Diffusion GPU generation use a recent Python and CUDA-enabled PyTorch).

customtkinter, Pillow, numpy, libraries are required for the GUI and image processing.

torch and diffusers are required only for the local Stable Diffusion generation (ai_menu local mode). 

## File overview
main.py - Application entry point and GUI orchestrator. Creates the main window, canvas and menu buttons, loads menu classes on demand, manages image stack, undo/redo, selection, drag & drop on canvas and overall state.

file_menu.py - File operations window (load single/multiple images, load folder, save current/composite/canvas, delete images, stack management like bring to front/back, reset canvas).

filters_menu.py - Image filters and RGB adjustments. Provides standard filters (sepia, grayscale, invert, blur, sharpen, etc.) and sliders for custom RGB/brightness/contrast with live preview and apply-to-target options.

draw_menu.py - Drawing tools: freehand drawing, shapes, color picker, line styles, eraser, clear/undo drawing actions; draws directly on the canvas as separate drawing layers.

text_menu.py - Add/edit text elements on the canvas. Controls font, size, color, style (bold/italic/underline), position (click or coordinates) and an editable list of text elements.

rotate_menu.py - Rotate and mirror tools. Quick rotation buttons, custom angle, mouse-driven rotation, rotate canvas, mirror (flip) images, apply to single or all images.

trim_menu.py - Crop and resize tools. Activate crop mode, manual coordinate crop, resize by px or percent, real-time scaling preview and position adjustments.

batch_menu.py - Simple batch processor: configure rotation/scale/filter/color variations and generate multiple image variants in an output folder (defaults to batch_output).

advanced_batch_menu.py - Advanced batch processing with placeholders for ML algorithms, style transfer, custom transforms and more advanced output controls (defaults to advanced_batch_output). Some ML parts are placeholders (e.g. LightGlue) and need real implementations if required.

ai_menu.py - AI image generation UI. Supports multiple services: local (diffusers / Stable Diffusion), Stable Horde, Hugging Face inference, Fal.ai, OpenAI, Stability AI and custom endpoints. Handles prompts,  generation settings and history; saves results to ai_generated_images and auto-loads them to the canvas.
