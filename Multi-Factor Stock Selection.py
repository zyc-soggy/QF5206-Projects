import pandas as pd
import numpy as np

root_path = r"./"

# ==============import data=================


def mad_outlier(series, constant=1.4826, threshold=3.5):
    median = series.median()  # 计算数据列的中位数
    mad = constant * abs(series - median).median()  # 计算绝对偏差的中位数（MAD）
    modified_z_score = 0.6745 * (series - median) / mad  # 计算修改后的Z分数

    # 替换过大的异常值为中位数加上常数乘以MAD的积
    series[modified_z_score > threshold] = median + constant * mad
    # 替换过小的异常值为中位数减去常数乘以MAD的积
    series[modified_z_score < -threshold] = median - constant * mad

    return series


def read_and_process_csv(filename):
    df = pd.read_csv(filename, index_col=0)
    df = df.T.copy()
    df = df.apply(pd.to_numeric, errors='coerce')
    df.apply(mad_outlier)
    return df


year_list = [x for x in range(2009,2020)]

balance_dict = {}
cashflow_dict = {}
income_dict = {}
indicator_dict = {}

semi_balance_dict = {}
semi_cashflow_dict = {}
semi_income_dict = {}
semi_indicator_dict = {}

first_balance_dict = {}
first_cashflow_dict = {}
first_income_dict = {}
first_indicator_dict = {}

third_balance_dict = {}
third_cashflow_dict = {}
third_income_dict = {}
third_indicator_dict = {}

balance_dict_q = {}
cashflow_dict_q = {}
income_dict_q = {}
indicator_dict_q = {}


for i in year_list:
    balance_dict[i] = read_and_process_csv(root_path + 'data/balance_'+ str(i) + '.csv')
    cashflow_dict[i] = read_and_process_csv(root_path + 'data/cashflow_'+ str(i) + '.csv')
    income_dict[i] = read_and_process_csv(root_path + 'data/income_'+ str(i) + '.csv')
    indicator_dict[i] = read_and_process_csv(root_path + 'data/indicator_'+ str(i) + '.csv')

    semi_balance_dict[i] = read_and_process_csv(root_path + 'data/semi_balance_' + str(i) + '.csv')
    semi_cashflow_dict[i] = read_and_process_csv(root_path + 'data/semi_cashflow_' + str(i) + '.csv')
    semi_income_dict[i] = read_and_process_csv(root_path + 'data/semi_income_' + str(i) + '.csv')
    semi_indicator_dict[i] = read_and_process_csv(root_path + 'data/semi_indicator_' + str(i) + '.csv')

    first_balance_dict[i] = read_and_process_csv(root_path + 'data/1_balance_' + str(i) + '.csv')
    first_cashflow_dict[i] = read_and_process_csv(root_path + 'data/1_cashflow_' + str(i) + '.csv')
    first_income_dict[i] = read_and_process_csv(root_path + 'data/1_income_' + str(i) + '.csv')
    first_indicator_dict[i] = read_and_process_csv(root_path + 'data/1_indicator_' + str(i) + '.csv')

    third_balance_dict[i] = read_and_process_csv(root_path + 'data/3_balance_' + str(i) + '.csv')
    third_cashflow_dict[i] = read_and_process_csv(root_path + 'data/3_cashflow_' + str(i) + '.csv')
    third_income_dict[i] = read_and_process_csv(root_path + 'data/3_income_' + str(i) + '.csv')
    third_indicator_dict[i] = read_and_process_csv(root_path + 'data/3_indicator_' + str(i) + '.csv')

# reallowcate the data
k = 1
for i in year_list[:-1]:
    # Q1
    balance_dict_q[k] = first_balance_dict[i]
    cashflow_dict_q[k] = first_cashflow_dict[i]
    income_dict_q[k] = first_income_dict[i]
    indicator_dict_q[k] = first_indicator_dict[i]
    k += 1
    # Q2
    balance_dict_q[k] = semi_balance_dict[i] - first_balance_dict[i]
    cashflow_dict_q[k] = semi_cashflow_dict[i] - first_cashflow_dict[i]
    income_dict_q[k] = semi_income_dict[i] - first_income_dict[i]
    indicator_dict_q[k] = semi_indicator_dict[i]
    k += 1
    # Q3
    balance_dict_q[k] = third_balance_dict[i] - semi_balance_dict[i]
    cashflow_dict_q[k] = third_cashflow_dict[i] - semi_cashflow_dict[i]
    income_dict_q[k] = third_income_dict[i] - semi_income_dict[i]
    indicator_dict_q[k] = third_indicator_dict[i]
    k += 1
    # Q4
    balance_dict_q[k] = balance_dict[i+1] - third_balance_dict[i]
    cashflow_dict_q[k] = cashflow_dict[i+1] - third_cashflow_dict[i]
    income_dict_q[k] = income_dict[i+1] - third_income_dict[i]
    indicator_dict_q[k] = indicator_dict[i+1]
    k += 1

