# How to use
## [adding new commodity data]

    Depending on the file type (csv or xlsx, our group used both
    you will need to go through cleanfilename.py and make necessary
    adjustments such that the data can be processed using Phase1.py
    and Phase2.py.
    Simply put, Phase_x_.py will create a dictionary to store data
    from each file with [key]: [value] being [commodity name]:[data
    from file] and access data in this manner for all operations.

## [seeing results for In-House Data or Phase1]

    First open terminal and enter Python environment. 
    Then run the following commands and choose function 
    depending on the output you are looking for:
        
        from Phase1 import __function name goes here__
    
    1. separate factors:
        factor1 -> run factor1():
        factor2 -> run factor2():
        factor3 -> run factor3():
        factor4 -> run factor4():

    2. to see all results converted to excel:
        run get_all_signal() from Phase1 or
        get_all_pnl() from Phase2

**[seeing results for PnL]**



 # Errors/Notes
## [still needs troubleshooting for cumulative pnl]
## [files with errors]

    GF starts 2001
    KC, CL, SB has repeated data (Phase I)

## [calculating basis]
    SI updated: --> 0
        430	#NAME?
        928	#NAME?
        1177#NAME?
    HG updated:
        924	#NAME?
        1175 #NAME?

## [dates]
    Length of arrays fit to GF (shortest dataset)--> 
    most dates do not match up
