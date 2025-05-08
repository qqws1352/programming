```markdown
# Weather Data Analysis & Visualization System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green)](https://flask.palletsprojects.com/)
[![PyGWalker](https://img.shields.io/badge/PyGWalker-0.4.9.15-orange)](https://github.com/Kanaries/pygwalker)

基于OpenWeatherMap API的实时天气数据采集、分析与可视化系统，集成Flask Web展示与交互式分析功能。

---

## 🌟 项目亮点
- **全栈能力展示**：覆盖API调用→数据处理→可视化→Web部署全流程
- **交互式分析**：PyGWalker实现类Tableau的拖拽式数据探索
- **工程化实践**：环境变量管理、异常处理、自动化报告生成

## 🛠️ 技术栈
| 模块           | 技术实现                          |
|----------------|----------------------------------|
| 数据获取       | OpenWeatherMap API + Requests    |
| 数据处理       | Pandas                           |
| 可视化         | Matplotlib + PyGWalker           |
| Web框架        | Flask                            |
| 工程管理       | Python-dotenv + Git              |

---

## 🚀 快速启动

### 前置条件
- Python 3.8+
- [OpenWeatherMap API密钥](https://openweathermap.org/api)

### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/weather-analysis.git
   cd weather-analysis
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量  
   在项目根目录创建`.env`文件：
   ```python
   API_KEY=your_openweathermap_api_key
   ```

### 运行程序
```bash
python app.py
```
访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 查看效果

---

## 📂 项目结构
```text
weather-analysis/
├── app.py               # Flask主程序
├── data_utils.py        # 数据处理核心逻辑
├── .env                 # 环境变量配置
├── requirements.txt     # 依赖列表
├── static/              # 静态资源
│   ├── temp_comparison.png
│   ├── pyg_report.html
│   └── weather_data.csv
└── templates/           # 网页模板
    └── index.html
```

---

## 🖥️ 功能演示
### 1. 实时数据表格
![数据表格](https://via.placeholder.com/600x200?text=City+Temperature+Humidity+Wind_Speed)

### 2. 温度对比图表
![Matplotlib柱状图](https://via.placeholder.com/600x300?text=Temperature+Bar+Chart)

### 3. 交互式分析报告
```text
拖拽字段即可生成散点图/热力图/箱线图等
支持数据筛选、排序、图表类型切换
```

---

## 🛠️ 高级功能扩展
1. **历史数据存储**
   ```python
   # 在data_utils.py中添加
   def save_historical_data(df):
       import datetime
       timestamp = datetime.datetime.now().strftime("%Y%m%d")
       df.to_csv(f"static/history/weather_{timestamp}.csv")
   ```

2. **多城市选择**
   ```html
   <!-- 在index.html添加表单 -->
   <form method="POST">
     <input type="text" name="cities" placeholder="输入城市（用逗号分隔）">
     <button type="submit">更新数据</button>
   </form>
   ```

3. **部署到云服务**
   ```bash
   # 使用Heroku部署
   heroku create
   git push heroku main
   ```

---

## 📜 开源协议
[MIT License](LICENSE)

