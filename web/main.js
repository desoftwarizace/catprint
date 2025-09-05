document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const printButton = document.getElementById('print-button');
    const previewCanvas = document.getElementById('preview');
    let renderedImageData = null;

    imageInput.addEventListener('change', async () => {
        if (imageInput.files.length === 0) {
            return;
        }

        try {
            const file = imageInput.files[0];
            renderedImageData = await renderImage(file, previewCanvas);
        } catch (error) {
            console.error('Rendering failed:', error);
            alert('Rendering failed. See console for details.');
        }
    });

    printButton.addEventListener('click', async () => {
        if (!renderedImageData) {
            alert('Please select an image first.');
            return;
        }

        try {
            await printImage(renderedImageData);
        } catch (error) {
            console.error('Printing failed:', error);
            alert('Printing failed. See console for details.');
        }
    });
});