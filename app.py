import streamlit as st
import pandas as pd
from database import get_connection
from predictor import predict_health

st.set_page_config(page_title="Health Prediction App")

st.title("🏥 Health Prediction Application")

menu = [
    "Create Patient",
    "View Patients",
    "Update Patient",
    "Delete Patient"
]

choice = st.sidebar.selectbox("Menu", menu)

# ==========================
# CREATE PATIENT
# ==========================

if choice == "Create Patient":

    st.subheader("Add New Patient")

    name = st.text_input("Full Name")

    dob = st.date_input("Date of Birth")

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose",
        min_value=0.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0
    )

    if st.button("Save Patient"):

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO patients
        (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                name,
                str(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
        )

        conn.commit()

        conn.close()

        st.success("Patient Saved Successfully")

        st.write("Health Remark:", remarks)

# ==========================
# VIEW PATIENTS
# ==========================

elif choice == "View Patients":

    st.subheader("Patient Records")

    conn = get_connection()

    query = "SELECT * FROM patients"

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    conn.close()

# ==========================
# UPDATE PATIENT
# ==========================

elif choice == "Update Patient":

    st.subheader("Update Patient")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    glucose = st.number_input(
        "New Glucose",
        min_value=0.0
    )

    haemoglobin = st.number_input(
        "New Haemoglobin",
        min_value=0.0
    )

    cholesterol = st.number_input(
        "New Cholesterol",
        min_value=0.0
    )

    if st.button("Update Patient"):

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        UPDATE patients
        SET glucose=%s,
            haemoglobin=%s,
            cholesterol=%s,
            remarks=%s
        WHERE id=%s
        """

        cursor.execute(
            query,
            (
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                patient_id
            )
        )

        conn.commit()

        conn.close()

        st.success("Patient Updated Successfully")

# ==========================
# DELETE PATIENT
# ==========================

elif choice == "Delete Patient":

    st.subheader("Delete Patient")

    patient_id = st.number_input(
        "Patient ID To Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Patient"):

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        DELETE FROM patients
        WHERE id=%s
        """

        cursor.execute(
            query,
            (patient_id,)
        )

        conn.commit()

        conn.close()

        st.success("Patient Deleted Successfully")