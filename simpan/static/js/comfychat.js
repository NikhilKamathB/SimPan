/*==================== Variables ====================*/
let selectedFiles = [];
/*=========================================================*/

/*==================== Intialize tooltip ====================*/
$(document).ready(function () {
    $('[data-toggle="workspace-tooltip"]').tooltip();
});
/*=========================================================*/

/*==================== Add new workspace ====================*/
$('#workspace-add').click(function () {
    const oldTabCount = $('.workspace-tab').children().length;
    const newTabCount = oldTabCount + 1;
    const workspaceTab = `
        <li class="nav-item">
            <a class="nav-link" id="workspace-${newTabCount}-tab" type="button" data-bs-toggle="tab" data-bs-target="#workspace-${newTabCount}" aria-controls="workspace-${newTabCount}">Workspace ${newTabCount}</a>
        </li>
    `;
    const workspaceTabContent = `
        <div class="tab-pane fade workspace-tab-pane" id="workspace-${newTabCount}" aria-labelledby="workspace-${newTabCount}-tab">
            <div class="container">
                <p>You are in workspace ${newTabCount}</p>
            </div>
            <a class="workspace-delete" type="button">
                <i class="uil uil-trash-alt fa-custom-style fa-workspace" id="fa-trash-alt"></i>
            </a>
        </div>
    `;
    $('#workspace-tab').append(workspaceTab);
    $('#workspace-tab-content').append(workspaceTabContent);
    $(`#workspace-${newTabCount}-tab`).tab('show');
    document.getElementById(`workspace-${newTabCount}-tab`).scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
});
/*=========================================================*/

/*==================== Delete workspace ====================*/
$(document).on('click', '.workspace-delete', function () {
    const parent = $(this).parent();
    const parentID = parent.attr('id');
    parent.remove();
    $(`[data-bs-target="#${parentID}"]`).parent().remove();
    const lastTab = $('#workspace-tab .nav-link').last();
    if (lastTab.length) {
        lastTab.tab('show');
        lastTab[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
});
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

function updateFileList(id='#selected-files', showRemove = true) {
    const $fileList = $(id).empty();
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

function updateWorkspaceMetaView() {
    const $metaView = $('#selected-files-view').empty();
    window.workspaceFiles.forEach((file, index) => {
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
            }
        });
        $metaView.append($thumbnail);
    });
}

function clearFileSelection() {
    selectedFiles = [];
    $('#file-upload-input').val('');
    updateFileList();
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
                    <div class="chatbot-body-text-loader">
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

function getCurrentWorkspaceId() {
    const activeTab = $('#workspace-tab .nav-link.active');
    if (activeTab.length) {
        const tabId = activeTab.attr('id');
        return tabId;
    }
    return null;
}

function chatSubmit(e) {
    e.preventDefault();
    const csrftoken = window.getCookie('csrftoken');
    var message = $('#chatbot-textarea').val();
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
                    window.workspaceFiles.push(file);
                });
            }
            setTimeout(function () {
                $('.text-loader').remove();
                $('#chatbot-body').append(generateChatbotBody(type = "bot"));
                $('.chatbot-body-text-p-bot').last().append(response.data.chatResponse);
                resetChatbotTextarea();
                clearFileSelection();
                updateWorkspaceMetaView();
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