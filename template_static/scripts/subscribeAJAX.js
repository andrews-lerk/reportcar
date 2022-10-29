function subscribe(typename) {

    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
    }

    let body = {
    'typename': typename,
    }

    return fetch(URL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {

    if (response.ok) {
        return response.json().then(data => {
            window.location.href = data.url
        })
       }
    })
}