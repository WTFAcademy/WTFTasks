import get_repo
import get_pr
import merge2csv
import count_all_contributors


if __name__ == '__main__':
    # Set your GitHub personal access token
    # This is required to authenticate your request to the GitHub API
    # You can create a personal access token by following the instructions here:
    # https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
    personal_access_token = 'YOUR_PERSONAL_ACCESS_TOKEN'


    # 获取所有仓库列表并保存到repos.json
    repos = get_repo.get_all_repos(personal_access_token)

    get_repo.write_json(repos)

    print("repos.json文件已生成")
    

    # 根据repos.json获取所有仓库的贡献者并保存到output/contributors.csv
    # 注：这里为了方便检查，生成的文件都保存在output文件夹下
    get_pr.get_all_pr(personal_access_token)

    # 合并所有贡献者的pr数据并保存到result.xlsx
    merge2csv.csv2sheet()

    # 统计所有贡献者的pr数量并保存到output/contributors.csv
    count_all_contributors.process_sheets()

