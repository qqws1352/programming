import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 加载.env中的API_KEY


def fetch_weather_data(city="Beijing"):
    api_key = os.getenv("API_KEY")  # 从环境变量读取密钥
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)  # 发送API请求
    data = response.json()  # 解析JSON响应

    # 提取关键字段
    return {
        "temp": data["main"]["temp"],  # 温度（摄氏度）
        "humidity": data["main"]["humidity"],  # 湿度（百分比）
        "wind_speed": data["wind"]["speed"]  # 风速（米/秒）
    }

import pandas as pd

def create_dataframe(cities=["Beijing", "Shanghai", "Guangzhou","Hefei"]):
    data = [fetch_weather_data(city) for city in cities]  # 获取多城市数据
    df = pd.DataFrame(data, index=cities)  # 创建Pandas DataFrame
    return df

import matplotlib.pyplot as plt

def plot_weather(df):
    plt.figure(figsize=(10, 6))
    df['temp'].plot(kind='bar', color='skyblue')  # 生成柱状图
    plt.title('Temperature Comparison')
    plt.ylabel('°C')
    plt.savefig('static/temp_comparison.png')  # 保存图片到static目录

import pygwalker as pyg

def generate_pygwalker_report(df):
    try:
        os.makedirs("static", exist_ok=True)
        html = pyg.walk(df, return_html=True)
        with open("static/pyg_report.html", "w") as f:
            f.write(html)
    except Exception as e:
        print(f"生成PyGWalker报告失败: {str(e)}")


def save_to_csv(df):
    """将DataFrame保存到CSV文件"""
    # 确保static文件夹存在（否则会报错）
    df.to_csv('static/weather_data.csv', index_label="City")  # index_label为索引列命名

# # data_utils.py中修改保存函数
# import datetime
#
# def save_to_csv(df):
#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"static/weather_data_{timestamp}.csv"  # 按时间戳生成唯一文件名
#     df.to_csv(filename)