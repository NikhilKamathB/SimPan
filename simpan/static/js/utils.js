// Imports
import * as pdfjsLib from './pdf.mjs';

// Set PDF worker source
pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/js/pdf.worker.mjs';

// Get cookie for CSRF token verification
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show message
function showMessage(message, type) {
    let mainMessageContainer = document.body.querySelector('#main-messages');
    if (mainMessageContainer) {
        mainMessageContainer.remove();
    }
    mainMessageContainer = document.createElement('div');
    mainMessageContainer.append(`
        <div class="alert alert-dismissible fade show mt-0 messages-${type}" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `);
}

// Render PDF
function renderPDF(url, divID) {
    let pdf = null;
    let currentPage = 1;
    let isRendering = false;
    const divContainer = document.getElementById(divID);
    divContainer.innerHTML = '';

    // Create a wrapper for the entire PDF viewer
    const pdfViewerWrapper = document.createElement('div');
    pdfViewerWrapper.classList.add('d-flex', 'pdf-viewer-wrapper');
    divContainer.appendChild(pdfViewerWrapper);

    // Create thumbnails section
    const thumbnailsSection = document.createElement('div');
    thumbnailsSection.classList.add('pdf-thumbnails', 'd-flex', 'flex-column');
    pdfViewerWrapper.appendChild(thumbnailsSection);

    // Create main content section
    const mainContent = document.createElement('div');
    mainContent.classList.add('pdf-main-content', 'd-flex', 'justify-content-center', 'align-items-center');
    pdfViewerWrapper.appendChild(mainContent);
    
    // Controls
    const controls = document.createElement('div');
    controls.classList.add('pdf-controls');
    controls.innerHTML = `
        <a id="prev-page" class="mx-3" type="button"><i class="fa-solid fa-arrow-left fa-custom-style fa-custom-style-increased-font" id="fa-arrow-left"></i></a>
        <p id="page-num"></p> / <p id="page-count"></p>
        <a id="next-page" class="mx-3" type="button"><i class="fa-solid fa-arrow-right fa-custom-style fa-custom-style-increased-font" id="fa-arrow-right"></i></a>
    `;
    mainContent.appendChild(controls);

    // Create a container for the canvas and text layer
    const canvasContainer = document.createElement('div');
    canvasContainer.style.position = 'relative';
    canvasContainer.style.width = '100%';
    canvasContainer.style.height = '100%';
    mainContent.appendChild(canvasContainer);

    // Canvas
    const canvas = document.createElement('canvas');
    canvas.classList.add('pdf-canvas');
    canvasContainer.appendChild(canvas);

    // Text layer
    const textLayer = document.createElement('div');
    textLayer.id = 'text-layer';
    textLayer.style.position = 'absolute';
    textLayer.style.left = '0';
    textLayer.style.top = '0';
    textLayer.style.right = '0';
    textLayer.style.bottom = '0';
    textLayer.style.overflow = 'hidden';
    textLayer.style.pointerEvents = 'none';
    canvasContainer.appendChild(textLayer);

    // Buttons
    const prevButton = controls.querySelector('#prev-page');
    const nextButton = controls.querySelector('#next-page');
    const pageNum = controls.querySelector('#page-num');
    const pageCount = controls.querySelector('#page-count');

    function renderPage(pageNumber) {
        if (isRendering) return;
        isRendering = true;
        pdf.getPage(pageNumber).then(function (page) {
            const context = canvas.getContext('2d');
            const parentWidth = canvasContainer.clientWidth;
            const parentHeight = canvasContainer.clientHeight;
            const originalViewport = page.getViewport({ scale: 1 });
            const scaleX = parentWidth / originalViewport.width;
            const scaleY = parentHeight / originalViewport.height;
            const scale = Math.min(scaleX, scaleY);
            const viewport = page.getViewport({ scale: scale });

            canvas.height = viewport.height;
            canvas.width = viewport.width;
            canvasContainer.style.width = `${viewport.width}px`;
            canvasContainer.style.height = `${viewport.height}px`;

            const renderContext = {
                canvasContext: context,
                viewport: viewport,
            };

            // Clear and set up text layer
            textLayer.innerHTML = '';
            textLayer.style.width = `${viewport.width}px`;
            textLayer.style.height = `${viewport.height}px`;

            const renderTask = page.render(renderContext);
            const textContent = page.getTextContent();

            Promise.all([renderTask.promise, textContent])
                .then(([_, textContent]) => {
                    const textItems = textContent.items;
                    const textLayerFrag = document.createDocumentFragment();

                    textItems.forEach(function (item) {
                        const tx = pdfjsLib.Util.transform(viewport.transform, item.transform);

                        const fontHeight = Math.sqrt((tx[2] * tx[2]) + (tx[3] * tx[3]));
                        const divLeft = Math.floor(tx[4]);
                        const divTop = Math.floor(tx[5] - fontHeight);
                        const divWidth = Math.max(1, Math.ceil(item.width * viewport.scale));
                        const divHeight = Math.max(1, Math.ceil(fontHeight));

                        const textElement = document.createElement('span');
                        textElement.textContent = item.str;
                        Object.assign(textElement.style, {
                            left: `${divLeft}px`,
                            top: `${divTop}px`,
                            fontSize: `${Math.floor(fontHeight)}px`,
                            fontFamily: item.fontName,
                            width: `${divWidth}px`,
                            height: `${divHeight}px`,
                            position: 'absolute',
                            whiteSpace: 'pre',
                            transformOrigin: '0% 0%',
                            transform: `scaleX(${viewport.scale})`,
                            color: 'transparent',
                            background: 'rgba(255, 255, 0, 0.8)',
                        });

                        textLayerFrag.appendChild(textElement);
                    });

                    textLayer.appendChild(textLayerFrag);

                    currentPage = pageNumber;
                    pageNum.textContent = currentPage;
                    prevButton.classList.toggle('disabled', currentPage <= 1);
                    nextButton.classList.toggle('disabled', currentPage >= pdf.numPages);
                    isRendering = false;
                    highlightThumbnail(pageNumber);
                    scrollThumbnailIntoView(pageNumber);
                });
        });
    }

    // Change page
    function changePage(delta) {
        const newPage = currentPage + delta;
        if (newPage >= 1 && newPage <= pdf.numPages) {
            renderPage(newPage);
        }
    }

    // Scroll event handler
    function handleScroll(event) {
        event.preventDefault();
        const delta = Math.sign(event.deltaY);
        changePage(delta);
    }

    // Add scroll event listener
    mainContent.addEventListener('wheel', handleScroll, { passive: false });

    // Touch events for mobile devices
    let touchStartY = 0;
    mainContent.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    // Touch move event
    mainContent.addEventListener('touchmove', (e) => {
        const touchEndY = e.touches[0].clientY;
        const delta = touchStartY - touchEndY;
        if (Math.abs(delta) > 50) { // Threshold to trigger page change
            changePage(Math.sign(delta));
            touchStartY = touchEndY;
        }
    }, { passive: true });

    // Button click events
    prevButton.addEventListener('click', () => changePage(-1));
    nextButton.addEventListener('click', () => changePage(1));

    // Keyboard navigation
    function handleKeyDown(event) {
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            changePage(-1);
        } else if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            changePage(1);
        }
    }

    // Add keyboard event listener
    document.addEventListener('keydown', handleKeyDown);

    // Function to render thumbnails
    function renderThumbnails() {
        for (let i = 1; i <= pdf.numPages; i++) {
            pdf.getPage(i).then(function (page) {
                const viewport = page.getViewport({ scale: 0.15 });
                const canvas = document.createElement('canvas');
                canvas.classList.add('pdf-thumbnail-canvas');
                canvas.width = viewport.width;
                canvas.height = viewport.height;
                canvas.dataset.pageNumber = i;
                const context = canvas.getContext('2d');
                page.render({ canvasContext: context, viewport: viewport });
                canvas.addEventListener('click', function () {
                    renderPage(parseInt(this.dataset.pageNumber));
                });
                thumbnailsSection.appendChild(canvas);
            });
        }
    }

    // Function to highlight the current thumbnail
    function highlightThumbnail(pageNumber) {
        const thumbnails = thumbnailsSection.querySelectorAll('canvas');
        thumbnails.forEach(thumbnail => {
            if (parseInt(thumbnail.dataset.pageNumber) === pageNumber) {
                thumbnail.style.border = '2px solid blue';
                thumbnail.style.boxShadow = '0 0 5px var(--first-color)';
            } else {
                thumbnail.style.border = 'none';
                thumbnail.style.boxShadow = 'none';
            }
        });
    }

    // Function to scroll the thumbnail into view
    function scrollThumbnailIntoView(pageNumber) {
        const thumbnail = thumbnailsSection.querySelector(`canvas[data-page-number="${pageNumber}"]`);
        if (thumbnail) {
            const thumbnailRect = thumbnail.getBoundingClientRect();
            const sectionRect = thumbnailsSection.getBoundingClientRect();
            if (thumbnailRect.top < sectionRect.top || thumbnailRect.bottom > sectionRect.bottom) {
                thumbnail.scrollIntoView({
                    behavior: 'auto',
                    block: 'nearest'
                });
            }
        }
    }

    // Load the PDF
    pdfjsLib.getDocument(url).promise.then(function (loadedPdf) {
        pdf = loadedPdf;
        pageCount.textContent = pdf.numPages;
        renderPage(currentPage);
        renderThumbnails();
    }).catch(function (error) {
        divContainer.innerHTML = `<p>Error loading PDF: ${error.message}</p>`;
    });

    // Cleanup function to remove event listeners when needed
    return function cleanup() {
        document.removeEventListener('keydown', handleKeyDown);
        mainContent.removeEventListener('wheel', handleScroll);
    };
}

// Definitions
const VehicleType = {
    VEHICLE: 'vehicle',
    PEDESTRIAN: 'pedestrian'
};

// Global scoped
window.getCookie = getCookie;
window.renderPDF = renderPDF;
window.showMessage = showMessage;

export { getCookie, VehicleType };