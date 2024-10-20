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
    let isTooltipVisible = false;
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

    // Tooltip element for selected text
    const tooltip = document.createElement('div');
    tooltip.classList.add('pdf-tooltip');
    document.body.appendChild(tooltip);

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

                        // Create a separate element for highlighting
                        const highlightElement = document.createElement('div');
                        Object.assign(highlightElement.style, {
                            position: 'absolute',
                            left: `${divLeft}px`,
                            top: `${divTop}px`,
                            width: `${divWidth}px`,
                            height: `${divHeight}px`,
                        });
                        // Create a transparent text element under span tag to make it selectable
                        const transparentTextSpan = document.createElement('span');
                        transparentTextSpan.textContent = item.str;
                        Object.assign(transparentTextSpan.style, {
                            position: 'absolute',
                            left: `${divLeft}px`,
                            top: `${divTop}px`,
                            fontFamily: item.fontName,
                            fontSize: `${Math.floor(fontHeight)}px`,
                        });
                        textLayerFrag.appendChild(transparentTextSpan);
                        textLayerFrag.appendChild(highlightElement);
                    });

                    textLayer.appendChild(textLayerFrag);
                    textLayer.addEventListener('mouseup', handleTextSelection);

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

    // Function to handle text selection and show tooltip
    function handleTextSelection(event) {
        const selection = window.getSelection();
        const selectedText = selection.toString();
        if (selectedText.trim().length > 0 && isDescendant(textLayer, selection.anchorNode)) {
            // There is selected text within textLayer
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            // Show the tooltip near the selected text
            showTooltip(rect, selectedText);
        } else {
            // No text selected, or selection is outside textLayer
            hideTooltip();
        }
    }

    // Helper function to check if a node is a descendant of a parent node
    function isDescendant(parent, child) {
        let node = child;
        while (node != null) {
            if (node === parent) {
                return true;
            }
            node = node.parentNode;
        }
        return false;
    }

    // Function to show the tooltip
    function showTooltip(rect, selectedText) {
        // Set the content of the tooltip
        tooltip.innerHTML = `
            <div class="d-flex justify-content-between align-items-center pdf-tooltip-content">
                <div class="text-align-justify pdf-tooltip-body m-2">
                    <h5>Selected Text</h5>
                    <p>${selectedText}</p>
                </div>
                <div class="text-align-justify pdf-tooltip-footer p-2 m-1">
                    <p><strong>Your Query:</strong></p>
                    <form class="chobot-form-body">
                        <div class="form-group">
                            <div class="input-group">
                                <textarea wrap="off" class="form-control chatbot-textarea" id="chatbot-textarea-tooltip"
                                    oninput="auto_grow(this)">Explain this piece text to me.</textarea>
                                <span class="input-group-addon fa-plane-send-span" id="fa-plane-send-span-tooltip">
                                    <a class="send-button chatbot-submit" type="submit" id="chatbot-submit-tooltip">
                                        <i class="fa-solid fa-paper-plane fa-custom-style" id="fa-plane-send-tooltip"></i>
                                    </a>
                                </span>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        `;
        // Position the tooltip near the selected text
        let tooltipX = rect.left + window.scrollX;
        let tooltipY = rect.bottom + window.scrollY;
        // Show the tooltip to get its dimensions
        tooltip.style.display = 'block';
        tooltip.style.left = `${tooltipX}px`;
        tooltip.style.top = `${tooltipY}px`;
        // Adjust position if tooltip goes off-screen
        let tooltipRect = tooltip.getBoundingClientRect();
        const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        if (tooltipRect.bottom > viewportHeight) {
            // Tooltip goes off-screen below, position it above
            tooltipY = rect.top + window.scrollY - tooltipRect.height;
            tooltip.style.top = `${tooltipY}px`;
            Object.assign(tooltipRect, tooltip.getBoundingClientRect());
        }
        // Recalculate tooltipRect after repositioning
        tooltipRect = tooltip.getBoundingClientRect();
        if (tooltipRect.top < 0) {
            // Tooltip still goes off-screen above, center it vertically
            tooltipY = window.scrollY + (viewportHeight - tooltipRect.height) / 2;
            tooltip.style.top = `${tooltipY}px`;
        }
        // Adjust horizontal position if needed
        if (tooltipRect.right > viewportWidth) {
            // Tooltip goes off-screen to the right, adjust position
            tooltipX = viewportWidth - tooltipRect.width - 10; // 10px padding
            tooltip.style.left = `${tooltipX}px`;
        } else if (tooltipRect.left < 0) {
            // Tooltip goes off-screen to the left, adjust position
            tooltipX = 10; // 10px padding
            tooltip.style.left = `${tooltipX}px`;
        }
        // Added event listener to submit the form
        const aButton = document.getElementById('chatbot-submit-tooltip');
        aButton.addEventListener('click', function (e) {
            var context = `
            ${selectedText}
            `;
            var message = document.getElementById('chatbot-textarea-tooltip').value;
            chatSubmit(e, `${context}\n\n${message}`);
            hideTooltip();
        });
        // Add event listener to detect clicks outside the tooltip
        if (!isTooltipVisible) {
            document.addEventListener('mousedown', outsideClickListener);
            isTooltipVisible = true;
        }
    }

    // Function to hide the tooltip
    function hideTooltip() {
        tooltip.style.display = 'none';
        if (isTooltipVisible) {
            document.removeEventListener('mousedown', outsideClickListener);
            isTooltipVisible = false;
        }
    }

    // Function to handle clicks outside the tooltip
    function outsideClickListener(event) {
        if (!tooltip.contains(event.target)) {
            hideTooltip();
        }
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
        textLayer.removeEventListener('mouseup', handleTextSelection);
        document.body.removeChild(tooltip);
        if (isTooltipVisible) {
            document.removeEventListener('mousedown', outsideClickListener);
            isTooltipVisible = false;
        }
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