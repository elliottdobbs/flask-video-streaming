import io
import time
from picamera2 import Picamera2, Preview
from base_camera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with Picamera2() as camera:
            camera.configure(camera.create_video_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores"))
            camera.start()

            # let camera warm up
            time.sleep(2) 

            stream = io.BytesIO()
            try:
                while True:
                    camera.capture_file(stream, format='jpeg')
                    stream.seek(0)
                    yield stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()
            finally:
                camera.stop()