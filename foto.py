import cv2
import sys
from datetime import date


def capture_image():
    """
    Captura uma imagem da câmera e salva no diretório Media com a data atual.
    A imagem é salva quando a tecla 'p' é pressionada.
    """
    s = 0
    if len(sys.argv) > 1:
        s = sys.argv[1]

    dia = date.today().strftime("%Y-%m-%d")

    source = cv2.VideoCapture(s)
    win_name = 'Camera Preview'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    while cv2.waitKey(1) != 27: # Escape
        has_frame, frame = source.read()
        if not has_frame:
            break
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite(f'Media/Fotos/{dia}.jpg', frame)
            cv2.destroyAllWindows()
            break

    source.release()

capture_image()