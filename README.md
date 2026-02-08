# AI Investment Strategist

## Overview
An AI-powered investment analysis tool that generates comprehensive stock market reports using real-time data and AI-driven insights. The application analyzes multiple stocks, compares their performance, and provides data-driven investment recommendations.

## Features
- **Real-time Stock Analysis**: Fetches live stock data from Yahoo Finance
- **6-Month Performance Tracking**: Analyzes stock performance over the past 6 months
- **AI-Powered Insights**: Uses Groq's Llama 3.3 70B model to generate detailed investment reports
- **Company Research**: Retrieves company fundamentals, market cap, P/E ratio, dividend yield, and latest news
- **Interactive Visualizations**: Plotly-based charts showing stock performance comparisons
- **Investment Rankings**: AI ranks stocks and provides BUY/HOLD/AVOID recommendations

## Technologies Used
- **Python**
- **Streamlit** - Web interface
- **yfinance** - Stock data retrieval
- **Groq API** - AI analysis (Llama 3.3 70B)
- **Plotly** - Interactive charts
- **python-dotenv** - Environment variable management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Investment-Strategist.git
cd AI-Investment-Strategist
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run investment.py
```

2. Enter stock symbols (e.g., AAPL, TSLA, GOOG) separated by commas

3. Click "Generate Investment Report"

4. View the comprehensive analysis including:
   - Executive Summary
   - Individual Stock Analysis
   - Competitive Analysis
   - Investment Rankings
   - Final Recommendations

## Project Structure
```
AI-Investment-Strategist/
├── investment.py          # Main application file
├── .env                   # API keys (not uploaded)
├── .gitignore            # Git ignore file
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Features in Detail

### Stock Analysis
- Current price and 52-week range
- Market capitalization
- P/E ratio and dividend yield
- Sector and industry information
- Latest news headlines

### AI Report Generation
The AI analyzes stocks and provides:
1. Executive Summary
2. Individual Stock Analysis (fundamentals, metrics, strengths/risks)
3. Competitive Analysis
4. Investment Rankings
5. Final Recommendations with reasoning

### Interactive Charts
- 6-month price performance comparison
- Normalized percentage change visualization
- Color-coded for easy comparison

## Requirements

Create a `requirements.txt` file with:
```
streamlit
yfinance
groq
python-dotenv
plotly
```

## API Key Setup

Get your free Groq API key from: [https://console.groq.com](https://console.groq.com)

## Screenshots

<img width="2858" height="1486" alt="Screenshot 2026-02-08 AI1" src="https://github.com/user-attachments/assets/2eb6865a-369a-4f27-937b-66822b65bf14" />
<img width="2756" height="1470" alt="Screenshot 2026-02-08 AI2" src="https://github.com/user-attachments/assets/9ad74673-fd64-4cf2-af40-be447c7cc695" />


<img width="2764" height="1542" alt="Screenshot 2026-02-08 AI3" src="https://github.com/user-attachments/assets/a3acc5c6-d1c4-4b11-898d-dd509aae045b" />

<img width="2862" height="1328" alt="Screenshot 2026-02-08 AI4" src="https://github.com/user-attachments/assets/f4ce52e9-5db4-498e-acd7-d95064507a5d" />






## Notes
- Best results with 2-4 stocks for comparison
- Data is cached for 1 hour to improve performance
- Requires active internet connection for real-time data

## Future Enhancements
- Add more financial metrics
- Export reports to PDF
- Portfolio tracking features
- Historical performance backtesting



## Author
Nikita Gupta


---

**Also create a `requirements.txt` file:**
```
streamlit
yfinance
groq
python-dotenv
plotly
```

**And update your `.gitignore`:**
```
.env
__pycache__/
*.pyc
*.log
.DS_Store
