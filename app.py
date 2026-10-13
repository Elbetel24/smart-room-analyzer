import streamlit as st
from ultralytics import YOLO
from PIL import Image
from collections import Counter


st.set_page_config(
    page_title="Smart room analyzer",
    layout="wide"
)


st.title("AI room analyzer")
st.write(
    "Upload a room photo to detect objects and "
    "generate an inventory using computer vision"
)


@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")


model=load_model()

uploaded_file=st.file_uploader(
    "Upload a room image",
    type=["jpg", "jpeg", "png"]
)


confidence=st.slider(
    "Detection confidence",
    min_value=0.10,
    max_value=0.90,
    value=0.40,
    step=0.05
)


if uploaded_file is not None:
    image=Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Room image")
    st.image(image)

    with st.spinner("Analyzing your room..."):
        results=model.predict(
            source=image,
            conf=confidence,
            verbose=False
        )


    result=results[0]

    annotated_image=result.plot()[:, :, ::-1]

    left, right=st.columns(2)

    with left:
        st.subheader("AI detection results")
        st.image( annotated_image,
                 width="stretch"
                 )

    with right:
        st.subheader("Room inventory")

        if result.boxes is not None and len(result.boxes)> 0:
            detected_classes=[
                result.names[int(class_id)]
                for class_id in result.boxes.cls.tolist()
            ]

            counts=Counter(detected_classes)

            total=sum(counts.values())
            st.metric("Objects detected", total)
            st.write("### Detected Objects ")

            for object_name,count in sorted(counts.items()):
                st.write(f"**{object_name.title()}**: {count}")

            inventory_text="Room inventory \n\n"
            inventory_text+=f"Total detections: {total}\n\n"

            for object_name, count in sorted(counts.items()):
                inventory_text+=(
                    f"{object_name.title()}: {count}\n"
                )

            st.download_button(
                "Download Room inventory",
                data=inventory_text,
                file_name="room_inventory.txt",
                mime="text/plain"
            )
        else:
            st.warning(
                "No objects detected. Try another image."
                "or lower the confidence threshold."
            )
    st.caption(
        "Note: Detection counts are estimates. Objects may be "
        "missed or counted more than once. The model only "
        "recognizes categories it was trained to detect."

    )



        


