# pip install pafy
# sudo pip install --upgrade youtube_dl
import cv2
import pafy


def youtube():
    url = "https://www.youtube.com/watch?v=0cNbwb009DI"
    video = pafy.new(url)
    best = video.getbest(preftype="webm")
    # documentation: https://pypi.org/project/pafy/

    capture = cv2.VideoCapture(best.url)
    check, frame = capture.read()
    print(check, frame)

    cv2.imshow('frame', frame)
    cv2.waitKey(10)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    youtube()
