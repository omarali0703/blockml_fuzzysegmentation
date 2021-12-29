window.onload = init();

function init() {

}

function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
        return;
    }
    var reader = new FileReader();
    reader.onload = function (e) {
        var contents = e.target.result;
        var parentElement = e.target.parentElement;
        generateSegmentationVisualisation(parentElement, contents);
    };
    reader.readAsText(file);
}

function displayContents(contents) {
    var element = document.getElementById('file-content');
    element.textContent = contents;
}

document.getElementById('file-input')
    .addEventListener('change', readSingleFile, false);

function generateSegmentationVisualisation(parentElement, fileData) {
    let canvas = document.createElement('canvas');
    
    parentElement.appendChild(canvas);
}

generateSegmentationVisualisation(document.querySelector('.segmentation-container'), '00000100010101101000010101010100000000011000100000000011')
