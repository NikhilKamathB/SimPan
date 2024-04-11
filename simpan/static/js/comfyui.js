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
    var canvas = document.getElementById('ui-canvas');

    var graph = new LGraph();
    var canvas = new LGraphCanvas("#ui-canvas", graph);
    graph.start();
}

initCanvas(); // Initial call
/*=========================================================*/

/*======================= Add Node ========================*/
// class MultiplyNode extends LGraphNode {

//     constructor() {
//         super();
//         this.addInput("A", "number");
//         this.addInput("B", "number");
//         this.addOutput("A*B", "number");
//     }

//     onExecute() {
//         var A = this.getInputData(0);
//         var B = this.getInputData(1);
//         if (A != null && B != null) {
//             this.setOutputData(0, A * B);
//         } else {
//             this.setOutputData(0, null);
//         }
//     }
// }

// LiteGraph.registerNodeType("3D Vision/multiply", MultiplyNode);
/*=========================================================*/