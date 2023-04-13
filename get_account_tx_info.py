# 계정, 트랜잭션 분석 코드

import pandas as pd

csv_data = pd.read_csv('./result.csv')


sum_of_one_tx_account = 0
one_tx_account_dict = dict()  # 한 번만 거래했는지 여부
info_dict = dict()

for row in csv_data.itertuples():
    from_address = row.from_address
    to_address = row.to_address
    
    # 딕셔너리에 없으면 추가 (한 번도 아직 체크 안된 계정)
    if(one_tx_account_dict.get(from_address,None)==None):
        one_tx_account_dict[from_address] = True
        sum_of_one_tx_account += 1

        # info_dict에 추가하고 sum_of_tx는 1로 초기화
        info_dict[from_address] = dict()
        info_dict[from_address]["sum_of_tx"] = 1
        # 거래한 계정을 추가(계정 중복 검사하기 위해)
        info_dict[from_address][to_address] = 1 
        # 몇 개의 계정과 거래했는지 저장
        info_dict[from_address]["sum_of_account"] = 1 
    else:
        #한 번 이상 나온 계정
        # 트랜잭션 수 update
        info_dict[from_address]["sum_of_tx"] += 1
        
        # 이미 거래했던 계정인지 검사하고, 거래안했으면 sum_of_account 증가
        if(info_dict[from_address].get(to_address,None)==None):
            info_dict[from_address][to_address] = 1 
            info_dict[from_address]["sum_of_account"] += 1


        if(one_tx_account_dict.get(from_address,None)==True):
            # 2번 이상 거래했으니까 false
            one_tx_account_dict[from_address] = False
            sum_of_one_tx_account -= 1

print("<한번의 트랜잭션만 생성한 계정 수>")
print(sum_of_one_tx_account)

arr = []
for key, value in info_dict.items():
    # key가 sender, value["sum_of_account"]가 num_of_account, value["sum_of_tx"]가 num_of_tx
    arr.append([key, value["sum_of_account"], value["sum_of_tx"]])
    
df = pd.DataFrame(arr, columns=['sender','num_of_account','num_of_tx'])
 # tx로 내림차순 정렬
sorted = df.sort_values(by=['num_of_tx'], ascending=False)  
# 인덱스 reset하기
sorted.reset_index(drop=True, inplace=True)
# 파일로 저장하기
sorted.to_csv("./account_tx_info.csv", index=True)

