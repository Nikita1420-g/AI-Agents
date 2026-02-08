import os
import yfinance as yf
import streamlit as st
from groq  import Groq
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

#initialise Groq client
client= Groq(api_key=os.getenv("GROQ_API_KEY"))

#function to fetch and compare stock data
def compare_stocks(symbols):
    data={}
    for symbol in symbols:
        try:

            #fetch stock data
            stock= yf.Ticker(symbol)
            hist= stock.history(period="6mo") # fect last 6 months ago

            if hist.empty:
                print(f"No data found for {symbol}, skiping it")
                continue
            start_price= hist['Close'].iloc[0]
            end_price= hist['Close'].iloc[-1]
            percent_change=((end_price- start_price)/start_price)*100

            #calculate overall % change
            data[symbol]= percent_change

        except Exception as e:
            print(f"could not retrieve data for {symbol}, Reason: {str(e)}")
            continue

    return data
    
# define the ,arket analysis agent
#market_analysis=Agent(
    #model= Gemini(id="models/gemini-2.5-flash"),
    #description="Analysis anad compare stock prices over time",
    #instructions=[
     #   "Retrieve and compare stock performance from yahoo finance",
      #  "Calculate percentage change over 6-month period",
       # "Rank stocks based on their relative performance."
    #],
    #show_tool_calls= True,
    #markdown= True
#)



    

def get_company_info(symbol):
    try:
       stock= yf.Ticker(symbol)
       info= stock.info
       return {
        "name": info.get("longName","N/A"),
        "sector": info.get("sector","N/A"),
        "industry": info.get("industry","N/A"),
        "market_cap":info.get("marketCap",0),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh","N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow","N/A"),
        "current_price": info.get("currentPrice","N/A"),
        "summary": info.get("longBusinessSummary","N/A"),


    }
    except Exception as e:
        print(f"Error fetching info for {symbol}: {str(e)}")
        return{
            "name": symbol,
            "sector": "N/A",
            "industry":"N/A",
            "market_cap":0,
            "pe_ratio":"N/A",
            "dividend_yield":"N/A",
            "52_week_low":"N/A",
            "52_week_high":"N/A",
            "current_price":"N/A",
            "summary": "N/A",
        }

def get_company_news(symbol):
    try:
      stock=yf.Ticker(symbol)
      news= stock.news[:5] if hasattr(stock, 'news') and stock.news else[]
      return [{"title": article.get('title','N/A'),
              "publisher": article.get('publisher','N/A'),
              "link": article.get('link', '#')} for article in news]
    except Exception as e:
        print(f"Error fetching news for {symbol}: {str(e)}")
        return []
    
@st.cache_data(ttl=3600)

#company_researcher= Agent(
    #model=Gemini(id="models/gemini-2.5-flash"),
   # description="fetches company profiles, financials, and latest news.",
   # instructions=[
       # "Retrieve company information from yahoo finance",
       # "Summarize latest company news relevant to investors",
      #  "Provide sector, market cap, and business interview"
    #],
    #markdown= True
#)#

