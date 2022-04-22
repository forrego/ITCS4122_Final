def countywise_cases_deaths(df_fin,selected_state):
    df_temp1=df_fin[df_fin['state']==selected_state]
    df_temp2=df_temp1.groupby('county').sum()[['cases','deaths']].reset_index()
    return df_temp2





def covidcases_state_countywise(df_fin,selected_state,selected_county):
    df_temp1=df_fin[df_fin['state']==selected_state]
    df_temp2=df_temp1[df_temp1['county']==selected_county]
    df_temp3=df_temp2.groupby('month').sum()[['cases','deaths']].reset_index()
    return df_temp3


def get_cases_total(df_fin,selected_state):
    df_temp1=df_fin[df_fin['state'].isin(selected_state)]
    df_temp2=df_temp1.groupby(['state','month']).sum()[['cases','deaths']].reset_index()
    return df_temp2


def get_countycases_comparsion(df_fin,selected_state,selected_county):
    df_temp1=df_fin[df_fin['state']==selected_state]
    df_temp2=df_temp1[df_temp1['county'].isin(selected_county)]
    df_temp3=df_temp2.groupby(['county','month']).sum()[['cases','deaths']].reset_index()
    return df_temp3



        

