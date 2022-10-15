# Import Libraries
import pandas as pd 
import numpy as np 
import os  
import warnings
import plotly.express as px
from tqdm import tqdm 
from typing import List, Dict 
from dash import Dash, html, dcc

warnings.filterwarnings("ignore")

class Dash_Demo:
    """This class used to generate Dash Demo Dashboard
    """
    
    
    def __init__(self, data_file_path: str, convert_dict: Dict) -> None:
        """Initialises constructor variables

        Args:
            data_file_path (str): Tennis csv file path
            convert_dict (Dict): Datatypes
        """
        self.data_file_path = data_file_path
        self.convert_dict = convert_dict
        # pass
        
    
    
    def read_data(self) -> pd.DataFrame:
        """Reads CSV file

        Returns:
            pd.DataFrame: Stores CSV data into dataframe
        """
        df: pd.DataFrame = pd.DataFrame({})
        try:
            df = pd.read_csv(self.data_file_path, header=0, 
                            delimiter=",",low_memory=True,
                            usecols=["datetime_24hr_format","outlook","temp","humidity","windy","play","temperature"]
                            )
        except FileNotFoundError:
            print("File not found!!")
        except pd.errors.EmptyDataError:
            print("No Data!!")
        except pd.errors.ParserError:
            print("Parse Error!!")
        except Exception:
            print("Some exception occured!!")   
        if df.shape[0] < 1:
            raise Exception("No Data Loaded")
        else:
            return df   
        
    
    def create_dash_server(self) -> Dash:
        """Creates Dash Server
        """
        app = Dash(__name__)
        return app
    

    def data_preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess Tennis Data

        Args:
            df (pd.DataFrame): Preprocessed Tennis Data
            
        Returns:
            pd.DataFrame: Preprocessed data into dataframe            
        """
        
        # Column Rename : datetime_24hr_format -> play_time
        df = df.rename(columns={"datetime_24hr_format":"play_time"},inplace=False)
    
        # Convert Datatypes
        try:
            # Using Datatypes Dict
            df = df.astype(self.convert_dict)
            # Convert playtime[str] -> datetime
            df["play_time"] = pd.to_datetime(df["play_time"], format="%d-%m-%Y %H:%M:%S")
        except ValueError as e:
            print("Datatype Conversion Issue")
            print(e)
        except Exception:
            print("Issue during datatype conversion")
            
        # Sort the Data Order in Asc
        df = df.sort_values(by=["play_time"], ascending=True).reset_index().drop("index",axis=1)
        
        # Data Overview 
        print("--"*30)
        print("Data Overview : After Datatypes conversion")
        print("--"*30)
        # print(f"Load Data Shape : {df.shape}")
        print("\n")
        print(df.info())
        print("\n")
        print(df.head(2))
        print("\n")
        return df        


    def create_dashboards(self, app: Dash, df: pd.DataFrame) -> Dash:
        """Create Dash Dashboard

        Args:
            df (pd.DataFrame): Data for plotting

        Returns:
            Dash: Generates Bar Plot
        """
        
        fig = px.bar(df, x="outlook", y="temperature", color="play", barmode="group")
        
        app.layout = html.Div(children=[
                                html.H1(children='Dash Demo Dashboard'),

                                html.Div(children='''
                                    Dash: A web dashboard
                                '''),

                                dcc.Graph(
                                    id='Demo Graph',
                                    figure=fig
                                )
                            ])
        return app
        
        
        
if __name__ == "__main__":
    
    # Data File Path
    data_file_path: str = os.path.dirname(os.getcwd())+"/Sample_Data/tennis.csv"
    print("\n")
    print(f"Data File Path : {data_file_path}")
    print("\n")      
    
    # As per Database Table Datatypes
    convert_dict = {'play_time': str,
                    'outlook': str,
                    'temp': str,
                    'humidity': str,
                    'windy': str,
                    'play': str,
                    'temperature': int
                    }
    
    # Dash Demo Obj
    dash_demo: Dash_Demo = Dash_Demo(data_file_path, convert_dict)
    
    # Read Data
    df_plot: pd.DataFrame = dash_demo.read_data()  
    
    # Data Preprocess
    df_plot: pd.DataFrame = dash_demo.data_preprocess(df_plot)
    
    # Create Dash Server
    app: Dash = dash_demo.create_dash_server()
    
    # Create Dash Dashboards
    dash_demo.create_dashboards(app, df_plot) 
    
    # Run Dash Server
    app.run_server(debug=True)