############## OCR-функция #############
# на вход подаётся путь до изображения #
# возвращает заполненный датафрейм     #
########################################


import re
from cv2 import imread
from pathlib import Path
import pandas as pd
from easyocr import Reader


class donation_ocr():
    # инициализация модели и переменных
    def __init__(self, cut=True):
        self.reader = Reader(['ru'])
        self.date_r = re.compile('^(0[1-9]|[12][0-9]|3[01])[- /.|,| |-](0[1-9]|1[012])[- /.|,| |-](19|20)\d\d$')
        self.bt_pattern = r'[\{\(\[]([^()\[\]]*?)[\)\]\}]'
        self.bloodsdict = {
            'к': 'Цельная кровь',
            'р': 'Цельная кровь',
            'п': 'Плазма',
            'л': 'Плазма',
            'ц': 'Тромбоциты'
        }
        self.cut = cut

    # предсказание на основе easyocr
    def predict(self, image):
        # переменные для рассчёта точности
        sum_acc = 0
        iteration = 0

        # открыть изображение, обрезать и распознать текст
        im = imread(image)
        if self.cut:
            height, width, channels = im.shape
            hei = int(height / 2)
            im = im[hei: height, 0:width]
        result = self.reader.readtext(im)

        # вытащить из результата ocr даты, виды и типы донаций
        dates = []
        bloodstypes = []
        index = 0

        for i in range(len(result)):
            try:
                text = result[index][1]
                if self.date_r.match(text):
                    text = text.replace(',', '.')
                    text = text.replace('-', '.')
                    text = text.replace(' ', '.')
                    dates.append(text)
                    temp = result[index+1]
                    text = temp[1]
                    text = text.strip(' ')
                    text = text.lower()
                    bloodstypes.append(text)
                    index += 3
                else:
                    index += 1
            except: continue

        # разбить bloodstypes на списки видов донации и типов донации
        bt_pattern = r'[\{\(\[]([^()\[\]]*?)[\)\]\}]'
        bloods = []
        types = []

        for row in bloodstypes:
            matches = re.findall(bt_pattern, row)
            types.append(' '.join(matches))
            bl = re.sub(bt_pattern, '', row)
            bloods.append(bl.strip(' '))

        # переименовать виды и типы донации
        for i in range(len(bloods)):
            is_found = False
            for key in self.bloodsdict.keys():
                if key in bloods[i]:
                    bloods[i] = self.bloodsdict[key]
                    is_found = True
                    break
            if not is_found:
                bloods[i] = ' '
                

        for i in range(len(types)):
            if len(types[i]) > 2:
                types[i] = 'Платно'
            else:
                types[i] = 'Безвозмездно'

        # собрать датафрейм и сортировать по дате донации
        df_pred = pd.DataFrame(
        columns=[
            'Класс крови', 
            'Дата донации', 
            'Тип донации'
        ]
        )

        for i in range(len(dates)):

            df_pred.loc[i, 'Класс крови'] = bloods[i]
            df_pred.loc[i, 'Дата донации'] = dates[i]
            df_pred.loc[i, 'Тип донации'] = types[i]
            
        df_pred['Дата донации'] = pd.to_datetime(df_pred['Дата донации'], dayfirst=True)
        df_pred.drop_duplicates(subset=['Дата донации'], keep='last', inplace=True, ignore_index=True) # удалить дубликаты по дате
        df_pred.sort_values(by=['Дата донации'], inplace=True, ignore_index=True)
        df_pred['Дата донации'] = df_pred['Дата донации'].dt.strftime('%d.%m.%Y')
        df_pred['Дата донации'] = df_pred['Дата донации'].astype('str')

        save_path = Path('results/')
        if save_path.exists():
            df_pred.to_csv(str(save_path) + '/' + Path(image).stem + '.csv', columns=df_pred.columns)
        else:
            save_path.mkdir()
            df_pred.to_csv(str(save_path) + '/' + Path(image).stem + '.csv', columns=df_pred.columns)

        return df_pred