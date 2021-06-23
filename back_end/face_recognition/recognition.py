'''
많은 머신 러닝 알고리즘이 구현되어 있는 dlib와 
그것을 얼굴 인식 기능에 촛점을 맞춘 wrapper인 
face_recognition 패키지를 이용
'''

import face_recognition
import cv2
import camera
import os
import time
import requests
import numpy as np
import sys
import dlib

from imutils import face_utils
from tensorflow.keras.models import load_model


class FaceRecog():
    def __init__(self):
        # 스트리밍 영상 가져옴
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = [] 

        # 사진 로드 후, 학습
        dirname = 'C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name) # 저장된 얼굴사진 추가
                pathname = os.path.join(dirname, filename) # 저장된 얼굴사진 경로 추가

                img = face_recognition.load_image_file(pathname) # 얼굴사진 불러오기
                # 사진에서 얼굴 영역을 알아내고, 
                # face landmarks라 불리는 68개 얼굴 특징의 위치를 분석
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding) # 분석한 데이터 추가

        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        self.count = 0
        self.face_signal = 'False'
        self.start_time = float(sys.argv[1])
        
        self.face_url = "http://118.67.130.241:8080/face"

        self.accurcy = 0

    def __del__(self):
        print("카메라 종료")
        del self.camera

    def get_frame(self):
        # 영상의 단일 프레임 캡처
        frame = self.camera.get_frame()

        # 계산량을 줄이기 위해서 영상으로부터 frame을 읽어서 1/4 크기로 줄임
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # OpenCV RGB color에서 face_recognition에서 사용할 RGB color로 변환
        rgb_small_frame = small_frame[:, :, ::-1]

        # 계산 양을 더 줄이기 위해서 두 frame당 1번씩만 계산
        if self.process_this_frame:
            # 현재 영상 frame에서 모든 얼굴 및 얼굴 인코딩을 찾음
            # 읽은 frame에서 얼굴 영역과 특징을 추출
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            
            for face_encoding in self.face_encodings:
                # 얼굴이 저장된 사진과 같은지 확인
                # frame에서 추출한 얼굴 특징과 knowns에 있던 얼굴 사진의 특징을 비교하여, 얼마나 비슷한지 거리 척도로 환산 
                # 거리가 가깝다는 것 즉, distance가 작다는 것으로써 비슷한 얼굴이라는 의미
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # 거리가 0.7 이하라면 모르는 얼굴로 설정
                self.name = "Unknown"

                if min_value < 0.3: # 낮출수록 엄격함
                    # distances의 최소값을 가진 사람의 이름을 찾음
                    index = np.argmin(distances)
                    # name이 1011 : 101호 1번째, 1012 : 101호 2번째, 2011 : 201호 1번째, ... 이렇게 되어있음
                    self.name = self.known_face_names[index]
                    self.name = str(self.name)[:-1] # ex) 1011 -> 101
                    print("known")

                    self.count += 1
                    
                print(self.name)

                self.accurcy = 1-min_value # 정확도
                print(self.accurcy) 

                self.face_names.append(self.name)

        self.process_this_frame = not self.process_this_frame # True -> Fasle

        # 인식한 사람의 얼굴 영역과 이름을 화면에 그림
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # 감지한 frame이 위에서 1/4 크기로 조정되었으므로 백업 얼굴 위치를 조정
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # 얼굴 주위에 박스를 그림
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # 얼굴 아래에 이름이 있는 라벨을 그림
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 5, bottom - 5), font, 1.0, (255, 255, 255), 1)
            accuracy_text = str(round(self.accurcy*100, 2)) + "%"
            cv2.putText(frame, accuracy_text, (left + 10, bottom + 25), font, 1.0, (255, 255, 255), 1)

        return frame


