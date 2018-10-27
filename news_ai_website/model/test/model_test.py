from model.AnalyticsModel import AnalyticsModel

model = AnalyticsModel('model/deep_net_config_1.hdf5')
print (model.predict('U.S. Has Highest Share of Foreign-Born Since 1910, With More Coming From Asia', 'The foreign-born population in the United States has reached its highest share since 1910, according to government data released Thursday, and the new arrivals are more likely to come from Asia and to have college degrees than those who arrived in past decades.', 'other'))