# last year Q1
balance_dict_q[k] = first_balance_dict[year_list[-1]]
cashflow_dict_q[k] = first_cashflow_dict[year_list[-1]]
income_dict_q[k] = first_income_dict[year_list[-1]]
indicator_dict_q[k] = first_indicator_dict[year_list[-1]]
k += 1
# last year Q2
balance_dict_q[k] = semi_balance_dict[year_list[-1]] - first_balance_dict[year_list[-1]]
cashflow_dict_q[k] = semi_cashflow_dict[year_list[-1]] - first_cashflow_dict[year_list[-1]]
income_dict_q[k] = semi_income_dict[year_list[-1]] - first_income_dict[year_list[-1]]
indicator_dict_q[k] = semi_indicator_dict[year_list[-1]]


# =============== factor ===============

def get_seasonal_factor_df(num_period):

    balance_n = balance_dict_q[num_period]
    balance_l = balance_dict_q[num_period-1]
    # balance_q = balance_dict_q[num_period-4]
    cashflow_n = cashflow_dict_q[num_period]
    cashflow_l = cashflow_dict_q[num_period-1]
    cashflow_q = cashflow_dict_q[num_period-4]
    income_n = income_dict_q[num_period]
    income_l = income_dict_q[num_period-1]
    income_q = income_dict_q[num_period-4]
    indicator_n = indicator_dict_q[num_period]
    indicator_l = indicator_dict_q[num_period-1]

    factor_df = pd.DataFrame(index=balance_dict[2009].index)

    # 成长因子
    # EPS_Q_YOY
    factor_df['EPS_Q_YOY'] = (income_n['basic_eps'] - income_q['basic_eps']) / income_q['basic_eps']
    # NP_Q_YOY
    factor_df['NP_Q_YOY'] = (income_n['n_income_attr_p'] - income_q['n_income_attr_p']) / income_q['n_income_attr_p']
    # NP_QOQ
    factor_df['NP_QOQ'] = (income_n['n_income_attr_p'] - income_l['n_income_attr_p']) / income_l['n_income_attr_p']
    # OCF_Q_YOY
    factor_df['OCF_Q_YOY'] = (cashflow_n['n_cashflow_act'] - cashflow_q['n_cashflow_act']) / cashflow_q['n_cashflow_act']
    # OP_Q_YOY
    factor_df['OP_Q_YOY'] = (income_n['operate_profit'] - income_q['operate_profit']) / income_q['operate_profit']
    # OP_QOQ
    factor_df['OP_QOQ'] = (income_n['operate_profit'] - income_l['operate_profit']) / income_l['operate_profit']
    # 安全性因子(全部按季节算)
    # CCR
    factor_df['CCR'] = cashflow_n['n_cashflow_act'] / balance_n['total_cur_liab']
    # CCRD
    this_df1 = factor_df['CCR']
    this_df2 = cashflow_l['n_cashflow_act'] / balance_l['total_cur_liab']
    factor_df['CCRD'] = this_df1 - this_df2
    # CUR
    factor_df['CUR'] = indicator_n['current_ratio']
    # CURD
    factor_df['CURD'] = indicator_n['current_ratio'] - indicator_l['current_ratio']
    # DAD
    factor_df['DAD'] = indicator_n['debt_to_assets'] - indicator_l['debt_to_assets']
    # Debt_Asset
    factor_df['Debt_Asset'] = balance_n['total_liab'] / balance_n['total_assets']
    # DTE
    factor_df['DTE'] = indicator_n['debt_to_eqt']
    # DTED
    factor_df['DTED'] = indicator_n['debt_to_eqt'] / indicator_l['debt_to_eqt']
    # QR
    factor_df['QR'] = indicator_n['quick_ratio']
    # QRD
    factor_df['QRD'] = indicator_n['quick_ratio'] - indicator_l['quick_ratio']

    # 盈余质量
    # CSR
    factor_df['CSR'] = cashflow_n['c_cash_equ_end_period'] / balance_n['total_cur_liab']
    # CSRD
    factor_df['CSRD'] = factor_df['CSR'] - (cashflow_l['c_cash_equ_end_period'] / balance_l['total_cur_liab'])

    return factor_df


