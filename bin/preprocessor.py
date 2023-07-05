#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 21:42:10 2023

@author: alejandracamelocruz
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np


class Preprocessor:
    
    def __init__(self, data_folder='data/'):
        self.data_folder = data_folder
        self.files = self.file_list(data_folder)


    def index_cleaning(self,index_list:list) -> list:
        """
        This function takes the index list of any DataFrame, cleans it and returns it 
        to the calling function to replace the previous data index with the cleaned data index. 
        """
        outlist = []
        for country in index_list:
            if country[0:5] == "China":
                outlist.append(country.split(": ")[-1].replace(" ","_"))
            else:
                outlist.append(country.split(",")[0].replace(" ","_"))
        return outlist

    def data_cleaning(self,file_location:str) -> pd.DataFrame:
        """
        This function reads any particular data set provided and 
        cleans the column headers and indexes and returns the DataFrame.
        """
        data = pd.read_excel(file_location)
        data.index = data["Unnamed: 0"]
        data = data.drop(columns=["Unnamed: 0"])
        data.columns = [c.strip().replace(" ","_") for c in data.columns.values.tolist()]
        data.index = self.index_cleaning(data.index.tolist())
        
        return data
    
    def list_countries(self,intext=""):
        data = self.data_cleaning(self.files[0])
        list_countries = data.index.to_list()
        intext = input("Enter a part of the countries you want. "
                       "Don't write anything or write \"all\" if you want to see "
                       "a list with all available countries: ")
        intext = intext.capitalize()
        all_countries = (intext == "" or intext == 'All')
        if all_countries:
            return list_countries
        else:
            if intext.endswith("*"):
                list_countries_specific = []
                for country in list_countries:
                    if country.startswith(intext[:-1]):
                        list_countries_specific.append(country)
                
                return list_countries_specific
            else:
                list_countries_specific = []
                for country in list_countries:
                    if intext in country:
                        list_countries_specific.append(country)
                return list_countries_specific
    
    def by_country(self,product:str,country_list:list) -> pd.DataFrame:
        """
        Returns data with only selected countries.
        """
        
        print(f"You have chosen the following countries : {country_list}")
        self.country_list = country_list
        self.product = product
        data = self.by_product(product)
        data_countries = data.loc[country_list]
    
        return data_countries
    
    def list_years():
        pass
    
    def by_year(self,product:str,country_list:list,start,stop):
        data = self.by_country(product,country_list)
        wanted_columns = data.columns.values[np.where(data.columns.values == start)[0][0]:np.where(data.columns.values == stop)[0][0]]
        data_years = data[wanted_columns]
        print(f"You have chosen the time data from {wanted_columns[0]} to {wanted_columns[-1]}")
        # print(np.where(data.columns.values == start)[0][0])
        # print(np.where(data.columns.values == stop)[0][0])
    
    def list_products(self) -> list:
        list_products = []
        for file in self.files:
            list_products.append(file.split("_CPI_")[-1].split(".")[0])
        return list_products
    
    
    def by_product(self, product):
        self.product = product
        print(f"You have chosen {self.product}")
        self.data_file = "../data/Consumer_Price_Index_CPI_"+product+".xlsx"
        data = self.data_cleaning(self.data_file)
    
        return data

    def display_head(self, data: pd.DataFrame) -> None:
        print(data.head())

    @staticmethod
    def file_list(directory):
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'data'))
        file_list = [os.path.join(data_dir, file) 
                     for file in os.listdir(data_dir)]
        
        return file_list
        
def main(args):
    # print(args)
    prpr = Preprocessor()
    parser = argparse.ArgumentParser(description='Command line inputs')
    parser.add_argument('--product', type=str, help='Product name')
    parser.add_argument('--countries', nargs='+', help='List of countries')
    parser.add_argument('--time', type=str, nargs=2, help='Start, Stop')

    args = parser.parse_args()

    if not args.product or args.product is None:
        print("Missing arguement : --products is required")
        print(prpr.list_products())
    else:
        if not args.countries or args.countries is None:
            prpr.by_product(args.product)
            print("Missing arguement : --countries is required")
            print(prpr.list_countries())
        else:
            
            if not args.time:
                prpr.by_country(args.product,args.countries)
                print("Missing arguement : --time is required")
            else:
                start,stop = args.time
                data = prpr.by_year(args.product,args.countries,start,stop)
                prpr.display_head(data)


    product = args.product
    countries = args.countries
    start_year, stop_year = args.time

    print('Product:', product)
    print('Countries:', countries)
    print('Start year:', start_year)
    print('Stop year:', stop_year)

if __name__ == "__main__":
    main(sys.argv)