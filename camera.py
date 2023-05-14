def camera_function(x):
    from time import sleep

    from picamera2 import Picamera2, Preview

    picam2 = Picamera2()

    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QTGL)

    picam2.start()
    sleep(1)

    metadata = picam2.capture_file("test%s.jpg"%x)

    print(metadata)
    # picam2.close()

    sleep(2)

    picam2.close()

def new_camera():
    for i in range(2):
        camera_function(i)

def video_function():
    
    # working of the camera to record a video for the purpose of ease
    import time

    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder

    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    encoder = H264Encoder(10000000)

    picam2.start_recording(encoder, 'test.h264')

    time.sleep(5)

    picam2.stop_recording()
    picam2.close()

