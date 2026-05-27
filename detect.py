"""
Anomaly Detection Module
Detects anomalous temperatures (heat waves or cold snaps) using Isolation Forest
"""

import pandas as pd #pandas 가져오기
from sklearn.ensemble import IsolationForest #sklearn 라이브러리에서 isolationforest 알고리즘 불러오기
import warnings # warnings 모듈 가져오기 (경고메세지 제어함)

warnings.filterwarnings("ignore") #발생한 경고를 출력하지 않고 모두 무시


def detect_anomalies():
    """
    Detects temperature anomalies from weather.csv using Isolation Forest
    Anomalies represent extreme temperatures (heat waves or cold snaps)
    Prints detected anomalies with dates and temperatures
    """
    
    try:
        # Load the CSV file
        df = pd.read_csv("weather.csv") #데이터 로드, csv파일을 읽어 데이터프레임으로 저장
        df["date"] = pd.to_datetime(df["date"]) #데이터프레임에서 date 칼럼을 날짜타임으로 변환
        
        if df.empty: #데이터가 비어있으면
            print("✗ No data found in weather.csv") #출력하고
            return None #종료
        
        print(f"Loaded {len(df)} temperature records") #로드된 데이터 행 수 출력
        
        # Prepare data for Isolation Forest
        X = df[["max_temp"]].values #max_temp 컬럼을 numpy 배열로 추출함, isolationforest가 numpy 선호
        
        # Initialize Isolation Forest
        # contamination: expected proportion of anomalies (adjust as needed)
        iso_forest = IsolationForest(
            contamination=0.05,  # Expect ~5% anomalies // 전체 데이터 중 이상치가 차지하는 비율
            random_state=42,#재현성을 위해 랜덤 시드값을 42로 고정함
            n_estimators=100 #사용할 결정 트리 개수 설정, 수가 높을수록 정확성이 높아짐 (기준/질문을 더 많이하는것)
        )
        
        # Predict anomalies (-1 = anomaly, 1 = normal)
        predictions = iso_forest.fit_predict(X) #X 데이터프레임을 가지고 학습한 후에 예측, 변수 선언
        
        # Add predictions to dataframe
        df["anomaly"] = predictions #anomaly라는 컬럼을 만들고 predictions 변수 추가
        df["is_anomaly"] = df["anomaly"] == -1 #anomaly 컬럼이 -1이면 True, 1이면 False로 새 컬럼 생성
        
        # Extract anomalies
        anomalies = df[df["is_anomaly"]] # is_anomaly가 True인 행만 추출해서 anomalies 변수에 저장 >> 이상치 목록 완성
        
        # Print results
        print(f"\n{'='*60}") # = 60개 출력
        print(f"Anomaly Detection Results (Isolation Forest)") #제목 출력
        print(f"{'='*60}") # = 60개 출력
        print(f"Total anomalies detected: {len(anomalies)}") # 탐지된 이상치 개수 출력
        print(f"Normal records: {len(df) - len(anomalies)}") # 정상 데이터 개수 출력
        print(f"\n{'Date':<15} {'Temperature (°C)':<20} {'Type':<20}") # 테이블 헤더 출력 (컬럼명)
        print(f"{'-'*55}") # - 55개 출력
        
        if len(anomalies) > 0: # 이상치가 0보다 크면 실행
            for idx, row in anomalies.iterrows(): #이상치 데이터 한 행씩 반복
                date_str = row["date"].strftime("%Y-%m-%d") #날짜를 년-월-일 형식으로 변환
                temp = row["max_temp"] #해당 행의 최고 기온 추출
                
                # Determine type of anomaly
                mean_temp = df["max_temp"].mean() #전체 기온 평균 계산, 변수 선언
                if temp > mean_temp:
                    anomaly_type = "Heat Wave 🔥"
                else:
                    anomaly_type = "Cold Snap ❄️"
                
                print(f"{date_str:<15} {temp:>18.1f}°C  {anomaly_type:<20}")
        else:
            print("No anomalies detected")
        
        print(f"{'='*60}\n")
        
        # Save results
        df.to_csv("weather_with_anomalies.csv", index=False, encoding="utf-8")
        print(f"✓ Results saved to weather_with_anomalies.csv")
        
        return df
    
    except FileNotFoundError:
        print("✗ weather.csv not found. Please run collect_data.py first.")
        return None
    except Exception as e:
        print(f"✗ Error during anomaly detection: {e}")
        return None


if __name__ == "__main__":
    detect_anomalies()
