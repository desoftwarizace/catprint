document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const printButton = document.getElementById('print-button');
    const previewCanvas = document.getElementById('preview');
    const previewContainer = document.getElementById('preview-container');
    const previewText = document.getElementById('preview-text');
    let renderedImageData = null;
    let dragCounter = 0;

    const handleFile = async (file) => {
        try {
            renderedImageData = await renderImage(file, previewCanvas);
            previewContainer.classList.add('has-image');
        } catch (error) {
            console.error('Rendering failed:', error);
            alert('Rendering failed. See console for details.');
            previewContainer.classList.remove('has-image');
        }
    };

    imageInput.addEventListener('change', () => {
        if (imageInput.files.length > 0) {
            handleFile(imageInput.files[0]);
        }
    });

    previewContainer.addEventListener('click', () => {
        imageInput.click();
    });

    previewContainer.addEventListener('dragenter', (event) => {
        event.preventDefault();
        dragCounter++;
        previewContainer.classList.add('drag-over');
    });

    previewContainer.addEventListener('dragover', (event) => {
        event.preventDefault();
    });

    previewContainer.addEventListener('dragleave', (event) => {
        event.preventDefault();
        dragCounter--;
        if (dragCounter === 0) {
            previewContainer.classList.remove('drag-over');
        }
    });

    previewContainer.addEventListener('drop', (event) => {
        event.preventDefault();
        dragCounter = 0;
        previewContainer.classList.remove('drag-over');
        if (event.dataTransfer.files.length > 0) {
            handleFile(event.dataTransfer.files[0]);
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