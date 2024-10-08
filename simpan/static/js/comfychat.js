/*==================== Variables ====================*/
let selectedFiles = [];
let selectedFileId = null;
/*=========================================================*/

/*==================== Intialize tooltip ====================*/
$(document).ready(function () {
    $('[data-toggle="workspace-tooltip"]').tooltip();
});
/*=========================================================*/

/*==================== Add/Open/Delete workspace ====================*/
function createWorkspace() {
    const csrftoken = window.getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: window.location.origin + "/services/api/workspace/",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (response) {
            responseData = {
                "workspace": response.data.id,
                "workspace_name": response.data.name,
                "workspace_files": response.data.workspace_files ? response.data.workspace_files : [],
                "workspace_chat": response.data.conversation ? response.data.conversation : [],
                "workspace_created_at": response.data.created_at,
                "workspace_updated_at": response.data.updated_at
            }
            window.context_data[response.data.id] = responseData;
            openWorkspace(window.context_data[response.data.id].workspace);
            updateOffcanvasWorkspace(window.context_data[response.data.id].workspace);
            openWorkspaceAccordion(window.context_data[response.data.id].workspace);
        },
        error: function (response) {
            const errorMessage = response.responseJSON.message;
            const capitalizedMessage = errorMessage.charAt(0).toUpperCase() + errorMessage.slice(1);
            alert(capitalizedMessage + " : " + response.responseJSON.data.message);
        }
    });
}

$('#workspace-add').click(function () {
    createWorkspace();
});

function openWorkspace(workspaceID) {
    const workspaceName = window.context_data[workspaceID].workspace_name ? window.context_data[workspaceID].workspace_name : workspaceID;
    $('#workspace-heading').empty().append(`<h5 data-toggle="workspace-title-tooltip" data-placement="top" title="Workspace ID - ${workspaceID}">${workspaceName}</h5>`);
    $('[data-toggle="workspace-title-tooltip"]').tooltip();
    $('#workspace-tab-content').empty();
    $('#workspace-tab-content').append(`
    <div class="workspace-tab-pane" id="${workspaceID}">
        <div id="workspace-display-container">
            <div class="justify-content-between align-items-center workspace-viewport m-3">
                <div class="container workspace-body p-0">
                    <div class="container workspace-body-header"></div>
                    <div id="workspace-body-main" class="justify-content-between align-items-center workspace-body-main">
                    </div>
                    <div class="container workspace-body-footer"></div>
                </div>
            </div>
            <div id="selected-files-view"
                class="d-flex justify-content-center align-items-center selected-files-view workspace-metaview px-2">
            </div>
        </div>
    </div>
    `);
    if (window.context_data[workspaceID] && window.context_data[workspaceID].workspace_files && window.context_data[workspaceID].workspace_files.length > 0) {
        const lastFile = window.context_data[workspaceID].workspace_files[window.context_data[workspaceID].workspace_files.length - 1];
        selectedFileId = lastFile.id;
        updateWorkspaceMetaView();
        thumbnailClick(lastFile);
        updateThumbnailStyles();
    }
    generateInitialChatbotBody(window.context_data[workspaceID].workspace_chat);
}

function deleteWorkspace(workspaceID) {
    const csrftoken = window.getCookie('csrftoken');
    $.ajax({
        type: "DELETE",
        url: window.location.origin + "/services/api/workspace/" + workspaceID + "/",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (response) {
            delete window.context_data[workspaceID];
            removeOffcanvasWorkspaceAccordion(workspaceID);
            if (Object.keys(window.context_data).length > 0) {
                const workspace = window.context_data[Object.keys(window.context_data)[0]];
                openWorkspace(workspace.workspace);
                openWorkspaceAccordion(workspace.workspace);
            }
            else {
                createWorkspace();
            }
            alert("Workspace deleted successfully");
        },
        error: function (response) {
            alert(response.responseJSON.message);
        }
    });
}
/*=========================================================*/

/*==================== Enable Auto-grow ====================*/
function auto_grow(element) {
    element.style.height = "25px";
    element.style.height = (element.scrollHeight) + "px";
}
/*=========================================================*/

