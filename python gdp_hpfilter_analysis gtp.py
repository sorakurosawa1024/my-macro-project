import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas_datareader import data as web

# ---- 設定 ----
plt.style.use('ggplot')
start_date = '1980-01-01'
end_date = '2022-01-01'
country_code = 'JP'
gdp_series_id = 'JPNRGDPEXP'  # 日本の実質GDP (FRED)

# ---- 1. データ取得 ----
gdp = web.DataReader(gdp_series_id, 'fred', start_date, end_date)
gdp.dropna(inplace=True)

# ---- 2. 自然対数変換 ----
log_gdp = np.log(gdp)

# ---- 3. HPフィルターの適用（λ=10, 100, 1600） ----
lambdas = [10, 100, 1600]
trends = {}
cycles = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lam)
    trends[lam] = trend
    cycles[lam] = cycle

# ---- 4. 可視化 ----

# グラフ1：元データとトレンド成分
plt.figure(figsize=(12, 6))
plt.plot(log_gdp, label='Log Real GDP', color='black', linewidth=2)
for lam in lambdas:
    plt.plot(trends[lam], label=f'Trend (λ={lam})')
plt.title('Japan Log Real GDP and HP Trends (λ=10, 100, 1600)')
plt.xlabel('Date')
plt.ylabel('Log GDP')
plt.legend()
plt.tight_layout()
plt.savefig("japan_gdp_trends.png", dpi=300)
plt.show()

# グラフ2：循環成分の比較
plt.figure(figsize=(12, 6))
for lam in lambdas:
    plt.plot(cycles[lam], label=f'Cycle (λ={lam})')
plt.title('Japan GDP Cyclical Component via HP Filter')
plt.xlabel('Date')
plt.ylabel('Deviation from Trend (log)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.legend()
plt.tight_layout()
plt.savefig("japan_gdp_cycles.png", dpi=300)
plt.show()
