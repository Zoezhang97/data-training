import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math

def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)
        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
                Data Type: Dataframe
                Please read the assignment specs to know how to create the output dataframe
        """
    #################################################
    df2 = pd.read_csv(exposure, sep=';', encoding='latin-1', low_memory=False)
    df3 = pd.read_csv(countries)
    # Drop all rows from the "exposure" dataset without country name
    df2['country'] = df2['country'].fillna('null')
    df2 = df2[~df2['country'].isin(['null'])]
    df2['country'] = df2['country'].replace(
        ["Cabo Verde", "Palestine", "United States of America", "Congo DR", "Korea Republic of", "Lao PDR", "Congo",
         "Brunei Darussalam", "Viet Nam",
         "Eswatini", "North Macedonia", "Moldova Republic of", "Russian Federation", "Korea", "Côte d'Ivoire",
         "Korea DPR"],
        ["Cape Verde", "Palestinian Territory", "United States", "Democratic Republic of the Congo", "North Korea",
         "Laos", "Republic of the Congo", "Brunei", "Vietnam",
         "Swaziland", "Macedonia", "Moldova", "Russia", "South Korea", "Ivory Coast", "North Korea"])
    df1 = pd.merge(left=df2, right=df3, left_on='country', right_on='Country')
    to_drop = ['country']
    df1 = df1.drop(to_drop, axis=1)
    df1.set_index('Country', inplace=True)
    df1 = df1.sort_index()
    #################################################
    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1

df1=question_1("exposure.csv", "Countries.csv")





def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    def avg_lat(df):
        list = []
        list = df.split("|||")
        length = len(list)
        sum_lat = 0
        for i in range(length):
            j = list[i]
            f = json.loads(j)
            latitude = f['Latitude']
            sum_lat = sum_lat + latitude
        avg_lat = float(sum_lat / length)
        return avg_lat
    def avg_lon(df):
        list = []
        list = df.split("|||")
        length = len(list)
        sum_lon = 0
        for i in range(length):
            j = list[i]
            f = json.loads(j)
            longitude = f['Longitude']
            sum_lon = sum_lon + longitude
        avg_lon = float(sum_lon / length)
        return avg_lon
    df1["avg_latitude"]= df1["Cities"].apply(avg_lat)
    df1[ "avg_longitude"] = df1["Cities"].apply(avg_lon)
    df2=df1
    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2
df2 = question_2(df1)





def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    def distance(x):
        # lat,lon,wuhan_lat,wuhan_long = map(math.radians(),lat,lon,30.5928,114.3055)
        lat = math.radians(x.avg_latitude)
        lon = math.radians(x.avg_longitude)
        wuhan_lat = math.radians(30.5928)
        wuhan_long = math.radians(114.3055)
        delt_lat = lat - wuhan_lat
        delt_lon = lon - wuhan_long
        a = 2 * math.asin(math.sqrt(
            math.pow(math.sin(delt_lat / 2), 2) + math.cos(lat) * math.cos(wuhan_lat) * math.pow(math.sin(delt_lon / 2),
                                                                                                 2)))
        r = 6373
        d = a * r
        return d
    df3 =df2
    df3["distance_to_Wuhan"] = df3.apply(distance,axis =1)

    df3.sort_values("distance_to_Wuhan",inplace=True)
    #df3["distance_to_Wuhan"] = df2[["avg_latitude","avg_longitude"]].apply(distance)
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3
#df = question_3(df2)

def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    df = pd.read_csv(continents)
    df2["Covid_19_Economic_exposure_index"]=df2["Covid_19_Economic_exposure_index"].apply(lambda x:x.replace(',','.'))
    df2 = df2[~df2["Covid_19_Economic_exposure_index"].isin(["x"])]

    df4 = pd.merge(left=df,right=df2["Covid_19_Economic_exposure_index"],left_on="Country",right_on="Country")
    df4.set_index('Continent', inplace=True)

    to_drop = ['Country']
    df4 = df4.drop(to_drop, axis=1)
    df4["Covid_19_Economic_exposure_index"] = df4["Covid_19_Economic_exposure_index"].astype('float')
    group=df4.groupby("Continent").mean()
    df4["average_covid_19_Economic_exposure_index"]=group
    df4 = df4.drop("Covid_19_Economic_exposure_index", axis=1)
    df4=df4.drop_duplicates()
    df4=df4.sort_values("average_covid_19_Economic_exposure_index",ascending=True)
    #################################################

    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    #df = df2[["Income classification according to WB","Foreign direct investment","Net_ODA_received_perc_of_GNI"]]
    df=pd.DataFrame(df2,columns=["Income classification according to WB","Foreign direct investment","Net_ODA_received_perc_of_GNI"])
    df["Net_ODA_received_perc_of_GNI"]= df["Net_ODA_received_perc_of_GNI"].apply(lambda x:x.replace(',','.'))
    df["Foreign direct investment"] = df["Foreign direct investment"].apply(lambda x:x.replace(',','.'))
    df = df.replace("No data",np.NAN)#[~df["Net_ODA_received_perc_of_GNI"].isin(["No data"])]
    df =df.replace("x",np.NAN)#[~df["Foreign direct investment"].isin(["x"])]
    df=df.rename(columns={"Income classification according to WB":"Income Class"})
    df["Net_ODA_received_perc_of_GNI"] = df["Net_ODA_received_perc_of_GNI"].astype("float")
    df["Foreign direct investment"] = df["Foreign direct investment"].astype("float")
    df5= df.groupby("Income Class").mean()
    df5.columns =["Avg Foreign direct investment","Avg_ Net_ODA_received_perc_of_GNI"]
    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5

#df5 = question_5(df2)

def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    df = df2[df2["Income classification according to WB"]=="LIC"]
    df6 = pd.DataFrame(df,columns=["Cities"])
    df6["Cities"] = df6["Cities"].apply(lambda x:x.split("|||"))
    df6 = df6.explode("Cities")
    df6["Cities"]= df6["Cities"].apply(lambda x:json.loads(x))
    df1 = df6["Cities"].apply(pd.Series)
    df1=df1.dropna()
    df1=df1[["City","Population"]]
    df1=df1.sort_values("Population",ascending=False)
    cities_lst=df1["City"].to_list()
    cities_lst=cities_lst[0:5]
    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return cities_lst

#df= question_6(df2)

def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    def newcity(string):
        l = string.split("|||")
        new_city = []
        for i in range(len(l)):
            j = l[i]
            f = json.loads(j)
            new_city.append(f["City"])
        return new_city
    df = pd.DataFrame(df2, columns=["Cities"])
    df["Country"] = df2.index
    df["Cities"] = df["Cities"].apply(newcity)
    df = pd.DataFrame({"Country": df.Country.repeat(df.Cities.str.len()), 'Cities': np.concatenate(df.Cities.values)})
    df = df.drop_duplicates( keep='first')
    df = df[df["Cities"].duplicated(keep=False)]

    df7 = df.groupby("Cities").apply(lambda x: [','.join(x['Country'])]).reset_index()

    df7=df7.rename(columns = {"Cities":"city",0:"countries"})
    df7.set_index("city", inplace=True)
    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7
df7 = question_7(df2)
#print(df7.head(70),df7.shape)

def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    def newcity(string):
        l = string.split("|||")
        sum = 0
        for i in range(len(l)):
            j = l[i]
            f = json.loads(j)
            if f["Population"]!=None:
                sum = sum + f["Population"]
        return sum
    df = pd.read_csv(continents)
    df1 = pd.DataFrame(df2,columns=["Country","Cities"])
    df1["Cities"] = df1["Cities"].apply(newcity)

    df4 = pd.merge(left=df, right=df1["Cities"], left_on="Country", right_on="Country")
    total_p = df4["Cities"].sum()
    df5 =df4[df4["Continent"]=="South America"]
    df5["Percentage"]= df5["Cities"].apply(lambda x: x*100/total_p)
    df5=df5.set_index("Country")
    df5 = df5.drop(columns=["Cities","Continent"])
    df5.plot.bar(rot=20,figsize =(30,20))
    plt.title("percentage of the world population is living in each South American country",fontsize=40)
    plt.xlabel("Country",fontsize=40)
    plt.ylabel("population percentage",fontsize=40)
    plt.xticks(fontsize = 30)
    plt.legend(fontsize=40)
    plt.yticks(fontsize=30)
    #################################################

    plt.savefig("{}-Q11.png".format('z5243683'))


#question_8(df2,"Countries-Continents.csv")

def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    df = pd.DataFrame(df2, columns=["Income classification according to WB", "Covid_19_Economic_exposure_index_Ex_aid_and_FDI",
                                    "Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import","Foreign direct investment",
                                    "Foreign direct investment, net inflows percent of GDP"])

    df["Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import"] = df["Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import"].apply(lambda x: x.replace(',', '.'))
    df["Covid_19_Economic_exposure_index_Ex_aid_and_FDI"] = df["Covid_19_Economic_exposure_index_Ex_aid_and_FDI"].apply(
        lambda x: x.replace(',', '.'))
    df["Foreign direct investment, net inflows percent of GDP"] = df["Foreign direct investment, net inflows percent of GDP"].apply(lambda x: x.replace(',', '.'))
    df["Foreign direct investment"] = df["Foreign direct investment"].apply(lambda x: x.replace(',', '.'))

    df = df.replace("x", np.NAN)
    df[[ "Covid_19_Economic_exposure_index_Ex_aid_and_FDI",
              "Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import","Foreign direct investment",
                                    "Foreign direct investment, net inflows percent of GDP"]] = df[[ "Covid_19_Economic_exposure_index_Ex_aid_and_FDI",
                                    "Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import","Foreign direct investment",
                                    "Foreign direct investment, net inflows percent of GDP"]].astype("float")
    df9 = df.groupby("Income classification according to WB").mean()
    df9 = df9.T
    df9.plot.bar(figsize =(50,20))
    plt.title("Economic comparison of the high, middle, and low income level countries",fontsize=50)
    plt.xlabel("four categories",fontsize=40)
    plt.ylabel("value",fontsize=50)
    plt.legend(fontsize=40)
    plt.xticks(fontsize=30,rotation=4)
    plt.yticks(fontsize=40)


    #################################################

    plt.savefig("{}-Q12.png".format('z5243683'))

#df9 = question_9(df2)

def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################
    def newcity(string):
        l = string.split("|||")
        sum = 0
        for i in range(len(l)):
            j = l[i]
            f = json.loads(j)
            if f["Population"]!=None:
                sum = sum + f["Population"]
        return sum
    df = pd.read_csv(continents)
    df1 = pd.DataFrame(df2, columns=[ "avg_latitude", "avg_longitude","Cities"])
    df1["Cities"] = df1["Cities"].apply(newcity)
    #df4 = pd.merge(left=df1, right=df, left_on=df.index.all(), right_on="Country")
    df4 = pd.merge(left=df, right=df1, left_on="Country", right_on="Country")
    plt.figure(figsize=(25, 15))
    df01 = df4[df4["Continent"]=="Africa"]
    y = df01["avg_latitude"]
    x = df01["avg_longitude"]
    value = df01["Cities"]
    p1=plt.scatter(x,y,c ='r',s=value/50000,alpha = 0.5)
    df02 = df4[df4["Continent"] == "Asia"]
    y = df02["avg_latitude"]
    x = df02["avg_longitude"]
    value = df02["Cities"]
    p2=plt.scatter(x,y,c ='b',s=value/50000,alpha = 0.5)
    df03 = df4[df4["Continent"] == "Europe"]
    y = df03["avg_latitude"]
    x = df03["avg_longitude"]
    value = df03["Cities"]
    p3=plt.scatter(x, y, c='g', s=value / 50000, alpha=0.5)
    plt.legend([p1, p2, p3], ["Africa", "Asia", "Europe"], loc='upper right')
    df04 = df4[df4["Continent"] == "North America"]
    y = df04["avg_latitude"]
    x = df04["avg_longitude"]
    value = df04["Cities"]
    p4=plt.scatter(x, y, c='orange', s=value / 50000, alpha=0.5)
    df05 = df4[df4["Continent"] == "Oceania"]
    y = df05["avg_latitude"]
    x = df05["avg_longitude"]
    value = df05["Cities"]
    p5=plt.scatter(x, y, c='grey', s=value / 50000, alpha=0.5)
    df06 = df4[df4["Continent"] == "South America"]
    y = df06["avg_latitude"]
    x = df06["avg_longitude"]
    value = df06["Cities"]
    p6=plt.scatter(x, y, c='purple', s=value / 50000, alpha=0.5)

    plt.legend([p1, p2, p3,p4,p5,p6],["Africa", "Asia", "Europe","North America","Oceania","South America"],loc='best',markerscale=0.7,fontsize=20)
    plt.xlabel("Countries' avg_longitude",fontsize=20)
    plt.ylabel("Countries' avg_longitude",fontsize=20)
    plt.title("Country coordinate distribution",fontsize=20)

    #################################################

    plt.savefig("{}-Q13.png".format('data'))
    #return df4

#question_10(df2,"Countries-Continents.csv")
#print(df4.head())