def get_annul_factor(num_year):

    balance_n = balance_dict[num_year]
    balance_l = balance_dict[num_year - 1]
    cashflow_n = cashflow_dict[num_year]
    cashflow_l = cashflow_dict[num_year - 1]
    income_n = income_dict[num_year]
    income_l = income_dict[num_year - 1]
    indicator_n = indicator_dict[num_year]
    indicator_l = indicator_dict[num_year - 1]

    factor_df = pd.DataFrame(index=balance_dict[2009].index)

    # 盈利能力因子
    # CFOA
    factor_df['CFOA'] = (cashflow_n['c_inf_fr_operate_a'] - cashflow_n['st_cash_out_act']) / balance_n['total_assets']
    # CFOAD
    this_df1 = (cashflow_l['c_inf_fr_operate_a'] - cashflow_l['st_cash_out_act']) / balance_l['total_assets']
    this_df2 = factor_df['CFOA']
    factor_df['CFOAD'] = this_df2 - this_df1
    # ROA_TTM
    factor_df['ROA_TTM'] = income_n['n_income_attr_p'] / balance_n['total_assets']
    # ROAD
    this_df1 = income_l['n_income_attr_p'] / balance_l['total_assets']
    this_df2 = factor_df['ROA_TTM']
    factor_df['ROAD'] = this_df2 - this_df1
    # ROE_TTM
    factor_df['ROE_TTM'] = indicator_n['roe']
    # ROED
    this_df1 = income_l['n_income_attr_p'] / balance_l['total_hldr_eqy_exc_min_int']
    this_df2 = factor_df['ROE_TTM']
    factor_df['ROED'] = this_df2 - this_df1
    # ROIC_TTM
    factor_df['ROIC_TTM'] = indicator_n['roic']
    # ROICD
    factor_df['ROIC_TTM'] = indicator_n['roic'] - indicator_l['roic']
    # 盈利能力因子
    # TOE
    factor_df['TOE'] = (balance_n['taxes_payable'] - balance_l['taxes_payable'] + cashflow_n['c_paid_for_taxes']) / balance_l['total_hldr_eqy_exc_min_int']
    # TOE_Z
    this_df1 = factor_df['TOE']
    factor_df['TOE_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()

    # 成长因子
    # EPS_YOY
    factor_df['EPS_YOY'] = (income_n['basic_eps'] - income_l['basic_eps']) / income_l['basic_eps']
    # NP_Deducted_YOY
    factor_df['NP_Deducted_YOY'] = (indicator_n['profit_dedt'] - indicator_l['profit_dedt']) / indicator_l['profit_dedt']
    # NP_YOY
    factor_df['NP_YOY'] = indicator_n['netprofit_yoy']
    # NP_Z
    this_df1 = factor_df['NP_YOY']
    factor_df['NP_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
    # OCF_YOY
    factor_df['OCF_YOY'] = (cashflow_n['n_cashflow_act'] - cashflow_l['n_cashflow_act']) / cashflow_l['n_cashflow_act']
    # OP_YOY
    factor_df['OP_YOY'] = indicator_n['op_yoy']
    # OP_Z
    this_df1 = factor_df['OP_YOY']
    factor_df['OP_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
    # OR_YOY
    factor_df['OR_YOY'] = indicator_n['or_yoy']
    # OT_Z
    this_df1 = income_n['biz_tax_surchg']
    factor_df['OT_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
    # PTCF_Z
    this_df1 = (cashflow_n['c_paid_for_taxes'] - cashflow_l['c_paid_for_taxes']) / cashflow_l['c_paid_for_taxes']
    factor_df['PTCF_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
    # ROE_YOY
    factor_df['ROE_YOY'] = indicator_n['roe_yoy']
    # TA_YOY
    factor_df['TA_YOY'] = indicator_n['assets_yoy']

    # 公司治理
    # DPR_TTM
    factor_df["DRP_TTM"] = cashflow_n['c_pay_dist_dpcp_int_exp'] / income_n['n_income']

    # 盈余质量
    # APR_TTM
    factor_df['APR_TTM'] = (income_n['n_income_attr_p'] - cashflow_n['n_cashflow_act']) / income_n['operate_profit']

    # 营运效率
    # AT
    factor_df['AT'] = income_n['total_revenue'] / balance_n['total_assets']
    # ATD
    this_df1 = income_l['total_revenue'] / balance_l['total_assets']
    factor_df['ATD'] = factor_df['AT'] - this_df1
    # GPMD
    factor_df['GPMD'] = indicator_n['grossprofit_margin'] - indicator_l['grossprofit_margin']
    # INVT
    factor_df['INVT'] = income_n['oper_cost'] / balance_n['inventories']
    # INVTD
    this_df1 = income_l['oper_cost'] / balance_l['inventories']
    factor_df['INVTD'] = factor_df['INVT'] - this_df1
    # NPM_TTM
    factor_df['NPM_TTM'] = income_n['n_income_attr_p'] / income_n['revenue']
    # OPM_TTM
    factor_df['OPM_TTM'] = income_n['operate_profit'] / income_n['revenue']
    # OPMD
    factor_df['OPMD'] = income_l['operate_profit'] / income_l['revenue']
    # OPtoGR_TTM
    factor_df['OPtoGR_TTM'] = income_n['operate_profit'] / indicator_n['gross_margin']
    # RAT
    factor_df['RAT'] = income_n['revenue'] / (balance_n['accounts_receiv'] + balance_n['notes_receiv'])
    # RATD
    factor_df['RATD'] = indicator_n['ar_turn'] - indicator_l['ar_turn']

    return factor_df


def calculate_ic(factor_data, returns):
    ic_values = pd.Series(index=factor_data.columns, dtype=float)
    for factor in factor_data.columns:
        ic = np.corrcoef(factor_data[factor], returns)[0, 1]
        ic_values[factor] = ic
    return ic_values.to_frame()

# ======================get the price=============================
p = pd.read_excel(root_path + r'/price_data/data/key_closed.xlsx', index_col=0)
log_return = np.log(p/p.shift(1))
log_return = log_return.iloc[1::2]
log_return.fillna(0, inplace=True)
log_return_rank = log_return.rank(axis=1,ascending=False)   # by row, largest one is No. 1

# target_dates = ['03-31', '06-30', '12-31']
# filtered_df = p[p.index.strftime('%m-%d').str.contains('|'.join(target_dates))]
# # get next day price
# next_indices = [p.index[p.index.get_loc(idx) + 1] for idx in filtered_df.index if idx != p.index[-1]]
# next_rows = p.loc[next_indices]
# result_df = pd.concat([filtered_df, next_rows])
# result_df = result_df.sort_index()


# =============== IC ===============
ic_values = pd.DataFrame()

for i in year_list[1:]:
    print(f'processing year {i}')
    annual_factor_df = get_annul_factor(i)

    q_num = 4 * (i - year_list[0]) + 1

    if i == 2019:
        period = 2
    else:
        period = 4

    for j in range(period):
        qq_num = q_num + j - 5
        time_columns = log_return.index[qq_num]
        q_factor_df = get_seasonal_factor_df(q_num+j)
        q_factor_df = q_factor_df.join(annual_factor_df)

        # fill all the NaN values with the average of their respective columns
        q_factor_df = q_factor_df.replace([np.inf, -np.inf], np.nan)
        factor_means = q_factor_df.mean()
        q_factor_df = q_factor_df.fillna(factor_means)

        q_factor_df.to_csv(str(i) + '_q' + str(j) + '_factor.csv')

        q_factor_df_rank = q_factor_df.rank(axis=0, ascending=False)    # by columns, largest one is No. 1

        ic_values[time_columns] = calculate_ic(q_factor_df_rank, log_return_rank.iloc[qq_num])

# ic_values.to_csv('ic_values.csv')

# 成长因子
# LPNP
# NP_SD
# NP_SUE0
# NP_SUE1
# OP_SD
# QPT

#营运效率
# OCFA

# =============== factor process ===============

# what about the extreme value?

# Drop columns with > 50% NaN values
# nan_percentage = (factor_df.isna().sum() / len(factor_df)) * 100
# columns_to_drop = nan_percentage[nan_percentage > 50].index
# factor_df = factor_df.drop(columns=columns_to_drop)
# # Drop rows with > 50% NaN values
# nan_percentage = (factor_df.isna().sum(axis=1) / len(factor_df.columns)) * 100
# rows_to_drop = nan_percentage[nan_percentage > 50].index
# factor_df = factor_df.drop(index=rows_to_drop)
# # fill all the NaN values with the average of their respective columns
# factor_means = factor_df.mean()
# factor_df = factor_df.fillna(factor_means)
#
# del nan_percentage, factor_means





