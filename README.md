# BBC_monitoring
Backtest of selected stocks. Portfolio monitoring

CODE DESCRIPTION:

    the main code is inside the backtest.py file, however it uses as inputs data from 
    other files.
    
    the run_bt file launch the code, therefore all the inputs are defined within that file.
    Subsequently, these inputs are recalled in backtes.py through the config.py so that the
    code is scalable.
    
    in bbc_function we can write some functions that we can use for our analysis, 
    at the moment I have the sample metrics, the maximum drawdrown, and I am working on the
    fama french exposures.
