# #!/usr/bin/python3

import ffmpeg
import numpy as np

width = 1920
height = 1080

process1 = (   
    ffmpeg.input("C:\\Users\\Andrew\\Downloads\\GMT20220424-103837_Recording_avo_1920x1080-merged.mp4")
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run_async(pipe_stdout=True)
)

process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    .output('outtest.mp4', pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

whitePixel = np.array([255,255,255])

while True:
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break

    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )

    # Find pixel at (37,1068)
    targetPixel = in_frame[1067, 36]
    
    # Skip if not HEX #FFF
    if not all([targetPixel[0] == 255, targetPixel[1] == 255, targetPixel[2] == 255]):
        continue

    process2.stdin.write(
        in_frame
        # out_frame
        .astype(np.uint8)
        .tobytes()
    )

process2.stdin.close()
process1.wait()
process2.wait()