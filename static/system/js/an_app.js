// init module webshopcart
var an_app = angular.module('an_app', ['ngCookies']);

// init staticObject custom object
an_app.staticObject = new SystemObject();

// set config default
an_app.config(function($interpolateProvider, $cookiesProvider) {
	$interpolateProvider.startSymbol('!{');
	$interpolateProvider.endSymbol('}!');
	$cookiesProvider.defaults = {
		path: '/',
	};
});

// registration controllers

an_app.controller('GetProductsInCartController', function($scope, $http, $cookies, $rootScope){

	$rootScope.totalCount = 0;
	$rootScope.totalPrice = 0;
	$rootScope.cartVisible = false;

    var getCart = an_app.staticObject.getCookies($cookies);
	var response = $http.get('/cart/api/');

	response.success(function(data, status, headers, config) {
		var products = data.products;

		if (products.length > 0) {
			$rootScope.totalCount = an_app.staticObject.productGetTotalCount(getCart);
			$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(getCart);
			$rootScope.cartVisible = true;
		}

		$scope.products = products;
	});

	response.error(function(data, status, headers, config) {
		console.log('ERROR: AJAX failed!');
		console.log(status);
	});
});

an_app.controller('ActionCartController', function($scope, $cookies, $rootScope){

	$scope.getCart = an_app.staticObject.getCookies($cookies);
	$scope.count = 1;
	$scope.productInCart = false;

	$scope.productAddToCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var getCart = an_app.staticObject.getCookies($cookies);
			var json = an_app.staticObject.productSetCart(
				{id: id, corrector_id: corrector_id, price: price, count: count},
				getCart
			);

			an_app.staticObject.setCookies($cookies, json);

			$scope.count = count;
			$scope.productInCart = true;
			$rootScope.totalCount = an_app.staticObject.productGetTotalCount(json);
			$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(json);
		}
	};

	$scope.productIncCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var new_count = (1 * count) + 1;
			$scope.count = new_count;
			var getCart = an_app.staticObject.getCookies($cookies);
			var json = an_app.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			an_app.staticObject.setCookies($cookies, json);
			$rootScope.totalCount = an_app.staticObject.productGetTotalCount(json);
			$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(json);
		}
	};

	$scope.productDecCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 1){
			var new_count = (1 * count) - 1;
			$scope.count = new_count;
			var getCart = an_app.staticObject.getCookies($cookies);
			var json = an_app.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			an_app.staticObject.setCookies($cookies, json);
			$rootScope.totalCount = an_app.staticObject.productGetTotalCount(json);
			$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(json);
		}
	};

	$scope.productChangeCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var getCart = an_app.staticObject.getCookies($cookies);
			var json = an_app.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: count},
				getCart
			);
			an_app.staticObject.setCookies($cookies, json);
			$rootScope.totalCount = an_app.staticObject.productGetTotalCount(json);
			$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(json);
		}
	};

	$scope.productDeleteInCart = function(id, corrector_id, price){
		var getCart = an_app.staticObject.getCookies($cookies);
		var json = an_app.staticObject.productDelete(
			{id: id, corrector_id: corrector_id, price: price},
			getCart
		);
		an_app.staticObject.setCookies($cookies, json);
		var id_block = '_' + id.toString() + '_' + corrector_id.toString();
		angular.element(document.getElementById(id_block)).remove();
		$rootScope.totalCount = an_app.staticObject.productGetTotalCount(json);
		$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(json);
		if (json['products'].length <= 0){
			$rootScope.cartVisible = false;
		}
	};

	$scope.clearCart = function(){
		var getCart = an_app.staticObject.getCookies($cookies);
		if (getCart){
			an_app.staticObject.clearCart($cookies);
		}
	};

	$scope.initButtonCart = function(product_id, corrector_id){
		var getCart = $scope.getCart;
		if (getCart){
			if (
				((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (getCart.corrector_ids.indexOf(corrector_id.toString()) >= 0)) ||
				((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (corrector_id === false))
			){
				$scope.count = an_app.staticObject.productGetCount(product_id, corrector_id, getCart);
				$scope.productInCart = true;
			}
		}
	};

	$scope.initProductCount = function(product_id, corrector_id){
		var getCart = an_app.staticObject.getCookies($cookies);
		if (getCart){
			if ((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (getCart.corrector_ids.indexOf(corrector_id.toString()) >= 0)){
				$scope.count = an_app.staticObject.productGetCount(product_id, corrector_id, getCart);
			}
			if ((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (corrector_id === '')){
				$scope.count = an_app.staticObject.productGetCount(product_id, false, getCart);
			}
		}
	};
});

an_app.controller('CartPreviewController', function($scope, $cookies, $rootScope){
	var getCart = an_app.staticObject.getCookies($cookies);
	$rootScope.cartVisible = false;
	if (getCart){
		$rootScope.totalCount = an_app.staticObject.productGetTotalCount(getCart);
		$rootScope.totalPrice = an_app.staticObject.productGetTotalPrice(getCart);
		$rootScope.cartVisible = true;
	}
});

an_app.controller('CartSendController', function($scope, $cookies, $rootScope){
	$scope.submit = function(){
		var getCart = an_app.staticObject.getCookies($cookies);
		if (getCart){
			formCartSend.totalPrice.value = $rootScope.totalPrice;
			formCartSend.submit();
		}
	};
});

an_app.controller('LanguageChangeController', function($scope, $http){
	$scope.change = function(ln){
		var response = $http.get('/api/set_language/' + ln);
		response.success(function(data, status, headers, config) {
			window.location.href = window.location.href;
		});
		response.error(function(data, status, headers, config) {
			console.log('ERROR: AJAX failed!');
			console.log(status);
		});
	};
});

an_app.controller('FilteredProductsController', function($scope){

	$scope.urlAction = '';
	$scope.getQuery = '';
	$scope.setOrderItem = '';

	$scope.initialize = function(urlAction, setOrderItem, getQuery){
		$scope.urlAction = urlAction;
		$scope.setOrderItem = setOrderItem;
		$scope.getQuery = getQuery;
	};

	$scope.sorted = function(){
		var url = $scope.urlAction;
		if ($scope.setOrderItem != ''){
			url += 'sort_' + $scope.setOrderItem + '/';
		}
		if ($scope.getQuery != ''){
			url += '?' + $scope.getQuery;
		}
		window.location.href = url;
	};
});
