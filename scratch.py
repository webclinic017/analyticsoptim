from datapackage import Package
import pandas as pd
import yahoo_fin as yf
import yahoo_fin.stock_info as si
package = Package('https://datahub.io/core/finance-vix/datapackage.json')
spy = si.get_data("SPY")
# print list of all resources:
print(__name__, package.resource_names)
# print(package.resources vix-daily_csv)
vix = pd.DataFrame(package.resources[1].read())
vix = vix.set_index(0)
vix = vix.rename({1: "Open_vix", 2: "High_vix", 3: "Low_vix", 4: "Close_vix"}, axis=1)
vix.index = pd.to_datetime(vix.index)
df = pd.concat([vix,spy], axis=1)
# print processed tabular data (if exists any)
# for resource in package.resources:
#     if resource.descriptor['datahub']['type'] == 'derived/csv':
#         print(resource.read())
