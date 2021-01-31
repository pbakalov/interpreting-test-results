# import ipywidgets as widgets
import plotly.graph_objects as go 
from numpy import linspace


def leaf_plot(sense, spec):
    fig = go.Figure()

    x = linspace(0,1,101)
    x[0] += 1e-16
    x[-1] -= 1e-16
    #Bayes' rule: p(a|b) = p(b|a)*p(a)/p(b)
    #
    #p(pr) = sensitivity*p(base) + (1-specificity)*(1-p(base))
    #p(nr) = (1-sensitivity)*p(base) + specificity*(1-p(base))

    positive = sense*x/(sense*x + (1-spec)*(1-x)) 
                                                    #probability a person is infected, given a positive test result, 
                                                    #P(p|pr) = P(pr|p)*P(p)/P(pr)
                                                    #        = P(pr|p)*P(p)/(P(pr|p)*P(p) + P(pr|n)*P(n))
                                                    #        =   sense*P(p)/(  sense*P(p) +(1-spec)*P(n))
    negative = 1-spec*(1-x)/((1-sense)*x + spec*(1-x))

    fig.add_trace(
        go.Scatter(x=x, y  = positive, name="Positive",marker=dict( color='red'))
    )

    fig.add_trace(
        go.Scatter(x=x, y  = negative, 
                   name="Negative", 
                   mode = 'lines+markers',
                   marker=dict( color='green'))
    )
    
    fig.update_layout(
    xaxis_title="Base rate",
    yaxis_title="After-test probability",
    )

    return fig


#from jupyter_dash import JupyterDash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Build App
#app = JupyterDash(__name__)
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Interpreting Test Results"),
    dcc.Graph(id='graph'),
    html.Label([
        "sensitivity",
        dcc.Slider(
            id='sensitivity-slider',
            min=0,
            max=1,
            step=0.01,
            value=0.5,
            marks = {i: '{:5.2f}'.format(i) for i in linspace(1e-16,1-1e-16,11)}
        ),
    ]),
    html.Label([
        "specificity",
        dcc.Slider(
            id='specificity-slider',
            min=0,
            max=1,
            step=0.01,
            value=0.5,
            marks = {i: '{:5.2f}'.format(i) for i in linspace(1e-16,1-1e-16,11)}
        ),
    ]),
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    Input("sensitivity-slider", "value"),
    Input("specificity-slider", "value")
)
def update_figure(sense, spec):
    return leaf_plot(sense, spec)

# Run app and display result inline in the notebook
app.run_server()
