(function() {
    if (document.readyState === 'loading') {
    document.addEventListener("DOMContentLoaded", function() {
        run();
    });
    } else {
        run();
    }
    function run() {
        var but = document.getElementById('js-get_controller_status');
        but.onclick = function () {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'http://localhost:8080/api/controller/status');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    var json_data = JSON.parse(xhr.responseText);
                    document.getElementById('js-display').innerText = 'Status: ' + json_data.status;
                }
            };
            xhr.send();
        };
    }
}());