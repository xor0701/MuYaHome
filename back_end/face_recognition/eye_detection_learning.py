import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from tensorflow.keras.layers import Input, Activation, Conv2D, Flatten, Dense, MaxPooling2D
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import accuracy_score, confusion_matrix

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# plt.style.use('dark_background')

class Eye_Detection():
    def __init__(self):
        self.x_train = np.load('eye_detection_dataset/x_train.npy').astype(np.float32)
        self.y_train = np.load('eye_detection_dataset/y_train.npy').astype(np.float32)
        self.x_val = np.load('eye_detection_dataset/x_val.npy').astype(np.float32)
        self.y_val = np.load('eye_detection_dataset/y_val.npy').astype(np.float32)

        # shape : (26, 34, 1) -> 세로:26, 가로:34
        print(self.x_train.shape, self.y_train.shape)
        print(self.x_val.shape, self.y_val.shape)

        self.start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        self.train_generator = None
        self.val_generator = None
        self.model = None

    def Image_Date_Generator(self):
        # ImageDataGenerator : 이미지 처리를 도와주는 class
        train_datagen = ImageDataGenerator(
            rescale=1./255,  # 0~255 데이터를 0~1로 정규화
            rotation_range=10,  # 랜덤하게 10도 정도 돌림
            width_shift_range=0.2,  # 랜덤하게 가로 크기를 0.2만큼 변형
            height_shift_range=0.2,  # 랜덤하게 세로 크기를 0.2만큼 변형
            shear_range=0.2,  # 랜덤하게 0.2만큼 약간 비틈
        )  # 사용 이유 :  이미지 형태가 다양해지므로 더 잘 학습됨

        # val_datagen : 모델이 잘 학습됬는지 확인용
        val_datagen = ImageDataGenerator(rescale=1./255)

        # flow : data generator를 쉽게 만들 수 있음
        self.train_generator = train_datagen.flow(
            x=self.x_train,
            y=self.y_train,
            batch_size=32,
            shuffle=True
        )
        self.val_generator = val_datagen.flow(
            x=self.x_val,
            y=self.y_val,
            batch_size=32,
            shuffle=False
        )

    def Model_Generator(self):
        # 모델 생성 (CNN 구조 : C-P-C-P-C-P-FC-FC)
        inputs = Input(shape=(26, 34, 1))

        net = Conv2D(32, kernel_size=3, strides=1,
                     padding='same', activation='relu')(inputs)
        net = MaxPooling2D(pool_size=2)(net)

        net = Conv2D(64, kernel_size=3, strides=1,
                     padding='same', activation='relu')(net)
        net = MaxPooling2D(pool_size=2)(net)

        net = Conv2D(128, kernel_size=3, strides=1,
                     padding='same', activation='relu')(net)
        net = MaxPooling2D(pool_size=2)(net)

        net = Flatten()(net)

        net = Dense(512)(net)
        net = Activation('relu')(net)
        net = Dense(1)(net)  # 0~1 사이의 값이 나오도록 출력은 1개
        outputs = Activation('sigmoid')(net)

        self.model = Model(inputs=inputs, outputs=outputs)

        # binary_crossentropy : 0 or 1만 판단
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy', metrics=['acc'])

        self.model.summary()

    def Model_fit(self):
        start_time = self.start_time
        model = self.model
        train_generator = self.train_generator
        val_generator = self.val_generator

        model.fit_generator(
            train_generator,
            epochs=50,
            validation_data=val_generator,
            callbacks=[
                # 모델이 좋으면 저장
                ModelCheckpoint('models/%s.h5' % (start_time),
                                monitor='val_acc',
                                save_best_only=True,
                                mode='max',
                                verbose=1),
                # 학습이 잘 안되면 learning rate을 줄임
                ReduceLROnPlateau(monitor='val_acc',
                                  factor=0.2,
                                  patience=10,
                                  verbose=1,
                                  mode='auto',
                                  min_lr=1e-05)
            ]
        )

    def Model_Confirm(self):
        start_time = self.start_time

        # 저장된 model 불러오기
        model = load_model('models/%s.h5' % (start_time))
        # model = load_model('models/2021_06_19_19_43_16.h5')

        # 모델을 통해 데이터를 예측
        y_pred = model.predict(self.x_val/255.)
        # 0 : 눈을 감은 이미지, 1 : 눈을 뜬 이미지
        # 0.5 보다 크면 눈을 떳다고 설정
        y_pred_logical = (y_pred > 0.5).astype(np.int)

        # accuracy_score() : 테스트 결과 정확도 계산
        print('test acc: %s' % accuracy_score(self.y_val, y_pred_logical))
        cm = confusion_matrix(self.y_val, y_pred_logical)
        sns.heatmap(cm, annot=True)
        plt.show()


eye_detection = Eye_Detection()
eye_detection.Image_Date_Generator()
eye_detection.Model_Generator()
eye_detection.Model_fit()
eye_detection.Model_Confirm()
