import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_total_sum_plot(items, name):
    df = pd.DataFrame(items, columns=["total_sum", "receipt_date"])
    df.rename(columns={"receipt_date": "date"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)

    fig = px.line(df, x='date', y='total_sum',
                  title=f'Sum of {name} Over Time', markers=True)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def get_multiple_axes_plot(items):
    df = pd.DataFrame(items)
    df.rename(columns={"receipt_date": "date"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)

    import plotly.graph_objects as go

    fig = go.Figure()

    # Line for price
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['price'],
        mode='lines+markers',
        name='Price'
    ))

    # Line for sum
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_sum'],
        mode='lines+markers',
        name='Sum'
    ))

    fig.update_layout(
        title="Price and Sum Over Time",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_dark",  # optional
        hovermode="x unified"
    )

    return fig.to_html(full_html=False, include_plotlyjs=False)