/*================ File Upload and display ================*/
function getFileExtension(filename) {
    return filename.split('.').pop().toUpperCase();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

function handleFileSelect(event) {
    const newFiles = Array.from(event.target.files);
    const uniqueNewFiles = newFiles.filter(newFile =>
        !selectedFiles.some(existingFile =>
            existingFile.name === newFile.name && existingFile.size === newFile.size
        )
    );
    selectedFiles = [...selectedFiles, ...uniqueNewFiles];
    updateFileList();
    event.target.value = '';
}

function thumbnailClick(file) {
    if (file.type.match(/(pdf)$/i)) {
        const _ = $('#workspace-body-main').empty();
        renderPDF(file.url, 'workspace-body-main');
        return true;
    }
    return false;
}

function clearFileSelection() {
    selectedFiles = [];
    $('#file-upload-input').val('');
    updateFileList();
}

function generateInitialWorkspaceFileDisplay() {
    if (window.workspaceFiles.length > 0) {
        for (let file of window.workspaceFiles) {
            if (thumbnailClick(file)) {
                selectedFileId = file.id;
                updateThumbnailStyles();
                break;
            }
        }
    }
}

function updateFileList(id = '#selected-files', showRemove = true) {
    const $fileList = $(id).empty();
    $("#chatbot-container-body").animate({ scrollTop: $('#chatbot-body').height() }, "slow");
    selectedFiles.forEach((file, index) => {
        const $thumbnail = $('<div>').addClass('d-flex justify-content-between align-items-center file-thumbnail');
        const $extension = $('<div>').addClass('file-extension').text(getFileExtension(file.name));
        $thumbnail.append($extension);
        if (showRemove) {
            const $removeBtn = $('<div>').addClass('remove-file').html('&times;').click(() => removeFile(index));
            $thumbnail.append($removeBtn);
        }
        if (file.type.startsWith('image/') || (file.type === 'application/pdf')) {
            const $img = $('<img>').attr('src', URL.createObjectURL(file));
            $thumbnail.append($img);
        } else {
            const $icon = $('<i>').addClass('fa-solid fa-file fa-custom-style');
            $thumbnail.append($icon);
        }
        $fileList.append($thumbnail);
    });
}

function updateThumbnailStyles() {
    $('.file-thumbnail-view').each(function () {
        const $this = $(this);
        if ($this.attr('id') === `${selectedFileId}`) {
            $this.css({
                'transform': 'scale(1.175)',
                'margin': '.75rem',
                'box-shadow': '0 0 10px var(--first-color)',
                'z-index': '1',
            });
            this.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        } else {
            $this.css({
                'transform': 'scale(1)',
                'box-shadow': 'none',
                'z-index': '0',
                'margin': '0',
            });
        }
    });
}

function updateWorkspaceMetaView() {
    const $metaView = $('#selected-files-view').empty();
    window.context_data[getCurrentWorkspaceId()].workspace_files.forEach((file, index) => {
        const $thumbnail = $('<div>').addClass('d-flex justify-content-between align-items-center file-thumbnail file-thumbnail-view');
        $thumbnail.attr('id', `${file.id}`);
        const $extension = $('<div>').addClass('file-extension').text(getFileExtension(file.type.toUpperCase()));
        if (file.type.match(/(jpg|jpeg|png|gif|pdf)$/i)) {
            const $img = $('<img>').attr('src', file.url);
            $thumbnail.append($img);
        } else {
            const $icon = $('<i>').addClass('fa-solid fa-file fa-custom-style');
            $thumbnail.append($icon);
        }
        $thumbnail.append($extension);
        $thumbnail.click(() => {
            if (file.type.match(/(pdf)$/i)) {
                const _ = $('#workspace-body-main').empty();
                renderPDF(file.url, 'workspace-body-main');
                selectedFileId = file.id;
                updateThumbnailStyles();
            }
        });
        $metaView.append($thumbnail);
    });
    if ($metaView.children().length > 0) {
        $metaView.css({
            'padding': '.25rem',
            'margin': 'auto'
        });
    }
}

$('#file-upload-button').click(function () {
    $('#file-upload-input').click();
});

$('#file-upload-input').change(handleFileSelect);
/*=========================================================*/

/*====================== Chat Submit ======================*/
$('#chatbot-submit').click(function (e) {
    chatSubmit(e);
});

$('#file-upload-input').change(handleFileSelect);

$('#chatbot-textarea').keypress(function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        chatSubmit(e);
    }
})

function generateChatbotBodyLoader(type = "bot") {
    const icon = '<i class="fa-solid fa-robot chatbot-profile-bot"></i>';
    var chatbotBodyLoader = `
        <div class="chatbot-body-text-${type} text-loader" id="section">
            <div>
                ${icon}
                <div class="chatbot-body-text">
                    <div class="d-flex chatbot-body-text-loader">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        </div>
        `
    return chatbotBodyLoader;
}

