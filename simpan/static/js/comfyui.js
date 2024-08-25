import * as Node from './node.js';
import { getCookie } from "./utils.js";

var canvas = document.getElementById('ui-canvas');

/*==================== Resize Canvas ====================*/
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas, false);
resizeCanvas(); // Initial call
/*=========================================================*/

/*==================== Initalize Canvas ====================*/
function initCanvas() {
    var graph = new LGraph();
    var canvas = new LGraphCanvas("#ui-canvas", graph);
}

initCanvas(); // Initial call
Node.executePreCommits();
/*=========================================================*/

/*==================== Trigger LLM ====================*/
$('#chatbot-submit-message').click(function (e) {
    console.log('submit');
    chatSubmitMessage(e);
});

function chatSubmitMessage(e) {
    e.preventDefault();
    const csrftoken = getCookie('csrftoken');
    var message = $('#prompt').val();
    if (message.trim() == '') {
        return false;
    }
    $.ajax({
        type: "POST",
        url: window.location.origin + "/comfyui/chat/",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            "chat-query": message
        },
        success: function (response) {
            console.log(response);

        },
        error: function (response) {
            console.log(response);
        }
    });
}