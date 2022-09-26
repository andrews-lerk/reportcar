function sendRequest() {

    let button = document.querySelector('#submit-button')
    button.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')

    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value

    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

    let body = {
    'email': email
    }

    return fetch(requestURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {

    if (response.ok) {

        button.style = ""
        button.onclick = ""
        button.type = "submit"
        button.innerHTML = '<span>Войти</span>'

        document.querySelector('#loader').style = ""
        document.querySelector('#password-label').hidden = false
        document.querySelector('#password').hidden = false

        return
    }
    })
    }

function sendForRestrictRequest() {

    let button = document.querySelector('#submit-button')
    let mbutton = document.querySelector('#m-button')
    button.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')


    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value

    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

    let body = {
    'email': email
    }

    return fetch(requestURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {

    if (response.ok) {

        button.style = "display: none"
        mbutton.style = ""
        button.innerHTML = '<span>Перейти к оплате</span>'

        document.querySelector('#loader').style = ""
        document.querySelector('#password-label').hidden = false
        document.querySelector('#password').hidden = false

        return
    }
    })
    }