async function renderImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                const newWidth = 384;
                const newHeight = Math.floor(img.height * (newWidth / img.width));

                canvas.width = newWidth;
                canvas.height = newHeight;

                // Flip horizontally
                ctx.translate(newWidth, 0);
                ctx.scale(-1, 1);

                ctx.drawImage(img, 0, 0, newWidth, newHeight);

                // Convert to black and white
                const imageData = ctx.getImageData(0, 0, newWidth, newHeight);
                const data = imageData.data;
                for (let i = 0; i < data.length; i += 4) {
                    const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
                    const color = avg > 128 ? 255 : 0;
                    data[i] = color;
                    data[i + 1] = color;
                    data[i + 2] = color;
                }
                ctx.putImageData(imageData, 0, 0);
                resolve(ctx.getImageData(0, 0, newWidth, newHeight));
            };
            img.onerror = reject;
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}