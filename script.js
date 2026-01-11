function previewImage() {
    const file = document.getElementById("imageInput").files[0];
    const preview = document.getElementById("preview");

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }
}

function uploadImage() {
    const input = document.getElementById("imageInput");
    const file = input.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    document.getElementById("status").innerText = "Predicting...";
    document.getElementById("result").innerText = "";

    const formData = new FormData();
    formData.append("image", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").innerText = "";
        document.getElementById("result").innerHTML =
            `🍎 <b>${data.fruit}</b><br>Confidence: ${data.confidence}%`;
    })
    .catch(() => {
        document.getElementById("status").innerText = "Error occurred!";
    });
}
