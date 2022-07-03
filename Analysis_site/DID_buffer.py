import statsmodels.formula.api as smf
import pandas as pd

v1 = [0.467730, 0.477147, 0.452539, 0.441864, 0.29276, 0.393443, 0.374697, 0.346989, 0.385783, 0.307801]
t1 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
g1 = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
tg1 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
aa = pd.DataFrame({'t1': t1, 'g1': g1, 'tg1': tg1, 'v1': v1})
X = aa[['t1', 'g1', 'tg1']]
y = aa['v1']
est = smf.ols(formula='v1 ~ t1 + g1 + tg1', data=aa).fit()
y_pred = est.predict(X)
aa['v1_pred'] = y_pred
print(aa)
print(est.summary())
print(est.params)
