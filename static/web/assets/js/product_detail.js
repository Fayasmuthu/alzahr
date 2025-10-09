
$(document).ready(function () {
  // Function to update prices and offer percent for a specific card
  function updatePricesAndOffer(card) {
    var selectedRadio = card.find('input[name="product_size"]:checked');
    if (selectedRadio.length > 0) {
      var salePrice = selectedRadio.data('sale_price');
      var originalPrice = selectedRadio.data('original_price');
      var offerPercent = parseFloat(selectedRadio.data('offer_percent')).toFixed(2); 
      
      card.find('.sale_price').text('₹' + salePrice);
      card.find('.original_price').text('₹' + originalPrice);
      card.find('.offer_percent').text(offerPercent + '% OFF');

    }
  }

  // Event listener for radio button click within each card
  $('input[name="product_size"]').off('click').on('click', function () {
    var card = $(this).closest('.cart-div');
    updatePricesAndOffer(card);
  });
  $(".input-group").on("click", ".button-plus", function (event) {
    event.preventDefault();
    handleQuantityChange(1);
});

$(".input-group").on("click", ".button-minus", function (event) {
    event.preventDefault();
    handleQuantityChange(-1);
});

function handleQuantityChange(change) {
    var inputField = $(".input-group .quantity-field");
    var currentQuantity = parseInt(inputField.val(), 10);
    
    // Increment or decrement the quantity
    var newQuantity = currentQuantity + change;

    // Ensure the new quantity is positive
    newQuantity = Math.max(0, newQuantity);

    // Update the input field with the new quantity
    inputField.val(newQuantity);

    // Enable or disable the "Add to Cart" button based on the new quantity
    var addToCartButton = $("#cart-add-btn");
    addToCartButton.prop("disabled", newQuantity === 0);
}
  // Event listener for add cart button click
  $("#cart-add-btn").click(function () {
      var product_Id = $('input[name="product_size"]:checked').val();
      var quantity = $("input[name='quantity']").val()
      var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
      $.ajax({
          type: "GET",
          url: url,
          
          success: function (data) {
            $('.header_cart_count').html(data.cart_count)
        Swal.fire({
          title: "<strong>Item Added to Cart</strong>",
          icon: "success",
          html: `
              <p>Your item has been added to the cart successfully!</p>
              <p>What would you like to do next?</p>
          `,
          showCloseButton: true,
          showCancelButton: true,
          focusConfirm: false,
          confirmButtonText: `
              View Cart
              <i class="fa fa-shopping-cart"></i>
          `,
          confirmButtonAriaLabel: "View Cart",
          cancelButtonText: `
              Checkout
              <i class="fa fa-credit-card"></i>
          `,
          cancelButtonAriaLabel: "Checkout",
          timer: 5000, 
          timerProgressBar: true
        }).then((result) => {
            if (result.isConfirmed) {
                // Redirect to the view cart page
                window.location.href = '/shop/cart/';
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                // Redirect to the checkout page
                window.location.href = '/checkout/';
            }
        });
        
          
      },
      error: function (data) {
        if (data.status == '401') {
          window.location.href = '/accounts/login/';
      } else {
          // Display error message with SweetAlert
          Swal.fire({
              title: "Error",
              icon: "error",
              text: data.responseJSON.message || "An error occurred while adding the item to the cart."
          });
      }
    }
      });
  });

  $(".cart-add-btn-combo").click(function () {
    var product_Id = $(this).data("product-id");
    var quantity = $("input[name='quantity']").val()
    var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
    $.ajax({
        type: "GET",
        url: url,
        
        success: function (data) {
          $('.header_cart_count').html(data.cart_count)
      Swal.fire({
        title: "<strong>Item Added to Cart</strong>",
        icon: "success",
        html: `
            <p>Your item has been added to the cart successfully!</p>
            <p>What would you like to do next?</p>
        `,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: `
            View Cart
            <i class="fa fa-shopping-cart"></i>
        `,
        confirmButtonAriaLabel: "View Cart",
        cancelButtonText: `
            Checkout
            <i class="fa fa-credit-card"></i>
        `,
        cancelButtonAriaLabel: "Checkout",
        timer: 5000, 
        timerProgressBar: true
      }).then((result) => {
          if (result.isConfirmed) {
              // Redirect to the view cart page
              window.location.href = '/shop/cart/';
          } else if (result.dismiss === Swal.DismissReason.cancel) {
              // Redirect to the checkout page
              window.location.href = '/checkout/';
          }
      });
      
        
    },
    error: function (data) {
      if (data.status == '401') {
        window.location.href = '/accounts/login/';
    } else {
        // Display error message with SweetAlert
        Swal.fire({
            title: "Error",
            icon: "error",
            text: data.responseJSON.message || "An error occurred while adding the item to the cart."
        });
    }
  }
    });
});
});
