import pandas as pd
import argparse
import json

parser = argparse.ArgumentParser() 
parser.add_argument('--config',help='Configuration file for for subselection of entries')
parser.add_argument('--o',help = 'Output to be written')

#Return a mapping between samples and dataframe columns
def build_col_mapping(samples,df_cols):
    col_mapping = {}
    for sample in samples:
        col_mapping[sample]=[]
        for col in df_cols:
            if sample in col:
                col_mapping[sample].append(col)
    return col_mapping

#Put all values of a dictionary into a list and return the list
def collapse_dict_vals(dict):
    vals = []
    for key in dict:
        vals = vals + dict[key]
    return vals
#BEWARE: Ensure the 0 indexing for sheetname and filename won't break anything in the future
def construct_df_list(file,entities,entity_labels,aggregate_col):
    print "Reading file",file['filename']
    #TODO: Need to auto ask for a delimiter
    df = pd.read_csv(file['filename'][0],delimiter = '\t')
    cols = entity_labels
    cols = cols + collapse_dict_vals(build_col_mapping(file['samples'],df.columns))
    df = df[cols]
    print "Read in df of length:",len(df),"with columns:",df.columns
    if len(entities)>0: #Only filter rows if there is something in entities to filter, otherwise just return everything
        df = subselect_df(entity_labels,entities,aggregate_col,df)
    df.set_index(aggregate_col,inplace=True)
    #TODO: Make this more robust so that an appropriate mapping can happen. Might require a change in the json
    if len(file['new_col_names'])>0:
        df.columns = file['new_col_names']
    print "Read in df of length:",len(df),"with columns:",df.columns
    return df

#Subselect the dataframe with specific rows that you want to keep
def subselect_df(entity_labels,entities,aggregate_col,df_full):
    df = pd.DataFrame(columns=df_full.columns)
    for entity_label in entity_labels:
        print "Looking at entity label:", entity_label
        for entity in entities:
            print "Filtering entity:",entity
            df_temp = df_full.loc[df_full[entity_label].str.contains(entity,na=False)]
            if len(df_temp)>0:
                #print "df_temp:"
                #print df_temp
                #if df_temp[aggregate_col].str not in df[aggregate_col].unique():
                    #print "Found",len(df_temp),"matching entries in entity:",entity_label
                df = df.append(df_temp,ignore_index=True)
    print "Filtered df and new size is:",len(df)
    return df

#Drop duplicate columns -- TODO: Can fix this to make not nested for loops and compare everything
def drop_col(entity_labels,df):
    for col in df.columns:
        for entity in entity_labels:
            bad_entity = entity + "_"
            if bad_entity in col:
                df.drop([col],axis=1,inplace=True)
    return df

#Construct the full dataframe 
def construct_df(data):
    entities = data['entities']
    entity_labels = data['entity_labels']
    df_list = map(lambda f: construct_df_list(f,entities,entity_labels,data["aggregate_col"]),data['files'])
    print "Total number of dataframes:",len(df_list)
    for i,df_temp in enumerate(df_list):
        if i==0:
            df = df_temp.copy()
            continue
        rs = "_"+str(i)
        #create the overall dataframe by going through the outer joins
        ind = set(df.index)
        df = df.join(df_temp,how='outer',rsuffix=rs)
        ind_new = set(df.index)-ind
        if len(ind_new)>0:
            for entity_label in entity_labels:
                df[entity_label].loc[ind_new]=df[entity_label+rs].loc[ind_new]
        #check to see if there
    #drop columns that are redundant for entities:
    df = drop_col(entity_labels, df)
    return df

def main(args):
    with open(args.config) as f:
            #TODO: json object being used right now is not great.
            configuration_object = json.load(f)
    data = configuration_object["data"]
    df = construct_df(data)
    df.to_csv(args.o)
    
if __name__ == '__main__':
  args = parser.parse_args()
  main(args)