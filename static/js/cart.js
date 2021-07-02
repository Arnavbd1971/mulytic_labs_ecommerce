var updateBtns = document.getElementsByClassName('update-cart')

// define every click in cart page 
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var stockQuantity = this.dataset.stock
		var action = this.dataset.action
		console.log('productId:', productId, 'stockQuantity:', stockQuantity, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, stockQuantity, action)
		}else{
			updateUserOrder(productId, stockQuantity, action)
		}
	})
}

// if User is authenticated updateUserOrder will work 
function updateUserOrder(productId, stockQuantity, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'stockQuantity':stockQuantity, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

// if User is not authenticated addCookieItem will work 
function addCookieItem(productId, stockQuantity, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}else{
			// cart[productId]['quantity'] += 1
			console.log(stockQuantity)
			if (cart[productId]['quantity'] < stockQuantity){
				cart[productId]['quantity'] += 1
			}else{
				alert("Sorry Not enough stock available of this product!")
			}
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}