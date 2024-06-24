import pandas as pd

# 遍历output文件夹下的所有csv文件

def get_all_sheets():
    # 读取xlsx中的所有表
    all_sheets = pd.read_excel('./wtf2024.xlsx', sheet_name=None)
    return all_sheets    


def process_pre_outstanding_contributions(pre_outstanding_contributions):
    outstanding_contributions = {}
    for name in pre_outstanding_contributions:
        if pre_outstanding_contributions[name] >= 3:
            outstanding_contributions[name] = "多次优质pr贡献者"

    
    return outstanding_contributions
    

    

# 处理表格数据
def process_sheets():
    all_sheets = get_all_sheets()
    contributions = []
    pre_outstanding_contributions = {}
    continuous_contributions = {}

    project = [
        'SoLive',
        'solui',
        'frontend'
    ]


    for sheet_name in all_sheets:
        sheet = all_sheets[sheet_name]        
        for index, row in sheet.iterrows():
            name = row['用户名']
            isMerged = row['合并时间']
            prType = row['Type']

            if isMerged == '未合并':
                continue

            if name not in contributions:
                contributions.append(name)

            
            if prType != 1:
                # 统计每个人的pr数量
                if name not in pre_outstanding_contributions:
                    pre_outstanding_contributions[name] = 1
                else:
                    pre_outstanding_contributions[name] += 1
            
            if sheet_name in project:
                if name not in continuous_contributions:
                    if name == "buttonwild":
                        print(sheet_name)
                    continuous_contributions[name] = "开源软件贡献者"
        

    outstanding_contributions = process_pre_outstanding_contributions(pre_outstanding_contributions)

    writer = pd.ExcelWriter('./result.xlsx')
    contributions_df = pd.DataFrame(contributions, columns=['用户名'])
    outstanding_contributions_df = pd.DataFrame(outstanding_contributions.items(), columns=['用户名', '类型'])
    continuous_contributions_df = pd.DataFrame(continuous_contributions.items(), columns=['用户名', '类型'])
    contributions_df.to_excel(writer, sheet_name='Contributions', index=False)
    outstanding_contributions_df.to_excel(writer, sheet_name='Outstanding', index=False)
    continuous_contributions_df.to_excel(writer, sheet_name='Continuous', index=False)
    

    writer.close()

process_sheets()
