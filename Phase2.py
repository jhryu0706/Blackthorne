from Phase1 import factor1, factor2, factor3, dict, _factorHnL
import numpy as np
import pandas as pd
#make factorHnL an external variable
f = _factorHnL()
fb = _factorHnL('B')
f1 = factor1()
f2 =factor2()
f3 = factor3()

def factorA_01(factor):
    return pd.DataFrame(np.where(factor>0,1,-1))

def factorB_01(factor, rocp):
    """
    factor: globar variable ex)f1
    rocp is rocp required for comparison
    """
    dict1={}
    for x in dict:
        dict1[x] = dict[x][rocp]
    #dict1 is rocp 21 for all commodities
    df = pd.DataFrame(dict1)
    df['omega']=factor[factor.columns[0]]
    df = df.truncate(after=len(factor))
    def temp(val, x):
        t = df['omega'][x]
        if np.isnan(val):
            return None
        if val >t:
            return 1
        elif val != t:
            return -1
        return None
    for x in range(len(df)):
        temp_row = df.loc[x].apply(temp,args=(x,))
        df.loc[x] =temp_row
    df.drop(columns=['omega'], inplace=True)
    return df

def factor1A():
    return factorA_01(f1)

def factor1B():
    """
    factor_name must be the global variable for the output of factor 
    from Phase 1
    """
    return factorB_01(f1,'rocp 21 day')

def factor2A():
    return factorA_01(f2)

def factor2B():
    """
    factor_name must be the global variable for the output of factor 
    from Phase 1
    """
    return factorB_01(f2,'rocp 252 day')

def factorA_0304():
    """
    similar to tfactorB row by row operation, _factorHnL[1] return a list of all
    high and low terms so use that
    define f which is output of _factorHnL() differently depending on whether A or B
    """
    dict2 ={}
    for x in dict.keys():
        dict2[x]=[]
    for comm in dict2.keys():
        for i in range(len(f[1]['H'])):
            if comm in f[1]['H'][i]:
                dict2[comm].append(1)
            else:
                dict2[comm].append(-1)

    return pd.DataFrame(dict2)

def factorB_0304():
    dict2 ={}
    for x in dict.keys():
        dict2[x]=[]
    for comm in dict2.keys():
        for i in range(len(fb[1]['H'])):
            if comm in fb[1]['H'][i]:
                dict2[comm].append(1)
            elif comm in fb[1]['L'][i]:
                dict2[comm].append(-1)
            else:
                dict2[comm].append(0)
    return pd.DataFrame(dict2)

def create_rocp1_dataframe():
    dict_rocp1 = {}
    for comm in dict.keys():
        dict_rocp1[comm] = dict[comm]['rocp 1 day']
    
    rocp1_df = pd.DataFrame(dict_rocp1)
    return rocp1_df
    

rocp1_dataframe = create_rocp1_dataframe()


def calculate_pnl(binary_factors, rocp_dict):
    pnl_dict = {}
    """
    Main function that calculates the PnL for each commodity
    """
    # Calculate the profit and loss for each commodity
    for commodity in binary_factors.columns:
        binary_factor = binary_factors[commodity].shift(-1)  # Shift the binary factor by one day
        rocp1_values = rocp_dict.get(commodity)  # Use get() method to prevent KeyError
        if rocp1_values is not None:
            pnl = binary_factor * rocp1_values * 1000000
            pnl_dict[commodity] = pnl
        
    pnl_df = pd.DataFrame(pnl_dict)
    pnl_df.dropna(inplace=True)  # Drop rows containing NaN values

    return pnl_df

def expand_factor(factor, rocp1_dict):
    """
    for factor 1A and 2A, want to repicate signals across all commodities
    """
    expanded_factor = pd.DataFrame()
    for commodity in rocp1_dict.keys():
        expanded_factor[commodity] = factor[factor.columns[0]]
    expanded_factor.index = factor.index  # Ensure the expanded factor has the same index as the original factor
    return expanded_factor


def calculate_pnl_expanded_factor(factor, rocp1_dataframe):

    expanded_factor = expand_factor(factor, rocp1_dataframe)
    return calculate_pnl(expanded_factor, rocp1_dataframe)



factor1A_pnl = calculate_pnl_expanded_factor(factor1A(), rocp1_dataframe)
factor1B_pnl = calculate_pnl(factor1B(), rocp1_dataframe)
factor2A_pnl = calculate_pnl_expanded_factor(factor2A(), rocp1_dataframe)
factor2B_pnl = calculate_pnl(factor2B(), rocp1_dataframe)
factorA_0304_pnl = calculate_pnl(factorA_0304(), rocp1_dataframe)
factorB_0304_pnl = calculate_pnl(factorB_0304(), rocp1_dataframe)


def portfolio_pnl(factor_names, *pnl_dataframes):
    individual_pnls = {}
    
    for i, pnl_df in enumerate(pnl_dataframes):
        daily_pnl = pnl_df.sum(axis=1)
        cumulative_pnl = daily_pnl.cumsum()

        individual_pnls[factor_names[i]] = pd.DataFrame({
            'Daily PnL': daily_pnl,
            'Cumulative PnL': cumulative_pnl
        })

    return individual_pnls

factor_names = ["Factor 1A", "Factor 1B", "Factor 2A", "Factor 2B", "Factor A_0304", "Factor B_0304"]
individual_pnls = portfolio_pnl(factor_names, factor1A_pnl, factor1B_pnl, factor2A_pnl, factor2B_pnl, factorA_0304_pnl, factorB_0304_pnl)


factor1A_pnl_df = individual_pnls['Factor 1A']
factor1B_pnl_df = individual_pnls['Factor 1B']
factor2A_pnl_df = individual_pnls['Factor 2A']
factor2B_pnl_df = individual_pnls['Factor 2B']
factor34A_pnl_df = individual_pnls['Factor A_0304']
factor34B_pnl_df = individual_pnls['Factor B_0304']
rvpnl=[factor1A_pnl_df, factor1B_pnl_df, factor2A_pnl_df, factor2B_pnl_df, factor34A_pnl_df, factor34B_pnl_df]

def pnl_to_xl():
    names = ['Factor 1A','Factor 1B','Factor 2A','Factor 2B','Factor34A','Factor34B']
    writer=pd.ExcelWriter('pnl.xlsx')
    for i, A in enumerate(rvpnl):
        A.to_excel(writer,sheet_name="{0}".format(names[i]))
    writer.save()
