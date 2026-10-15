
from flask import Flask, render_template, request
from ultralytics import YOLO
from PIL import Image
from collections import Counter
from io import BytesIO
import base64

app=Flask(__name__)

#Load the AI model once when the apps start
model=YOLO("yolo11n.pt")


@app.route("/", methods=["GET", "POST"])
def index():
    annotated_image=None
    counts={}
    total=0
    error=None

    if request.method == "POST":
        uploaded_file=request.files.get("room_image")

        try:
            confidence=float(
                request.form.get("confidence",0.40)
            )
            if not 0.10 <= confidence <= 0.90 :
                raise ValueError("Invalid confidence value.")

            if not uploaded_file or not uploaded_file.filename:
                raise ValueError("Please select an image.")

            image=Image.open(uploaded_file).convert("RGB")

            result=model.predict(
                source=image,
                conf=confidence,
                verbose=False
            )[0]

            plotted_image=result.plot()[:,:,::-1]

            buffer=BytesIO()
            Image.fromarray(plotted_image).save(
                buffer, format="JPEG"
            )
            annotated_image=base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

            if result.boxes is not None and len(result.boxes) > 0:
                detected_classes=[
                    result.names[int(class_id)]
                    for class_id in result.boxes.cls.tolist()
                ]

                counts=dict(Counter(detected_classes))
                counts=dict(sorted(counts.items()))
                total=sum(counts.values())
        except (ValueError, OSError) as exc:
            error=str(exc) or "could not read this image."





    return render_template(
        "index.html",
        annotated_image=annotated_image,
        counts=counts,
        total=total,
        error=error
        )


if __name__=="__main__":
    app.run(debug=True)
