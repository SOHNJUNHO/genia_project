import noun
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import re
from nltk import bigrams
from matplotlib import rc
from matplotlib import font_manager
from nltk.util import ngrams


font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


## noun.py의 댓글별 명사 리스트에서 bigram 형성
bigram=[]
for i in range(len(noun.lists)):
    bgram = bigrams(noun.lists[i])
    bgram_list = [x for x in bgram]
    bigram += bgram_list

## bigram 센 후 빈도로 데이터프레임
bgram_counts = Counter(bigram)
bgram_df = pd.DataFrame({'bgram':bgram_counts.keys(), 'frequency':bgram_counts.values()})
bgram_df.sort_values('frequency', ascending=False, inplace=True)

## 특정 단어가 들어가는 bigram만 뽑아내기
keyword_list = ['밀크티','학원','문제집','엘리하이']

## 기타 후보 -  '와이즈','선생','홈런','초등','책','학교','윙크','엘리하이','학습지','문제','과목','화상','연산','7살','초1','초3','강의','한글','파닉스'

for key in keyword_list:
    test_list = []

    for i in range(len(bgram_df)):
        if key in bgram_df.iloc[i,0]:
            test_list.append(True)

        else:
            test_list.append(False)
    bgram_df[key] = test_list

##그래프 그리기 --> 앞뒤로 나온 단어 빈도수 측정
for key in keyword_list:
    twogram_df = bgram_df[bgram_df[key]==True].reset_index()
    twogram_df.drop(columns=['index'],axis=0,inplace=True)
    twogram_df = twogram_df[twogram_df['frequency']>50]
    twogram_df = twogram_df[['bgram','frequency']]
    for i in range(len(twogram_df)):
        twogram_df.iloc[i,0] = str(twogram_df.iloc[i,0])
        twogram_df.iloc[i,0] = re.sub('[^ㄱ-힗0-9]','', twogram_df.iloc[i,0])
        twogram_df.iloc[i,0] = re.sub(f'{key}','', twogram_df.iloc[i,0])
    twogram_df.set_index('bgram', inplace=True)
    twogram_df = twogram_df.groupby(twogram_df.index).sum().sort_values(by='frequency', ascending=False)
    ax = twogram_df.plot.bar(figsize=(25,13),legend=None)
    plt.xticks(fontsize=12,rotation=90)
    plt.xlabel(None)
    plt.title(f'{key}', fontsize=35)
    ax.bar_label(ax.containers[0],fontsize=12)
plt.show()
