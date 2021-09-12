

from pycaret.classification import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy
model = load_model('Flight_Price_Prediction')






def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Describe features", "Upload csv"))
    st.sidebar.info('This app is created for flight price prediction')
    st.title("Flight Price Prediction")
    if (add_selectbox == 'Describe features'):
        Airline=st.selectbox('Airline', ['Jet Airways','IndiGo','Air India','Multiple carriers','SpiceJet','Vistara','Air Asia','GoAir','Multiple carriers Premium economy','Jet Airways Business','Vistara Premium economy'])
        Source = st.selectbox('Source', ['Delhi','Kolkata','Banglore','Mumbai','Chennai'])
        Destination = st.selectbox('Destination', ['Cochin','Banglore','Delhi','New Delhi','Hyderabad','Kolkata'])
        Total_Stops = st.number_input('total stops', min_value=0, max_value=4, value=1)
        Route_1= st.selectbox('Route 1', ['None','BLR ', 'CCU ', 'DEL ', 'MAA ', 'BOM '])
        Route_2= st.selectbox('Route 2', ['None','DEL', 'IXR ', 'LKO ', 'NAG ', 'BLR', 'BOM ', 'BLR ', 'CCU','AMD ', 'PNQ ', 'CCU ', 'COK ', 'IDR ', 'GAU ', 'MAA ', 'HYD ','COK', 'DEL ', 'HYD', 'BHO ', 'JAI ', 'ATQ ', 'JDH ', 'BBI ','GOI ', 'BDQ ', 'TRV ', 'IXU ', 'IXB ', 'UDR ', 'RPR ', 'DED ','VGA ', 'VNS ', 'IXC ', 'PAT ', 'JLR ', 'KNU ', 'GWL ', 'VTZ ','NDC ', 'IXZ ', 'HBX ', 'IXA ', 'STV '])
        Route_3= st.selectbox('Route 3', ['None','BBI ', 'BOM ', 'BLR', 'DEL', 'COK', 'DEL ', 'AMD ', 'HYD','JDH ', 'MAA ', 'COK ', 'GOI ', 'NAG ', 'GAU ', 'BHO ', 'IXR ','IDR ', 'ISK ', 'HYD ', 'VGA ', 'PNQ ', 'JAI ', 'TRV ', 'HBX ','IMF ', 'CCU ', 'UDR ', 'VTZ ', 'IXC '])
        Route_4= st.selectbox('Route 4', ['None','BLR', 'COK', 'DEL', 'BOM ', 'HYD', 'DEL ', 'HYD ', 'GWL ','TRV ', 'BBI ', 'BHO ', 'AMD ', 'NAG '])
        Route_5= st.selectbox('Route 5', ['None','COK', 'BLR', 'DEL', 'HYD', 'VGA '])
        Additional_Info = st.selectbox('Additional Info', ['No info','In-flight meal not included','No check-in baggage included','1 Long layover','Change airports','Business class','2 Long layover','Red-eye flight','1 Short layover'])
        Date = st.number_input('Date',  min_value=1, max_value=31, value=1)
        Month = st.number_input('Month', min_value=1, max_value=12, value=1)
        Year = st.number_input('Year', min_value=2019, max_value=2022, value=2019)
        Departure_Hour = st.number_input('Departure Hour', min_value=0, max_value=23, value=0)
        Departure_Minute = st.number_input('Departure Minute', min_value=0, max_value=60, value=10)
        Arrival_Hour =st.number_input('Arrival Hour', min_value=0, max_value=23,value=1)
        Arrival_Minute =st.number_input('Arrival Minute', min_value=0, max_value=60, value=10)
        Duration_Hour = st.number_input('Duration hour', min_value=0, max_value=23, value=12)
        Duration_Minute =st.number_input('Duration Minute', min_value=0, max_value=60, value=10)
        output=""
        input_dict={'Airline':Airline,'Source':Source,'Destination':Destination,'Total_Stops':Total_Stops,'Route_1':Route_1,'Route_2':Route_2,'Route_3':Route_3,'Route_4':Route_4,'Route_5':Route_5,'Additional_Info':Additional_Info,'Date':Date,'Month':Month,'Year':Year,'Departure_Hour':Departure_Hour,'Departure_Minute':Departure_Minute,'Arrival_Hour':Arrival_Hour,'Arrival_Minute':Arrival_Minute,'Duration_Hour':Duration_Hour,'Duration_Minute':Duration_Minute}
        input_df = pd.DataFrame([input_dict])
        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = str(output)
        st.success('The output is {}'.format(output))
    if add_selectbox == 'Upload csv':
        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
        if file_upload is not None:
            data = pd.read_csv(file_upload)
            data['Date'] = data['Date_of_Journey'].str.split('/').str[0]
            data['Month'] = data['Date_of_Journey'].str.split('/').str[1]
            data['Year'] = data['Date_of_Journey'].str.split('/').str[2]
            data = data.drop(['Date_of_Journey'],axis=1)
            data['Arrival_Time'] = data['Arrival_Time'].str.split(' ').str[0]
            data['Total_Stops'] = data['Total_Stops'].replace('non-stop','0 stop')
            data['Total_Stops'] = data['Total_Stops'].str.split(' ').str[0]
            data['Arrival_Hour'] = data['Arrival_Time'].str.split(':').str[0]
            data['Arrival_Minute'] = data['Arrival_Time'].str.split(':').str[1]
            data = data.drop(['Arrival_Time'],axis=1)
            data['Departure_Hour'] = data['Dep_Time'].str.split(':').str[0]
            data['Departure_Minute'] = data['Dep_Time'].str.split(':').str[1]
            data = data.drop(['Dep_Time'],axis=1)
            data['Duration_Hour'] = data['Duration'].str.split(' ').str[0]
            data['Duration_Minute'] = data['Duration'].str.split(' ').str[1]
            data['Duration_Hour']= data['Duration_Hour'].str.split('h').str[0]
            data['Duration_Minute'] = data['Duration_Minute'].str.split('m').str[0]
            data['Duration_Minute'] = data['Duration_Minute'].fillna(0)
            data['Duration_Hour'] = data['Duration_Hour'].fillna(0)
            data = data.drop(['Duration'],axis=1)
            data['Route_1'] = data['Route'].str.split('→ ').str[0]
            data['Route_2'] = data['Route'].str.split('→ ').str[1]
            data['Route_3'] = data['Route'].str.split('→ ').str[2]
            data['Route_4'] = data['Route'].str.split('→ ').str[3]
            data['Route_5'] = data['Route'].str.split('→ ').str[4]
            data['Route_1'].fillna('None',inplace=True)
            data['Route_2'].fillna('None',inplace=True)
            data['Route_3'].fillna('None',inplace=True)
            data['Route_4'].fillna('None',inplace=True)
            data['Route_5'].fillna('None',inplace=True)
            data = data.drop(['Route'],axis=1)
            data['Date'] = data['Date'].astype(int)
            data['Month'] = data['Month'].astype(int)
            data['Year'] = data['Year'].astype(int)
            data['Total_Stops'] = data['Total_Stops'].astype('int')
            data['Arrival_Hour'] = data['Arrival_Hour'].astype('int')
            data['Arrival_Minute'] = data['Arrival_Minute'].astype('int')
            data['Departure_Hour'] = data['Departure_Hour'].astype('int')
            data['Departure_Minute'] = data['Departure_Minute'].astype('int')
            data['Duration_Minute'] = data['Duration_Minute'].astype(int)
            data['Duration_Hour'] = data['Duration_Hour'].str.split('m').str[0]
            data['Duration_Hour'] = data['Duration_Hour'].astype(int)
            predictions = predict_model(estimator=model,data=data)
            
            st.write(predictions)
def main():
    run()

if __name__ == "__main__":
  main()
