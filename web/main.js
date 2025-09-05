document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const printButton = document.getElementById('print-button');

    printButton.addEventListener('click', async () => {
        if (imageInput.files.length === 0) {
            alert('Please select an image first.');
            return;
        }

        try {
            const file = imageInput.files[0];
            const imageData = await renderImage(file);
            await printImage(imageData);
        } catch (error) {
            console.error('Printing failed:', error);
            alert('Printing failed. See console for details.');
        }
    });
});
