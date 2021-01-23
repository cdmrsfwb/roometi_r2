var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser'){
            updateCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateCookieItem(productId, action) {
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = 0
        }
        cart[productId] += 1
    } else if (action == 'remove') {
        cart[productId] -= 1
        if (cart[productId] < 1) {
            delete cart[productId];
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(productId, action) {
    console.log('Updating user order')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
}
