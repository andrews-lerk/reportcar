function sendRequest() {

    let button = document.querySelector('#submit-button')
    button.style = "display: none;"
    let buttonReload = document.querySelector('#reload-code')
    buttonReload.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')

    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value
    form.email.setAttribute('readonly', true)
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

        buttonReload.style = ""
        button.style = ""
        button.setAttribute('onclick','auth()')
        button.setAttribute('type','button')
        button.innerHTML = '<span>Войти</span>'

        document.querySelector('#loader').style = ""
        document.querySelector('#password-label').hidden = false
        document.querySelector('#password').hidden = false

        return
       }
    })
}

function sendPayRequest() {

    let button = document.querySelector('#submit-button')
    button.style = "display: none;"
    let buttonReload = document.querySelector('#reload-code')
    buttonReload.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')

    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value
    form.email.setAttribute('readonly', true)
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

        buttonReload.style = ""
        button.style = ""
        button.setAttribute('onclick','payauth(99)')
        button.setAttribute('type','button')
        button.innerHTML = '<span>Перейти к оплате</span>'

        document.querySelector('#loader').style = ""
        document.querySelector('#password-label').hidden = false
        document.querySelector('#password').hidden = false

        return
       }
    })
}

function auth() {

    let button = document.querySelector('#submit-button')
    button.style = "display: none;"
    let buttonReload = document.querySelector('#reload-code')
    buttonReload.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')

    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value
    let pass = form.password.value

    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

    let body = {
    'email': email,
    'pass' : pass
    }

    return fetch(authURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {

    if (response.ok) {
        document.location.href=redirectURL
       } else {
       buttonReload.style = ""
       button.style = ""
       document.querySelector('#loader').style = "display: none;"
       document.querySelector('#warning_').style = ""
       }
    })
}

function payauth (price) {

    let button = document.querySelector('#submit-button')
    button.style = "display: none;"
    let buttonReload = document.querySelector('#reload-code')
    buttonReload.style = "display: none;"
    document.querySelector('#loader').style = "display: block;"

    let form = document.querySelector('#login-form')

    let token = form.csrfmiddlewaretoken.value
    let email = form.email.value
    let pass = form.password.value

    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

    let body = {
    'email': email,
    'pass' : pass,
    'type' : type,
    'number' : number
    }

    return fetch(authURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {

    if (response.ok) {
        return response.json().then(data => {
        pay(type, number, data.user, data.invoice_id, token, price)
        })
       } else {
       buttonReload.style = ""
       button.style = ""
       document.querySelector('#loader').style = "display: none;"
       document.querySelector('#warning_').style = ""
       }
    })
}