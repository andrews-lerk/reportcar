function pay (type, number, user, invoice_id, csrf_token, price) {
 var widget = new cp.CloudPayments();
    widget.pay('charge',
        {
            publicId: 'pk_a1a62cc783c60a4c94626630db58f',
            description: `Оплата полного отчета для ${user}`,
            amount: price,
            currency: 'RUB',
            accountId: user,
            invoiceId: invoice_id,
            email: user,
            skin: "modern",
            data: {
                type: type,
                number: number,
                user: user
            }
        },
        {
           onSuccess: function (options) {
                document.location.href=redirectURL
            },
           onFail: function (reason, options) {
                document.location.href=redirectURLfail
            },

            onComplete: function (paymentResult, options) {
                const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
                }

                let body = {
                'invoice_id': options.invoiceId,
                'user': options.accountId,
                'type': options.data.type,
                'number': options.data.number,
                'results': paymentResult
                }

                return fetch(callbackURL, {
                method: "POST",
                body: JSON.stringify(body),
                headers: headers
                }).then(response => {return})
            }
        }
    )
};
