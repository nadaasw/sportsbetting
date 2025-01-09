import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore
from collections import Counter

# 훈련 데이터 불러오기
train_df = pd.read_excel("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/02.selenium/game_results.xlsx")

# 테스트 데이터 불러오기
test_df = pd.read_excel("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/testData.xlsx")

# game_no를 int형으로 변환
test_df["game_no"] = test_df["game_no"].astype(int)

# 데이터 전처리 - z-score 표준화 적용
train_df[["win_odds", "draw_odds", "lose_odds"]] = train_df[["win_odds", "draw_odds", "lose_odds"]].apply(zscore)
test_df[["win_odds", "draw_odds", "lose_odds"]] = test_df[["win_odds", "draw_odds", "lose_odds"]].apply(zscore)

# 훈련 데이터와 레이블 분리
X_train = train_df[["win_odds", "draw_odds", "lose_odds"]]
y_train = train_df["result"]

# KNN 모델 설정
k = 3  # 원하는 k 값 설정
knn = KNeighborsClassifier(n_neighbors=k, metric="cosine")

# 모델 훈련
knn.fit(X_train, y_train)

results = []
# 테스트 데이터에 대해 예측 수행
for i in range(len(test_df)):
    new_data = test_df.iloc[[i]][["win_odds", "draw_odds", "lose_odds"]]
    game_no = test_df.iloc[i]["game_no"]  # game_no 추출
    
    # 예측 결과와 각 클래스의 개수 확인
    distances, indices = knn.kneighbors(new_data)  # 거리와 인덱스 반환
    nearest_neighbors = y_train.iloc[indices[0]]  # k개의 가장 가까운 이웃들의 결과

    # 각 클래스(승, 무, 패)의 개수 카운트
    class_counts = Counter(nearest_neighbors)
    predicted_result = knn.predict(new_data)[0]


    # 결과를 딕셔너리 형태로 저장
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
    results_df.to_excel("game_result.xlsx", index=False)

    # 결과 출력
    print(f"게임 번호: {game_no}")
    print(f"예측된 경기 결과: {predicted_result}")
    print(f"가장 가까운 {k}개의 이웃들에 대한 클래스 개수: {class_counts}")
    print()