async function renderImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d', { willReadFrequently: true });

                const newWidth = 384;
                const newHeight = Math.floor(img.height * (newWidth / img.width));

                canvas.width = newWidth;
                canvas.height = newHeight;

                // Flip horizontally
                ctx.translate(newWidth, 0);
                ctx.scale(-1, 1);

                ctx.drawImage(img, 0, 0, newWidth, newHeight);

                // Floyd-Steinberg dithering
                const imageData = ctx.getImageData(0, 0, newWidth, newHeight);
                const data = imageData.data;
                const grayscale = new Uint8Array(newWidth * newHeight);

                for (let i = 0; i < data.length; i += 4) {
                    grayscale[i / 4] = (data[i] + data[i + 1] + data[i + 2]) / 3;
                }

                for (let y = 0; y < newHeight; y++) {
                    for (let x = 0; x < newWidth; x++) {
                        const index = y * newWidth + x;
                        const oldPixel = grayscale[index];
                        const newPixel = oldPixel > 128 ? 255 : 0;
                        grayscale[index] = newPixel;
                        const error = oldPixel - newPixel;

                        if (x + 1 < newWidth) {
                            grayscale[index + 1] += error * 7 / 16;
                        }
                        if (x - 1 >= 0 && y + 1 < newHeight) {
                            grayscale[index - 1 + newWidth] += error * 3 / 16;
                        }
                        if (y + 1 < newHeight) {
                            grayscale[index + newWidth] += error * 5 / 16;
                        }
                        if (x + 1 < newWidth && y + 1 < newHeight) {
                            grayscale[index + 1 + newWidth] += error * 1 / 16;
                        }
                    }
                }

                for (let i = 0; i < data.length; i += 4) {
                    const color = grayscale[i / 4];
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
