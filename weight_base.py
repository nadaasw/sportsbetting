import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cosine, euclidean
from collections import Counter
import numpy as np
import glob

# 여러 개의 훈련 데이터 파일 불러오기
file_paths = glob.glob("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/training_data/*.xlsx")
train_df_list = [pd.read_excel(file) for file in file_paths]
train_df = pd.concat(train_df_list, ignore_index=True)  # 여러 파일을 하나의 DataFrame으로 결합

# 테스트 데이터 불러오기
test_df = pd.read_excel("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/testData.xlsx")

# game_no를 int형으로 변환
test_df["game_no"] = test_df["game_no"].astype(int)

# 데이터 전처리 - z-score 표준화 적용
scaler = StandardScaler()
train_df[["win_odds", "draw_odds", "lose_odds"]] = scaler.fit_transform(train_df[["win_odds", "draw_odds", "lose_odds"]])
test_df[["win_odds", "draw_odds", "lose_odds"]] = scaler.transform(test_df[["win_odds", "draw_odds", "lose_odds"]])

# 훈련 데이터와 레이블 분리
X_train = train_df[["win_odds", "draw_odds", "lose_odds"]].values
y_train = train_df["result"].values

# 거리 가중치 설정
w_cosine = 0.3  # 코사인 유사도 가중치
w_euclidean = 0.7  # 유클리디안 거리 가중치
k = 3  # k 값 설정

results = []

# 테스트 데이터에 대해 예측 수행
for i in range(len(test_df)):
    new_data = test_df.iloc[i][["win_odds", "draw_odds", "lose_odds"]].values
    game_no = test_df.iloc[i]["game_no"]  # game_no 추출

    # 각 훈련 데이터와의 코사인 및 유클리디안 거리 계산
    distances = []
    for j in range(len(X_train)):
        cos_dist = cosine(new_data, X_train[j])  # 코사인 거리 계산
        euclid_dist = euclidean(new_data, X_train[j])  # 유클리디안 거리 계산
        combined_dist = w_cosine * cos_dist + w_euclidean * euclid_dist  # 가중치 기반 거리
        distances.append((combined_dist, y_train[j]))

    # 가장 가까운 k개의 이웃 선택
    distances = sorted(distances, key=lambda x: x[0])[:k]
    nearest_neighbors = [neighbor[1] for neighbor in distances]

    # 각 클래스(승, 무, 패)의 개수 카운트
    class_counts = Counter(nearest_neighbors)
    predicted_result = class_counts.most_common(1)[0][0]  # 다수결로 예측

    # 결과 저장
    result = {
        "게임 번호": game_no,
        "예측된 경기 결과": predicted_result,
        "승 개수": class_counts.get(1, 0),
        "무 개수": class_counts.get(0, 0),
        "패 개수": class_counts.get(-1, 0),
        "실제 결과": None
    }
    results.append(result)

# 결과를 DataFrame으로 변환
results_df = pd.DataFrame(results)

# 결과를 엑셀 파일로 저장
results_df.to_excel("game_result_combined_distances.xlsx", index=False)

# 결과 출력
for result in results:
    print(f"게임 번호: {result['게임 번호']}")
    print(f"예측된 경기 결과: {result['예측된 경기 결과']}")
    print(f"가장 가까운 {k}개의 이웃들에 대한 클래스 개수: 승({result['승 개수']}), 무({result['무 개수']}), 패({result['패 개수']})")
    print()