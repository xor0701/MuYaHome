import cv2
import time
import sys
import camera


class Record():
    def __init__(self):
        self.camera = camera.VideoCamera()

        self.start_time = float(sys.argv[1])

        self.video_path_name = 'Record/' + time.strftime('%Y-%m-%d %H시-%M분', time.localtime(self.start_time))+'.avi'

    def __del__(self):
        print("비디오 종료")
        del self.camera

    def get_frame(self):
        video_frame = self.camera.get_frame()

        return video_frame

    def video(self):
        cam = self.camera
        # fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        # 해당 카메라의 width, heigh, 초당 프레임 수
        w, h, fps = cam.get_info()
        # 해당 카메라의 초당 프레임 수 가져오기
        
        video = cv2.VideoWriter(self.video_path_name, codec, fps, (w, h))

        return video


record = Record() # 녹화 클래스
video = record.video()

while(True):
    video_frame = record.get_frame() # 비디오 녹화를 위한 frame 계속 돌림
    video.write(video_frame) # 녹화

    cv2.imshow('Record&Save', video_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

video.release() # VideoWriter 종료
cv2.destroyAllWindows()