function generateChatbotBody(type = 'user') {
    const icon = type == 'user' ? '<i class="fa-solid fa-user chatbot-profile-user"></i>' : '<i class="fa-solid fa-robot chatbot-profile-bot"></i>';
    var chatbotBody = type == 'user' ? `
            <div class="chatbot-body-text-${type}" id="section">
                <div class="chatbot-body-text">
                    <p class="chatbot-body-text-p-${type}"></p>
                </div>
                ${icon}
            </div>
        ` :
        `
            <div class="chatbot-body-text-${type}" id="section">
                ${icon}
                <div class="chatbot-body-text">
                    <p class="chatbot-body-text-p-${type}"></p>
                </div>
            </div>
        `
    return chatbotBody;
}

function resetChatbotTextarea() {
    $("#chatbot-container-body").animate({ scrollTop: $('#chatbot-body').height() }, "slow");
    $('#chatbot-textarea').prop('disabled', false);
    $('#chatbot-textarea').focus();
}

function generateInitialChatbotBody(jsonObject) {
    if (jsonObject && jsonObject.length > 0) {
        $('#chatbot-body').empty();
        const botIcon = '<i class="fa-solid fa-robot chatbot-profile-bot"></i>';
        const userIcon = '<i class="fa-solid fa-user chatbot-profile-user"></i>';
        jsonObject.forEach((message, index) => {
            console.log(message.response);
            var chatbotBody = `
            <div class="chatbot-body-text-user" id="section">
                <div class="chatbot-body-text">
                    <p class="chatbot-body-text-p-user">${message.query}</p>
                </div>
                ${userIcon}
            </div>
            <div class="chatbot-body-text-bot" id="section">
                ${botIcon}
                <div class="chatbot-body-text">
                    <p class="chatbot-body-text-p-bot"></p>
                </div>
            </div>
        `
            $('#chatbot-body').append(chatbotBody);
            $('.chatbot-body-text-p-bot').last().append(message.response);
        });
        resetChatbotTextarea();
    }
    else {
        $('#chatbot-body').empty();
        resetChatbotTextarea();
    }
}

function chatSubmit(e, message = null) {
    e.preventDefault();
    const csrftoken = window.getCookie('csrftoken');
    if (message == null) {
        message = $('#chatbot-textarea').val();
    }
    if (message.trim() == '') {
        return false;
    }
    $('#chatbot-textarea').val('');
    $('#chatbot-textarea').prop('disabled', true);
    auto_grow(document.getElementById('chatbot-textarea'));
    $('#chatbot-body').append(generateChatbotBody());
    $('.chatbot-body-text-p-user').last().append(`<p>${message}<p>`);
    $('#chatbot-body').append(generateChatbotBodyLoader());
    $("#chatbot-container-body").animate({ scrollTop: $('#chatbot-body').height() }, "slow");
    const formData = new FormData();
    formData.append('chat_query', message);
    const currentWorkspaceId = getCurrentWorkspaceId();
    formData.append('workspace_id', currentWorkspaceId);
    selectedFiles.forEach((file, index) => {
        formData.append(`file${index}`, file);
    });
    $.ajax({
        type: "POST",
        url: window.location.origin + "/services/api/chat/",
        headers: { 'X-CSRFToken': csrftoken },
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.data.files) {
                response.data.files.forEach(file => {
                    if (!window.context_data[currentWorkspaceId].workspace_files.some(existingFile => existingFile.id === file.id)) {
                        window.context_data[currentWorkspaceId].workspace_files.push(file);
                    }
                });
            }
            if (window.context_data[currentWorkspaceId].workspace_chat) {
                window.context_data[currentWorkspaceId].workspace_chat.push({
                    query: message,
                    response: response.data.chat_response
                });
            }
            else {
                window.context_data[currentWorkspaceId].workspace_chat = [
                    {
                        query: message,
                        response: response.data.chat_response
                    }
                ];
            }
            setTimeout(function () {
                $('.text-loader').remove();
                $('#chatbot-body').append(generateChatbotBody(type = "bot"));
                $('.chatbot-body-text-p-bot').last().append(response.data.chat_response);
                resetChatbotTextarea();
                if (selectedFiles.length > 0) {
                    const lastFile = window.context_data[currentWorkspaceId].workspace_files[window.context_data[currentWorkspaceId].workspace_files.length - 1];
                    selectedFileId = lastFile.id;
                    updateWorkspaceMetaView();
                    thumbnailClick(lastFile);
                    updateThumbnailStyles();
                    clearFileSelection();
                }
                $('#td-files-' + currentWorkspaceId).text(window.context_data[currentWorkspaceId].workspace_files.length);
                $('#td-conversation-' + currentWorkspaceId).text(window.context_data[currentWorkspaceId].workspace_chat.length);
            }, 1000);
        },
        error: function (response) {
            const data = response.responseJSON;
            setTimeout(function () {
                $('.text-loader').remove();
                $('#chatbot-body').append(generateChatbotBody(type = "bot"));
                $('.chatbot-body-text-p-bot').last().append(`<p><i>${data.description}</i></p>`);
                resetChatbotTextarea()
            }, 1000);
        }
    });
}
/*=========================================================*/

