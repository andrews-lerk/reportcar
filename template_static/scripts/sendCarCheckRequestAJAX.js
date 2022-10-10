let form = document.querySelector('#login-form')

let token = form.csrfmiddlewaretoken.value
const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

let body = {
    'type': type,
    'number': number
}

fetch(carURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
}).then(response => {

    if (response.ok) {
        return response.json().then(data => {
            if (data.car){
                document.querySelector('#title').innerHTML = "Купить полный отчет"
                document.querySelector('#list-info').innerHTML  = `<li style="color: black;">Модель: <mark>${data.model}</mark></li>
                                                                  <li style="color: black;">Цвет: <mark>${data.color}</mark></li>
                                                                  <li style="color: black;">Год: <mark>${data.year}</mark></li>
                                                                  <p></p>`
                document.querySelector('#loading').style = "display: none;"
                if (isUser == 'False'){
                    document.querySelector('#login-form').style = ""
                } else {
                    document.querySelector('#pay-form').style = ""
                }
            } else {
                document.querySelector('#title').innerHTML = "Ошибка запроса"
                document.querySelector('#list-info').innerHTML  = `<li style="color: red;">Ответ от сервиса: <mark>${data.message}</mark></li>`
                document.querySelector('#loading').style = "display: none;"
                document.querySelector('#on-main').style = ""
            }
        })
    }
})
