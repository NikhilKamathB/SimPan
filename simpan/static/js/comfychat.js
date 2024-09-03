/*==================== Enable Auto-grow ====================*/
function auto_grow(element) {
    element.style.height = "25px";
    element.style.height = (element.scrollHeight) + "px";
}
/*=========================================================*/

/*====================== Chat Submit ======================*/

// Chat submit
$('#chatbot-submit').click(function (e) {
    chatSubmit(e);
})

// Chat enter submit
$('#chatbot-textarea').keypress(function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        chatSubmit(e);
    }
})

// Chatbot body helper - loader
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

// Chatbot body helper - chatbot
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

// Reset chatbot textarea
function resetChatbotTextarea() {
    $("#chatbot-container-body").animate({ scrollTop: $('#chatbot-body').height() }, "slow");
    $('#chatbot-textarea').prop('disabled', false);
    $('#chatbot-textarea').focus();
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
    $.ajax({
        type: "POST",
        url: window.location.origin + "/comfychat/chat/",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            "chat-query": message
        },
        success: function (response) {
            setTimeout(function () {
                $('.text-loader').remove();
                $('#chatbot-body').append(generateChatbotBody(type = "bot"));
                $('.chatbot-body-text-p-bot').last().append(response.description);
                resetChatbotTextarea()
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