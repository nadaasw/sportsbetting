from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
# Chrome 드라이버 설정 및 URL 설정
uid = 155
url = f'https://www.betman.co.kr/main/mainPage/gamebuy/closedGameSlip.do?gmId=G101&gmTs=240{uid}'
driver = webdriver.Chrome()
# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y%m%d")  # 예: 20241026

try:
    # 페이지 열기
    driver.get(url)

    WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '#tbd_gmBuySlipList tr'))
    )
    # 모든 <tr> 태그 가져오기 (tbody 안의 tr 태그들)
    rows = driver.find_elements(By.CSS_SELECTOR, '#tbd_gmBuySlipList tr')

    # 결과 저장용 리스트
    game_data = []

    # 각 행에서 정보 추출
    for index, row in enumerate(rows):
        try:
            # 경기 상태 추출 (class "fs11"인 <td> 요소에서 상태 추출)
            game_status = row.find_element(By.CSS_SELECTOR, 'td.fs11').text

            # '결과발표'인 경기만 처리
            if "결과발표" in game_status:
                # "일반" 텍스트 추출
                try:
                    game_type = row.find_element(By.CSS_SELECTOR, 'span.badge.gray').text  # "일반"만 가져옴
                except Exception:
                    continue

                if "일반" in game_type:  # "일반 경기"만 필터링
                    # 홈 팀과 원정 팀 점수 추출
                    home_score_text = row.find_element(By.CSS_SELECTOR, 'div.cell.tar strong').text
                    home_score = int(home_score_text.replace("점수\n", "").strip())

                    away_score_text = row.find_element(By.CSS_SELECTOR, 'div.cell.tal strong').text
                    away_score = int(away_score_text.replace("점수\n", "").strip())

                    # 경기 결과 판단 (승, 무, 패)
                    if home_score > away_score:
                        result = 1
                    elif home_score == away_score:
                        result = 0
                    else:
                        result = -1

                    # 숫자와 소수점만 남기고 나머지 제거하는 함수
                    def extract_only_numbers(text):
                        return ''.join([char for char in text if char.isdigit() or char == '.'])

                    # 승, 무, 패 배당률 추출
                    win_odds_text = row.find_element(By.CSS_SELECTOR, 'button[data-selkey="1"] span.db').text
                    win_odds = extract_only_numbers(win_odds_text).strip()

                    try:
                        draw_odds_text = row.find_element(By.CSS_SELECTOR, 'button[data-selkey="2"].btnChk span.db').text
                        draw_odds = extract_only_numbers(draw_odds_text).strip()
                    except:
                        draw_odds = 0.0

                    lose_odds_text = row.find_element(By.CSS_SELECTOR, 'button[data-selkey="3"] span.db').text
                    lose_odds = extract_only_numbers(lose_odds_text).strip()

                    # 간소화된 데이터 저장
                    game_data.append({
                        "result": result,
                        "win_odds": win_odds,
                        "draw_odds": draw_odds,
                        "lose_odds": lose_odds
                    })
        except Exception as e:
            print(f"Error extracting data from row {index + 1}: {e}")
    # 파일명에 날짜 추가
    file_name = f"game_results_{uid}.xlsx"

    # 데이터프레임 생성
    df = pd.DataFrame(game_data)

    # 엑셀 파일로 저장
    df.to_excel(file_name, index=False)
    print("엑셀 파일이 성공적으로 저장되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 브라우저 종료
    driver.quit()