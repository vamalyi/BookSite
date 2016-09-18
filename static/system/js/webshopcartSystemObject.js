// system static object
function SystemObject(){};

SystemObject.prototype.setCookies = function(object, data){
	object.put('productsInCart', JSON.stringify(data), {
		path: '/'
	});
};

SystemObject.prototype.getCookies = function(object){
	var cookies = object.get('productsInCart');
	return (cookies === undefined) ? false : JSON.parse(cookies);
};

SystemObject.prototype.productSetCart = function(data, cart){

	if (cart === null){
		return false;
	}

	var products = (cart.products == undefined)?[]:cart.products;
	var product_ids = (cart.product_ids == undefined)?[]:cart.product_ids;
	var corrector_ids = (cart.corrector_ids == undefined)?[]:cart.corrector_ids;

	if (!(product_ids.indexOf(data.id.toString()) >= 0)) {
		var new_price_correctors = [];
		if (data.corrector_id > 0) {
			new_price_correctors.push({
				id: data.corrector_id,
				data: {
					price: data.price,
					count: data.count
				}
			});
			products.push({
				id: data.id,
				data: {
					price_correctors: new_price_correctors
				}
			});
			corrector_ids.push(data.corrector_id.toString());
		}else{
			products.push({
				id: data.id,
				data: {
					price_correctors: new_price_correctors,
					price: data.price,
					count: data.count
				}
			});
		}
		product_ids.push(data.id.toString());
	}else{
		var new_price_correctors = [];
		if (data.corrector_id > 0){
			if (!(corrector_ids.indexOf(data.corrector_id.toString()) >= 0)){
				new_price_correctors = {
					id: data.corrector_id,
					data: {
						price: data.price,
						count: data.count
					}
				};
				for (var i=0; i<products.length; i++){
					if (data.id == products[i].id){
						products[i].data.price_correctors.push(new_price_correctors);
					}
				}
				corrector_ids.push(data.corrector_id.toString());
			}else{
				for (var i=0; i<products.length; i++){
					if (data.id == products[i].id){
						for (var j=0; j<products[i].data.price_correctors.length; j++){
							if (data.corrector_id == products[i].data.price_correctors[j].id){
								if (data.count == products[i].data.price_correctors[j].data.count){
									products[i].data.price_correctors[j].data.count++;
								}else{
									products[i].data.price_correctors[j].data.count = count;
								}
								products[i].data.price_correctors[j].data.price = data.price;
							}
						}
					}
				}
			}
		}else{
			for (var i=0; i<products.length; i++){
				if (data.id == products[i].id){
					products[i].data.price_correctors = new_price_correctors;
					if (data.count == products[i].data.count){
						products[i].data.count = (1 * products[i].data.count) + 1;
					}else{
						products[i].data.count = data.count;
					}
					products[i].data.price = data.price;
				}
			}
		}
	}

	var clientCart = {};
	clientCart.products = products;
	clientCart.product_ids = product_ids;
	clientCart.corrector_ids = corrector_ids;

	return clientCart;
};

SystemObject.prototype.productSetCount = function(data, cart){
	var products = (cart.products == undefined)?[]:cart.products;
	var product_ids = (cart.product_ids == undefined)?[]:cart.product_ids;
	var corrector_ids = (cart.corrector_ids == undefined)?[]:cart.corrector_ids;

	if (product_ids.indexOf(data.id.toString()) >= 0) {
		if (data.corrector_id > 0){
			if (corrector_ids.indexOf(data.corrector_id.toString() >= 0)){
				for (var i=0; i<products.length; i++){
					if (data.id == products[i].id){
						for (var j=0; j<products[i].data.price_correctors.length; j++){
							if (data.corrector_id == products[i].data.price_correctors[j].id){
								products[i].data.price_correctors[j].data.count = data.count;
							}
						}
					}
				}
			}
		}else{
			for (var i=0; i<products.length; i++){
				if (data.id == products[i].id){
					products[i].data.count = data.count;
				}
			}
		}
	}

	var clientCart = {};
	clientCart.products = products;
	clientCart.product_ids = product_ids;
	clientCart.corrector_ids = corrector_ids;

	return clientCart;
};

SystemObject.prototype.productGetCount = function(product_id, corrector_id, cart){
	var products = cart.products;
	var count = 1;

	for (var i=0; i<products.length; i++){
		if (product_id == products[i].id){
			if (corrector_id === false){
				count = products[i].data.count;
			}else{
				for (var j=0; j<products[i].data.price_correctors.length; j++){
					if (corrector_id == products[i].data.price_correctors[j].id){
						count = products[i].data.price_correctors[j].data.count;
					}
				}
			}
		}
	}
	return count;
};

SystemObject.prototype.productGetTotalCount = function(cart){
	var totalCount = 0;
	for (var i=0; i<cart.products.length; i++){
		if (cart.products[i].data.price_correctors.length > 0){
			for (var j=0; j<cart.products[i].data.price_correctors.length; j++){
				totalCount += cart.products[i].data.price_correctors[j].data.count;
			}
		}else{
			totalCount += cart.products[i].data.count;
		}
	}
	return totalCount;
};

SystemObject.prototype.productGetTotalPrice = function(cart){
	var totalPrice = 0;
	for (var i=0; i<cart.products.length; i++){
		if (cart.products[i].data.price_correctors.length > 0){
			for (var j=0; j<cart.products[i].data.price_correctors.length; j++){
				totalPrice += (cart.products[i].data.price_correctors[j].data.count * cart.products[i].data.price_correctors[j].data.price);
			}
		}else{
			totalPrice += (cart.products[i].data.count * cart.products[i].data.price);
		}
	}
	return totalPrice;
};

SystemObject.prototype.productDelete = function(data, cart){
	var products = (cart.products == undefined)?[]:cart.products;
	var product_ids = (cart.product_ids == undefined)?[]:cart.product_ids;
	var corrector_ids = (cart.corrector_ids == undefined)?[]:cart.corrector_ids;

	if (product_ids.indexOf(data.id.toString()) >= 0) {
        product_ids.splice( product_ids.indexOf(data.id.toString()), 1 );
		if (data.corrector_id > 0){
			if (corrector_ids.indexOf(data.corrector_id.toString()) >= 0){
                corrector_ids.splice( corrector_ids.indexOf(data.corrector_id.toString()), 1 );
				for (var i=0; i<products.length; i++){
					if (data.id == products[i].id){
						for (var j=0; j<products[i].data.price_correctors.length; j++){
							if (data.corrector_id == products[i].data.price_correctors[j].id){
                                products[i].data.price_correctors.splice(j, 1);
							}
						}
					}
				}
			}
		}else{
			for (var i=0; i<products.length; i++){
				if (data.id == products[i].id){
                    products.splice(i, 1);
				}
			}
		}
	}

	var clientCart = {};
	clientCart.products = products;
	clientCart.product_ids = product_ids;
	clientCart.corrector_ids = corrector_ids;

	return clientCart;
};

SystemObject.prototype.clearCart = function(object){
	object.remove('productsInCart', {
		path: '/'
	});
};