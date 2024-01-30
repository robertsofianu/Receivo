document.getElementById('add_c_amout').addEventListener('click', function(){
    var inputValue = encodeURIComponent(document.getElementById('input').value);
    var amountValue = encodeURIComponent(document.getElementById('amount').value);


    // Build the URL with the input value
    var url = "http://127.0.0.1:5000/add_subtract_customer_amout/" + inputValue + "/" + amountValue + "/1";

    // Navigate to the constructed URL
    window.location.href = url;
})



document.getElementById('subtract_c_amout').addEventListener('click', function(){
    var inputValue = encodeURIComponent(document.getElementById('input').value);
    var amountValue = encodeURIComponent(document.getElementById('amount').value);


    // Build the URL with the input value
    var url = "http://127.0.0.1:5000/add_subtract_customer_amout/" + inputValue + "/" + amountValue + "/2";

    // Navigate to the constructed URL
    window.location.href = url;
})


document.getElementById('show_more_details').addEventListener('click', function(){
    var inputValue = encodeURIComponent(document.getElementById('input').value);

    var url = "http://127.0.0.1:5000//show_more_details_cust/" + inputValue;

    window.location.href = url;
})