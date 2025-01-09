from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# Chrome 드라이버 설정 및 URL 설정
url = 'https://www.betman.co.kr/main/mainPage/gamebuy/closedGameSlip.do?gmId=G101&gmTs=240143'
driver = webdriver.Chrome()
current_date = datetime.now().strftime("%Y%m%d")  # 예: 20241026

# 크롤링 데이터 저장할 리스트
game_data = []

try:
    # 페이지 열기
    driver.get(url)

    WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '#tbd_gmBuySlipList tr'))
    )

    # 모든 <tr> 태그 가져오기 (tbody 안의 tr 태그들)
    rows = driver.find_elements(By.CSS_SELECTOR, '#tbd_gmBuySlipList tr')

    # 각 행에서 정보 추출
    for index, row in enumerate(rows):
        try:
            
            game_no = row.get_attribute("data-matchseq")
            if game_no is None:
                print(f"Row {index + 1}: 'data-matchseq' 속성이 없음, 건너뜀")
                continue
            game_no = int(game_no)  # int로 변환
            
            # 경기 상태 추출 (class "fs11"인 <td> 요소에서 상태 추출)
            game_status = row.find_element(By.CSS_SELECTOR, 'td.fs11').text

            # '결과발표'인 경기만 처리
            if "결과발표" in game_status:
                # "일반" 텍스트 추출
            
                try:
                        game_type = row.find_element(By.CSS_SELECTOR, 'span.badge.gray').text
                except Exception:
                        continue

                if "일반" in game_type:
                    
                        # 홈 팀 이름과 점수 추출
                        home_team = row.find_element(By.CSS_SELECTOR, 'div.cell.tar span').text
                        home_score_text = row.find_element(By.CSS_SELECTOR, 'div.cell.tar strong').text.replace("점수\n", "").strip()
                        if not home_score_text.isdigit():
                            continue
                        home_score = int(home_score_text)  # "점수\n" 제거 후 숫자로 변환
                        
                        
                        # 원정 팀 이름과 점수 추출
                        away_team = row.find_element(By.CSS_SELECTOR, 'div.cell.tal span').text
                        away_score_text = row.find_element(By.CSS_SELECTOR, 'div.cell.tal strong').text
                        away_score = int(away_score_text.replace("점수\n", "").strip())  # "점수\n" 제거 후 숫자로 변환

                        # 경기 결과 판단 (승, 무, 패)
                        if home_score > away_score:
                            result = 1
                        elif home_score == away_score:
                            result = 0
                        else:
                            result = -1

                        # 간소화된 데이터 저장
                        game_data.append({
                            "result": result,
                            "game_no": game_no  
                        })
        except Exception as e:
            print(f"Error extracting data from row {index + 1}: {e}")

    # 크롤링 데이터 DataFrame 생성
    df_crawled = pd.DataFrame(game_data)

    # 엑셀 파일로 저장
    df_crawled.to_excel("verification.xlsx", index=False)
    print("엑셀 파일이 성공적으로 저장되었습니다.")
  

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 브라우저 종료
    driver.quit()