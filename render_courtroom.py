"""
Blender Courtroom Cinematic Render Script
==========================================
This script creates a cinematic flythrough of your courtroom with smooth camera keyframing.
Run this in Blender's Python console or as a script.

Usage:
    1. Open DraftCourt.blend in Blender
    2. Go to Scripting workspace
    3. Create new text file, paste this code
    4. Run the script (Alt+P)
"""

import bpy
import math
from mathutils import Vector

# ====================
# CONFIGURATION
# ====================
RENDER_RESOLUTION = (1920, 1080)
FPS = 24
DURATION_SECONDS = 90  # 90 second video
TOTAL_FRAMES = DURATION_SECONDS * FPS
OUTPUT_PATH = "//render_output.mp4"  # // means same directory as .blend
RENDER_ENGINE = "CYCLES"  # Best quality for architectural viz
RENDER_SAMPLES = 256  # Higher = more quality but slower
USE_DENOISER = True

# ====================
# SETUP RENDER SETTINGS
# ====================
def setup_render_settings():
    """Configure Blender render settings"""
    scene = bpy.context.scene
    
    # Render settings
    scene.render.resolution_x = RENDER_RESOLUTION[0]
    scene.render.resolution_y = RENDER_RESOLUTION[1]
    scene.render.fps = FPS
    scene.frame_end = TOTAL_FRAMES
    
    # Output
    scene.render.filepath = OUTPUT_PATH
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.image_settings.ffmpeg_codec = 'H264'
    scene.render.image_settings.ffmpeg_quality = 100
    
    # Render engine
    scene.render.engine = RENDER_ENGINE
    
    # Cycles settings
    if RENDER_ENGINE == "CYCLES":
        scene.cycles.samples = RENDER_SAMPLES
        scene.cycles.use_denoiser = USE_DENOISER
        scene.cycles.denoiser = 'OPTIX'  # Change to 'OPENIMAGEDENOISE' if OPTIX unavailable
        scene.cycles.use_adaptive_sampling = True
    
    print(f"✓ Render settings configured: {RENDER_RESOLUTION[0]}x{RENDER_RESOLUTION[1]} @ {FPS}fps")

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
    """Create a cinematic flythrough of the courtroom with smooth keyframes"""
    
    # Clear existing keyframes
    if camera.animation_data:
        camera.animation_data_clear()
    
    scene = bpy.context.scene
    
    # Define camera path waypoints with timing
    # Format: (frame, location, rotation_euler)
    # Adjust these based on your courtroom size/layout
    
    keyframes = [
        # Start: Front entrance view
        (0, Vector((0, -30, 3)), Vector((math.radians(0), 0, 0))),
        
        # Move through main courtroom area
        (int(TOTAL_FRAMES * 0.15), Vector((5, -20, 4)), Vector((math.radians(5), 0, math.radians(10)))),
        
        # Judge's bench area
        (int(TOTAL_FRAMES * 0.3), Vector((10, 5, 4)), Vector((math.radians(10), 0, math.radians(30)))),
        
        # Witness stand view
        (int(TOTAL_FRAMES * 0.45), Vector((15, 10, 5)), Vector((math.radians(15), 0, math.radians(50)))),
        
        # Jury box sweep
        (int(TOTAL_FRAMES * 0.6), Vector((-15, 15, 4)), Vector((math.radians(8), 0, math.radians(120)))),
        
        # Prosecution table
        (int(TOTAL_FRAMES * 0.75), Vector((8, 5, 3)), Vector((math.radians(5), 0, math.radians(200)))),
        
        # Defense table
        (int(TOTAL_FRAMES * 0.85), Vector((-10, 5, 3)), Vector((math.radians(5), 0, math.radians(280)))),
        
        # End: Overview from above
        (TOTAL_FRAMES - 1, Vector((0, 0, 12)), Vector((math.radians(60), 0, 0))),
    ]
    
    # Set keyframes with smooth interpolation
    for frame, location, rotation in keyframes:
        scene.frame_set(frame)
        
        # Location keyframes
        camera.location = location
        camera.keyframe_insert(data_path="location", frame=frame)
        
        # Rotation keyframes
        camera.rotation_euler = rotation
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    # Set smooth interpolation for all keyframes
    for fcurve in camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'AUTO'
            keyframe.handle_right_type = 'AUTO'
    
    print(f"✓ Created {len(keyframes)} camera keyframes with smooth interpolation")

# ====================
# SET FOCAL LENGTH
# ====================
def set_camera_properties(camera):
    """Configure camera lens properties"""
    camera.data.lens = 50  # 50mm lens (good for architectural viz)
    camera.data.sensor_width = 36  # Full-frame equivalent
    print(f"✓ Camera focal length set to 50mm")

# ====================
# RENDER VIDEO
# ====================
def render_video():
    """Render the final video"""
    scene = bpy.context.scene
    scene.frame_set(0)
    
    print(f"\n{'='*50}")
    print(f"Starting render: {TOTAL_FRAMES} frames @ {FPS}fps")
    print(f"Duration: {TOTAL_FRAMES / FPS} seconds")
    print(f"Output: {OUTPUT_PATH}")
    print(f"{'='*50}\n")
    
    bpy.ops.render.render(animation=True)
    print(f"\n✓ Render complete! Video saved to: {OUTPUT_PATH}")

# ====================
# MAIN EXECUTION
# ====================
def main():
    print("\n" + "="*50)
    print("BLENDER COURTROOM CINEMATIC RENDER")
    print("="*50 + "\n")
    
    # Setup
    setup_render_settings()
    camera = get_or_create_camera()
    set_camera_properties(camera)
    
    # Create animation
    create_courtroom_flythrough(camera)
    
    # Render
    render_video()
    
    print("\n" + "="*50)
    print("Process complete!")
    print("="*50)

# Run the script
if __name__ == "__main__":
    main()
