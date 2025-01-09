import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
predict_file = "day16"
actual_file = "day15"
# 예측 결과와 실제 결과 파일 불러오기
results_df = pd.read_excel(f"/Users/sangwoo/Desktop/experience/{predict_file}/game_result.xlsx")  # 예측 결과 파일
actual_results_df = pd.read_excel(f"/Users/sangwoo/Desktop/experience/{actual_file}/verification.xlsx")  # 실제 결과 파일

# 예측 결과와 실제 결과 병합
merged_df = pd.merge(results_df, actual_results_df, on="게임 번호", how="inner")
merged_df.rename(columns={"실제 결과_x": "실제 결과", "실제 결과_y": "예측된 결과"}, inplace=True)

# 정확도 계산
accuracy = accuracy_score(merged_df["실제 결과"], merged_df["예측된 경기 결과"])
print(f"전체 정확도: {accuracy:.2%}")

# 클래스별 정밀도, 재현율, F1 점수
print("\n클래스별 성능 분석:")
print(classification_report(merged_df["실제 결과"], merged_df["예측된 경기 결과"], target_names=["패", "무", "승"]))

# 혼동 행렬
conf_matrix = confusion_matrix(merged_df["실제 결과"], merged_df["예측된 경기 결과"])
conf_matrix_df = pd.DataFrame(conf_matrix, columns=["패 예측", "무 예측", "승 예측"], index=["패 실제", "무 실제", "승 실제"])
print("\n혼동 행렬:")
print(conf_matrix_df)

# 상세 피드백: 잘못된 예측 분석
wrong_predictions = merged_df[merged_df["실제 결과"] != merged_df["예측된 경기 결과"]]
print("\n잘못된 예측 요약:")
for _, row in wrong_predictions.iterrows():
    print(f"게임 번호 {row['게임 번호']} | 예측: {row['예측된 경기 결과']} | 실제: {row['실제 결과']}")

# 클래스별 잘못된 예측 빈도
wrong_class_counts = wrong_predictions["실제 결과"].value_counts()
print("\n클래스별 잘못된 예측 빈도:")
print(wrong_class_counts)

# 전체 결과를 엑셀로 저장
merged_df.to_excel("detailed_feedback.xlsx", index=False)