from dash import Dash, html
import dash_cytoscape as cyto
import pandas as pd

csv_data = pd.read_csv('./result.csv',)

sum_of_one_tx_account = 0
one_tx_account_dict = dict()  # 한 번만 거래했는지 여부
info_dict = dict()

for row in csv_data.itertuples():
    from_address = row.from_address
    to_address = row.to_address

    # 딕셔너리에 없으면 추가
    if (one_tx_account_dict.get(from_address, None) == None):
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
        # 트랜잭션 수 update
        info_dict[from_address]["sum_of_tx"] += 1

        # 이미 거래했던 계정인지 검사하고, 거래안했으면 sum_of_account 증가
        if (info_dict[from_address].get(to_address, None) == None):
            info_dict[from_address][to_address] = 1
            info_dict[from_address]["sum_of_account"] += 1

        if (one_tx_account_dict.get(from_address, None) == True):
            # 2번 이상 거래했으니까 false
            one_tx_account_dict[from_address] = False
            sum_of_one_tx_account -= 1

print("info dict 저장 완료")

arr = []
for key, value in info_dict.items():
    # key가 sender, value["sum_of_account"]가 num_of_account, value["sum_of_tx"]가 num_of_tx
    arr.append([key, value["sum_of_account"], value["sum_of_tx"]])

df = pd.DataFrame(arr, columns=['sender', 'num_of_account', 'num_of_tx'])
# tx기준으로 내림차순 정렬
sorted = df.sort_values(by=['num_of_tx'], ascending=False)
# sorted.to_csv("./account_tx_info2.csv", index=True)

graph_element = []
# 정렬된 sorted를 이용해서 상위 일부 계정을 가져와서 관계 그래프 생성
group_limit = 0
node_size = 0.3
for adr in sorted['sender']:
    if group_limit < 80:
        group_limit += 1
        # 그래프에 노드 추가
        graph_element.append({'data': {'id': adr, 'size': node_size}, 'classes': 'basic_color'})
        dct = info_dict.get(adr)

        rel_limit = 0
        for key, value in dct.items():
            if rel_limit < 40:
                # key값이 계정 값일 때 그래프에 노드 추가하고 관계 추가
                if key != "sum_of_account" and key != "sum_of_tx":
                    rel_limit += 1
                    graph_element.append({'data': {'id': key, 'size': node_size}, 'classes': 'basic_color'})
                    graph_element.append({'data': {'source': adr, 'target': key}, })
    else:
        break

app = Dash(__name__)

app.layout = html.Div([
    html.P("계정 간 거래:"),
    cyto.Cytoscape(
        id='network-graphs-x-cytoscape',
        elements=graph_element,
        layout={'name': 'cose'},  # breadthfirst, grid ...
        style={'width': '1200px', 'height': '1200px'},
        stylesheet=[
                    {
                        'selector': 'edge',
                        'style': {
                            'width': 1
                        }
                    },
                    {
                        'selector': '.basic_color',
                        'style': {
                            'background-color': "#c6e2e9",
                            'border-width': 0.5,
                            'border-color': "#01010e",
                            'width': '10px',
                            'height': '10px'

                        }
                    },

                ]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
