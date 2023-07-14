##########################################
# основная функция                       #
# через cmd или conda                    #
# cd путь/donation_ocr#                  #
# python main-test.py путь/до/изображения#
##########################################

import sys

from d_ocr import donation_ocr


def main():
    try:
        image = sys.argv[1]
    except: 
        print('Не указано изображение')
    try:
        ocr = donation_ocr()
    except:
        print('Не удалось загрузить d_ocr.py')
    try:
        df_pred = ocr.predict(image)
        print('Распознавание прошло успешно')
    except:
        print('Распознавание не удалось')
    if len(df_pred) == 0:
        print('Попробуйте другое фото')
    else:
        print('Проверьте папку results')

        
if __name__ == '__main__':
    main()