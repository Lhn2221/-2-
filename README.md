1. 사용한 프롬프트 링크

2. 데이터 및 시각화 결과
   1) 사용 데이터
      - 강수량: https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69 (250801~250831)
      - 습득물: https://data.seoul.go.kr/dataList/OA-15490/S/1/datasetView.do
      - 회사정보: https://data.seoul.go.kr/dataList/OA-15491/S/1/datasetView.do
      - 교통량: https://topis.seoul.go.kr/refRoom/openRefRoom_8.do (월간 통계 보고서 25년도 8월 pdf 파일)
      - 운행정보: https://topis.seoul.go.kr/refRoom/openRefRoom_3_1.do (25년도 8월 파일 다운로드)
   3) 정제 과정
      - 강수량: 위쪽부터 5줄 삭제
      - 습득물: 데이터 크기 문제인 듯하여 8월 데이터만 붙여넣기,
                '조회수/분실물등록id/수령일자/유식물상세정보' 삭제,
                '수령위치(회사)'→'회사'/'등록날짜'→'날짜'/'분실물SEQ'→'접수번호'로 변경
      - 회사정보: '회사구분' 삭제, '회사명'→'회사'로 변경,
                  '구분번호' 중복 문제로 13번째부터 24번째 행까지 숫자 임의 수정 및 449, 450번째 행 삭제
      - 교통량: PDF 파일 23p 구 단위 통행량 부분을 엑셀파일로 기입 후 csv 파일로 변환
      - 운행정보: 첫 줄 서식 삭제 및 재작성
                 '회사'로 명칭 변경, '최소/최대/인가대수/운행대수/예비대수' 삭제
                  기본 키 설정을 위해 '회사ID' 삽입
   4) 시각화 결과: 차트 설명 및 인사이트
