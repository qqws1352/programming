from flask import Flask, render_template
from data_utils import create_dataframe, plot_weather, save_to_csv,generate_pygwalker_report

app = Flask(__name__)


# app.py

@app.route('/')
def index():
    df = create_dataframe()
    save_to_csv(df)
    plot_weather(df)

    # 新增调用：生成PyGWalker报告
    generate_pygwalker_report(df)  # <-- 添加此行

    return render_template('index.html',
                           table=df.to_html(classes='table table-striped'),
                           img_path='temp_comparison.png',
                           pyg_report='pyg_report.html')


if __name__ == '__main__':
    app.run(debug=True)
