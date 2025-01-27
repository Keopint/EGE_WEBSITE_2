function getchatid() {
  var div = document.getElementById("chatinfodiv37")
  return div.innerText
}

function send_message() {
  var inp = document.getElementById("send_message_input")

  var xhr = new XMLHttpRequest()
  xhr.open("POST", "/api/forum/" + getchatid(), false)
  xhr.setRequestHeader("Content-Type", "application/json");
  var div = document.getElementById("chatdiv37")

xhr.onload = function() {
        console.log(`Загружено: ${xhr.status} ${xhr.response}`);
        var cont = JSON.parse(xhr.response)
        console.log(cont)
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

    xhr.send(JSON.stringify({"text": inp.value}))
    inp.value = "";

}