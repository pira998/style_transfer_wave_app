from matplotlib.pyplot import title
import plotly.express as px
import pandas as pd 
import numpy as np

import plotly.graph_objects as go
from plotly import io as pio

np.random.seed(19680801)
async def plotly_test():
	n = 25
	fig = go.Figure(data=go.Scatter(
		x=np.random.rand(n),
		y=np.random.rand(n),
		mode='markers',
		marker=dict(size=(8 * np.random.rand(n)) ** 2,
					color=np.random.rand(n)),
		opacity=0.8,
	))
	_ = fig.update_layout(
		margin=dict(l=10, r=10, t=10, b=10),
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		font_color="rgb(0,0,0)",
	)
	html = fig.to_html(include_plotlyjs='cdn', config={
	                   'scrollZoom': False, 'showLink': False, 'displayModeBar': False})

	return html
