 $('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString(); // pid is attribute given in plus button to get product id
   // console.log(id) // to check that we are getting id or not when hit plus button
   var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",       // GET method
        url: "/pluscart", // this will send to pluscart function in views.py
        data: {
            product_id : id // this will store id in product_id and send id to views.py
        },
        success: function (data) {
           // console.log(data) // to check if we are getting data after pressing plus add button
           // console.log('success') // to check if there is no logical error
           eml.innerText = data.quantity  //we can use both methods to get element to update quantity this and below
        //    document.getElementById("quantity").innerText = data.quantity
           document.getElementById("amount").innerText = data.amount
           document.getElementById("totalamount").innerText = data.total_amount

        }
        
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        url: "/minuscart", 
        data: {
            product_id : id 
        },
        success: function (data) {
            eml.innerText = data.quantity
            // document.getElementById("quantity").innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.total_amount

        }
        
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        url: "/removecart", 
        data: {
            product_id : id 
        },
        success: function (data) {
          
           
           document.getElementById("amount").innerText = data.amount;
           document.getElementById("totalamount").innerText = data.total_amount;
        //    document.getElementById("removeit").remove()
            eml.parentNode.parentNode.parentNode.parentNode.remove();

        }
        
    })
})

$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this address?');
})

// function changelabel(){
//     document.getElementById('lblemp').innerHTML='added';
//     console.log('button clicked')
//     alert('item added')
// }

//add to wishlist:
$(document).on("click", ".add-to-wishlist", function(){
    let product_id = $(this).attr("data-product-item")
    let this_val = $(this)

    console.log("product id", product_id);

    $.ajax({
        url: "/add-to-wishlist",
        data: {
            "id": product_id
        },
        dataType: "json",
        
        success: function(response){
            if (response.bool === true){
            this_val.html("❤")
            console.log("added to wishlist");   
            }
            else{
            this_val.html("🤍")
            console.log("deleted from wishlist");
            }
            
        }
    })
})


