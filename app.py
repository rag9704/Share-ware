import streamlit as st
import pandas as pd
import random
from datetime import datetime,timedelta
import pytz
import yfinance as yf
import time

# Define IST timezone
IST = pytz.timezone("Asia/Kolkata")
# Get today's date in IST
today_ist = datetime.now(IST).date()


st.title("Monkey Business")
st.markdown(
    """
    ### 🐒 Monkey vs Market: Can Random Picks Beat Your Portfolio?

    In 1973, Princeton professor **Burton Malkiel** famously claimed in his book _A Random Walk Down Wall Street_ that  
    > “A blindfolded monkey throwing darts at a newspaper's financial pages could select a portfolio that would do just as well as one carefully selected by experts.”

    But what if the monkey *actually* performs better?

    According to research by **Rob Arnott** and his team at Research Affiliates, 100 randomly selected portfolios (a.k.a. "monkeys")  
    beat the market nearly **98% of the time** over several decades!  
    [📖 Read the full article on Forbes →](https://www.forbes.com/sites/rickferri/2012/12/20/any-monkey-can-beat-the-market/)

    ---

    This tool lets you simulate that experiment.  
    Select a date, choose the number of random companies, and see if a dart-throwing monkey would have done better than your hand-picked portfolio!

    🔄 Let the monkey games begin...
    """
)

st.write("Does random selection of stock beat your portfolio? ")
start_date = st.date_input("share buying date", datetime.today() - timedelta(days=183))

if start_date.weekday() == 5:  # Saturday
    start_date += timedelta(days=2)
elif start_date.weekday() == 6:  # Sunday
    start_date += timedelta(days=1)



end_date =  today_ist

if end_date.weekday() == 5:  # Saturday
    end_date += timedelta(days=2)
elif end_date.weekday() == 6:  # Sunday
    end_date += timedelta(days=1)


st.write("Your share buying date is:", start_date)
symbols = pd.read_csv("EQUITY_L.csv")["SYMBOL"].tolist()
tickers = [f"{s}.NS" for s in symbols]
n_o_s = st.number_input (
    "number of companies", value=5, placeholder="Type a number..."
)
if st.button("Run Simulation"):
        progress_text = "Downloading stock data... Please wait."
        my_bar = st.progress(0, text=progress_text)

        random_sample = random.sample(tickers, n_o_s)
        ret = []
        graph=[]
        
        for i,tkr in enumerate(random_sample):
            x = yf.download(
                    tickers=tkr,
                    start=start_date,
                    end=today_ist,
                    interval="1d",
                    threads=False,
                    progress=False,
                    auto_adjust=False
                )['Close'][tkr]
            
            graph.append(list(x.values))
            ret.append((x[-1] / x[0] - 1))
            percent_complete = int((i + 1) / len(random_sample) * 100)
            my_bar.progress(percent_complete, text=f"{progress_text} ({percent_complete}%)")
            time.sleep(0.1)  
        time.sleep(0.5)

        portfolio = 100*sum(ret)/len(ret)
        if portfolio < 0:
            st.write(f"Your return would have been :red[{portfolio:.2f}%]")
        else:
            st.write(f"Your return would have been :green[{portfolio:.2f}%]")

        df = pd.DataFrame(
            {
                    "name": random_sample,
                    "views_history": graph,
                }
            )
        row_height = 40  # Approximate row height in pixels
        base_height = 100  # Space for header, padding, etc.

        dynamic_height =len(df) * row_height
            
        st.dataframe(
                    df,
                    column_config={
                        "name": "Stocks",
                        "views_history": st.column_config.LineChartColumn(
                            "Views (past 30 days)", y_min=0, y_max=1000
                        ),
                    },
                    hide_index=True,
                    use_container_width=True,  # expands to full width
                    height=dynamic_height,  # increase this value for more height
                )

       





