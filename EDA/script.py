def eda_script(data_path):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import skew
    import os
    import time
    
    # load data and some basic info
    try:
        df = pd.read_csv(data_path)   
    except Exception :
        try : 
            df = pd.read_excel(data_path) 
        except Exception : 
            try :
                df = pd.read_json(data_path)
            except Exception :
                try :
                    df = pd.read_xml(data_path)
                except Exception :
                    print('wrong data path check the path and that your data has these extension :\n\
                1- csv\
                2- excel\
                3- json\
                4- xml')
                    
    else :
        print('DataFrame : ')
        display(df.head())

        print('=============================================================================')
        print('data info : ')
        print(df.info())
        
        print('=============================================================================')
        print('data describtion : ')
        display(df.describe().T)
        
        print('=============================================================================')
        nan_percentage_dict = dict()
        print('NaN percentage for each column : ')
        name = []
        percentage = []
        for i in df.columns:
            name.append(i)
            s = (str((df[i].isnull().sum()/df.shape[0]*100).round(2))+'%')
            percentage.append(s)
        nan_percentage_dict['name'] = name
        nan_percentage_dict['percentage'] = percentage
        nan_percentage_df = pd.DataFrame(nan_percentage_dict)
        display(nan_percentage_df)
    
    # seperate numerical and categorical columns
    numerical_col = []
    cat_col = []
    cols = df.columns
    for i in range(len(cols)):
        if df[cols[i]].dtype == np.int64 or df[cols[i]].dtype == np.int32 or df[cols[i]].dtype == np.float64 or df[cols[i]].dtype == np.float32 :
            numerical_col.append(cols[i])
        else :
            cat_col.append(cols[i])
    
    # check NaN
    numerical_col_nan = [] 
    cat_col_nan = []       
    for i in numerical_col:
        if(df[i].isnull().sum()>0 ):
            numerical_col_nan.append(i)
    for i in cat_col:
        if(df[i].isnull().sum() >0):
            cat_col_nan.append(i)
                             
    
    # fill NaN
    if(len(numerical_col_nan)>0 ): #there was nan
        print('imputing numerical NaNs now : ')
        for i in numerical_col_nan:
            median = df[i].describe()['50%'].round(2)
            df[i].fillna(median , inplace= True)
    elif (len(cat_col_nan) > 0):
        print('imputing categotical NaNs now : ')
        for i in cat_col_nan :
            mode = df[i].describe()['freq']
            df[i].fillna(mode , inplace= True) 
    else :
        print('there is no NaNs in data to impute')
        
    # check skew for numerical after imputing
    print('=============================================================================') 
    print('check skewness for numerical after imputing : ')
    name = []
    skew_value_list = []
    skew_type_list = list()
    skew_dict = dict()
    for i in numerical_col :
        name.append(i)
        skew_value = skew(df[i])
        skew_value  = float("{:.2f}".format(skew_value))
        skew_value_list.append(skew_value)
        skew_type = ''
        if(skew_value ==0):
            skew_type  = 'no_skew'
        elif(skew_value > 0):
            skew_type = 'positive'
        else :
            skew_type = 'negative'
        skew_type_list = skew_type

    skew_dict['col_name'] = name
    skew_dict['skew_value'] = skew_value_list
    skew_dict['skew_type'] = skew_type_list
    skew_df = pd.DataFrame(skew_dict)
    display(skew_df)
    
    # count values for data
    print('=============================================================================') 
    print('count values for categorical columns : ')
    value_count_dict = dict()
    for i in cat_col:
        print(i,'column\'s count values : ' )
        index , count = df[i].value_counts().index , df[i].value_counts().values
        value_count_dict['value']  = list(index)
        value_count_dict['count'] = list(count)
        value_count_df = pd.DataFrame(value_count_dict)
        if value_count_df.shape[0]>10:
            display(value_count_df.head(10))
        else :
            display(value_count_df.head())
    
    
    print('some plots : ')      
    # some plts 
    if (len(cat_col) <= 4 ) :#on one line  # to adjust figure size
        plt.figure(figsize = (30,5))
    else:
        plt.figure(figsize = (30,15))
    rows = len(cat_col)//4
    cat_col_bar = []
    for i in cat_col :
        if len(df[i].unique())<=10:
            cat_col_bar.append(i)        
    for index , i in enumerate(cat_col_bar):
        ax = plt.subplot( rows+1 , 4, index+1)
        (df[i].value_counts()).plot.bar()
        ax.set_ylabel(i)
        ax.set_ylabel("count")
            #plt.show()
    
    
    plt.figure(figsize = (30,15))
    rows = len(cat_col)//4
    cat_col_pie = []
    for i in (cat_col) :
        if len(df[i].unique())<=5: # we want to draw pie for columns with min unique values = 5
            cat_col_pie.append(i)
    
    for index , i in enumerate(cat_col_pie):
        ax = plt.subplot( rows+1 , 4, index+1)
        (df[i].value_counts()).plot.pie(autopct='%.2f%%',labels=df[i].index,startangle=90,counterclock=False)
        plt.title(i)
        #plt.show() 

    
    if (len(numerical_col) <= 4 ) :#on one line
        plt.figure(figsize = (30,5))
    else:
        plt.figure(figsize = (30,15))           
    rows = len(numerical_col)//4
    for index , i in enumerate(numerical_col):
        ax = plt.subplot( rows+1 , 4, index+1)
        df[i].hist(bins = 15)
        ax.set_xlabel(i)
        ax.set_ylabel('frequency')
    
    
    #bivarite plots :
    # i will draw 16 random plots
    if len(numerical_col) > 4:
        plt.figure(figsize=(30,15)) 
        plt.tight_layout(pad = 15)
        for iterate in range(1,17):
            ax = plt.subplot( 4 , 4, iterate )
            i = np.random.randint(len(numerical_col))
            j = np.random.randint(len(numerical_col))
            sns.scatterplot(data=df, x=numerical_col[i], y=numerical_col[j],ax = ax)
            ax.set_xlabel(numerical_col[i])
            ax.set_ylabel(numerical_col[j])  
    else :
        index = 1
        plt.figure(figsize = (30,5))
        plt.tight_layout(pad = 5)
        rows = (np.math.factorial(len(numerical_col)-1))//4
        for i in range(len(numerical_col)-1):
            for j in range(i+1 ,len(numerical_col)):
                #print(i , j , (i+1)*j)
                ax = plt.subplot( rows+1 , 4, index )
                index+=1

                sns.scatterplot(data=df, x=numerical_col[i], y=numerical_col[j],ax = ax)
                ax.set_xlabel(numerical_col[i])
                ax.set_ylabel(numerical_col[j])
                
                
                
    # boxplots :             

    total = len(numerical_col) * len(cat_col)
    index = 1
    if (total > 4 ):
        plt.figure(figsize=(40,30)) 
        plt.tight_layout(pad = 15)
    else : 
        plt.figure(figsize=(30,5)) 
        plt.tight_layout(pad = 5)
    for i in range(len(cat_col)):
        for j in range(len(numerical_col)):  
            #ax = plt.subplot( (total//4)+1 , 4, (i+1)*(j+1) )
            ax = plt.subplot( (total//4)+1 , 4, index )
            sns.boxplot(x=cat_col[i], y=numerical_col[j],data = df)
            ax.set_xlabel(cat_col[i])
            ax.set_ylabel(numerical_col[j]) 
            index+=1 
    
    
    # heatmap
    plt.figure(figsize=(12, 6))
    # define the mask to set the values in the upper triangle to True
    mask = np.triu(np.ones_like(df.corr(), dtype=np.bool))
    heatmap = sns.heatmap(df.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Triangle Correlation Heatmap', fontdict={'fontsize':18}, pad=16);
        
    
    # rows = (np.math.factorial(len(numerical_col)-1))//4
    # _,axs = plt.subplots(rows+1 , 4,figsize = (16,17))
    # axs = axs.ravel()
    # plt.tight_layout(pad = 15)
    # index = (rows+1) * 4
    # for i in range(len(numerical_col)-1):
    #     for j in range(i+1 ,len(numerical_col)):
    #         sns.scatterplot(data=df, x=numerical_col[i], y=numerical_col[j],ax = axs[(i+1)*j])
    
        
            
    
    return df
    #plt.show
            
        
    