import pandas as pd

# 파일 경로 설정
existing_file_path = "/Users/sangwoo/Desktop/experience/day21/game_result_combined_distances.xlsx"  # 기존 경기 결과 파일 경로
verification_file_path = "/Users/sangwoo/Desktop/experience/day21/verification.xlsx"  # 새로운 경기 예측 데이터 파일 경로
output_file_path = "/Users/sangwoo/Desktop/experience/day21/comparison_result_combined.xlsx"  # 결과 저장 경로

# 엑셀 파일 불러오기
df_existing = pd.read_excel(existing_file_path)
df_verification = pd.read_excel(verification_file_path)

# 열 이름 변경 (기존 파일의 '게임 번호'를 'game_no'로 변경)
df_existing = df_existing.rename(columns={"게임 번호": "game_no"})

# game_no를 기준으로 두 데이터프레임 병합
df_comparison = pd.merge(df_existing, df_verification, on="game_no", suffixes=("_existing", "_verification"))

# 경기 결과 비교 (예측된 경기 결과와 실제 결과 비교)
df_comparison["맞춤"] = df_comparison["예측된 경기 결과"] == df_comparison["result"]

# 총 경기 수, 맞춘 경기 수, 틀린 경기 수 계산
total_games = len(df_comparison)
correct_predictions = df_comparison["맞춤"].sum()
incorrect_predictions = total_games - correct_predictions

# 요약 정보 DataFrame 생성
summary_data = {
    "총 경기 수": [total_games],
    "맞춘 경기 수": [correct_predictions],
    "틀린 경기 수": [incorrect_predictions]
}
df_summary = pd.DataFrame(summary_data)

# 결과 엑셀 파일에 저장
with pd.ExcelWriter(output_file_path) as writer:
    df_comparison.to_excel(writer, sheet_name="경기 비교", index=False)
    df_summary.to_excel(writer, sheet_name="요약 정보", index=False)

print("비교 결과가 엑셀 파일로 저장되었습니다.")