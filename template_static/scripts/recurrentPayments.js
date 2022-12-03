function recurrentPayHandler (type, csrf_token, forloop) {
//    var loader = document.querySelector('#loader'+forloop)
//    var button = document.querySelector('#choice'+forloop)
//    loader.setAttribute('style','display: block;')
//    button.setAttribute('style','display: none;')
    var check1 = document.querySelector('#flexCheckDefault1')
    var check2 = document.querySelector('#flexCheckDefault2')
    var check3 = document.querySelector('#flexCheckDefault3')
    if (!check1.checked || !check2.checked || !check3.checked) {
        var agree = document.querySelector('#agree_')
        agree.setAttribute('style','')
        return
    }
    const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token
    }

    let body = {
    'type': type,
    }

    return fetch(pricingURL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers
    }).then(response => {
        if (response.ok){
            return response.json().then(data => {
                if (data.subscribe) {
                    var warning = document.querySelector('#subscribe-error')
                    warning.setAttribute('style','')
                    loader.setAttribute('style','display: none;')
                    button.setAttribute('style','')
                    return
                }
                recurrentPay(data.type, data.startPrice, data.user, csrf_token, data.invoiceId, forloop)
            })
        } else {
            loader.setAttribute('style','display: none;')
            button.setAttribute('style','')
            return
        }
    })
}


function recurrentPay (type, startPrice, user, csrf_token, invoiceId, forloop) {
    var modal = document.querySelector('#centered')
    modal.setAttribute('style','display: none;')
    var widget = new cp.CloudPayments();
    widget.pay('charge',
    {
            publicId: 'pk_a1a62cc783c60a4c94626630db58f',
            description: `Оплата подписки на тариф ${type} для ${user}`,
            amount: startPrice,
            currency: 'RUB',
            invoiceId: invoiceId,
            accountId: user,
            email: user,
            skin: "modern",
            data: {
                type: type,
                user: user,
            }
        },
        {
           onSuccess: function (options) {
                document.location.href=redirectURL
            },

           onFail: function (reason, options) {
                document.location.href=pricingURL
                var loader = document.querySelector('#loader'+forloop)
                var button = document.querySelector('#choice'+forloop)
                loader.setAttribute('style','display: none;')
                button.setAttribute('style','')
            },

           onComplete: function (paymentResult, options) {
                const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
                }

                let body = {
                'results': paymentResult,
                'options': options
                }

                return fetch(recurrentCallbackURL, {
                method: "POST",
                body: JSON.stringify(body),
                headers: headers
                }).then(response => {return})
            }
        }
    )
};