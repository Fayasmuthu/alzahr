
$(document).ready(function () {
    // Function to update prices  for a specific card
    function updatePricesAndOffer(card) {
        var selected = card.find('select[name="product_size"] option:selected');
        if (selected.length > 0) {
            var salePrice = selected.data('sale_price');
            var originalPrice = selected.data('original_price');
            card.find('.sale_price').text('dh' + salePrice);
            card.find('.original_price').text('dh' + originalPrice);
        }
    }

    // Event listener for select button click within each card
    $('select[name="product_size"]').change(function () {
        var card = $(this).closest('.card-product');
        updatePricesAndOffer(card);
    });
    
    // add cart ajax
    
$(".cart-add-btn").click(function () {
    var card = $(this).closest('.card-product');
    var selected = card.find('select[name="product_size"] option:selected');
    var product= selected.val();
    var url = "/shop/cart/add/?product_id="+product; 
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            // Display success message
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
                    <i class="fa fa-credit-card" ></i>
                `,
                cancelButtonAriaLabel: "Checkout",
                timer: 5000, 
                timerProgressBar: true
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirect to the view cart page
                    window.location.href = '/shop/cart/';
                } else if (result.dismiss === Swal.DismissReason.cancel) {
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


    $(".cart-add-btn-offer").click(function () {
        var product_Id = $(this).data("product-id");
        var quantity = 1
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


// // add wishlist ajax
// $(".btn-action-wishlist").click(function () {
//     var $card = $(this).closest('.product-box-4, .card-product');
//     // var selected = card.find('select[name="product_size"] option:selected').val();
//     var $select = $card.find('select[name="product_size"]');
//     var selected = null;
//     if ($select.length > 0) {
//         selected = $select.find('option:selected').val();  // get selected variant id
//     }
    
//     var product_Id = $(this).data("product_id");
    
//     var finalProductId = selected || product_Id; 

//     if (!finalProductId) {
//         showAlert("Please select a product first.", "alert-danger");
//         return;
//     }

//     // var url = "/shop/wishlist/add/?product_id="+product_Id;
//     // var url = "/shop/wishlist/add/?product_id=" + finalProductId;

//     $.ajax({
//     type: "GET",
//     // url: url,
//     url: "/shop/wishlist/add/",
//     data: { product_id: finalProductId },
//     success: function (data) {
//         console.log("Wishlist Count Returned:", data.wishlist_count);
//         // Display success message
//         $('#header_wishlist_count').html(data.wishlist_count)
        
//         showAlert(data.message, "alert-success");
//     },
//     error: function (data) {
//         if (data.status == '401') {window.location.href = '/accounts/login/';
//         }else{showAlert(data.responseJSON.message, "alert-danger");}
//     }
//     });
// });
// function showAlert(message, alertClass) {
//     var alertContainer = $("#alert-container");
//     var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
//     alertContainer.append(alertDiv);
//     // Automatically hide the alert after 5 seconds
//     setTimeout(function () {
//         alertDiv.remove();
//     }, 800);
// }
// --------------------------------------------------------------------------------------
// $(".btn-action-wishlist").click(function () {
//     var $card = $(this).parents('.card-product');
//     var $select = $card.find('select[name="product_size"]');

//     var selected = null;
//     if ($select.length > 0) {
//         selected = $select.find('option:selected').val();
//     }

//     var product_Id = $(this).data("product_id");
//     var finalProductId = selected ? selected : product_Id;

//     if (!finalProductId) {
//         showAlert("Please select a product first.", "alert-danger");
//         return;
//     }

//     $.ajax({
//         type: "GET",
//         url: "/shop/wishlist/add/",
//         data: { product_id: finalProductId },
//         success: function (data) {
//             $('#header_wishlist_count').html(data.wishlist_count);
//             showAlert(data.message, "alert-success");
//         },
//         error: function (xhr) {
//             if (xhr.status == 401) {
//                 window.location.href = '/accounts/login/';
//             } else if (xhr.responseJSON && xhr.responseJSON.message) {
//                 showAlert(xhr.responseJSON.message, "alert-danger");
//             } else {
//                 showAlert("Something went wrong. Please try again.", "alert-danger");
//             }
//         }
//     });
// });
$(".btn-action-wishlist").click(function () {
    var $card = $(this).closest('.card-product');
    var $select = $card.find('select[name="product_size"]');
    var product_Id = $(this).data("product_id");
    var finalProductId = product_Id;

    if ($select.length > 0) {
        var selectedOption = $select.find('option:selected');
        var availableId = selectedOption.data('available_id');
        finalProductId = availableId || product_Id;
    }

    if (!finalProductId) {
        showAlert("Please select a product first.", "alert-danger");
        return;
    }

    $.ajax({
        type: "GET",
        url: "/shop/wishlist/add/",
        data: { product_id: finalProductId },
        success: function (data) {
            $('#header_wishlist_count').html(data.wishlist_count);
            showAlert(data.message, "alert-success");
        },
        error: function (xhr) {
            if (xhr.status == 401) {
                window.location.href = '/accounts/login/';
            } else if (xhr.responseJSON && xhr.responseJSON.message) {
                showAlert(xhr.responseJSON.message, "alert-danger");
            } else {
                showAlert("Something went wrong. Please try again.", "alert-danger");
            }
        }
    });
});


// $(".btn-action-wishlist").click(function () {
//     var product_Id = $(this).data("product_id");
//     var url = "/shop/wishlist/add/?product_id=" + product_Id;

//     $.ajax({
//         type: "GET",
//         url: url,
//         success: function (data) {
//             $('#header_wishlist_count').html(data.wishlist_count);
//             showAlert(data.message, "alert-success");
//         },
//         error: function (data) {
//             if (data.status == 401) {
//                 window.location.href = '/accounts/login/';
//             } else {
//                 showAlert(data.responseJSON.message, "alert-danger");
//             }
//         }
//     });
// });


// add wishlist ajax
$(".btn-action-compare").click(function () {
    var card = $(this).closest('.card-product');
    var selected = card.find('select[name="product_size"] option:selected');
    var product= selected.val();
    var url = "/shop/compare/add/?product_id="+product; 
    $.ajax({
    type: "GET",
    url: url,
    success: function (data) {
        // Display success message
        console.log("-------------")
        console.log("----data.compare_count---------",data.compare_count)
        $('#header_compare_count').html(data.compare_count)
        
        showAlert(data.message, "alert-success");
    },
    error: function (data) {
        if (data.status == '401') {window.location.href = '/accounts/login/';
        }else{showAlert(data.responseJSON.message, "alert-danger");}
    }
    });
});
function showAlert(message, alertClass) {
    var alertContainer = $("#alert-container");
    var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
    alertContainer.append(alertDiv);
    // Automatically hide the alert after 5 seconds
    setTimeout(function () {
        alertDiv.remove();
    }, 800);
}
});




