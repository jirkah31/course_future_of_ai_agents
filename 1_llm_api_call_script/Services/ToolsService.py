import yfinance


class ToolsService:
    def __init__(self):
        self.__tools_list = [
            {
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "description": "Use this function to get the current price of a stock.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "The ticker symbol for the stock, e.g. GOOG",
                            }
                        },
                        "required": ["ticker"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_dividend_date",
                    "description": "Use this function to get the next dividend payment date of a stock.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "The ticker symbol for the stock, e.g. GOOG",
                            }
                        },
                        "required": ["ticker"],
                    },
                },
            },
        ]

        self.__tool_functions = {
            "get_stock_price": self.__get_stock_price,
            "get_dividend_date": self.__get_dividend_date,
        }

    def get_tools_list(self):
        return self.__tools_list

    def get_tool(self, tool_name: str):
        return self.__tool_functions.get(tool_name)

    def __get_stock_price(self,ticker: str):
        ticker_info = yfinance.Ticker(ticker).info
        current_price = ticker_info.get("currentPrice")
        return {"ticker": ticker, "current_price": current_price}

    def __get_dividend_date(self, ticker: str):
        ticker_info = yfinance.Ticker(ticker).info
        dividend_date = ticker_info.get("dividendDate")
        return {"ticker": ticker, "dividend_date": dividend_date}
