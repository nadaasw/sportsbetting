import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from collections import Counter
import glob

# 훈련 데이터 로드 및 결합
file_paths = glob.glob("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/training_data/*.xlsx")
train_df_list = [pd.read_excel(file) for file in file_paths]
train_df = pd.concat(train_df_list, ignore_index=True)

# 테스트 데이터 로드
test_df = pd.read_excel("/Users/sangwoo/Desktop/pythonworkplace/python_webcrwaling/testData.xlsx")
test_df["game_no"] = test_df["game_no"].astype(int)

# 데이터 전처리 - z-score 정규화
scaler = StandardScaler()
train_df[["win_odds", "draw_odds", "lose_odds"]] = scaler.fit_transform(train_df[["win_odds", "draw_odds", "lose_odds"]])
test_df[["win_odds", "draw_odds", "lose_odds"]] = scaler.transform(test_df[["win_odds", "draw_odds", "lose_odds"]])

# 훈련 데이터와 레이블 분리
X_train = train_df[["win_odds", "draw_odds", "lose_odds"]]
y_train = train_df["result"]

# KNN 모델 설정 (유클리디안 거리 사용)
k = 3  # 최적 k값은 교차 검증으로 결정 가능
knn = KNeighborsClassifier(n_neighbors=k, metric="euclidean")

# 모델 훈련
knn.fit(X_train, y_train)

results = []
# 테스트 데이터에 대해 예측 수행
for i in range(len(test_df)):
    new_data = test_df.iloc[[i]][["win_odds", "draw_odds", "lose_odds"]]
    game_no = test_df.iloc[i]["game_no"]  # game_no 추출

    # 예측 결과 및 가까운 이웃 결과
    distances, indices = knn.kneighbors(new_data)  # 거리와 인덱스 반환
    nearest_neighbors = y_train.iloc[indices[0]]  # k개의 가장 가까운 이웃들의 결과

    # 각 클래스(승, 무, 패)의 개수 카운트
    class_counts = Counter(nearest_neighbors)
    predicted_result = knn.predict(new_data)[0]  # 다수결로 예측

    # 결과 저장
    result = {
        "게임 번호": game_no,
        "예측된 경기 결과": predicted_result,
        "승 개수": class_counts.get(1, 0),
        "무 개수": class_counts.get(0, 0),
        "패 개수": class_counts.get(-1, 0),
        "실제 결과": None  # 실제 결과는 이후 추가 가능
    }
    results.append(result)

# 결과를 DataFrame으로 변환
results_df = pd.DataFrame(results)

# 결과를 엑셀 파일로 저장
results_df.to_excel("game_result_euclidian_with_counts.xlsx", index=False)

# 결과 출력
for result in results:
    print(f"게임 번호: {result['게임 번호']}")
    print(f"예측된 경기 결과: {result['예측된 경기 결과']}")
    print(f"가장 가까운 {k}개의 이웃들: 승({result['승 개수']}), 무({result['무 개수']}), 패({result['패 개수']})")
    print()