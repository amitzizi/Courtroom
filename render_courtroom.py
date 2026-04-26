import bpy
import math
from mathutils import Vector

RENDER_RESOLUTION = (1920, 1080)
FPS = 24
DURATION_SECONDS = 90
TOTAL_FRAMES = DURATION_SECONDS * FPS
OUTPUT_PATH = "//render_frames/"
RENDER_ENGINE = "CYCLES"
RENDER_SAMPLES = 64

def setup_render_settings():
    scene = bpy.context.scene
    scene.render.resolution_x = RENDER_RESOLUTION[0]
    scene.render.resolution_y = RENDER_RESOLUTION[1]
    scene.render.fps = FPS
    scene.frame_end = TOTAL_FRAMES
    scene.render.filepath = OUTPUT_PATH
    scene.render.image_settings.file_format = 'PNG'
    scene.render.engine = RENDER_ENGINE
    
    if RENDER_ENGINE == "CYCLES":
        scene.cycles.samples = RENDER_SAMPLES
    
    print("Render settings configured")

def get_or_create_camera():
    scene = bpy.context.scene
    if scene.camera:
        camera = scene.camera
    else:
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        scene.camera = camera
    return camera

def create_courtroom_flythrough(camera):
    if camera.animation_data:
        camera.animation_data_clear()
    
    scene = bpy.context.scene
    
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
    
    print("Camera keyframes created")

def set_camera_properties(camera):
    camera.data.lens = 50
    camera.data.sensor_width = 36

def render_animation():
    scene = bpy.context.scene
    scene.frame_set(0)
    print("Starting render...")
    bpy.ops.render.render(animation=True)
    print("Render complete!")

def main():
    setup_render_settings()
    camera = get_or_create_camera()
    set_camera_properties(camera)
    create_courtroom_flythrough(camera)
    render_animation()

main()
