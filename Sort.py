import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler

# 读取数据
scores = pd.read_excel('score_2018.xlsx')
names = pd.read_excel('names.xlsx')

# 只取股票代码的前六位数字
names['股票代码'] = names['股票代码'].apply(lambda x: str(x)[:6])

# 确保 'Stock_Code' 列是6位数字字符串格式，不足的在前面补充0
scores['Stock_Code'] = scores['Stock_Code'].apply(lambda x: str(x).zfill(6))

# 创建一个新的DataFrame，列为 'names.xlsx' 中的 '股票代码'，行为 'score_2019.xlsx' 中的日期
new_df = pd.DataFrame(index=pd.date_range(start='2018/1/1', end='2018/12/31'), columns=names['股票代码'])

# 填充新的DataFrame
for _, row in scores.iterrows():
    stock_code = row['Stock_Code']
    date = row['时间']
    sentiment = row['sentiment']
    if stock_code in new_df.columns:
        new_df.loc[date, stock_code] = sentiment

# 将没有评分的日期填充为0
new_df.fillna(0, inplace=True)

# 写入新的excel文件
new_df.to_excel('新的打分.xlsx')

# 对每一列进行处理
for column in new_df.columns:
    # 获取非零值的索引
    non_zero_indices = new_df[column].to_numpy().nonzero()[0]

    # 如果只有一个非零值，则将整列数据都设置为这个值
    if len(non_zero_indices) == 1:
        new_df[column] = new_df[column].iloc[non_zero_indices[0]]
        continue

    # 对每两个非零值之间的部分进行处理
    for i in range(len(non_zero_indices) - 1):
        start_index = non_zero_indices[i]
        end_index = non_zero_indices[i + 1]

        # 如果两个非零值之间只有一个点，则跳过
        if end_index - start_index <= 1:
            continue

        start_value = new_df[column].iloc[start_index]
        end_value = new_df[column].iloc[end_index]

        # 创建等差数列
        sequence = np.linspace(start_value, end_value, end_index - start_index + 1)

        new_df.loc[new_df.index[start_index:end_index + 1], column] = sequence

# 对每一列进行处理
for column in new_df.columns:
    # 获取列的数据
    data = new_df[column]

    # 找到非零值
    non_zero_data = data[data != 0]

    # 计算非零值的均值和标准差
    mean = non_zero_data.mean()
    std = non_zero_data.std()

    # 标准化非零值
    data_normalized = (non_zero_data - mean) / std

    # 调整到期望的均值和标准差
    data_adjusted = data_normalized * (5/3) + 5

    # 将调整后的非零数据存回 DataFrame
    new_df.loc[data != 0, column] = data_adjusted

# 将结果写入新的 Excel 文件
new_df.to_excel('标准化评分.xlsx')