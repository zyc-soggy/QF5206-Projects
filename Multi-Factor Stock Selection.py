import pandas as pd
import numpy as np

root_path = r"./"

# ==============import data=================


def read_and_process_csv(filename):
    df = pd.read_csv(filename, index_col=0)
    df = df.T.copy()
    return df.apply(pd.to_numeric, errors='coerce')


# Process the DataFrames
balance_2017 = read_and_process_csv(root_path + 'data/2017/balance_2017.csv')
balance_2018 = read_and_process_csv(root_path + 'data/2018/balance_2018.csv')
balance_2019 = read_and_process_csv(root_path + 'data/2019/balance_2019.csv')

cashflow_2017 = read_and_process_csv(root_path + 'data/2017/cashflow_2017.csv')
cashflow_2018 = read_and_process_csv(root_path + 'data/2018/cashflow_2018.csv')
cashflow_2019 = read_and_process_csv(root_path + 'data/2019/cashflow_2019.csv')

income_2017 = read_and_process_csv(root_path + 'data/2017/income_2017.csv')
income_2018 = read_and_process_csv(root_path + 'data/2018/income_2018.csv')
income_2019 = read_and_process_csv(root_path + 'data/2019/income_2019.csv')

indicator_2017 = read_and_process_csv(root_path + 'data/2017/indicator_2017.csv')
indicator_2018 = read_and_process_csv(root_path + 'data/2018/indicator_2018.csv')
indicator_2019 = read_and_process_csv(root_path + 'data/2019/indicator_2019.csv')

semi_income_2018 = read_and_process_csv(root_path + 'data/2018/semi_income_2018.csv')
semi_income_2019 = read_and_process_csv(root_path + 'data/2019/semi_income_2019.csv')

semi_cashflow_2018 = read_and_process_csv(root_path + 'data/2018/semi_cashflow_2018.csv')
semi_cashflow_2019 = read_and_process_csv(root_path + 'data/2019/semi_cashflow_2019.csv')

factor_df = pd.DataFrame(index=balance_2019.index)

# =============== data cleaning =============
# def is_numeric(s):
#     try:
#         pd.to_numeric(s)
#         return True
#     except ValueError:
#         return False


# =============== factor ===============
# 为了避免占用太多内存，临时储存数据的变量应反复使用this_df1,this_df2,...
# 最后计算的结果储存在factor_df表格中

