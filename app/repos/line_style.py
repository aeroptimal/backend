import plotly.express as px
import plotly.graph_objects as go
import numpy as np 
import pandas as pd

def style(df,title,xlabel,ylabel):
    fig = px.line(df,x=xlabel, y=ylabel, title=title, color_discrete_sequence=["black"])
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    fig.update_yaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)', scaleanchor = "x", scaleratio = 1)
    return fig

def style_thrust(df,title,xlabel,ylabel):
    fig = px.line(df,x=xlabel, y=ylabel, title=title, color_discrete_sequence=["black"])
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    fig.update_yaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    return fig

def style_takeOff(x,names,title,xlabel,ylabel):
    if x[-1] < 1.5:
        x = list(np.array(x)+1.5)
    names = [names[i] for i in range(0,len(x)) if x[i]]
    x = [x[i] for i in range(0,len(x)) if x[i]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0,1.5], y=[0,2+len(x)-1],line_shape='linear',line=dict(color='black'),showlegend = False))
    fig.add_trace(go.Scatter(x=[1.5,(x[0]+5)], y=[2+len(x)-1,2+len(x)-1],line_shape='linear',line=dict(color='black'),showlegend = False))
    fig.add_trace(go.Scatter(x=[(x[0]+3.5),(x[0]+5)], y=[0,2+len(x)-1],line_shape='linear',line=dict(color='black'),showlegend = False))
    fig.add_trace(go.Scatter(x=[0,(x[0]+3.5)], y=[0,0],line_shape='linear',line=dict(color='black'),showlegend = False))
    fig.update_layout(showlegend=False)
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)',range=[0,x[0]+8],showgrid= False)
    fig.update_yaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)',range=[0,len(x)+10],showgrid= False)
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel, title=title)

    colors = ['red','orange', 'blue','cyan','green','darkgreen']

    fig.update_layout(showlegend=True)
    inc = 0
    for i in range(0,len(x),1):
        fig.add_trace(go.Scatter(x=[0.25+(1.5/(2+len(x)-1))*i,(x[0]+3.5+(1.5/(2+len(x)-1))*i)], y=[1+inc,1+inc],line_shape='linear',line=dict(color='black',width=0.5),showlegend = False))
        fig.add_trace(go.Scatter(x=[0.25+(1.5/(2+len(x)-1))*i,x[i]], y=[1+inc,1+inc],name=names[i] + '% Throtle'  ,line_shape='linear',line=dict(color=colors[i],dash='dot',width=8),showlegend = True))
        inc+=0.75
    return fig

def style_battery(df,title,xlabel,ylabel):
    fig = px.line(df,x=xlabel, y=ylabel, title=title, color_discrete_sequence=["black"])
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=True, fixedrange=True, range=[0,df[xlabel].iloc[-1]], gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    fig.update_yaxes(visible=True, fixedrange=True, range=[df[ylabel].iloc[-1]*(0.95),df[ylabel].iloc[0]], gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    return fig

def style_battery_load(df,title,xlabel,ylabel):
    fig = px.line(df,x=xlabel, y=ylabel, title=title, color_discrete_sequence=["black"])
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    fig.update_yaxes(visible=True, fixedrange=True, gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)')
    return fig

def style_mesh(x,y,title,xlabel,ylabel):
    fig = px.scatter(x=x, y=y, color_discrete_sequence=["black"])
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    fig.update_traces(marker_size=3)
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)', visible=True, range=[min(x)*1.1,max(x)*1.1])
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.3)', linecolor='rgba(0,0,0,0.5)', scaleanchor = "x", scaleratio = 1)
    return fig