import * as Node from './node.js';

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