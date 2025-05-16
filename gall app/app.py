import os
import pickle
import time
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Gallbladder Prediction App",
                   layout="wide")
                   #page_icon="🧑‍⚕️")


    
# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

gall_model = pickle.load(open(f'{working_dir}/Saved_models/gall_cancer_model.sav', 'rb'))

with st.sidebar:
    selected = option_menu('Gall Bladder Prediction Screening Tool',

                           ['Gall Bladder'],
                            #st.image()
                           #menu_icon='hospital-fill',
                           icons=['person'],
                           default_index=0)
st.sidebar.markdown("""
### Gall Bladder Cancer
 Gall Bladder Cancer is a rare but aggressive disease that affects the biliary system.
 - <span style='color:blue'>Often diagnosed late</span> due to unclear symptoms.
 - <span style='color:blue'>Risk Factors</span> include gallstones and chronic inflammation.
 - Common Symptoms: abdominal pain, jaundice and weight loss.
 -<span style='color:red'>Early detection is very Important</span> for better Health.
### Always consult a Gastroenterologist for medical Advice.                 
""", unsafe_allow_html=True                  )

# Diabetes Prediction Page
if selected == 'Gall Bladder':

    # page title
    st.title('Gall Bladder Screening Tool: Please fill in your Details below')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    

    with col1:
        Age = st.number_input('Your specified Age',min_value=0, max_value=120, step = 1)

    with col2:
        Gender = st.selectbox('Select your Gender',["Male","Female"])
          
    with col3:
        Ethnicity = st.selectbox('Select Your Ethnic group',["Asian","Hispanic","African Ethnicity","Caucasian","Other"])   

    with col1:
        Stage = st.selectbox('Select your Cancer Stage',["I","II","III","IV"])

    with col2:
        Smoking_History = st.selectbox('Are you smoking?',["No","Yes"])

    with col3:
        Alcohol_Consumption = st.selectbox('Do you take Alcohol?',["No","Yes"])

    with col1:
        Family_History = st.selectbox('Do members of Your Family have gallbladder Cancer?', ["No","Yes"])

    with col2:
        Diabetes = st.selectbox('Are you Diabetic?',["No","Yes"])

    with col3:
        Gallstones = st.selectbox('Do you have gallstones?',["No","Yes"])    

    with col1:
        Jaundice = st.selectbox('Do you have Jaundice?',["No","Yes"])

    with col2:
        CEA_Level = st.number_input('Your Carcinoembyonic Antigen Level', min_value=0.0, step = 0.1)        

    # Map categorical values to numericals
    gender_map = {"Male": 1, "Female": 0}
    yn_map = {"Yes":1, "No": 0}
    ethnicity_map = {"Asian": 0, "Hispanic": 1, "African Ethnicity":2, "Caucasian":3,"Other":4}
    stage_map = {"I":0, "II": 1, "III": 2, "IV": 3}

    # code for Prediction
    gall_diagnosis = ''

    # creating a button for Prediction

    if st.button('Gall Bladder Cancer Predict'):
        with st.spinner("Thinking..."):
            time.sleep(3)

        user_input = [
            Age,
            gender_map[Gender],
            ethnicity_map[Ethnicity],
            stage_map[Stage],
            yn_map[Smoking_History],
            yn_map[Alcohol_Consumption],
            yn_map[Family_History],
            yn_map[Diabetes],
            yn_map[Gallstones],
            yn_map[Jaundice],
            CEA_Level
        ]    

        
        user_input = [float(x) for x in user_input]

        gall_prediction = gall_model.predict([user_input])
        user_input_array = np.array(user_input).reshape(1,-1)
        pred_prob = gall_model.predict_proba(user_input_array)[:, 1][0]

        st.write(f"**Probability of Gall Bladder Cancer:** {pred_prob:.2%}")
        st.write(f"**Predicted Class:** {'High Risk' if gall_prediction[0] == 'Deceased' else 'Low Risk'}")



        if gall_prediction[0] == "Deceased":
            st.markdown(
                "<div style='color:red; font-size:20px; font-weight:bold;'>⚠️ High Risk of Gall Bladder Cancer</div>", 
                unsafe_allow_html=True
            )
            st.markdown(
                """
                **Recommendations:**
                - Please consult an oncologist or gastroenterologist for full diagnostic evaluation and treatment plan.  
                - Consider possible chemotherapy, radiation or targeted therapy.  
                - Adopt a Healthy Lifestyle(Quit Smoking and alcohol Consumption).
                - Seek emotional and psychological support through counselling.
                - Ensure Regular follow-ups for progress tracking and symptom management.
                """
            )
        else:
            st.markdown(
                "<div style='color:green; font-size:20px; font-weight:bold;'>✅ Low Risk of Gall Bladder Cancer</div>", 
                unsafe_allow_html=True
            )
            st.markdown(
                """
                **Recommendations:**
                - Keep up with your healthy lifestyle habits(Avoid Risk Factors).  
                - Keep conditions like Diabetes and Gallstones under control.  
                - Educate yourself about gall bladder health and early warning signs like abdominal pain or jaundice.
                """
            )
    
