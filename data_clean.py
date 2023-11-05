import pandas as pd
import re

# 定义一个函数来检查字符串是否包含英文
def contains_english(s):
    return bool(re.search('[a-zA-Z]', str(s)))

# 读取csv文件
df = pd.read_csv('20100101-to-20231022.csv')

df_names = pd.read_excel('names.xlsx')

# 提取公司名称和股票代码列
company_names = df_names['公司名称']
stock_codes = df_names['股票代码'].astype(str).str[:6]  # 提取股票代码的前六位

# 应用这个函数到标题列，找出所有包含英文的行
mask = df['标题'].apply(contains_english)

# 删除所有包含英文的行
df = df[~mask]

# 定义一个函数来匹配和提取股票代码
def extract_stock_code(title):
    match = re.search('\((\d{6})\)', title)
    if match:
        return match.group(1)  # 返回匹配到的第一个组，即6位股票代码
    else:
        return None  # 如果没有匹配到，返回None

def extract_company_name(title):
    for name in company_names:
        if name in title:
            return name
    return None

# 在标题中提取股票代码
df['Stock_Code'] = df['标题'].apply(extract_stock_code)

# 创建一个映射字典，键为 df_new 中的 Stock_Code（前六位），值为 df_names 中的完整股票代码
stock_code_mapping = pd.Series(stock_codes.values, index=stock_codes.str[:6]).to_dict()

# 创建一个映射字典，键为 df_new 中的公司名称，值为 df_names 中的完整股票代码
company_name_mapping = pd.Series(stock_codes.values, index=company_names).to_dict()

# 在标题中提取股票代码和公司名称
df['Stock_Code'] = df['标题'].apply(extract_stock_code)
df['Company_Name'] = df['标题'].apply(extract_company_name)

# 使用 isin 方法，筛选出 new_file.csv 中股票代码也在 names.xlsx 中出现过的行
df_filtered_stock_code = df[df['Stock_Code'].astype(str).str[:6].isin(stock_codes.str[:6])]

# 筛选出 new_file.csv 中公司名称在标题中出现过的行
df_filtered_company_name = df[df['Company_Name'].notna()]

# 使用映射字典将公司名称和股票代码映射为完整的股票代码
df_filtered_stock_code.loc[:, 'Stock_Code'] = df_filtered_stock_code['Stock_Code'].map(stock_code_mapping)
df_filtered_company_name.loc[:, 'Stock_Code'] = df_filtered_company_name['Company_Name'].map(company_name_mapping)

# 将两个筛选结果合并
df_filtered = pd.concat([df_filtered_stock_code, df_filtered_company_name])
df_filtered.drop_duplicates(subset=['标题'], inplace=True)

# 将结果保存到新的csv文件
df_filtered.to_csv('data.csv', index=False)