async function generateQR() {
    const data = document.getElementById('qr-input').value;
    if (!data) {
        alert('Please enter some data to generate QR code');
        return;
    }
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data})
    });
    const result = await response.json();
    if (result.image) {
        document.getElementById('qr-image').src = 'data:image/png;base64,' + result.image;
    } else if (result.error) {
        alert(result.error);
    }
}

async function scanQR() {
    const fileInput = document.getElementById('qr-upload');
    if (fileInput.files.length === 0) {
        alert('Please upload a QR code image to scan');
        return;
    }
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    const response = await fetch('/scan', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    document.getElementById('scan-result').textContent = result.result || result.error;
}

