indicators.py implements indicators as functions that operate on dataframes. The "main" code in indicators.py generate the charts that illustrate indicators in the report. 
It can be run using: python indicators.py from terminals

marketsimcode.py is an improved version of your marketsim code that accepts a "trades" data frame (instead of a file). 
This file does not contain main routine and can not be executed directly.

ManualStrategy.py Code implements a ManualStrategy object . It implement testPolicy() which returns a trades data frame. The main part of this code call marketsimcode as necessary to generate the plots used in the report.
It can be run using: python ManualStrategy.py  from terminals

TheoreticallyOptimalStrategy.py Code implements a TheoreticallyOptimalStrategy object. It should implement testPolicy() which returns a trades data frame. The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
It can be run using: python TheoreticallyOptimalStrategy.py from terminals
