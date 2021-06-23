import cv2
import time

class VideoCamera(object):
    def __init__(self):
        # 스트리밍 영상 가져옴
        streaming = 'http://220.81.195.100:5000/index.html'
        self.video = cv2.VideoCapture(streaming)

    def __del__(self):
        print("영상 해제")
        self.video.release()

    def get_frame(self):
        # 영상의 단일 프레임 캡처
        ret, frame = self.video.read()
        return frame

    def get_info(self):
        # 웹캠의 속성 값을 받아오기
        # 영상의 width, height 정수 형태로 변환하기 위해 round
        w = round(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = round(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 영상의 초당 프레임 수
        fps = self.video.get(cv2.CAP_PROP_FPS)
        return w, h, fps