def get_final_investment_report(symbols_tuple):
    symbols=list(symbols_tuple)

    performance_data= compare_stocks(symbols)
    company_data={}

    for symbol in symbols:
        info= get_company_info(symbol)
        news=get_company_news(symbol)

        market_cap= info['market_cap']
        if isinstance(market_cap, (int, float)):
            if market_cap >=1e12:
                market_cap_str= f"${market_cap/1e12:.2f}T"
            elif market_cap>=1e9:
                market_cap_str= f"${market_cap/1e9:.2f}B"
            elif market_cap>=1e6:
                market_cap_str= f"${market_cap/1e6:.2f}M"
            else: 
                market_cap_str= f"${market_cap:,.0f}"
        else:
            market_cap_str= "N/A" 

        company_data[symbol]={
            "name":info['name'],
            "sector": info['sector'],
            "industry": info['industry'],
            "market_cap": market_cap_str,
            "pe_ratio": f"{info['pe_ratio']:.2f}" if isinstance(info['pe_ratio'],(int, float)) and info['pe_ratio']>0 else "N/A",
            "dividend_yield": f"${info['dividend_yield']*100:.2f}" if isinstance(info['dividend_yield'],(int, float)) and info['dividend_yield']>0 else "N/A",
            "current_price": f"${info['current_price']:.2f}" if isinstance(info['current_price'],(int, float))and info['current_price']>0 else "N/A",
            "52_week_range": f"${info['52_week_low']:.2f}-${info['52_week_high']:.2f}" if isinstance(info['52_week_low'],(int,float)) and isinstance(info['52_week_high'],(int,float)) and info["52_week_low"]>0 else "N/A",
            "summary": info['summary'][:600]+ "..." if len(info['summary'])>600 else info['summary'],
            "news_headlines": [n['title'] for n in news[:3]],
            "6_month_performance": f"{performance_data.get(symbol,0):.2f}%"
        }
        try:
            chat_completion= client.chat.completions.create(
                messages=[
                    {
                        "role":"system",
                        "content": "you're an expert inivestment analyst with deep knowledge of financial markets"
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze these stockes and create a comprhensive investment report:

        STOCK DATA:
        {company_data}
        Provide:

        1. Executive Summary
        2. Individual stock Analysis (fundamentals, metrics, news, strengths/risks)
        3. Competitive Analysis
        4. Investment Rankings (1st, 2nd, 3rd,....)
        5. Final Recommendations( BUY/ HOLD/AVOID with reasoning)

        Be specific and data-dirven."""

             
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=3000,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f" Error: {str(e)}\n\n Checek your Groq API Key."







# streamlit page config
st.set_page_config(page_title="AI Investment Strategist", layout="wide")

#Title and header
st.markdown("""
    <h1 style="text-align:center; color: #4CAF50,"> AI Investment Strategist</h1>
            <h3 style="text-align: center; color: #6c757d;"> Generate personalised investment reports with the latest market insights.</h3>
            """, unsafe_allow_html= True)

# sidebar styling
st.sidebar.markdown("""
    <h2 style="color: #343a40,"> Configuration</h2>
            <p style="color: #6c757d;"> Enter the stock symbols you want to analyze. The AI Will provide detailed insights, performance reports, and top recommendations </p>
            """, unsafe_allow_html= True)

#stock symbol input
input_symbols=st.sidebar.text_input("Enter stock symbols (Separated by commas)", "AAPL, TSLA, GOOG")


#Parse the stock symbols input
stocks_symbols=[symbol.strip().upper() for symbol in input_symbols.split(",") if symbol.strip()]
st.sidebar.info("Tip: Analyze 2-4 sstocks for best results..")

if os.getenv("GROQ_API_KEY"):
    st.sidebar.success("Groq API Key configured")
else:
    st.sidebar.error("Groq API key missing")

#Genereate investment report button
if st.sidebar.button("Generate Investment Report"):
    if not stocks_symbols:
        st.sidebar.warning("Please enter atleast one stock symbol")

    elif not os.getenv("GROQ_API_KEY"):
        st.sidebar.warning("Configure your Groq API key in .env file")

    else:
        with st.spinner(f"Analyzing {len(stocks_symbols)}stock(s)..."):
          try:
        #Generate the final report
             report= get_final_investment_report(tuple(stocks_symbols))

        #Display the report
             st.markdown("Investment Analysis report")
             st.markdown(report)

             st.info("This report provides detailed insights, including stock performance, company analyiss,a nd invetsment recommednations")

        #Interactive stock performance chart
             st.markdown("### Stock Performance (6-Month)")
             stock_data= yf.download(stocks_symbols, period="6mo")['Close']

             fig= go.Figure()
             if len(stocks_symbols)== 1:
               fig.add_trace(go.Scatter(x=stock_data.index, y= stock_data, mode='lines', name= stocks_symbols[0]))
             else:
               colors=['#4CAF50','#2196F3', '#FF9800', '#E91E63', '#9C27B0']
               for idx, symbol in enumerate(stocks_symbols):
                 normalized= (stock_data[symbol]/ stock_data[symbol].iloc[0]-1)*100
                 fig.add_trace(go.Scatter(x=stock_data.index, y= normalized, mode='lines', name=symbol, line=dict(color=colors[idx%len(colors)])))

                
            
             fig.update_layout(title= "Stock Performance over the last 6 months",
                          xaxis_title="Date",
                          yaxis_title="Price (in USD)" if len(stocks_symbols)== 1 else "% change",
                          template= "plotly_dark", height=500
                         )
             st.plotly_chart(fig, use_container_width= True)

          except Exception as e:
             st.error(f"Error: {str(e)}")
        
st.markdown("----")





