import os
import sys
import bz2
from keras.utils import get_file
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector

LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'


def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, 'wb') as fp:
        fp.write(data)
    return dst_path


if __name__ == "__main__":
    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """

    landmarks_model_path = unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
                                               LANDMARKS_MODEL_URL, cache_subdir='temp'))
    RAW_IMAGES_DIR = sys.argv[1]
    ALIGNED_IMAGES_DIR = sys.argv[2]
    NUM_FACES = 1 if len(sys.argv) < 4 else sys.argv[3]

    landmarks_detector = LandmarksDetector(landmarks_model_path)
    image_names = os.listdir(RAW_IMAGES_DIR)
    for i in range(len(image_names)):
        img_name = image_names[i]
        print("Processing image {0}/{1}: {2}".format(i, len(image_names), img_name))
        raw_img_path = os.path.join(RAW_IMAGES_DIR, img_name)
        face_i = 0
        for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
            face_i += 1
            if face_i > NUM_FACES:
              continue
            face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], i)
            aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)

            image_align(raw_img_path, aligned_face_path, face_landmarks)