/*==================== Utility Functions ====================*/
function getCurrentWorkspaceId() {
    const activeTab = $('#workspace-tab-content');
    const workspaceID = activeTab.children().attr('id');
    return workspaceID;
}

function initializeWorkspace(key = null) {
    if (key == null) {
        const firstKey = Object.keys(window.context_data)[0];
        openWorkspace(firstKey);
        openWorkspaceAccordion(firstKey);
    } else {
        openWorkspace(key);
        openWorkspaceAccordion(key);
    }
}

function convertToLocalDateTime(date) {
    const rawDate = new Date(date);
    const parts = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(rawDate);
    const func = parts.reduce((acc, part) => {
        acc[part.type] = part.value;
        return acc;
    }, {});
    return `${func.day} ${func.month} ${func.year} ${func.hour}:${func.minute}`;
}

function openWorkspaceAccordion(workspaceID) {
    $('.accordion-collapse').removeClass('show');
    $('.accordion-button').addClass('collapsed').attr('aria-expanded', 'false');
    const newAccordionId = `offcanvas-workspace-${workspaceID}`;
    $(`#${newAccordionId}`).addClass('show');
    $(`#heading-${workspaceID} .accordion-button`)
        .removeClass('collapsed')
        .attr('aria-expanded', 'true');
    document.getElementById(`heading-${workspaceID}`).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

function removeOffcanvasWorkspaceAccordion(workspaceID) {
    $(`#heading-${workspaceID}`).parent().remove();
}

function updateOffcanvasWorkspace(workspaceID) {
    const workspace = window.context_data[workspaceID];
    const title = workspace.workspace_name ? workspace.workspace_name : workspaceID;
    const createdAt = convertToLocalDateTime(workspace.workspace_created_at);
    const updatedAt = convertToLocalDateTime(workspace.workspace_updated_at);
    $('#accordian-workspace').append(`
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading-${workspace.workspace}">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#offcanvas-workspace-${workspace.workspace}" aria-expanded="false"
                aria-controls="offcanvas-workspace-${workspace.workspace}">
                <span class="workspace-accordion-title">
                    Workspace ${$('#accordian-workspace').children().length + 1} - ${title}
                </span>
            </button>
        </h2>
        <div id="offcanvas-workspace-${workspace.workspace}" class="accordion-collapse collapse"
            aria-labelledby="heading-${workspace.workspace}" data-bs-parent="#accordian-workspace">
            <div class="accordion-body">
                <strong>Workspace meta data</strong>
                <hr class="mt-0">
                <div class="d-flex justify-content-center align-items-center">
                    <table class="table workspace-accordion-table">
                        <thead>
                            <tr>
                                <th scope="col">Item</th>
                                <th scope="col">Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>ID</td>
                                <td><code id=td-id-${workspace.workspace}>${workspace.workspace}</code></td>
                            </tr>
                            <tr>
                                <td>Total Conversation</td>
                                <td><code id=td-conversation-${workspace.workspace}>${workspace.conversation ? workspace.conversation.length : 0}</code></td>
                            </tr>
                            <tr>
                                <td>Total Files</td>
                                <td><code id=td-files-${workspace.workspace}>${workspace.files ? workspace.files.length : 0}</code></td>
                            </tr>
                            <tr>
                                <td>Updated At</td>
                                <td><code id=td-updated-at-${workspace.workspace}>${updatedAt}</code></td>
                            </tr>
                            <tr>
                                <td>Created At</td>
                                <td><code id=td-created-at-${workspace.workspace}>${createdAt}</code></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="d-flex justify-content-around align-items-center">
                    <a class="btn btn-primary" onclick="openWorkspace('${workspace.workspace}')">Open</a>
                    <a class="btn btn-danger" onclick="deleteWorkspace('${workspace.workspace}')">Delete</a>
                </div>
            </div>
        </div>
    </div>
    `)
}
/*=========================================================*/
