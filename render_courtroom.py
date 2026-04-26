"""
Blender Courtroom Cinematic Render Script
==========================================
This script creates a cinematic flythrough of your courtroom with smooth camera keyframing.
Renders to PNG image sequence (more reliable than video codec).

Usage:
    1. Open DraftCourt.blend in Blender
    2. Go to Scripting workspace
    3. Create NEW text file, paste this code
    4. Run the script (Alt+P)
    5. After rendering, convert images to video using FFmpeg or Blender's Video Sequence Editor
"""

import bpy
import math
from mathutils import Vector

# ====================
# CONFIGURATION
# ====================
RENDER_RESOLUTION = (1920, 1080)
FPS = 24
DURATION_SECONDS = 90
TOTAL_FRAMES = DURATION_SECONDS * FPS
OUTPUT_PATH = "//render_frames/"  # Will create PNG sequence
RENDER_ENGINE = "CYCLES"
RENDER_SAMPLES = 128
USE_DENOISER = True

# ====================
# SETUP RENDER SETTINGS
# ====================
def setup_render_settings():
    """Configure Blender render settings"""
    scene = bpy.context.scene
    
    scene.render.resolution_x = RENDER_RESOLUTION[0]
    scene.render.resolution_y = RENDER_RESOLUTION[1]
    scene.render.fps = FPS
    scene.frame_end = TOTAL_FRAMES
    
    # Output to PNG sequence (no codec issues)
    scene.render.filepath = OUTPUT_PATH
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.compression = 15
    
    scene.render.engine = RENDER_ENGINE
    
    # Cycles settings
    if RENDER_ENGINE == "CYCLES":
        scene.cycles.samples = RENDER_SAMPLES
        scene.cycles.use_denoiser = USE_DENOISER
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.adaptive_threshold = 0.01
    
    print(f"✓ Render settings configured: {RENDER_RESOLUTION[0]}x{RENDER_RESOLUTION[1]} @ {FPS}fps")
    print(f"✓ Output: PNG sequence to {OUTPUT_PATH}")

# ====================
# CREATE/GET CAMERA
# ====================
def get_or_create_camera():
    """Get existing camera or create new one"""
    scene = bpy.context.scene
    
    if scene.camera:
        camera = scene.camera
        print(f"✓ Using existing camera: {camera.name}")
    else:
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        scene.camera = camera
        print(f"✓ Created new camera: {camera.name}")
    
    return camera

# ====================
# CAMERA KEYFRAME PATHS
# ====================
def create_courtroom_flythrough(camera):
    """Create a cinematic flythrough with smooth keyframes"""
    
    if camera.animation_data:
        camera.animation_data_clear()
    
    scene = bpy.context.scene
    
    # Keyframes: (frame, location, rotation)
    # Adjust these based on your courtroom dimensions
    keyframes = [
        (0, Vector((0, -30, 3)), Vector((math.radians(0), 0, 0))),
        (int(TOTAL_FRAMES * 0.15), Vector((5, -20, 4)), Vector((math.radians(5), 0, math.radians(10)))),
        (int(TOTAL_FRAMES * 0.3), Vector((10, 5, 4)), Vector((math.radians(10), 0, math.radians(30)))),
        (int(TOTAL_FRAMES * 0.45), Vector((15, 10, 5)), Vector((math.radians(15), 0, math.radians(50)))),
        (int(TOTAL_FRAMES * 0.6), Vector((-15, 15, 4)), Vector((math.radians(8), 0, math.radians(120)))),
        (int(TOTAL_FRAMES * 0.75), Vector((8, 5, 3)), Vector((math.radians(5), 0, math.radians(200)))),
        (int(TOTAL_FRAMES * 0.85), Vector((-10, 5, 3)), Vector((math.radians(5), 0, math.radians(280)))),
        (TOTAL_FRAMES - 1, Vector((0, 0, 12)), Vector((math.radians(60), 0, 0))),
    ]
    
    for frame, location, rotation in keyframes:
        scene.frame_set(frame)
        camera.location = location
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.rotation_euler = rotation
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    # Smooth interpolation
    for fcurve in camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'AUTO'
            keyframe.handle_right_type = 'AUTO'
    
    print(f"✓ Created {len(keyframes)} camera keyframes with smooth interpolation")

# ====================
# SET CAMERA PROPERTIES
# ====================
def set_camera_properties(camera):
    """Configure camera lens properties"""
    camera.data.lens = 50
    camera.data.sensor_width = 36
    print(f"✓ Camera focal length set to 50mm")

# ====================
# RENDER
# ====================
def render_animation():
    """Render animation to PNG sequence"""
    scene = bpy.context.scene
    scene.frame_set(0)
    
    print(f"\n{'='*60}")
    print(f"Starting render: {TOTAL_FRAMES} frames @ {FPS}fps")
    print(f"Duration: {TOTAL_FRAMES / FPS} seconds")
    print(f"Output: PNG sequence")
    print(f"{'='*60}\n")
    
    bpy.ops.render.render(animation=True)
    print(f"\n✓ Render complete!")

# ====================
# MAIN
# ====================
def main():
    print("\n" + "="*60)
    print("BLENDER COURTROOM CINEMATIC RENDER")
    print("="*60 + "\n")
    
    setup_render_settings()
    camera = get_or_create_camera()
    set_camera_properties(camera)
    create_courtroom_flythrough(camera)
    render_animation()
    
    print("\n" + "="*60)
    print("Render complete! Frames saved to: render_frames/")
    print("\nTo create video from PNG sequence:")
    print("1. Use Video Sequence Editor in Blender")
    print("2. Or use FFmpeg command:")
    print("   ffmpeg -framerate 24 -i render_frames/####.png -c:v libx264 -crf 23 output.mp4")
    print("="*60)

if __name__ == "__main__":
    main()