# 盈利能力因子
# CFOA
factor_df['CFOA'] = (cashflow_2019['c_inf_fr_operate_a'] - cashflow_2019['st_cash_out_act'])/balance_2019['total_assets']
# CFOAD
this_df1 = (cashflow_2018['c_inf_fr_operate_a'] - cashflow_2018['st_cash_out_act'])/balance_2018['total_assets']
this_df2 = factor_df['CFOA']
factor_df['CFOAD'] = this_df2 - this_df1
# ROA_TTM
# 净利润中有多个词条：cashflow_2019['net_profit']为空，不选; income_2019['n_income']为净利润(含少数股东损益);
# income_2019['n_income_attr_p']为净利润(不含少数股东损益)，此处选择income_2019['n_income_attr_p']
factor_df['ROA_TTM'] = income_2019['n_income_attr_p']/balance_2019['total_assets']
# ROAD
this_df1 = income_2018['n_income_attr_p']/balance_2018['total_assets']
this_df2 = factor_df['ROA_TTM']
factor_df['ROAD'] = this_df2 - this_df1
# ROE_TTM
factor_df['ROE_TTM'] = indicator_2019['roe']
# ROED
this_df1 = income_2018['n_income_attr_p']/balance_2018['total_hldr_eqy_exc_min_int']
this_df2 = factor_df['ROE_TTM']
factor_df['ROED'] = this_df2 - this_df1
# ROIC_TTM
factor_df['ROIC_TTM'] = indicator_2019['roic']
# ROICD
factor_df['ROIC_TTM'] = indicator_2019['roic'] - indicator_2018['roic']
# TOE
factor_df['TOE'] = (balance_2019['taxes_payable'] - balance_2018['taxes_payable']+cashflow_2019['c_paid_for_taxes'])/balance_2019['total_hldr_eqy_exc_min_int']
# TOE_Z
this_df1 = factor_df['TOE']
factor_df['TOE_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()

# 成长因子
# EPS_Diluted_Q_YOY
factor_df['EPS_Diluted_Q_YOY'] = (semi_income_2019['diluted_eps'] - semi_income_2018['diluted_eps'])/semi_income_2018['diluted_eps']
# EPS_Q_YOY
factor_df['EPS_Q_YOY'] = (semi_income_2019['basic_eps'] - semi_income_2018['basic_eps'])/semi_income_2018['basic_eps']
# EPS_YOY
factor_df['EPS_YOY'] = (income_2019['basic_eps'] - income_2018['basic_eps'])/income_2018['basic_eps']
# LPNP
# more history data needed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NP_Deducted_YOY
factor_df['NP_Deducted_YOY'] = (indicator_2019['profit_dedt'] - indicator_2018['profit_dedt'])/indicator_2018['profit_dedt']
# NP_Q_YOY
factor_df['NP_Q_YOY'] = (semi_income_2019['n_income_attr_p'] - semi_income_2018['n_income_attr_p']) / semi_income_2018['n_income_attr_p']
# NP_QOQ
this_df1 = income_2019['net_profit'] - semi_income_2018['net_profit']
factor_df['NP_QOQ'] = (semi_income_2019['net_profit'] - this_df1) / this_df1
# NP_SD
# more history data!!!!!!!!!!!!!!!!!!!!!!!!!!
# NP_SUE0
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NP_SUE1
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NP_YOY
factor_df['NP_YOY'] = indicator_2019['netprofit_yoy']
# NP_Z
this_df1 = factor_df['NP_YOY']
factor_df['NP_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
# OCF_Q_YOY
factor_df['OCF_Q_YOY'] = (semi_cashflow_2019['n_cashflow_act'] - semi_cashflow_2019['n_cashflow_act']) / semi_cashflow_2018['n_cashflow_act']
# OCF_YOY
factor_df['OCF_YOY'] = (cashflow_2019['n_cashflow_act'] - cashflow_2018['n_cashflow_act']) / cashflow_2018['n_cashflow_act']
# OP_Q_YOY
factor_df['OP_Q_YOY'] = (semi_income_2019['operate_profit'] - semi_income_2018['operate_profit']) / semi_income_2018['operate_profit']
# OP_QOQ
# this_df1 =
# OP_SD
# ??????????????????????????????????????????????
# OP_YOY
factor_df['OP_YOY'] = indicator_2019['op_yoy']
# OP_Z
this_df1 = factor_df['OP_YOY']
factor_df['OP_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
# OR_YOY
factor_df['OR_YOY'] = indicator_2019['or_yoy']
# OT_Z
this_df1 = income_2019['biz_tax_surchg']
factor_df['OT_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
# PTCF_Z
this_df1 = (cashflow_2019['c_paid_for_taxes'] - cashflow_2018['c_paid_for_taxes']) / cashflow_2018['c_paid_for_taxes']
factor_df['PTCF_Z'] = (this_df1 - this_df1.mean()) / this_df1.std()
# QPT
# ????????????????????????????????????????????????????
# ROE_YOY
factor_df['ROE_YOY'] = indicator_2019['roe_yoy']
# TA_YOY
factor_df['TA_YOY'] = indicator_2019['assets_yoy']

#公司治理
#DPR_TTM
factor_df["DRP_TTM"] = cashflow_2019['c_pay_dist_dpcp_int_exp']/income_2019['n_income']

#安全性因子
#CCR
factor_df['CCR'] = cashflow_2019['im_net_cashflow_oper_act']/balance_2019['total_cur_liab']
#CCRD
this_df1 = factor_df['CCR']
this_df2 = cashflow_2018['im_net_cashflow_oper_act']/balance_2018['total_cur_liab']
factor_df['CCRD'] = this_df1 - this_df2
#CUR
factor_df['CUR'] = indicator_2019['current_ratio']
#CURD
factor_df['CURD'] = indicator_2019['current_ratio'] - indicator_2018['current_ratio']
#DAD
factor_df['DAD'] = indicator_2019['debt_to_assets'] - indicator_2018['debt_to_assets']
#Debt_Asset
factor_df['Debt_Asset'] = balance_2019['total_liab']/balance_2019['total_assets']
#DTE
factor_df['DTE'] = indicator_2019['debt_to_eqt']
#DTED
factor_df['DTED'] = indicator_2019['debt_to_eqt']/indicator_2018['debt_to_eqt']
#QR
factor_df['QR'] = indicator_2019['quick_ratio']
#QRD
factor_df['QRD'] = indicator_2019['quick_ratio']-indicator_2018['quick_ratio']

#盈余质量
#APR_TTM 缺少应计利润数据
#CSR
factor_df['CSR'] = cashflow_2019['c_cash_equ_end_period']/balance_2019['total_cur_liab']
#CSRD
factor_df['CSRD'] = factor_df['CSR'] - (cashflow_2018['c_cash_equ_end_period']/balance_2018['total_cur_liab'])

#营运效率
#AT
this_df1 = income_2019['total_revenue']-income_2018['total_revenue']
this_df2 = pd.concat([balance_2019['total_assets'], balance_2019['total_assets']]).mean(axis=0)
factor_df['AT'] = this_df1/this_df2
#ATD
this_df1 = income_2018['total_revenue']-income_2018['total_revenue']
this_df2 = pd.concat([balance_2018['total_assets'], balance_2017['total_assets']]).mean(axis=0)
this_df3 = this_df1/this_df2
factor_df['ATD'] = factor_df['AT']-this_df3
#GPMD
factor_df['GPMD'] = indicator_2019['grossprofit_margin']-indicator_2018['grossprofit_margin']-(indicator_2018['grossprofit_margin']-indicator_2017['grossprofit_margin'])
#INVT
this_df1 = income_2019['oper_cost'] - income_2018['oper_cost']
this_df2 = (balance_2019['inventories'] + balance_2018['inventories'])/2
factor_df['INVT'] = this_df1/this_df2
#INVTD
this_df1 = income_2018['oper_cost'] - income_2017['oper_cost']
this_df2 = (balance_2018['inventories'] + balance_2017['inventories'])/2
this_df3 = this_df1/this_df2
factor_df['INVTD'] = factor_df['INVT'] - this_df3
#NPM_TTM
this_df1 = cashflow_2019['net_profit'] - cashflow_2018['net_profit']
this_df2 = income_2019['revenue'] - income_2018['revenue']
factor_df['NPM_TTM'] = this_df1/this_df2
#OCFA ?
#OPM_TTM
this_df1 = income_2019['operate_profit'] - income_2018['operate_profit']
this_df2 = income_2019['revenue'] - income_2018['revenue']
factor_df['OPM_TTM'] = this_df1/this_df2
#OPMD
this_df1 = income_2018['operate_profit'] - income_2017['operate_profit']
this_df2 = income_2018['revenue'] - income_2017['revenue']
this_df3= this_df1/this_df2
factor_df['OPMD'] = factor_df['OPM_TTM'] - this_df3
#OPtoGR_TTM
this_df1 = income_2019['operate_profit'] - income_2018['operate_profit']
this_df2 = indicator_2019['gross_margin'] - indicator_2018['gross_margin']
factor_df['OPtoGR_TTM'] = this_df1/this_df2
#RAT
this_df1 = (balance_2019['accounts_receiv'] + balance_2018['accounts_receiv'])/2
this_df2 = (balance_2019['notes_receiv'] + balance_2018['notes_receiv'])/2
this_df3 = income_2018['revenue'] - income_2017['revenue']
factor_df['RAT'] = this_df3/(this_df1+this_df2)
#RATD
factor_df['RATD'] = indicator_2019['ar_turn'] - indicator_2018['ar_turn']

del this_df1, this_df2, this_df3

# =============== factor process ===============

# what about the extreme value?

# Drop columns with > 50% NaN values
nan_percentage = (factor_df.isna().sum() / len(factor_df)) * 100
columns_to_drop = nan_percentage[nan_percentage > 50].index
factor_df = factor_df.drop(columns=columns_to_drop)
# Drop rows with > 50% NaN values
nan_percentage = (factor_df.isna().sum(axis=1) / len(factor_df.columns)) * 100
rows_to_drop = nan_percentage[nan_percentage > 50].index
factor_df = factor_df.drop(index=rows_to_drop)
# fill all the NaN values with the average of their respective columns
factor_means = factor_df.mean()
factor_df = factor_df.fillna(factor_means)

del nan_percentage, factor_means

# =============== IC ===============
factor_rank = factor_df.rank(axis=0)

p = pd.read_excel(root_path+r'/price_data/data/closed.xlsx', index_col=0)
log_return = (p.iloc[-1]/p.iloc[-244]).rank()    # -244 to get the price one year before
del p
log_return.dropna(inplace=True)

index_intersection = log_return.index.intersection(factor_rank.index)
log_return = log_return.loc[index_intersection]
factor_rank = factor_rank.loc[index_intersection]

# calculate ic
def calculate_ic(factor_data, returns):
    ic_values = {}
    for factor in factor_data.columns:
        ic = np.corrcoef(factor_data[factor], returns)[0, 1]
        ic_values[factor] = ic
    return ic_values

ic_values = calculate_ic(factor_rank, log_return)

# 按IC值排序
sorted_ic = sorted(ic_values.items(), key=lambda x: x[1], reverse=True)





