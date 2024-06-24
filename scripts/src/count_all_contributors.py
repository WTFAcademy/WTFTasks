import pandas as pd

# 遍历output文件夹下的所有csv文件

def get_all_sheets():
    # 读取xlsx中的所有表
    all_sheets = pd.read_excel('./output.xlsx', sheet_name=None)
    return all_sheets    
    

    

# 处理表格数据
def process_sheets():
    all_sheets = get_all_sheets()
    contributers = {}
    last_pr_time = {}
    all_pr_links = {}


    for sheet_name in all_sheets:
        sheet = all_sheets[sheet_name]        
        for index, row in sheet.iterrows():
            name = row['用户名']
            isMerged = row['合并时间']

            if isMerged == '未合并':
                continue


            if name not in contributers:
                contributers[name] = 1
                last_pr_time[name] = row['合并时间']
                all_pr_links[name] = [row['url']]
            else:
                contributers[name] += 1
                all_pr_links[name].append(row['url'])
                if row['合并时间'] > last_pr_time[name]:
                    last_pr_time[name] = row['合并时间']

        
    # 合并 contributers 和 last_pr_time
    result = []
    for name in contributers:
        result.append({'用户名': name, 'pr数量': contributers[name], '最后pr提交时间': last_pr_time[name], 
                       '所有pr链接': '\n'.join(all_pr_links[name])
                       })

    writer = pd.ExcelWriter('./contributors.xlsx')
    # contributions_df = pd.DataFrame(pr_contributions, columns=['用户名', 'pr数量'])
    contributions_df = pd.DataFrame(result,
                                     columns=['用户名', 'pr数量', '最后pr提交时间', '所有pr链接'])
    
    contributions_df.to_excel(writer, sheet_name='Contributions', index=False)
    
    

    writer.close()

# process_sheets()