class EyeBlinkDetector():
    def __init__(self):
        self.IMG_SIZE = (34, 26)

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/shape_predictor_68_face_landmarks.dat')

        self.model = load_model('C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/models/2021_06_19_22_45_22.h5')
        # self.model.summary()

        self.camera = camera.VideoCamera()

        self.count = 0
        self.count_bool = True

    def __del__(self):
        print("카메라 종료")
        del self.camera

    def crop_eye(self, img, eye_points):
        camera = self.camera.get_frame()
        camera = cv2.resize(camera, dsize=(0, 0), fx=0.5, fy=0.5)

        img = camera.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # faces = self.detector(gray)

        x1, y1 = np.amin(eye_points, axis=0)
        x2, y2 = np.amax(eye_points, axis=0)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        w = (x2 - x1) * 1.2
        h = w * self.IMG_SIZE[1] / self.IMG_SIZE[0]

        margin_x, margin_y = w/2, h/2

        min_x, min_y = int(cx - margin_x), int(cy - margin_y)
        max_x, max_y = int(cx + margin_x), int(cy + margin_y)

        eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

        eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

        return eye_img, eye_rect

    def get_frame(self):
        frame = self.camera.get_frame()

        frame = cv2.resize(frame, dsize=(0, 0), fx=0.5, fy=0.5)

        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector(gray)

        for face in faces:
            shapes = self.predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)

            eye_img_l, eye_rect_l = self.crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = self.crop_eye(gray, eye_points=shapes[42:48])

            eye_img_l = cv2.resize(eye_img_l, dsize=self.IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=self.IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            cv2.imshow('l', eye_img_l)
            cv2.imshow('r', eye_img_r)

            eye_input_l = eye_img_l.copy().reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.

            pred_l = self.model.predict(eye_input_l)
            pred_r = self.model.predict(eye_input_r)

            # visualize
            if ((pred_l > 0.01) & (pred_r > 0.01)):
                if (self.count_bool==False):
                    self.count_bool = True

                # print("눈 감지 않음")
            else:
                if (self.count_bool==True):
                    self.count += 1
                    self.count_bool = False

                # print("눈 감음")

            # print(pred_l, pred_r)

            cv2.rectangle(frame, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
            cv2.rectangle(frame, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,255,255), thickness=2)

            cv2.putText(frame, str(round(pred_l[0][0], 3)), tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(frame, str(round(pred_r[0][0], 3)), tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        return frame

eye_blink_detector = EyeBlinkDetector()

face_recog = FaceRecog() # 얼굴인식 클래스
print(face_recog.known_face_names)


while True:
    new_time = round(time.time(), 3)
    
    # 120초 안에 얼굴인식이 되지 않으면 카메라 끄기
    if ((new_time-face_recog.start_time) > 120):
        # pir 센서 서버에 얼굴인식이 되지 않았다는 값 보내기
        face_recog.face_signal = 'False'
        print(face_recog.face_signal) # python-shell에 보내서 쓰기위함
        
        break
    else:
        eye_frame = eye_blink_detector.get_frame()
        cv2.imshow("Eye_Frame", eye_frame)

        if (eye_blink_detector.count>=2):
            # print("눈 깜빡임 2번 이후 얼굴인식 시작")

            frame = face_recog.get_frame()
            cv2.imshow("Frame", frame) # 얼굴인식 화면

            # 얼굴인식
            if (face_recog.count==3): # 얼굴인식된 횟수
                # pir 센서 서버에 얼굴인식이 됬다는 값 보내기
                face_recog.face_signal = 'True'
                print(face_recog.face_signal) # python-shell에 보내서 쓰기위함

                # 인식된 id 값 보내기
                face_data = {
                    'face_id' : face_recog.name
                }
                face_headers = {'Content-Type':'application/json; charset=utf-8'}
                face_cookies = {'face_id_cookie':'face_id_cookies'}
                face_response = requests.post(face_recog.face_url, json=face_data, headers=face_headers, cookies=face_cookies)
                
                break
            else:
                pass
        else:
            pass
    
    key = cv2.waitKey(1) & 0xFF
    # q 키 누르면 종료
    if key == ord("q"):
        break

# 종료
cv2.destroyAllWindows()