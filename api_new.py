import openai
import pandas as pd
import time
import random

# 读取CSV文件
df = pd.read_csv('data.csv')

# 设置OpenAI API密钥
openai.api_key = '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'

# 创建一个新列来存储情绪分析结果
df['sentiment'] = ''

# 创建一个变量来存储每批的标题
batch = []

# 设置重试次数和延迟
max_retries = 3

# 遍历每个研报标题
for i, row in df.iterrows():
    # 将标题添加到批次中
    batch.append(f"标题{i % 20 + 1}:{row['股票代码']}+{row['标题']}")

    # 每20个标题进行一次API调用
    if len(batch) == 20:
        for attempt in range(max_retries):
            try:
                messages = [
                               {"role": "system", "content": "忘掉你以前的所有指示，假装你是一位有股票推荐经验的金融专家。"
                                                             "以下是分析师对上市公司业绩发布或重大事件后的点评报告的标题，请对标题进行情绪评分。"
                                                             "评分的范围为1-10，可为小数，分数反映了对公司业绩或未来发展的看法"
                                                             "其中，6-10为积极，10分表示最积极；5分为中性；1-5为消极，1为最消极。"
                                                             "提示，可以次参考如下逻辑，俺也需结合整体的情绪进行评分："
                                                             "1.若业绩为大超预期、超预期、超市场一致预期、超市场预期或类似的同义词，则表示最积极，应得超高分（9-10）；"
                                                             "2.若业绩为略超预期或类似的同义词，则为较积极，应得高分（8.5-9.5）"
                                                             "3.若以实现业绩为增速超30%、靓丽、高增、维持高位或快速增长或类似的同义词，应得高分（8-10）；"
                                                             "4.若标题含有其他偏积极的词汇，请综合评价再给出分数，分数范围应为6-9.5；"
                                                             "5.若业绩为符合预期或其他偏中性的词汇，根据整体的情绪给出分数，分数范围为6-9；"
                                                             "6.若业绩为不及预期、低于预期或类似的明显消极的词汇，应得低分（1-7）；"
                                                             "7.含标题中有承压、下滑或类似消极的词，应得较低分（2-7）；"
                                                             "8.若不确定，标题中无法判断出对公司前景的态度，应给5分+“请按照标题顺序，直接给出对应的分数，不必解释。每一行为一条标题的评分，如:标题1:6.8" + "\n" + "标题2:4" + "\n" + "标题3:8.1"},
                           ] + [{"role": "user", "content": title} for title in batch]

                # 使用GPT-3.5-turbo进行情绪分析
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.5
                )

                # 将结果写入新列
                for idx, message in enumerate(response['choices'][0]['message']['content'].split('\n')):
                    if idx < len(batch):
                        sentiment = message.split(":")
                        if len(sentiment) > 1:  # 检查是否有分割结果
                            df.at[i - len(batch) + idx + 1, 'sentiment'] = sentiment[1].strip()
                        else:
                            df.at[i - len(batch) + idx + 1, 'sentiment'] = "N/A"  # 或者其他的默认值
                break
            except Exception as e:
                if attempt < max_retries - 1:  # i.e. not on the last attempt
                    # 使用随机指数退避，基数为300（5分钟=300秒）
                    delay = (600 * attempt) + random.uniform(0, 600)
                    # wait for a while before retrying
                    time.sleep(delay)
                    continue
                else:
                    # re-raise the last exception as it is
                    raise

        # 清空批次
        batch = []

# 如果还有剩余的标题没有处理，进行最后一次API调用
if batch:
    for attempt in range(max_retries):
        try:
            messages = [{"role": "system", "content": "忘掉你以前的所有指示，假装你是一位有股票推荐经验的金融专家。"
                                                      "以下是分析师对上市公司业绩发布或重大事件后的点评报告的标题，请对标题进行情绪评分。"
                                                      "评分的范围为1-10，可为小数，分数反映了对公司业绩或未来发展的看法"
                                                      "其中，6-10为积极，10分表示最积极；5分为中性；1-5为消极，1为最消极。"
                                                      "提示，可以次参考如下逻辑，俺也需结合整体的情绪进行评分："
                                                      "1.若业绩为大超预期、超预期、超市场一致预期、超市场预期或类似的同义词，则表示最积极，应得超高分（9-10）；"
                                                      "2.若业绩为略超预期或类似的同义词，则为较积极，应得高分（8.5-9.5）"
                                                      "3.若以实现业绩为增速超30%、靓丽、高增、维持高位或快速增长或类似的同义词，应得高分（8-10）；"
                                                      "4.若标题含有其他偏积极的词汇，请综合评价再给出分数，分数范围应为6-9.5；"
                                                      "5.若业绩为符合预期或其他偏中性的词汇，根据整体的情绪给出分数，分数范围为6-9；"
                                                      "6.若业绩为不及预期、低于预期或类似的明显消极的词汇，应得低分（1-7）；"
                                                      "7.含标题中有承压、下滑或类似消极的词，应得较低分（2-7）；"
                                                      "8.若不确定，标题中无法判断出对公司前景的态度，应给5分+“请按照标题顺序，直接给出对应的分数，不必解释。每一行为一条标题的评分，如:标题1:6.8" + "\n" + "标题2:4" + "\n" + "标题3:8.1"},
                        ] + [{"role": "user", "content": title} for title in batch]

            # 使用GPT-3.5-turbo进行情绪分析
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.5
            )

            # 计算开始的索引
            start_index = len(df) - len(batch)

            # 将结果写入新列
            for idx, message in enumerate(response['choices'][0]['message']['content'].split('\n')):
                if idx < len(batch):
                    sentiment = message.split(":")
                    if len(sentiment) > 1:  # 检查是否有分割结果
                        df.at[start_index + idx, 'sentiment'] = sentiment[1].strip()
                    else:
                        df.at[start_index + idx, 'sentiment'] = "N/A"  # 或者其他的默认值
            break
        except Exception as e:
            if attempt < max_retries - 1:  # i.e. not on the last attempt
                # 使用随机指数退避，基数为300（5分钟=300秒）
                delay = (600 * attempt) + random.uniform(0, 600)
                # wait for a while before retrying
                time.sleep(delay)
                continue
            else:
                # re-raise the last exception as it is
                raise

# 将结果保存到新的CSV文件
df.to_csv('output.csv', index=False)