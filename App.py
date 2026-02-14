import streamlit as st
import textwrap

from CalculationsUnits import (
    extractAndReplaceMetricUnits,
    extractAndReplaceUnits,
    extractUnitsFromAnswer,
    extractUnitsFromText,
    ConvertMetToImpSeparate,
    ConvertImpToMetSeparate
)

st.set_page_config(page_title="UnitConverterPy", layout="centered")
st.title("Episode V: The Metric Strikes Back")
st.write("Darth Convertor says: 'I find your lack of metric... disturbing.'")

with st.sidebar:
    st.header("Controls")

    imp_to_met = st.toggle("Imperial → Metric", value=True)

    wrap = st.toggle("Wrap output to 70 chars", value=True)
    show_detected = st.toggle("Show detected units", value=False)
    show_conversions = st.toggle("Show conversions list", value=True)

direction_label = "Imperial → Metric" if imp_to_met else "Metric → Imperial"
st.subheader(direction_label)


text = st.text_area(
    "Input text",
    height=220,
    placeholder="Example: The car moves at 100 mi/hr and has an acceleration of 32 ft/s^2"
)

wrap = st.checkbox("Wrap output to 70 characters", value=True)

if st.button("Convert"):
    if not text.strip():
        st.warning("No text was input")
    else:
        try:
            if direction == "Imperial -> Metric":
                detected = extractUnitsFromText(text)
                if not detected:
                    st.error("No imperial units detected.")
                else:
                    conversions = ConvertImpToMetSeparate(detected)
                    st.subheader("🧪 Conversions:")
                    st.code("\n".join(conversions))

                    output = extractAndReplaceUnits(text)

                    if wrap:
                        output = textwrap.fill(output, width=70)

                    st.subheader("\n🧪 Converted Text:")
                    st.code(output)

            else:  # Metric -> Imperial
                detected = extractUnitsFromAnswer(text)
                if not detected:
                    st.error("No metric units detected.")
                else:
                    conversions = ConvertMetToImpSeparate(detected)
                    st.subheader("🧪 Conversions:")
                    st.code("\n".join(conversions))
                    output = extractAndReplaceMetricUnits(text)

                    if wrap:
                        output = textwrap.fill(output, width=70)

                    st.subheader("Converted Text")
                    st.code(output)

        except Exception as e:
            st.error(f"Conversion failed: {e}")
