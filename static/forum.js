function getchatid() {
  var div = document.getElementById("chatinfodiv37")
  return div.innerText
}

function reloadchat() {
  var xhr = new XMLHttpRequest()
  xhr.open("POST", "/getchat" + getchatid(), false)
  var div = document.getElementById("chatdiv37")

xhr.onload = function() {
        console.log(`Загружено: ${xhr.status} ${xhr.response}`);
        var cont = JSON.parse(xhr.response)
        var div_data = cont["data"]
        div.innerHTML = div_data
    };
    
xhr.onerror = function() { // происходит, только когда запрос совсем не получилось выполнить
    console.log(`Ошибка соединения. Status: ${xhr.status}`);
    };
    
    xhr.onprogress = function(event) { // запускается периодически
        // event.loaded - количество загруженных байт
        // event.lengthComputable = равно true, если сервер присылает заголовок Content-Length
        // event.total - количество байт всего (только если lengthComputable равно true)
        console.log(`Загружено ${event.loaded} из ${event.total}`);
    };

    xhr.send(JSON.stringify({}))

}