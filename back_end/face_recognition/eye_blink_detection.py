import cv2, dlib
import numpy as np
from imutils import face_utils
from tensorflow.keras.models import load_model
import camera

class EyeBlinkDetector():
    def __init__(self):
        self.IMG_SIZE = (34, 26)

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/shape_predictor_68_face_landmarks.dat')

        self.model = load_model('C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/models/2021_06_19_22_45_22.h5')
        self.model.summary()

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


while True:    
    eye_frame = eye_blink_detector.get_frame()
    if (eye_blink_detector.count>=2):
        # print("눈 깜빡임 2번 이후 얼굴인식 시작")

        break
    
    # frame 보여주기
    cv2.imshow("Eye_Frame", eye_frame)

    key = cv2.waitKey(1) & 0xFF
    # q 키 누르면 종료
    if key == ord("q"):
        break

# 종료
cv2.destroyAllWindows()
# IMG_SIZE = (34, 26)

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# model = load_model('models/2021_06_19_22_45_22.h5')
# model.summary()

# def crop_eye(img, eye_points):
#     x1, y1 = np.amin(eye_points, axis=0)
#     x2, y2 = np.amax(eye_points, axis=0)
#     cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

#     w = (x2 - x1) * 1.2
#     h = w * IMG_SIZE[1] / IMG_SIZE[0]

#     margin_x, margin_y = w / 2, h / 2

#     min_x, min_y = int(cx - margin_x), int(cy - margin_y)
#     max_x, max_y = int(cx + margin_x), int(cy + margin_y)

#     eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

#     eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

#     return eye_img, eye_rect

# # main
# streaming = 'http://220.81.195.100:5000/index.html'
# cap = cv2.VideoCapture(streaming)

# count = 0
# count_bool = False

# while cap.isOpened():
#     ret, img_ori = cap.read()

#     if not ret:
#        break

#     img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

#     img = img_ori.copy()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     faces = detector(gray)

#     for face in faces:
#         shapes = predictor(gray, face)
#         shapes = face_utils.shape_to_np(shapes)

#         eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
#         eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

#         eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
#         eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
#         eye_img_r = cv2.flip(eye_img_r, flipCode=1)

#         cv2.imshow('l', eye_img_l)
#         cv2.imshow('r', eye_img_r)

#         eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
#         eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

#         pred_l = model.predict(eye_input_l)
#         pred_r = model.predict(eye_input_r)

#         # visualize
#         if ((pred_l > 0.01) & (pred_r > 0.01)):
#             if (count_bool==False):
#                 count_bool = True

#             print("눈 감지 않음")
#         else:
#             if (count_bool==True):
#                 count += 1
#                 count_bool = False

#             print("눈 감음")

#         print(pred_l, pred_r)

#         cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
#         cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,255,255), thickness=2)

#         cv2.putText(img, str(round(pred_l[0][0], 3)), tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
#         cv2.putText(img, str(round(pred_r[0][0], 3)), tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

#     cv2.imshow('result', img)
#     if cv2.waitKey(1) == ord('q'):
#         break
#     if count==2:
#       print("사람이라고 판별")
#       break
