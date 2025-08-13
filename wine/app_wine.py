import streamlit as st
import pandas as pd
import joblib
import time

red_model = joblib.load('models/red_wine_model.joblib')
white_model = joblib.load('models/white_wine_model.joblib')
scaler = joblib.load('models/scaler.joblib')


st.title("🍷Predicción de Calidad de Vino")

st.write("""
Ajusta los valores de las características usando los campos y obtén la predicción de calidad.
""")

red_best_mean = {
    'fixed acidity': 8.25,
    'volatile acidity': 0.37,
    'citric acid': 0.42,
    'residual sugar': 2.1,
    'chlorides': 0.0705,
    'free sulfur dioxide': 7.5,
    'total sulfur dioxide': 21.5,
    'density': 0.9949,
    'pH': 3.23,
    'sulphates': 0.74,
    'alcohol': 12.5
}

white_best_mean = {
    'fixed acidity': 6.80,
    'volatile acidity': 0.26,
    'citric acid': 0.32,
    'residual sugar': 4.3,
    'chlorides': 0.0355,
    'free sulfur dioxide': 34.5,
    'total sulfur dioxide': 122.0,
    'density': 0.9916,
    'pH': 3.23,
    'sulphates': 0.46,
    'alcohol': 12.0
}

col1, col2,col3 = st.columns(3)
val = []
with col1:
    val.append(st.number_input("fixed acidity: g(tartaric acid)/dm3", min_value=5.6, max_value=11.8,step = 0.1, format="%.1f"))
    val.append(st.number_input("volatile acidity: g(acetic acid)/dm3", min_value=0.15, max_value=0.84,step = 0.01,format="%.2f"))
    val.append(st.number_input("citric acid: g/dm3", min_value=0.0, max_value=0.6, step = 0.01,format="%.2f"))
    val.append(st.number_input("residual sugar: g/dm3", min_value=1.1, max_value=15.7, step = 0.01,format="%.2f"))
with col2:
    val.append(st.number_input("chlorides: g(sodium chloride)/dm3", min_value=0.027, max_value=0.127, step = 0.001,format="%.3f"))
    val.append(st.number_input("free sulfur dioxide: mg/dm3", min_value=4.0, max_value=63.0, step = 0.5,format="%.1f"))
    val.append(st.number_input("total sulfur dioxide: mg/dm3", min_value=11.0, max_value=212.0, step = 1.0,format="%.1f"))
    val.append(st.number_input("density: g/cm3", min_value=0.9896, max_value=1.0, step = 0.0001,format="%.4f"))
with col3:
    val.append(st.number_input("pH", min_value=2.96, max_value=4.0, step = 0.01,format="%.2f"))
    val.append(st.number_input("sulphates: g(potassium sulphate)/dm3", min_value=0.34, max_value=0.93, step = 0.01,format="%.2f"))
    val.append(st.number_input("alcohol: % vol.", min_value=8.9, max_value=13.0, step = 0.01,format="%.2f"))
    
col1, col2 = st.columns(2)

with col1:
    if st.button("Predecir calidad vino tinto"):
        tiempo_inicio = time.time()
        input_df = pd.DataFrame([val])
        input_scaled = scaler.transform(input_df)
        prediction = red_model.predict(input_scaled)
        #st.success(f"Calidad del vino: **{prediction[0]} :  (1: Basic 2: Medium 3: Premium)**")
        if prediction == "1":
             st.success("Calidad del vino: BASIC")
        if prediction == "2":
             st.success("Calidad del vino: MEDIUM")
        if prediction == "3":
             st.success("Calidad del vino: PREMIUM")
        tiempo_final = time.time()
        tiempototal = tiempo_final - tiempo_inicio
        print (tiempototal)
        resultado = {k: v - val[i] for i, (k, v) in enumerate(red_best_mean.items())}
        st.write("Parametros a mejorar para que la calidad Premium:")
        for i, (k, v) in enumerate(red_best_mean.items()):
            resultado = v - val[i]
            if resultado == 0:
                st.write(f" el parametro **{k}** `es optimo`")
            if resultado > 0:
                st.write(f"Aumente **{k}** `{resultado:.2f}`")

            if resultado < 0:
                st.write(f"Disminuya **{k}**: = `{resultado:.2f}`")

    

with col2:
    if st.button("Predecir calidad vino blanco"):
        input_df = pd.DataFrame([val])
        input_scaled = scaler.transform(input_df)
        prediction = white_model.predict(input_scaled)
        if prediction == "1":
             st.success("Calidad del vino: BASIC")
        if prediction == "2":
             st.success("Calidad del vino: MEDIUM")
        if prediction == "3":
             st.success("Calidad del vino: PREMIUM")

        resultado = {k: v - val[i] for i, (k, v) in enumerate(white_best_mean.items())}
        print(resultado)
        st.write("Parametros a mejorar para que la calidad Premium:")
        for i, (k, v) in enumerate(white_best_mean.items()):
            resultado = v - val[i]
            if resultado == 0:
                st.write(f" el parametro **{k}** `es optimo`")
            if resultado > 0:
                st.write(f"Aumente **{k}** `{resultado:.2f}`")

            if resultado < 0:
                st.write(f"Disminuya **{k}**: = `{resultado:.2f}`")
            
    
print (val)





