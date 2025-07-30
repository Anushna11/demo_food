import streamlit as st
import pymongo
import requests

client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["Food_prediction"]
collection=db["users"]
prediction_collection = db["predictions"]
ADMIN_USERNAME="anu"
ADMIN_PASSWORD="anu"
st.title("  Food Predictor 😋 ")
select=st.sidebar.selectbox("Page Navigator",["Registration Page","Prediction Page","Admin Page"])
if(select=="Registration Page"):
    st.header("Registration Page")
    un=st.text_input("Username")
    pw=st.text_input("Password",type="password")
    bn=st.button("Register")
    if bn:
        if un!="" and pw!="":
            e_user=collection.find_one({"Username":un,"Password":pw})
            if e_user:
                st.error("Username,password already exists")
            else:
                collection.insert_one({
                        "username":un,
                        "password":pw})
                st.success("Registration is success")
        else:
            st.error("Enter the proper username and password")
elif(select=="Prediction Page"):
     
    st.header("Login")
    un=st.text_input("Username")
    pw=st.text_input("Password",type="password")
    if un!="" and pw!="":
       if(collection.find_one({"Username":un,"Password":pw}) is not None):
           st.markdown("--------------------------------")
           st.header(f"Hi {un} Predict yout food Preference")
           mood=st.selectbox("Mood",["happy","tired","sad","energetic","bored","angry","neutral","excited","stressed"])
           time_of_day=st.selectbox("time_of_day",["breakfast","lunch","evening","dinner"])
           diet=st.selectbox("Choose your diet",["veg","non-veg","vegan"])
           is_hungry=st.checkbox("Are you Hungry?")
           prefers_spicy=st.checkbox("Prefer Spicy !")
           if(st.button("Predict the Food")):
               data={
                   "mood":mood,
                   "time_of_day":time_of_day,
                   "is_hungry":is_hungry,
                   "prefers_spicy":prefers_spicy,
                   "diet":diet
               }
               res=requests.post("http://127.0.0.1:8000/predict",json=data)
               result=res.json()
               st.write("Predicted Food : ",result["Predicted_food"])
elif(select=="Admin Page"):
    st.header(" Admin Login")
    un = st.text_input("Admin Username")
    pw = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if un == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            st.success("✅ Admin Login Successful")
             
            st.subheader("Registered Users & Prediction Data")

            data = collection.find()
            for record in data:
                st.write(f" Username: {record.get('username')}")
                st.write(f" Password: {record.get('password')}")

                st.write(f" Predicted Food: {record.get('Predicted_food')}")
        else:
            st.error(" Invalid Admin Credentials")


    




