import cv2

"""
读取、保存视频
- cv2.VideoCapture(Cars.mp4)        读取视频文件
- cv2.VideoCapture(Cars%04d.jpg)    读取图片序列 
- cv2.VideoCapture(index)           读取摄像机
- cv2.VideoWriter(filename, apiPreference, fourcc, fps, frameSize[, isColor])  视频写入器
"""

if __name__ == "__main__":
    # 读取视频文件
    vid_capture = cv2.VideoCapture('Resources/cars.mp4')
    # 读取图片序列 Cars%04d.jpg 指定格式 Cars0001.jpg,Cars0002.jpg...
    # vid_capture_sequence = cv2.VideoCapture('Resources/Image_sequence/Cars%04d.jpg')
    # 读取摄像机，参数0表示第一个摄像头
    # vid_capture_webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # 判断是否成功打开视频
    if (vid_capture.isOpened() == False):
        print("Error opening the video file")
    else:
        # 获取宽高
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        frame_size = (frame_width, frame_height)

        # 获取帧速
        fps = int(vid_capture.get(5))
        print("Frame Rate : ", fps, "frames per second")

        # 获取总帧数
        frame_count = vid_capture.get(7)
        print("Frame count : ", frame_count)

        # 保存视频
        output = cv2.VideoWriter('Resources/output_video_from_file.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20,
                                 frame_size)
        while vid_capture.isOpened():
            ret, frame = vid_capture.read()
            if ret == True:
                # Write the frame to the output files
                output.write(frame)
            else:
                print('Stream disconnected')
                break

        vid_capture.release()
        output.release()